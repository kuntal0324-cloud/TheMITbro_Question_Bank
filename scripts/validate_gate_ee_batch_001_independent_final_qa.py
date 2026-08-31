from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/"GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
qa=json.loads((ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_INDEPENDENT_AI_QA.json").read_text())
fmt=json.loads((ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_FORMATTER_FINAL_EVIDENCE.json").read_text())
elig=json.loads((ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CANDIDATE.json").read_text())
human=json.loads((ROOT/"GATE_EE/corpus_v1/review_manifests/BATCH_001_HUMAN_FINAL_QA.json").read_text())
summary=json.loads((ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_QUALIFICATION_SUMMARY.json").read_text())

sha=hashlib.sha256(source.read_bytes()).hexdigest()
errors=[]
for name,obj in [("AI QA",qa),("Formatter evidence",fmt),("Eligibility candidate",elig),("Human QA",human)]:
    if obj.get("source_sha256") != sha:
        errors.append(f"{name}: source checksum mismatch")
if qa.get("technical_pass_count")!=20 or qa.get("answer_recomputed_pass_count")!=20 or qa.get("solution_consistency_pass_count")!=20:
    errors.append("AI QA is not 20/20.")
if fmt.get("formatter_pass_count")!=20 or fmt.get("formatter_review_count")!=0:
    errors.append("Formatter evidence is not 20 PASS / 0 REVIEW.")
if elig.get("paper_eligibility_candidate_count")!=20:
    errors.append("Eligibility candidate count mismatch.")
stage=summary.get("current_stage")
if stage=="READY_FOR_HUMAN_FINAL_QA":
    if elig.get("paper_eligible_count")!=0: errors.append("Paper eligibility must remain zero before human signoff.")
    if human.get("final_decision")!="PENDING": errors.append("Human final QA template must remain pending.")
elif stage=="PAPER_ELIGIBILITY_CERTIFIED":
    if human.get("final_decision")!="APPROVE_REVIEWED_RESULTS": errors.append("Certified stage requires human approval.")
    if elig.get("human_final_qa")!="COMPLETE": errors.append("Certified stage requires human_final_qa COMPLETE.")
else:
    errors.append("Qualification summary stage mismatch.")
if errors:
    print("\n".join(errors)); raise SystemExit(1)

print("GATE EE BATCH 001 INDEPENDENT FINAL QA: PASSED")
print("Independent AI technical/answer/solution QA: 20/20")
print("Formatter v2.0 final qualification: 20 PASS / 0 REVIEW")
print("Paper-eligibility candidates: 20")
print(f"Certified paper-eligible: {elig.get('paper_eligible_count',0)}")
print(f"Human final QA: {'COMPLETE' if summary.get('current_stage')=='PAPER_ELIGIBILITY_CERTIFIED' else 'PENDING'}")
print(f"Release gate: {elig.get('release_gate')}")
