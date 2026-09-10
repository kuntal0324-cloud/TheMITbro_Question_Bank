from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
SOURCE = BASE / "source_batches/BATCH_003_GENERAL_APTITUDE.jsonl"
FORMATTER = BASE / "qualification/BATCH_003_FORMATTER_FINAL_EVIDENCE.json"
QA = BASE / "qualification/BATCH_003_INDEPENDENT_AI_QA.json"
HUMAN = BASE / "review_manifests/BATCH_003_HUMAN_FINAL_QA.json"
SUMMARY = BASE / "qualification/BATCH_003_QUALIFICATION_SUMMARY.json"
CANDIDATE = BASE / "qualification/BATCH_003_PAPER_ELIGIBILITY_CANDIDATE.json"


CHECK_FIELDS = (
    "technical_correctness",
    "answer_correctness",
    "solution_correctness",
    "clarity_ambiguity",
    "originality_conflict_check",
)
ALLOWED_STAGES = {"READY_FOR_HUMAN_FINAL_QA", "PAPER_ELIGIBILITY_CERTIFIED"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(require_complete: bool = False) -> tuple[list[str], list[str], list[str], list[str], str]:
    human = load(HUMAN)
    summary = load(SUMMARY)
    candidate = load(CANDIDATE)
    formatter = load(FORMATTER)
    qa = load(QA)
    questions = [
        json.loads(line)
        for line in SOURCE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    errors: list[str] = []
    source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    formatter_sha = hashlib.sha256(FORMATTER.read_bytes()).hexdigest()
    expected = [(question["id"], question["revision"]) for question in questions]
    expected_ids = [question["id"] for question in questions]
    rows = human.get("questions", [])
    found = [(row.get("question_id"), row.get("revision")) for row in rows]
    stage = summary.get("current_stage")

    if human.get("signoff_contract") != "GATE_EE_BATCH_003_HUMAN_FINAL_QA_V1":
        errors.append("human-signoff contract mismatch")
    if human.get("batch_id") != "BATCH_003": errors.append("human-signoff batch mismatch")
    if human.get("source_sha256") != source_sha: errors.append("human-signoff source checksum mismatch")
    if human.get("formatter_report_sha256") != formatter_sha:
        errors.append("human-signoff Formatter checksum mismatch")
    if summary.get("source_sha256") != source_sha: errors.append("qualification-summary source checksum mismatch")
    if stage not in ALLOWED_STAGES: errors.append("Batch 003 is not at a valid human-final-QA state")
    if candidate.get("source_sha256") != source_sha: errors.append("candidate source checksum mismatch")
    if candidate.get("candidate_question_ids") != expected_ids:
        errors.append("candidate IDs do not match the canonical source")
    if candidate.get("paper_eligibility_candidate_count") != len(questions):
        errors.append("candidate count does not match the canonical source")
    if formatter.get("source_sha256") != source_sha:
        errors.append("Formatter evidence source checksum mismatch")
    if (
        formatter.get("status") != "PASS"
        or formatter.get("formatter_pass_count") != len(questions)
        or formatter.get("formatter_review_count") != 0
        or formatter.get("invalid_count") != 0
    ):
        errors.append("strict Formatter prerequisite is not 20 PASS / 0 REVIEW / 0 invalid")
    if qa.get("source_sha256") != source_sha or qa.get("formatter_report_sha256") != formatter_sha:
        errors.append("independent-AI prerequisite checksum mismatch")
    if (
        qa.get("status") != "PASS"
        or qa.get("evidence_valid_for_current_source") is not True
        or qa.get("human_review_substitute") is not False
    ):
        errors.append("valid independent-AI prerequisite is missing")
    if found != expected: errors.append("human-signoff IDs/revisions do not match the canonical source")

    decision = human.get("final_decision")
    reviewer = human.get("reviewer", {})
    approved: list[str] = []
    revise: list[str] = []
    reject: list[str] = []

    if decision == "PENDING":
        if require_complete or stage == "PAPER_ELIGIBILITY_CERTIFIED":
            errors.append("completed human approval is required for paper-eligibility certification")
        if any(
            str(reviewer.get(field, "")).strip()
            for field in ("name", "role_or_qualification", "review_date", "attestation")
        ):
            errors.append("pending template contains partial reviewer identity; complete the review or clear it")
        for row in rows:
            if row.get("decision") != "PENDING" or any(row.get(field) != "PENDING" for field in CHECK_FIELDS):
                errors.append(f"{row.get('question_id', '?')}: pending template contains a partial decision")
        return errors, approved, revise, reject, source_sha

    if decision != "APPROVE_REVIEWED_RESULTS":
        errors.append("final_decision must be PENDING or APPROVE_REVIEWED_RESULTS")
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

    pdf_evidence = human.get("pdf_evidence", {})
    if not str(pdf_evidence.get("filename", "")).strip(): errors.append("completed-PDF filename is missing")
    if not re.fullmatch(r"[0-9a-f]{64}", str(pdf_evidence.get("sha256", ""))):
        errors.append("completed-PDF SHA-256 is missing or invalid")
    if pdf_evidence.get("format") != "XELATEX_ACROFORM_V2":
        errors.append("completed-PDF format contract mismatch")
    if not str(pdf_evidence.get("reviewer_signature", "")).strip():
        errors.append("completed-PDF reviewer signature is missing")

    for row in rows:
        qid = row.get("question_id", "?")
        checks = [row.get(field) for field in CHECK_FIELDS]
        if any(value not in {"PASS", "FAIL"} for value in checks):
            errors.append(f"{qid}: all five checks must be PASS or FAIL")
        row_decision = row.get("decision")
        if row_decision == "PASS":
            if any(value != "PASS" for value in checks):
                errors.append(f"{qid}: PASS requires all five checks PASS")
            else:
                approved.append(qid)
        elif row_decision == "REVISE":
            revise.append(qid)
        elif row_decision == "REJECT":
            reject.append(qid)
        else:
            errors.append(f"{qid}: decision must be PASS, REVISE or REJECT")

    if sorted(approved + revise + reject) != sorted(expected_ids):
        errors.append("human decisions do not partition all canonical question IDs")
    return errors, approved, revise, reject, source_sha


def main() -> int:
    errors, approved, revise, reject, source_sha = validate()
    if errors:
        print("HUMAN FINAL QA SIGNOFF: BLOCKED")
        for error in errors:
            print("-", error)
        return 1

    human = load(HUMAN)
    summary = load(SUMMARY)
    if human.get("final_decision") == "PENDING":
        print("GATE EE BATCH 003 HUMAN FINAL QA: PENDING (VALID TEMPLATE)")
        print("Questions awaiting named human review: 20")
        print("Paper-eligible: 0")
    elif summary.get("current_stage") == "READY_FOR_HUMAN_FINAL_QA":
        print("GATE EE BATCH 003 HUMAN FINAL QA SIGNOFF: READY FOR PROMOTION")
        print(f"Source SHA-256: {source_sha}")
        print(f"PASS: {len(approved)}")
        print(f"REVISE: {len(revise)}")
        print(f"REJECT: {len(reject)}")
        print("Paper-eligibility promotion has not been run.")
    else:
        print("GATE EE BATCH 003 HUMAN FINAL QA SIGNOFF: PASSED")
        print(f"Source SHA-256: {source_sha}")
        print(f"PASS: {len(approved)}")
        print(f"REVISE: {len(revise)}")
        print(f"REJECT: {len(reject)}")
        print("Certification state: PAPER_ELIGIBILITY_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
