from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/"GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
human_path=ROOT/"GATE_EE/corpus_v1/review_manifests/BATCH_001_HUMAN_FINAL_QA.json"
elig_path=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CANDIDATE.json"

human=json.loads(human_path.read_text())
elig=json.loads(elig_path.read_text())
errors=[]
sha=hashlib.sha256(source.read_bytes()).hexdigest()
if human.get("source_sha256")!=sha:
    errors.append("Human QA source checksum mismatch.")

reviewer=human.get("reviewer",{})
for k in ("name","role_or_qualification","review_date","attestation"):
    if not str(reviewer.get(k,"")).strip():
        errors.append(f"Missing reviewer field: {k}")
if reviewer.get("attestation") != human.get("required_attestation"):
    errors.append("Reviewer attestation does not exactly match required attestation.")

approved=[]
for q in human.get("questions",[]):
    checks=[q.get("technical_correctness"),q.get("answer_correctness"),
            q.get("solution_correctness"),q.get("clarity_ambiguity"),
            q.get("originality_conflict_check")]
    decision=q.get("decision")
    if decision=="PASS":
        if any(x!="PASS" for x in checks):
            errors.append(f"{q.get('question_id')}: PASS decision without all PASS checks.")
        else:
            approved.append(q["question_id"])
    elif decision not in {"REJECT","REVISE"}:
        errors.append(f"{q.get('question_id')}: decision must be PASS, REJECT, or REVISE.")

if human.get("final_decision")!="APPROVE_REVIEWED_RESULTS":
    errors.append("Human final decision must be APPROVE_REVIEWED_RESULTS.")

if errors:
    print("PAPER-ELIGIBILITY PROMOTION: BLOCKED")
    for e in errors:
        print("-",e)
    raise SystemExit(1)

elig["human_final_qa"]="COMPLETE"
elig["certified_paper_eligible_question_ids"]=approved
elig["paper_eligible_count"]=len(approved)
elig["release_gate"]="PAPER_ELIGIBILITY_CERTIFIED"
elig_path.write_text(json.dumps(elig,indent=2))
print("PAPER-ELIGIBILITY PROMOTION: PASSED")
print(f"Certified paper-eligible: {len(approved)}")
