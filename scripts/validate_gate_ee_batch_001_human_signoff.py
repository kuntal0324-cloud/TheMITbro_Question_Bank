from pathlib import Path
from datetime import date
import json, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
HUMAN=ROOT/"GATE_EE/corpus_v1/review_manifests/BATCH_001_HUMAN_FINAL_QA.json"
CANDIDATE=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CANDIDATE.json"

def validate():
    human=json.loads(HUMAN.read_text(encoding="utf-8"))
    candidate=json.loads(CANDIDATE.read_text(encoding="utf-8"))
    source_sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    questions=[json.loads(x) for x in SOURCE.read_text(encoding="utf-8").splitlines() if x.strip()]
    expected={(q["id"],q["revision"]) for q in questions}
    errors=[]

    if human.get("source_sha256")!=source_sha: errors.append("Human QA source checksum mismatch.")
    if candidate.get("source_sha256")!=source_sha: errors.append("Eligibility candidate source checksum mismatch.")

    reviewer=human.get("reviewer",{})
    for field in ("name","role_or_qualification","review_date","attestation"):
        if not str(reviewer.get(field,"")).strip(): errors.append(f"Missing reviewer field: {field}")
    rd=str(reviewer.get("review_date",""))
    if rd and not re.fullmatch(r"\d{4}-\d{2}-\d{2}",rd): errors.append("review_date must use YYYY-MM-DD.")
    elif rd:
        try: date.fromisoformat(rd)
        except ValueError: errors.append("review_date is not a valid calendar date.")
    if reviewer.get("attestation")!=human.get("required_attestation"):
        errors.append("Reviewer attestation does not exactly match required_attestation.")

    rows=human.get("questions",[])
    found={(q.get("question_id"),q.get("revision")) for q in rows}
    if found!=expected or len(rows)!=len(expected): errors.append("Human QA IDs/revisions do not match canonical Batch 001.")

    approved=[]; revise=[]; reject=[]
    for row in rows:
        qid=row.get("question_id","?")
        checks=[row.get("technical_correctness"),row.get("answer_correctness"),row.get("solution_correctness"),
                row.get("clarity_ambiguity"),row.get("originality_conflict_check")]
        if any(v not in {"PASS","FAIL"} for v in checks):
            errors.append(f"{qid}: all five human checks must be PASS or FAIL.")
        decision=row.get("decision")
        if decision=="PASS":
            if any(v!="PASS" for v in checks): errors.append(f"{qid}: PASS requires all five checks PASS.")
            else: approved.append(qid)
        elif decision=="REVISE": revise.append(qid)
        elif decision=="REJECT": reject.append(qid)
        else: errors.append(f"{qid}: decision must be PASS, REVISE, or REJECT.")

    if human.get("final_decision")!="APPROVE_REVIEWED_RESULTS":
        errors.append("final_decision must be APPROVE_REVIEWED_RESULTS.")
    return errors,approved,revise,reject,source_sha

if __name__=="__main__":
    errors,approved,revise,reject,source_sha=validate()
    if errors:
        print("HUMAN FINAL QA SIGNOFF: BLOCKED")
        for e in errors: print("-",e)
        raise SystemExit(1)
    print("HUMAN FINAL QA SIGNOFF: PASSED")
    print(f"Source SHA-256: {source_sha}")
    print(f"PASS: {len(approved)}")
    print(f"REVISE: {len(revise)}")
    print(f"REJECT: {len(reject)}")
