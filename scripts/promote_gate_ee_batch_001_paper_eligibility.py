from pathlib import Path
import json, hashlib, os, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.validate_gate_ee_batch_001_human_signoff import validate

SOURCE=ROOT/"GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
HUMAN=ROOT/"GATE_EE/corpus_v1/review_manifests/BATCH_001_HUMAN_FINAL_QA.json"
CANDIDATE=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CANDIDATE.json"
SUMMARY=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_QUALIFICATION_SUMMARY.json"
REVIEW=ROOT/"GATE_EE/corpus_v1/review_manifests/BATCH_001_REVIEW.json"
CERT=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CERTIFICATE.json"
ADMISSION=ROOT/"GATE_EE/corpus_v1/manifests/BATCH_001_CORPUS_ADMISSION.json"

errors,approved,revise,reject,source_sha=validate()
if errors:
    print("PAPER-ELIGIBILITY PROMOTION: BLOCKED")
    for e in errors: print("-",e)
    raise SystemExit(1)

human=json.loads(HUMAN.read_text(encoding="utf-8"))
candidate=json.loads(CANDIDATE.read_text(encoding="utf-8"))
summary=json.loads(SUMMARY.read_text(encoding="utf-8"))
review=json.loads(REVIEW.read_text(encoding="utf-8"))
if summary.get("current_stage") != "READY_FOR_HUMAN_FINAL_QA":
    print("PAPER-ELIGIBILITY PROMOTION: BLOCKED")
    print("- Promotion requires current_stage READY_FOR_HUMAN_FINAL_QA.")
    raise SystemExit(1)
signoff_sha=hashlib.sha256(HUMAN.read_bytes()).hexdigest()

candidate.update({
    "human_final_qa":"COMPLETE",
    "certified_paper_eligible_question_ids":approved,
    "paper_eligible_count":len(approved),
    "release_gate":"PAPER_ELIGIBILITY_CERTIFIED",
    "human_signoff_sha256":signoff_sha,
})
certificate={
    "certificate_contract":"GATE_EE_BATCH001_PAPER_ELIGIBILITY_CERTIFICATE_V1",
    "batch_id":"BATCH_001","source_sha256":source_sha,"human_signoff_sha256":signoff_sha,
    "reviewer":{"name":human["reviewer"]["name"],"role_or_qualification":human["reviewer"]["role_or_qualification"],
                "review_date":human["reviewer"]["review_date"]},
    "approved_question_ids":approved,"revise_question_ids":revise,"rejected_question_ids":reject,
    "paper_eligible_count":len(approved),"decision":"CERTIFIED",
}
certificate_bytes=(json.dumps(certificate,indent=2)+"\n").encode("utf-8")

admission={
    "manifest_contract":"GATE_EE_CORPUS_V1_BATCH001_ADMISSION_V1","batch_id":"BATCH_001",
    "source_sha256":source_sha,
    "paper_eligibility_certificate_sha256":hashlib.sha256(certificate_bytes).hexdigest(),
    "admitted_question_ids":approved,"held_for_revision_question_ids":revise,"rejected_question_ids":reject,
    "admitted_count":len(approved),"status":"ADMITTED_TO_CORPUS_V1",
}

summary.update({
    "current_stage":"PAPER_ELIGIBILITY_CERTIFIED","paper_eligible_count":len(approved),
    "remaining_gates":[],
    "next_action":"Admit certified questions to Corpus V1 master pool and begin Production Batch 002.",
    "human_final_qa":{"status":"COMPLETE","review_date":human["reviewer"]["review_date"],
                      "paper_eligible":len(approved),"revise":len(revise),"reject":len(reject)}
})

review["status"]="HUMAN_FINAL_QA_COMPLETE"
human_by_id={row["question_id"]:row for row in human["questions"]}
for row in review.get("questions",[]):
    hr=human_by_id.get(row.get("question_id"))
    if hr is None:
        print("PAPER-ELIGIBILITY PROMOTION: BLOCKED")
        print(f"- Missing human review row for {row.get('question_id', '?')}.")
        raise SystemExit(1)
    row["human_decision"]=hr["decision"]
    row["human_checks"]={
        "technical_correctness":hr["technical_correctness"],
        "answer_correctness":hr["answer_correctness"],
        "solution_correctness":hr["solution_correctness"],
        "clarity_ambiguity":hr["clarity_ambiguity"],
        "originality_conflict_check":hr["originality_conflict_check"],
    }

if len(review.get("questions",[])) != len(human_by_id):
    print("PAPER-ELIGIBILITY PROMOTION: BLOCKED")
    print("- Review manifest and human signoff question counts differ.")
    raise SystemExit(1)

def atomic_bytes_write(path, data):
    fd,temp_name=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name,path)
    except Exception:
        try: os.unlink(temp_name)
        except FileNotFoundError: pass
        raise

def atomic_json_write(path, payload):
    atomic_bytes_write(path,(json.dumps(payload,indent=2)+"\n").encode("utf-8"))

atomic_json_write(CANDIDATE,candidate)
atomic_bytes_write(CERT,certificate_bytes)
atomic_json_write(ADMISSION,admission)
atomic_json_write(SUMMARY,summary)
atomic_json_write(REVIEW,review)

print("PAPER-ELIGIBILITY PROMOTION: PASSED")
print(f"Certified paper-eligible: {len(approved)}")
print(f"Held for revision: {len(revise)}")
print(f"Rejected: {len(reject)}")
