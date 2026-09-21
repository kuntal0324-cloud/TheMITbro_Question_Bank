from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
import json
from pathlib import Path
import re

from gate_ee_set01 import (
    COMPLETED_SIGNOFF,
    FORMATTER_RELEASE_EVIDENCE,
    HUMAN_QA,
    RELEASE_AUTHORIZATION_PDF,
    RELEASE_AUTHORIZATION_COMPLETED,
    RELEASE_AUTHORIZATION_COMPLETED_PDF,
    RELEASE_CANDIDATE,
    RELEASE_LEARNER_PACK_PDF,
    RELEASE_QUESTION_PDF,
    RELEASE_SOLUTION_PDF,
    content_sha256,
    sha256,
)
from validate_gate_ee_set01_human_signoff import validate_completed_signoff


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
    expected_day = start + timedelta(days=current_day - 1)
    if str(sprint.get("state", "")).startswith("SPRINT_CLOSED"):
        if as_of < end:
            errors.append("a closed sprint ledger cannot predate its planned end")
    elif current_day in range(1, 9) and as_of != expected_day:
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
complete_sets = 0
if COMPLETED_SIGNOFF.is_file():
    completed_payload = load(COMPLETED_SIGNOFF)
    signoff_errors, all_pass = validate_completed_signoff(completed_payload, load(HUMAN_QA))
    if signoff_errors:
        errors.extend(f"Set 01 completed signoff: {error}" for error in signoff_errors)
    elif all_pass:
        complete_sets = 1
if program.get("complete_65_question_sets") != complete_sets:
    errors.append("complete 65-question set count does not match the completed whole-paper signoff")
if program.get("released_sets") != 0:
    errors.append("no released set may be claimed before a promoted release manifest exists")

checkpoint = ledger.get("set_01_review_checkpoint", {})
if complete_sets:
    if checkpoint.get("complete_paper_human_qa") != "PASSED_65_OF_65":
        errors.append("Set 01 ledger checkpoint does not record the completed 65/65 human-QA PASS")
    if checkpoint.get("reviewer_metadata_reconfirmation") != "RESOLVED":
        errors.append("Set 01 reviewer metadata resolution is not recorded")
    formatter = load(FORMATTER_RELEASE_EVIDENCE)
    candidate = load(RELEASE_CANDIDATE)
    if not RELEASE_AUTHORIZATION_COMPLETED.is_file():
        errors.append("Set 01 completed release authorization record is missing")
        authorization = {}
    else:
        authorization = load(RELEASE_AUTHORIZATION_COMPLETED)
    hash_bindings = {
        "completed_human_qa_json_sha256": sha256(COMPLETED_SIGNOFF),
        "completed_human_qa_content_sha256": completed_payload.get("signoff_content_sha256"),
        "completed_human_qa_pdf_sha256": completed_payload.get("completed_pdf", {}).get("sha256"),
        "formatter_release_evidence_sha256": sha256(FORMATTER_RELEASE_EVIDENCE),
        "formatter_release_evidence_content_sha256": formatter.get("evidence_content_sha256"),
        "release_candidate_manifest_sha256": sha256(RELEASE_CANDIDATE),
        "release_candidate_content_sha256": candidate.get("candidate_content_sha256"),
        "release_question_pdf_sha256": sha256(RELEASE_QUESTION_PDF),
        "release_solution_pdf_sha256": sha256(RELEASE_SOLUTION_PDF),
        "release_learner_pack_pdf_sha256": sha256(RELEASE_LEARNER_PACK_PDF),
        "release_authorization_template_pdf_sha256": sha256(RELEASE_AUTHORIZATION_PDF),
        "release_authorization_json_file_sha256": (
            sha256(RELEASE_AUTHORIZATION_COMPLETED)
            if RELEASE_AUTHORIZATION_COMPLETED.is_file() else None
        ),
        "release_authorization_content_sha256": authorization.get("authorization_content_sha256"),
        "release_authorization_completed_pdf_sha256": (
            sha256(RELEASE_AUTHORIZATION_COMPLETED_PDF)
            if RELEASE_AUTHORIZATION_COMPLETED_PDF.is_file() else None
        ),
    }
    for field, expected in hash_bindings.items():
        if checkpoint.get(field) != expected:
            errors.append(f"Set 01 ledger checkpoint {field} mismatch")
    if formatter.get("evidence_content_sha256") != content_sha256(formatter, "evidence_content_sha256"):
        errors.append("Set 01 Formatter release evidence self-hash is invalid")
    if candidate.get("candidate_content_sha256") != content_sha256(candidate, "candidate_content_sha256"):
        errors.append("Set 01 release candidate self-hash is invalid")
    if authorization:
        if authorization.get("authorization_content_sha256") != content_sha256(
            authorization, "authorization_content_sha256"
        ):
            errors.append("Set 01 release authorization self-hash is invalid")
        if (
            authorization.get("candidate_id") != candidate.get("candidate_id")
            or authorization.get("paper_id") != candidate.get("paper_id")
            or authorization.get("candidate_content_sha256") != candidate.get("candidate_content_sha256")
        ):
            errors.append("Set 01 release authorization/candidate binding mismatch")
        for key in ("question_pdf", "solution_pdf", "learner_pack_pdf"):
            expected_artifact = {
                "path": candidate.get("artifacts", {}).get(key, {}).get("path"),
                "sha256": candidate.get("artifacts", {}).get(key, {}).get("sha256"),
            }
            if authorization.get("authorized_artifacts", {}).get(key) != expected_artifact:
                errors.append(f"Set 01 release authorization {key} binding mismatch")
        if authorization.get("completed_pdf", {}).get("sha256") != (
            sha256(RELEASE_AUTHORIZATION_COMPLETED_PDF)
            if RELEASE_AUTHORIZATION_COMPLETED_PDF.is_file() else None
        ):
            errors.append("Set 01 completed release-authorization PDF checksum mismatch")
        if (
            authorization.get("status") != "EXACT_ARTIFACT_RELEASE_AUTHORIZED"
            or authorization.get("release_authorized") is not True
        ):
            errors.append("Set 01 release authorization is not complete")
        for field in ("price_set", "storefront_activated", "sale_authorized"):
            if authorization.get(field) is not False:
                errors.append(f"Set 01 authorization improperly sets {field}")
    if checkpoint.get("release_candidate") != "RC1_VALIDATED":
        errors.append("Set 01 RC1 validation state is not recorded")
    if checkpoint.get("status") != "RELEASE_AUTHORIZED_AWAITING_PRICING_AND_STOREFRONT":
        errors.append("Set 01 post-authorization checkpoint status is invalid")
    if checkpoint.get("exact_artifact_release_authorization") != "PASSED":
        errors.append("Set 01 exact-artifact authorization PASS is not recorded")
    if checkpoint.get("release_authorized") is not True:
        errors.append("Set 01 ledger checkpoint does not record release authorization")
    for field in ("price_set", "storefront_activated", "sale_authorized"):
        if checkpoint.get(field) is not False:
            errors.append(f"Set 01 ledger checkpoint improperly sets {field}")
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
print(f"Complete/released sets: {complete_sets}/{program['released_sets']}")
print(f"Set 01 exact-artifact authorization: {checkpoint.get('exact_artifact_release_authorization', 'NOT_RECORDED')}")
print("Commercial release: BLOCKED pending pricing, sale and storefront authorization")
