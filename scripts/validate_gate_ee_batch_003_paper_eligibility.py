from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_gate_ee_batch_003_human_signoff import validate as validate_human_signoff


BASE = ROOT / "GATE_EE/corpus_v1"
SOURCE = BASE / "source_batches/BATCH_003_GENERAL_APTITUDE.jsonl"
FORMATTER = BASE / "qualification/BATCH_003_FORMATTER_FINAL_EVIDENCE.json"
QA = BASE / "qualification/BATCH_003_INDEPENDENT_AI_QA.json"
HUMAN = BASE / "review_manifests/BATCH_003_HUMAN_FINAL_QA.json"
CANDIDATE = BASE / "qualification/BATCH_003_PAPER_ELIGIBILITY_CANDIDATE.json"
SUMMARY = BASE / "qualification/BATCH_003_QUALIFICATION_SUMMARY.json"
CERTIFICATE = BASE / "qualification/BATCH_003_PAPER_ELIGIBILITY_CERTIFICATE.json"
ADMISSION = BASE / "manifests/BATCH_003_CORPUS_ADMISSION.json"
MANIFEST = BASE / "manifests/BATCH_003_MANIFEST.json"
BATCH_FAMILIES = BASE / "families/BATCH_003_FAMILIES.json"
FAMILY_REGISTRY = BASE / "families/FAMILY_REGISTRY.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    formatter_sha = hashlib.sha256(FORMATTER.read_bytes()).hexdigest()
    qa_sha = hashlib.sha256(QA.read_bytes()).hexdigest()
    signoff_sha = hashlib.sha256(HUMAN.read_bytes()).hexdigest()
    questions = [
        json.loads(line)
        for line in SOURCE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected_ids = [question["id"] for question in questions]
    human = load(HUMAN)
    candidate = load(CANDIDATE)
    summary = load(SUMMARY)
    manifest = load(MANIFEST)
    batch_families = load(BATCH_FAMILIES)
    family_registry = load(FAMILY_REGISTRY)
    errors: list[str] = []
    stage = summary.get("current_stage")
    certificate_exists = CERTIFICATE.exists()
    admission_exists = ADMISSION.exists()

    if certificate_exists != admission_exists:
        errors.append("Batch 003 certificate and admission manifest must exist together")
    if candidate.get("source_sha256") != source_sha: errors.append("candidate source checksum mismatch")
    if candidate.get("candidate_question_ids") != expected_ids:
        errors.append("candidate IDs do not match the canonical source")
    if candidate.get("paper_eligibility_candidate_count") != len(expected_ids):
        errors.append("candidate count does not match the canonical source")

    signoff_errors, approved, revise, reject, _ = validate_human_signoff()
    errors.extend(signoff_errors)

    if stage == "READY_FOR_HUMAN_FINAL_QA":
        if certificate_exists or admission_exists:
            errors.append("pre-promotion state must not contain a Batch 003 certificate or admission manifest")
        if candidate.get("paper_eligible_count") != 0:
            errors.append("pre-promotion Batch 003 paper eligibility must be zero")
        if candidate.get("prerequisites", {}).get("human_final_qa") != "PENDING":
            errors.append("candidate must remain pending until promotion")
        if candidate.get("certified_paper_eligible_question_ids", []) != []:
            errors.append("pre-promotion candidate must not contain certified IDs")
        if manifest.get("status") != "READY_FOR_HUMAN_FINAL_QA" or manifest.get("paper_eligible_count") != 0:
            errors.append("pre-promotion Batch 003 manifest state mismatch")
        if batch_families.get("admission_status") != "NOT_ADMITTED":
            errors.append("pre-promotion Batch 003 families must not be admitted")
        global_ids = {qid for row in family_registry.get("families", []) for qid in row.get("question_ids", [])}
        if global_ids.intersection(expected_ids):
            errors.append("pre-promotion global family registry contains Batch 003 IDs")
    elif stage == "PAPER_ELIGIBILITY_CERTIFIED":
        if not certificate_exists or not admission_exists:
            errors.append("certified state requires a certificate and Corpus V1 admission manifest")
        else:
            certificate = load(CERTIFICATE)
            admission = load(ADMISSION)
            expected_reviewer = {
                "name": human.get("reviewer", {}).get("name"),
                "role_or_qualification": human.get("reviewer", {}).get("role_or_qualification"),
                "review_date": human.get("reviewer", {}).get("review_date"),
            }
            if certificate.get("certificate_contract") != "GATE_EE_BATCH003_PAPER_ELIGIBILITY_CERTIFICATE_V1":
                errors.append("certificate contract mismatch")
            if certificate.get("batch_id") != "BATCH_003": errors.append("certificate batch mismatch")
            if certificate.get("source_sha256") != source_sha: errors.append("certificate source checksum mismatch")
            if certificate.get("formatter_evidence_sha256") != formatter_sha:
                errors.append("certificate Formatter checksum mismatch")
            if certificate.get("independent_ai_qa_sha256") != qa_sha:
                errors.append("certificate independent-AI checksum mismatch")
            if certificate.get("human_signoff_sha256") != signoff_sha:
                errors.append("certificate human-signoff checksum mismatch")
            if certificate.get("completed_pdf_sha256") != human.get("pdf_evidence", {}).get("sha256"):
                errors.append("certificate completed-PDF checksum mismatch")
            if certificate.get("reviewer") != expected_reviewer: errors.append("certificate reviewer mismatch")
            if certificate.get("approved_question_ids") != approved:
                errors.append("certificate approved IDs do not match human PASS decisions")
            if certificate.get("revise_question_ids") != revise:
                errors.append("certificate revision IDs do not match human REVISE decisions")
            if certificate.get("rejected_question_ids") != reject:
                errors.append("certificate rejected IDs do not match human REJECT decisions")
            if certificate.get("paper_eligible_count") != len(approved) or certificate.get("decision") != "CERTIFIED":
                errors.append("certificate decision/count mismatch")

            if admission.get("manifest_contract") != "GATE_EE_CORPUS_V1_BATCH003_ADMISSION_V1":
                errors.append("admission contract mismatch")
            if admission.get("batch_id") != "BATCH_003": errors.append("admission batch mismatch")
            if admission.get("source_sha256") != source_sha: errors.append("admission source checksum mismatch")
            if admission.get("paper_eligibility_certificate_sha256") != hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest():
                errors.append("admission certificate checksum mismatch")
            if admission.get("admitted_question_ids") != approved:
                errors.append("admission IDs do not match certified IDs")
            if admission.get("held_for_revision_question_ids") != revise:
                errors.append("admission revision IDs mismatch")
            if admission.get("rejected_question_ids") != reject:
                errors.append("admission rejected IDs mismatch")
            if admission.get("admitted_count") != len(approved) or admission.get("status") != "ADMITTED_TO_CORPUS_V1":
                errors.append("admission status/count mismatch")

            if candidate.get("human_final_qa") != "COMPLETE": errors.append("candidate human-QA state mismatch")
            if candidate.get("prerequisites", {}).get("human_final_qa") != "COMPLETE":
                errors.append("candidate human-QA prerequisite state mismatch")
            if candidate.get("human_signoff_sha256") != signoff_sha:
                errors.append("candidate human-signoff checksum mismatch")
            if candidate.get("certified_paper_eligible_question_ids") != approved:
                errors.append("candidate certified IDs mismatch")
            if candidate.get("paper_eligible_count") != len(approved): errors.append("candidate eligible count mismatch")
            if candidate.get("release_gate") != "PAPER_ELIGIBILITY_CERTIFIED":
                errors.append("candidate certification gate mismatch")

            human_summary = summary.get("human_final_qa", {})
            if summary.get("paper_eligible_count") != len(approved): errors.append("summary eligible count mismatch")
            if human_summary.get("status") != "COMPLETE" or human_summary.get("passed") != len(approved):
                errors.append("summary human-QA status/pass count mismatch")
            if human_summary.get("revise") != len(revise) or human_summary.get("reject") != len(reject):
                errors.append("summary human-QA non-pass counts mismatch")
            if summary.get("release_gate") != "BLOCKED_NO_COMPLETE_65_QUESTION_SET":
                errors.append("summary must keep paper release blocked")
            if manifest.get("status") != "PAPER_ELIGIBILITY_CERTIFIED_AND_ADMITTED":
                errors.append("certified Batch 003 manifest status mismatch")
            if manifest.get("paper_eligible_count") != len(approved):
                errors.append("Batch 003 manifest eligible count mismatch")
            if batch_families.get("admission_status") != "ADMITTED_TO_CORPUS_V1":
                errors.append("Batch 003 family admission state mismatch")

            approved_set = set(approved)
            expected_family_map = {
                row.get("family_id"): [qid for qid in row.get("question_ids", []) if qid in approved_set]
                for row in batch_families.get("families", [])
                if any(qid in approved_set for qid in row.get("question_ids", []))
            }
            found_family_map = {
                row.get("family_id"): row.get("question_ids")
                for row in family_registry.get("families", [])
                if row.get("admission_batch") == "BATCH_003"
            }
            if found_family_map != expected_family_map:
                errors.append("global family registry does not match admitted Batch 003 families")
    else:
        errors.append(f"unsupported Batch 003 qualification stage: {stage!r}")

    if errors:
        print("BATCH 003 PAPER-ELIGIBILITY CERTIFICATION: BLOCKED")
        for error in errors:
            print("-", error)
        return 1

    if stage == "READY_FOR_HUMAN_FINAL_QA":
        if human.get("final_decision") == "APPROVE_REVIEWED_RESULTS":
            print("BATCH 003 PAPER-ELIGIBILITY CERTIFICATION STATE: READY_FOR_PROMOTION")
            print(f"Human-approved: {len(approved)}")
            print(f"Held for revision: {len(revise)}")
            print(f"Rejected: {len(reject)}")
        else:
            print("BATCH 003 PAPER-ELIGIBILITY CERTIFICATION STATE: READY_FOR_HUMAN_FINAL_QA")
            print("Certified paper-eligible: 0")
    else:
        print("BATCH 003 PAPER-ELIGIBILITY CERTIFICATION: PASSED")
        print(f"Certified paper-eligible: {len(approved)}")
        print("Corpus V1 admission manifest: PASSED")
        print("Paper release gate: BLOCKED (no complete blueprint)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
