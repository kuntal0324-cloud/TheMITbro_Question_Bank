from __future__ import annotations

from datetime import date, timedelta
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
LEDGER = BASE / "production/EIGHT_DAY_PROGRESS.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


ledger = load(LEDGER)
errors: list[str] = []
sources = {
    "BATCH_001": BASE / "source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl",
    "BATCH_002": BASE / "source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl",
}
records = {batch: load_jsonl(path) for batch, path in sources.items()}

all_questions = [question for batch in records.values() for question in batch]
all_ids = [question["id"] for question in all_questions]
all_families = [question["family_id"] for question in all_questions]
if len(all_ids) != len(set(all_ids)): errors.append("duplicate question ID across production batches")
if len(all_families) != len(set(all_families)): errors.append("duplicate family across production batches")

sprint = ledger.get("sprint", {})
day1 = ledger.get("day_1", {})
opening = ledger.get("opening_inventory", {})
program = ledger.get("program_inventory", {})
daily_targets = sprint.get("daily_targets", [])
if len(daily_targets) != 8 or sum(daily_targets) != 3575:
    errors.append("eight-day daily targets must sum to 3,575")
if sprint.get("draft_target") != 3575: errors.append("sprint draft target mismatch")
try:
    start = date.fromisoformat(sprint.get("start_date", ""))
    end = date.fromisoformat(sprint.get("planned_end_date", ""))
    date.fromisoformat(ledger.get("as_of", ""))
    if end != start + timedelta(days=7): errors.append("planned end must be the eighth inclusive calendar day")
except ValueError:
    errors.append("invalid sprint calendar date")
if sprint.get("current_day") not in range(1, 9): errors.append("current sprint day must be from 1 through 8")

opening_batches = opening.get("source_batches", [])
day1_batches = day1.get("source_batches", [])
program_batches = program.get("source_batches", [])
if set(opening_batches).intersection(day1_batches): errors.append("opening inventory cannot be counted as sprint output")
if set(opening_batches + day1_batches + program_batches) - set(records):
    errors.append("ledger references an unknown source batch")
if set(program_batches) != set(records): errors.append("program inventory must enumerate every production batch")

opening_count = sum(len(records[batch]) for batch in opening_batches)
day1_count = sum(len(records[batch]) for batch in day1_batches)
program_count = sum(len(records[batch]) for batch in program_batches)
if opening.get("unique_candidates") != opening_count: errors.append("opening candidate count mismatch")
if day1.get("drafts_produced") != day1_count: errors.append("Day-1 draft count mismatch")
if day1.get("remaining") != day1.get("target", 0) - day1_count: errors.append("Day-1 remaining count mismatch")
if sprint.get("drafts_produced_during_sprint") != day1_count: errors.append("sprint production count mismatch")
if program.get("unique_candidates") != program_count: errors.append("program candidate count mismatch")

allocation = day1.get("allocation", {})
allocation_produced = sum(row.get("produced", 0) for row in allocation.values())
allocation_target = sum(row.get("target", 0) for row in allocation.values())
if allocation_produced != day1_count: errors.append("Day-1 subject production does not sum to Day-1 output")
if allocation_target != day1.get("target") or day1.get("target") != daily_targets[0]:
    errors.append("Day-1 allocation target mismatch")
if allocation.get("Electric Circuits", {}).get("produced") != len(records["BATCH_002"]):
    errors.append("Batch 002 is not reflected in the Electric Circuits Day-1 counter")


def certified_counts(batch_id: str) -> tuple[int, int]:
    certificate_path = BASE / "qualification" / f"{batch_id}_PAPER_ELIGIBILITY_CERTIFICATE.json"
    admission_path = BASE / "manifests" / f"{batch_id}_CORPUS_ADMISSION.json"
    if certificate_path.exists() != admission_path.exists():
        errors.append(f"{batch_id}: certificate and admission manifest must exist together")
        return 0, 0
    if not certificate_path.exists():
        return 0, 0
    certificate = load(certificate_path)
    admission = load(admission_path)
    eligible = certificate.get("paper_eligible_count", 0)
    admitted = admission.get("admitted_count", 0)
    if eligible != len(certificate.get("approved_question_ids", [])):
        errors.append(f"{batch_id}: certificate count mismatch")
    if admitted != len(admission.get("admitted_question_ids", [])):
        errors.append(f"{batch_id}: admission count mismatch")
    if admission.get("admitted_question_ids") != certificate.get("approved_question_ids"):
        errors.append(f"{batch_id}: certificate/admission ID mismatch")
    return eligible, admitted


certified = {batch: certified_counts(batch) for batch in records}
opening_eligible = sum(certified[batch][0] for batch in opening_batches)
opening_admitted = sum(certified[batch][1] for batch in opening_batches)
program_eligible = sum(certified[batch][0] for batch in program_batches)
program_admitted = sum(certified[batch][1] for batch in program_batches)
if opening.get("paper_eligible") != opening_eligible or opening.get("corpus_admitted") != opening_admitted:
    errors.append("opening certified inventory mismatch")
if program.get("paper_eligible") != program_eligible or program.get("corpus_admitted") != program_admitted:
    errors.append("program certified inventory mismatch")

formatter_files = {
    "BATCH_001": BASE / "qualification/BATCH_001_FORMATTER_FINAL_EVIDENCE.json",
    "BATCH_002": BASE / "qualification/BATCH_002_FORMATTER_FINAL_EVIDENCE.json",
}
formatter_passed = {
    batch: load(path).get("formatter_pass_count", 0) for batch, path in formatter_files.items()
}
if opening.get("formatter_passed") != sum(formatter_passed[batch] for batch in opening_batches):
    errors.append("opening Formatter-pass count mismatch")
if program.get("formatter_passed") != sum(formatter_passed[batch] for batch in program_batches):
    errors.append("program Formatter-pass count mismatch")
if opening.get("human_final_qa_passed") != opening_eligible:
    errors.append("opening human-final-QA PASS count mismatch")
if program.get("human_final_qa_passed") != program_eligible:
    errors.append("program human-final-QA PASS count mismatch")
if program.get("complete_65_question_sets") != 0 or program.get("released_sets") != 0:
    errors.append("no complete or released set may be claimed at the current inventory")
if not str(ledger.get("next_gate", "")).strip(): errors.append("next gate is missing")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("GATE EE EIGHT-DAY PRODUCTION CONTROL: PASSED")
print(f"Contract day: {sprint['current_day']} ({sprint['state']})")
print(f"Day-1 drafts: {day1_count}/{day1['target']} ({day1_count/day1['target']:.2%})")
print(f"Eight-day sprint drafts: {day1_count}/{sprint['draft_target']} ({day1_count/sprint['draft_target']:.2%})")
print(f"Program candidates: {program_count}")
print(f"Formatter-passed: {sum(formatter_passed[batch] for batch in program_batches)}")
print(f"Paper-eligible/admitted: {program_eligible}/{program_admitted}")
print("Complete/released sets: 0/0")
