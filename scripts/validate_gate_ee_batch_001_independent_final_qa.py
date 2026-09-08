from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


qa = load("GATE_EE/corpus_v1/qualification/BATCH_001_INDEPENDENT_AI_QA.json")
fmt = load("GATE_EE/corpus_v1/qualification/BATCH_001_FORMATTER_FINAL_EVIDENCE.json")
elig = load("GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CANDIDATE.json")
human = load("GATE_EE/corpus_v1/review_manifests/BATCH_001_HUMAN_FINAL_QA.json")
summary = load("GATE_EE/corpus_v1/qualification/BATCH_001_QUALIFICATION_SUMMARY.json")

sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
stage = summary.get("current_stage")
errors: list[str] = []

if elig.get("source_sha256") != sha:
    errors.append("Eligibility artifact checksum does not match the current source.")
if human.get("source_sha256") != sha:
    errors.append("Human-QA template checksum does not match the current source.")
if stage != "PAPER_ELIGIBILITY_CERTIFIED" and elig.get("paper_eligible_count") != 0:
    errors.append("No item may be paper-eligible before requalification and human signoff.")
if stage == "READY_FOR_HUMAN_FINAL_QA" and human.get("final_decision") not in {
    "PENDING",
    "APPROVE_REVIEWED_RESULTS",
}:
    errors.append("Human final QA has an unsupported pre-promotion decision.")

if stage == "READY_FOR_FORMATTER_REQUALIFICATION":
    if qa.get("status") != "STALE_SOURCE_CHANGED" or qa.get("evidence_valid_for_current_source") is not False:
        errors.append("Old independent-AI evidence must be explicitly marked stale.")
    if fmt.get("status") != "STALE_SOURCE_CHANGED" or fmt.get("evidence_valid_for_current_source") is not False:
        errors.append("Old Formatter evidence must be explicitly marked stale.")
    if summary.get("formatter_v2_final_qualification", {}).get("passed") != 0:
        errors.append("Formatter pass count must reset to zero after a source change.")
    if elig.get("paper_eligibility_candidate_count") != 0:
        errors.append("Candidate count must reset to zero until requalification.")
elif stage == "FORMATTER_REVIEW_REQUIRED":
    if fmt.get("source_sha256") != sha or fmt.get("evidence_valid_for_current_source") is not True:
        errors.append("Strict Formatter evidence must match the current source.")
    if fmt.get("status") != "REVIEW_REQUIRED" or fmt.get("formatter_pass_count") != 0 or fmt.get("formatter_review_count") != 20:
        errors.append("Expected the recorded strict result: 0 PASS / 20 REVIEW.")
    if elig.get("paper_eligibility_candidate_count") != 0:
        errors.append("Review-required records cannot become eligibility candidates.")
elif stage == "READY_FOR_HUMAN_FINAL_QA":
    if qa.get("source_sha256") != sha or fmt.get("source_sha256") != sha:
        errors.append("Current qualification evidence checksum mismatch.")
    if qa.get("status") != "PASS" or qa.get("evidence_valid_for_current_source") is not True:
        errors.append("Independent AI recomputation evidence is not current and passing.")
    if qa.get("human_review_substitute") is not False:
        errors.append("AI evidence must explicitly state that it is not a human-review substitute.")
    if any(qa.get(field) != 20 for field in (
        "technical_pass_count", "answer_recomputed_pass_count",
        "solution_consistency_pass_count", "machine_final_marker_pass_count",
    )):
        errors.append("Independent AI recomputation must pass all 20 questions and solutions.")
    source_questions=[json.loads(x) for x in SOURCE.read_text(encoding="utf-8").splitlines() if x.strip()]
    source_by_id={q["id"]:q for q in source_questions}
    expected={(q["id"],q["revision"]) for q in source_questions}
    qa_rows=qa.get("questions",[])
    found={(row.get("question_id"),row.get("revision")) for row in qa_rows}
    if len(qa_rows)!=20 or found!=expected:
        errors.append("Independent AI evidence IDs/revisions do not match the canonical source.")
    for row in qa_rows:
        if any(row.get(field)!="PASS" for field in (
            "technical_result","answer_result","solution_consistency_result","machine_final_marker_result"
        )):
            errors.append(f"{row.get('question_id','?')}: independent recomputation is incomplete.")
        canonical=source_by_id.get(row.get("question_id"))
        if canonical and (
            row.get("declared_answer") != canonical.get("answer")
            or row.get("recomputed_answer") != canonical.get("answer")
            or not str(row.get("derivation_summary","")).strip()
        ):
            errors.append(f"{row.get('question_id','?')}: recomputed answer evidence disagrees with the canonical answer.")
    if (
        fmt.get("status") != "PASS"
        or fmt.get("formatter_pass_count") != 20
        or fmt.get("formatter_review_count") != 0
        or fmt.get("invalid_count") != 0
    ):
        errors.append("Human-QA stage requires 20 current technical and Formatter passes.")
    expected_ids=[q["id"] for q in source_questions]
    if elig.get("candidate_question_ids") != expected_ids or elig.get("paper_eligibility_candidate_count") != 20:
        errors.append("Eligibility candidates do not match all current Batch 001 IDs.")
elif stage == "PAPER_ELIGIBILITY_CERTIFIED":
    if human.get("final_decision") != "APPROVE_REVIEWED_RESULTS":
        errors.append("Certified stage requires recorded human approval.")
    certified_ids = elig.get("certified_paper_eligible_question_ids", [])
    if elig.get("paper_eligible_count") != len(certified_ids):
        errors.append("Certified paper-eligible count does not match the certified ID list.")
else:
    errors.append(f"Unsupported qualification stage: {stage!r}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("GATE EE BATCH 001 QUALIFICATION STATE: CONSISTENT")
print(f"Current stage: {stage}")
print(f"Current source SHA-256: {sha}")
print(f"Paper-eligible: {elig.get('paper_eligible_count', 0)}")
print(f"Release gate: {elig.get('release_gate')}")
