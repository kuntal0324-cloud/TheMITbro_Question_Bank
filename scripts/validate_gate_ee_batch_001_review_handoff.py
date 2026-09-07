from pathlib import Path
import json, hashlib, re

ROOT = Path(__file__).resolve().parents[1]
batch_path = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
review_path = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_001_TECHNICAL_REVIEW.json"
handoff_path = ROOT / "GATE_EE/corpus_v1/formatter_handoff/BATCH_001_FORMATTER_V2_HANDOFF.json"
summary_path = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_001_QUALIFICATION_SUMMARY.json"
formatter_path = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_001_FORMATTER_FINAL_EVIDENCE.json"
review_manifest_path = ROOT / "GATE_EE/corpus_v1/review_manifests/BATCH_001_REVIEW.json"

errors = []
qs = [json.loads(x) for x in batch_path.read_text(encoding="utf-8").splitlines() if x.strip()]
review = json.loads(review_path.read_text(encoding="utf-8"))
handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
summary = json.loads(summary_path.read_text(encoding="utf-8"))
formatter = json.loads(formatter_path.read_text(encoding="utf-8"))
review_manifest = json.loads(review_manifest_path.read_text(encoding="utf-8"))

ids = [q["id"] for q in qs]
families = [q["family_id"] for q in qs]

if len(qs) != 20:
    errors.append("Batch 001 must contain 20 questions.")
if len(set(ids)) != len(ids):
    errors.append("Duplicate question IDs detected.")
if len(set(families)) != len(families):
    errors.append("Duplicate family IDs detected inside Batch 001.")
stage = summary.get("current_stage")
if stage == "FORMATTER_REVIEW_REQUIRED":
    if review.get("technical_second_pass_passed") != 0 or review.get("technical_second_pass_pending") != 20:
        errors.append("Revised source technical-review state must be 0 passed / 20 pending.")
elif review.get("technical_second_pass_passed") != 20:
    errors.append("Technical second-pass count mismatch.")
elif review.get("technical_second_pass_pending") != 0:
    errors.append("Technical second-pass pending count must be zero.")
if review.get("paper_eligible_count") != 0:
    errors.append("Questions must remain non-paper-eligible before Formatter + independent review.")
if review.get("independent_human_review_required") is not True:
    errors.append("Independent human review gate missing.")
if review.get("formatter_v2_validation_required") is not True:
    errors.append("Formatter v2 validation gate missing.")
if handoff.get("formatter_required_version") != "2.0.0":
    errors.append("Formatter target version mismatch.")
if handoff.get("source_sha256") != hashlib.sha256(batch_path.read_bytes()).hexdigest():
    errors.append("Formatter handoff source checksum mismatch.")
if handoff.get("release_gate") != "BLOCKED":
    errors.append("Release gate must remain blocked.")
allowed_stages = {
    "READY_FOR_FORMATTER_HANDOFF",
    "READY_FOR_FORMATTER_REQUALIFICATION",
    "FORMATTER_REVIEW_REQUIRED",
    "READY_FOR_HUMAN_FINAL_QA",
    "PAPER_ELIGIBILITY_CERTIFIED",
}
if stage not in allowed_stages:
    errors.append("Qualification stage mismatch.")
if summary.get("paper_eligible_count") != 0:
    errors.append("Qualification summary paper eligibility mismatch.")
if stage == "READY_FOR_HUMAN_FINAL_QA":
    if formatter.get("source_sha256") != hashlib.sha256(batch_path.read_bytes()).hexdigest():
        errors.append("Formatter evidence checksum mismatch.")
    if (formatter.get("status"), formatter.get("formatter_pass_count"), formatter.get("formatter_review_count"), formatter.get("invalid_count")) != ("PASS", 20, 0, 0):
        errors.append("Human-QA handoff requires Formatter 20 PASS / 0 REVIEW / 0 invalid.")
    if review_manifest.get("status") != "READY_FOR_HUMAN_FINAL_QA" or len(review_manifest.get("questions", [])) != 20:
        errors.append("Fresh human review manifest is missing or incomplete.")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("GATE EE BATCH 001 REVIEW/HANDOFF: PASSED")
print("Questions: 20")
print(f"Internal technical second-pass: {review.get('technical_second_pass_passed', 0)}/20")
print("Unique IDs/families: PASSED")
print("Formatter v2.0 handoff checksum: PASSED")
print("Paper-eligible: 0")
print("Next gate: named human technical and final review")
