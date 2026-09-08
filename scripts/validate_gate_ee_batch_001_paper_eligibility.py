from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_gate_ee_batch_001_human_signoff import validate as validate_human_signoff
SOURCE=ROOT/"GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
HUMAN=ROOT/"GATE_EE/corpus_v1/review_manifests/BATCH_001_HUMAN_FINAL_QA.json"
CANDIDATE=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CANDIDATE.json"
SUMMARY=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_QUALIFICATION_SUMMARY.json"
CERT=ROOT/"GATE_EE/corpus_v1/qualification/BATCH_001_PAPER_ELIGIBILITY_CERTIFICATE.json"
ADMISSION=ROOT/"GATE_EE/corpus_v1/manifests/BATCH_001_CORPUS_ADMISSION.json"
sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
human=json.loads(HUMAN.read_text(encoding="utf-8")); candidate=json.loads(CANDIDATE.read_text(encoding="utf-8"))
summary=json.loads(SUMMARY.read_text(encoding="utf-8")); errors=[]
if human.get("source_sha256")!=sha or candidate.get("source_sha256")!=sha: errors.append("Source checksum mismatch.")
stage=summary.get("current_stage")
if stage in {"READY_FOR_FORMATTER_REQUALIFICATION", "FORMATTER_REVIEW_REQUIRED"}:
    if candidate.get("paper_eligible_count")!=0: errors.append("Recovery stage paper eligibility must be zero.")
    if candidate.get("paper_eligibility_candidate_count")!=0: errors.append("Recovery stage candidate count must be zero.")
    if human.get("final_decision")!="PENDING": errors.append("Human decision must remain pending during recovery.")
    if errors: print("\n".join(errors)); raise SystemExit(1)
    print(f"BATCH 001 PAPER-ELIGIBILITY STATE: {stage}")
    print("Certified paper-eligible: 0")
    print("Release gate: BLOCKED")
elif stage=="READY_FOR_HUMAN_FINAL_QA":
    if candidate.get("paper_eligible_count")!=0: errors.append("Pre-signoff paper eligibility must be zero.")
    if CERT.exists() or ADMISSION.exists(): errors.append("Certificate/admission must not exist before promotion.")
    decision=human.get("final_decision")
    if decision=="APPROVE_REVIEWED_RESULTS":
        signoff_errors,approved,revise,reject,_=validate_human_signoff()
        errors.extend(signoff_errors)
    elif decision!="PENDING":
        errors.append("Unexpected human decision before promotion.")
    if errors: print("\n".join(errors)); raise SystemExit(1)
    if decision=="APPROVE_REVIEWED_RESULTS":
        print("BATCH 001 PAPER-ELIGIBILITY CERTIFICATION STATE: READY_FOR_PROMOTION")
        print(f"Human-approved: {len(approved)}")
        print(f"Held for revision: {len(revise)}")
        print(f"Rejected: {len(reject)}")
    else:
        print("BATCH 001 PAPER-ELIGIBILITY CERTIFICATION STATE: READY_FOR_HUMAN_FINAL_QA")
        print("Certified paper-eligible: 0")
        print("Human signoff: PENDING")
elif stage=="PAPER_ELIGIBILITY_CERTIFIED":
    signoff_errors,approved,revise,reject,_=validate_human_signoff()
    errors.extend(signoff_errors)
    if not CERT.exists() or not ADMISSION.exists(): errors.append("Certified state requires certificate and admission manifest.")
    else:
        cert=json.loads(CERT.read_text(encoding="utf-8")); admission=json.loads(ADMISSION.read_text(encoding="utf-8"))
        if cert.get("source_sha256")!=sha: errors.append("Certificate source checksum mismatch.")
        if cert.get("human_signoff_sha256")!=hashlib.sha256(HUMAN.read_bytes()).hexdigest(): errors.append("Human signoff checksum mismatch.")
        if cert.get("approved_question_ids")!=approved: errors.append("Certificate approved IDs do not match human PASS decisions.")
        if cert.get("revise_question_ids")!=revise: errors.append("Certificate revision IDs do not match human REVISE decisions.")
        if cert.get("rejected_question_ids")!=reject: errors.append("Certificate rejected IDs do not match human REJECT decisions.")
        if candidate.get("paper_eligible_count")!=cert.get("paper_eligible_count"): errors.append("Eligible count mismatch.")
        if candidate.get("certified_paper_eligible_question_ids")!=approved: errors.append("Candidate certified IDs do not match human PASS decisions.")
        if candidate.get("human_final_qa")!="COMPLETE" or candidate.get("release_gate")!="PAPER_ELIGIBILITY_CERTIFIED": errors.append("Candidate certification state mismatch.")
        if admission.get("admitted_question_ids")!=cert.get("approved_question_ids"): errors.append("Admission/certificate IDs mismatch.")
        if admission.get("paper_eligibility_certificate_sha256")!=hashlib.sha256(CERT.read_bytes()).hexdigest(): errors.append("Admission certificate checksum mismatch.")
        if summary.get("paper_eligible_count")!=len(approved): errors.append("Summary eligible count mismatch.")
    if errors: print("\n".join(errors)); raise SystemExit(1)
    print("BATCH 001 PAPER-ELIGIBILITY CERTIFICATION: PASSED")
    print(f"Certified paper-eligible: {candidate['paper_eligible_count']}")
    print("Corpus V1 admission manifest: PASSED")
else:
    print("Unknown certification stage."); raise SystemExit(1)
