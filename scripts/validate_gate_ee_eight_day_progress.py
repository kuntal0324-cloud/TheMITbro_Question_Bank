from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
LEDGER = BASE / "production/EIGHT_DAY_PROGRESS.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def batch_id_from_source(path: Path) -> str:
    match = re.match(r"(BATCH_\d{3})_", path.stem)
    if not match:
        raise ValueError(f"Unrecognized production-batch filename: {path.name}")
    return match.group(1)


ledger = load(LEDGER)
errors: list[str] = []
sources = {
    batch_id_from_source(path): path
    for path in sorted((BASE / "source_batches").glob("BATCH_*.jsonl"))
}
records = {batch: load_jsonl(path) for batch, path in sources.items()}
manifests = {
    batch: load(BASE / "manifests" / f"{batch}_MANIFEST.json")
    for batch in records
}

all_questions = [question for batch in records.values() for question in batch]
all_ids = [question["id"] for question in all_questions]
all_families = [question["family_id"] for question in all_questions]
if len(all_ids) != len(set(all_ids)): errors.append("duplicate question ID across production batches")
if len(all_families) != len(set(all_families)): errors.append("duplicate family across production batches")

sprint = ledger.get("sprint", {})
opening = ledger.get("opening_inventory", {})
program = ledger.get("program_inventory", {})
daily_targets = sprint.get("daily_targets", [])
if len(daily_targets) != 8 or sum(daily_targets) != 3575:
    errors.append("eight-day daily targets must sum to 3,575")
if sprint.get("draft_target") != 3575: errors.append("sprint draft target mismatch")
current_day = sprint.get("current_day")
if current_day not in range(1, 9): errors.append("current sprint day must be from 1 through 8")
try:
    start = date.fromisoformat(sprint.get("start_date", ""))
    end = date.fromisoformat(sprint.get("planned_end_date", ""))
    as_of = date.fromisoformat(ledger.get("as_of", ""))
    if end != start + timedelta(days=7): errors.append("planned end must be the eighth inclusive calendar day")
    if current_day in range(1, 9) and as_of != start + timedelta(days=current_day - 1):
        errors.append("current_day does not match the ledger as_of date")
except ValueError:
    errors.append("invalid sprint calendar date")

day_rows = [ledger.get(f"day_{index}", {}) for index in range(1, current_day + 1)]
if any(not row for row in day_rows): errors.append("a current-or-prior production day is missing")
opening_batches = opening.get("source_batches", [])
day_batches = [batch for row in day_rows for batch in row.get("source_batches", [])]
program_batches = program.get("source_batches", [])
if set(opening_batches).intersection(day_batches): errors.append("opening inventory cannot be counted as sprint output")
if len(day_batches) != len(set(day_batches)): errors.append("a production batch is counted on more than one sprint day")
if set(opening_batches + day_batches + program_batches) - set(records):
    errors.append("ledger references an unknown source batch")
if set(program_batches) != set(records): errors.append("program inventory must enumerate every production batch")
if set(program_batches) != set(opening_batches + day_batches):
    errors.append("program inventory must equal opening inventory plus sprint batches")

opening_count = sum(len(records[batch]) for batch in opening_batches)
sprint_count = sum(len(records[batch]) for batch in day_batches)
program_count = sum(len(records[batch]) for batch in program_batches)
if opening.get("unique_candidates") != opening_count: errors.append("opening candidate count mismatch")
if sprint.get("drafts_produced_during_sprint") != sprint_count: errors.append("sprint production count mismatch")
if program.get("unique_candidates") != program_count: errors.append("program candidate count mismatch")

for index, day in enumerate(day_rows, 1):
    batches = day.get("source_batches", [])
    produced = sum(len(records[batch]) for batch in batches)
    if day.get("target") != daily_targets[index - 1]: errors.append(f"Day-{index} target mismatch")
    if day.get("drafts_produced") != produced: errors.append(f"Day-{index} draft count mismatch")
    if day.get("remaining") != day.get("target", 0) - produced: errors.append(f"Day-{index} remaining mismatch")
    allocation = day.get("allocation", {})
    if sum(row.get("target", 0) for row in allocation.values()) != day.get("target"):
        errors.append(f"Day-{index} allocation targets do not sum to the daily target")
    if sum(row.get("produced", 0) for row in allocation.values()) != produced:
        errors.append(f"Day-{index} allocation output does not sum to the daily output")
    actual_domains = Counter(manifests[batch].get("domain") for batch in batches for _ in records[batch])
    for domain, row in allocation.items():
        if row.get("produced", 0) != actual_domains.get(domain, 0):
            errors.append(f"Day-{index} {domain} output does not match its source batches")


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

formatter_passed = {}
for batch in records:
    path = BASE / "qualification" / f"{batch}_FORMATTER_FINAL_EVIDENCE.json"
    formatter_passed[batch] = load(path).get("formatter_pass_count", 0) if path.exists() else 0
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

today = day_rows[-1]
print("GATE EE EIGHT-DAY PRODUCTION CONTROL: PASSED")
print(f"Contract day: {current_day} ({sprint['state']})")
print(f"Day-{current_day} drafts: {today['drafts_produced']}/{today['target']} ({today['drafts_produced']/today['target']:.2%})")
print(f"Eight-day sprint drafts: {sprint_count}/{sprint['draft_target']} ({sprint_count/sprint['draft_target']:.2%})")
print(f"Program candidates: {program_count}")
print(f"Formatter-passed: {sum(formatter_passed[batch] for batch in program_batches)}")
print(f"Paper-eligible/admitted: {program_eligible}/{program_admitted}")
print("Complete/released sets: 0/0")
