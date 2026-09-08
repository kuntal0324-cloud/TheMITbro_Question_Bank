from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
SOURCE = BASE / "source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
FORMATTER = BASE / "qualification/BATCH_002_FORMATTER_FINAL_EVIDENCE.json"
QA = BASE / "qualification/BATCH_002_INDEPENDENT_AI_QA.json"
HUMAN = BASE / "review_manifests/BATCH_002_HUMAN_FINAL_QA.json"
SUMMARY = BASE / "qualification/BATCH_002_QUALIFICATION_SUMMARY.json"


CHECK_FIELDS = (
    "technical_correctness", "answer_correctness", "solution_correctness",
    "clarity_ambiguity", "originality_conflict_check",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


human = load(HUMAN)
summary = load(SUMMARY)
qa = load(QA)
questions = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip()]
errors: list[str] = []
source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
formatter_sha = hashlib.sha256(FORMATTER.read_bytes()).hexdigest()
expected = [(question["id"], question["revision"]) for question in questions]
rows = human.get("questions", [])
found = [(row.get("question_id"), row.get("revision")) for row in rows]

if human.get("source_sha256") != source_sha: errors.append("human-signoff source checksum mismatch")
if human.get("formatter_report_sha256") != formatter_sha: errors.append("human-signoff Formatter checksum mismatch")
if qa.get("status") != "PASS" or qa.get("human_review_substitute") is not False:
    errors.append("valid independent-AI prerequisite is missing")
if summary.get("current_stage") != "READY_FOR_HUMAN_FINAL_QA": errors.append("Batch 002 is not at the human-final-QA gate")
if found != expected: errors.append("human-signoff IDs/revisions do not match the canonical source")

decision = human.get("final_decision")
reviewer = human.get("reviewer", {})
if decision == "PENDING":
    if any(str(reviewer.get(field, "")).strip() for field in ("name", "role_or_qualification", "review_date", "attestation")):
        errors.append("pending template contains partial reviewer identity; complete the review or clear it")
    for row in rows:
        if row.get("decision") != "PENDING" or any(row.get(field) != "PENDING" for field in CHECK_FIELDS):
            errors.append(f"{row.get('question_id', '?')}: pending template contains a partial decision")
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("GATE EE BATCH 002 HUMAN FINAL QA: PENDING (VALID TEMPLATE)")
    print("Questions awaiting named human review: 20")
    print("Paper-eligible: 0")
    raise SystemExit(0)

if decision != "APPROVE_REVIEWED_RESULTS": errors.append("final_decision must be PENDING or APPROVE_REVIEWED_RESULTS")
for field in ("name", "role_or_qualification", "review_date", "attestation"):
    if not str(reviewer.get(field, "")).strip(): errors.append(f"missing reviewer field: {field}")
review_date = str(reviewer.get("review_date", ""))
if review_date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", review_date):
    errors.append("review_date must use YYYY-MM-DD")
elif review_date:
    try:
        date.fromisoformat(review_date)
    except ValueError:
        errors.append("review_date is not a valid calendar date")
if reviewer.get("attestation") != human.get("required_attestation"):
    errors.append("reviewer attestation does not exactly match required_attestation")

approved: list[str] = []
revise: list[str] = []
reject: list[str] = []
for row in rows:
    qid = row.get("question_id", "?")
    checks = [row.get(field) for field in CHECK_FIELDS]
    if any(value not in {"PASS", "FAIL"} for value in checks):
        errors.append(f"{qid}: all five checks must be PASS or FAIL")
    row_decision = row.get("decision")
    if row_decision == "PASS":
        if any(value != "PASS" for value in checks): errors.append(f"{qid}: PASS requires all five checks PASS")
        else: approved.append(qid)
    elif row_decision == "REVISE": revise.append(qid)
    elif row_decision == "REJECT": reject.append(qid)
    else: errors.append(f"{qid}: decision must be PASS, REVISE or REJECT")

if errors:
    print("HUMAN FINAL QA SIGNOFF: BLOCKED")
    for error in errors: print("-", error)
    raise SystemExit(1)

print("GATE EE BATCH 002 HUMAN FINAL QA SIGNOFF: READY FOR PROMOTION")
print(f"PASS: {len(approved)}")
print(f"REVISE: {len(revise)}")
print(f"REJECT: {len(reject)}")
print("Paper-eligibility promotion has not been run.")
