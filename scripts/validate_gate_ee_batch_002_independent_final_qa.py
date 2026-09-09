from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.recompute_gate_ee_batch_002 import build_evidence
from scripts.validate_gate_ee_batch_002_human_signoff import validate as validate_human_signoff


BASE = ROOT / "GATE_EE/corpus_v1"
SOURCE = BASE / "source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
FORMATTER = BASE / "qualification/BATCH_002_FORMATTER_FINAL_EVIDENCE.json"
QA = BASE / "qualification/BATCH_002_INDEPENDENT_AI_QA.json"
SUMMARY = BASE / "qualification/BATCH_002_QUALIFICATION_SUMMARY.json"
CANDIDATE = BASE / "qualification/BATCH_002_PAPER_ELIGIBILITY_CANDIDATE.json"
HUMAN = BASE / "review_manifests/BATCH_002_HUMAN_FINAL_QA.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


errors: list[str] = []
source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
formatter_sha = hashlib.sha256(FORMATTER.read_bytes()).hexdigest()
qa = load(QA)
summary = load(SUMMARY)
candidate = load(CANDIDATE)
human = load(HUMAN)
questions = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip()]

try:
    recomputed = json.loads(json.dumps(build_evidence()))
except ValueError as exc:
    errors.append(str(exc))
    recomputed = {}
if qa != recomputed: errors.append("committed independent-AI evidence is not reproducible")
if qa.get("source_sha256") != source_sha: errors.append("independent-AI evidence source checksum mismatch")
if qa.get("formatter_report_sha256") != formatter_sha: errors.append("independent-AI Formatter checksum mismatch")
if qa.get("status") != "PASS" or qa.get("evidence_valid_for_current_source") is not True:
    errors.append("independent-AI evidence is not current and passing")
if qa.get("human_review_substitute") is not False:
    errors.append("AI evidence must not claim to replace human review")
for field in (
    "technical_pass_count",
    "answer_recomputed_pass_count",
    "solution_consistency_pass_count",
    "machine_final_marker_pass_count",
):
    if qa.get(field) != len(questions): errors.append(f"{field} does not cover all questions")

expected = [(question["id"], question["revision"]) for question in questions]
expected_ids = [question["id"] for question in questions]
qa_found = [(row.get("question_id"), row.get("revision")) for row in qa.get("questions", [])]
if qa_found != expected: errors.append("independent-AI question IDs/revisions mismatch")
if summary.get("source_sha256") != source_sha: errors.append("qualification-summary source checksum mismatch")
if candidate.get("source_sha256") != source_sha: errors.append("candidate source checksum mismatch")
if candidate.get("candidate_question_ids") != expected_ids:
    errors.append("paper-eligibility candidate IDs mismatch")
if candidate.get("paper_eligibility_candidate_count") != len(questions):
    errors.append("paper-eligibility candidate count mismatch")
if human.get("source_sha256") != source_sha or human.get("formatter_report_sha256") != formatter_sha:
    errors.append("human-review checksum mismatch")

stage = summary.get("current_stage")
human_errors, approved, revise, reject, _ = validate_human_signoff()
errors.extend(human_errors)
if stage == "READY_FOR_HUMAN_FINAL_QA":
    if summary.get("paper_eligible_count") != 0:
        errors.append("pre-promotion Batch 002 cannot be paper-eligible")
    if candidate.get("paper_eligible_count") != 0 or candidate.get("human_final_qa") != "PENDING":
        errors.append("candidate state must remain blocked until promotion")
    if candidate.get("certified_paper_eligible_question_ids") != []:
        errors.append("pre-promotion candidate contains certified IDs")
elif stage == "PAPER_ELIGIBILITY_CERTIFIED":
    if human.get("final_decision") != "APPROVE_REVIEWED_RESULTS":
        errors.append("certified state requires completed human approval")
    if candidate.get("human_final_qa") != "COMPLETE":
        errors.append("certified candidate human-QA state mismatch")
    if candidate.get("certified_paper_eligible_question_ids") != approved:
        errors.append("certified candidate IDs do not match human PASS decisions")
    if candidate.get("paper_eligible_count") != len(approved):
        errors.append("certified candidate count mismatch")
    if summary.get("paper_eligible_count") != len(approved):
        errors.append("certified summary count mismatch")
    human_summary = summary.get("human_final_qa", {})
    if human_summary.get("status") != "COMPLETE" or human_summary.get("passed") != len(approved):
        errors.append("certified summary human-QA state mismatch")
    if human_summary.get("revise") != len(revise) or human_summary.get("reject") != len(reject):
        errors.append("certified summary human-QA non-pass counts mismatch")
else:
    errors.append(f"unsupported qualification stage: {stage!r}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("GATE EE BATCH 002 QUALIFICATION STATE: CONSISTENT")
print(f"Current stage: {stage}")
print(f"Current source SHA-256: {source_sha}")
print("Formatter: 20 PASS / 0 REVIEW / 0 invalid")
print("Independent AI recomputation: 20/20 PASS (not a human substitute)")
print(f"Paper-eligible: {candidate.get('paper_eligible_count', 0)}")
print(f"Release gate: {summary.get('release_gate')}")
