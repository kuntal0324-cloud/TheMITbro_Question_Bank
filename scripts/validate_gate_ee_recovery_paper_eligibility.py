#!/usr/bin/env python3
"""Validate pre-promotion or certified state for Batches 004 and 005."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gate_ee_recovery_batches import BATCHES, BASE, RecoveryBatch, load_questions
from validate_gate_ee_recovery_human_signoff import validate as validate_human_signoff

FAMILY_REGISTRY = BASE / "families/FAMILY_REGISTRY.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate_path(batch: RecoveryBatch) -> Path:
    return BASE / "qualification" / f"{batch.batch_id}_PAPER_ELIGIBILITY_CERTIFICATE.json"


def admission_path(batch: RecoveryBatch) -> Path:
    return BASE / "manifests" / f"{batch.batch_id}_CORPUS_ADMISSION.json"


def validate_batch(batch: RecoveryBatch, global_rows: list[dict]) -> tuple[list[str], str, int]:
    errors: list[str] = []
    questions = load_questions(batch)
    expected_ids = [question["id"] for question in questions]
    source_sha = sha256(batch.source)
    formatter_sha = sha256(batch.formatter_evidence)
    qa_sha = sha256(batch.independent_qa)
    signoff_sha = sha256(batch.human_qa)
    human = load(batch.human_qa)
    candidate = load(batch.candidate)
    summary = load(batch.summary)
    manifest = load(batch.manifest)
    family_file = load(batch.families)
    stage = summary.get("current_stage")
    certificate_file = certificate_path(batch)
    admission_file = admission_path(batch)

    if certificate_file.exists() != admission_file.exists():
        errors.append("certificate and admission manifest must exist together")
    if candidate.get("source_sha256") != source_sha:
        errors.append("candidate source checksum mismatch")
    if candidate.get("candidate_question_ids") != expected_ids:
        errors.append("candidate IDs do not match the canonical source")
    if candidate.get("paper_eligibility_candidate_count") != len(expected_ids):
        errors.append("candidate count does not match the canonical source")

    human_errors, approved, revise, reject, _ = validate_human_signoff(batch.batch_id)
    errors.extend(human_errors)
    global_batch_rows = [row for row in global_rows if row.get("admission_batch") == batch.batch_id]
    global_other_rows = [row for row in global_rows if row.get("admission_batch") != batch.batch_id]
    other_family_ids = {row.get("family_id") for row in global_other_rows}
    other_question_ids = {
        qid for row in global_other_rows for qid in row.get("question_ids", [])
    }
    batch_family_rows = family_file.get("families", [])
    batch_family_ids = {row.get("family_id") for row in batch_family_rows}
    batch_question_ids = {
        qid for row in batch_family_rows for qid in row.get("question_ids", [])
    }
    if other_family_ids.intersection(batch_family_ids):
        errors.append("batch family collides with another admitted batch")
    if other_question_ids.intersection(batch_question_ids):
        errors.append("batch question ID collides with another admitted batch")

    if stage == "READY_FOR_HUMAN_FINAL_QA":
        if certificate_file.exists() or admission_file.exists():
            errors.append("pre-promotion state must not contain certificate/admission")
        if candidate.get("paper_eligible_count") != 0:
            errors.append("pre-promotion paper-eligible count must be zero")
        if candidate.get("prerequisites", {}).get("human_final_qa") != "PENDING":
            errors.append("candidate human-QA prerequisite must remain PENDING before promotion")
        if candidate.get("certified_paper_eligible_question_ids", []) != []:
            errors.append("pre-promotion candidate contains certified IDs")
        if manifest.get("status") != "READY_FOR_HUMAN_FINAL_QA" or manifest.get("paper_eligible_count") != 0:
            errors.append("pre-promotion source manifest state mismatch")
        if family_file.get("admission_status") != "NOT_ADMITTED_PENDING_HUMAN_FINAL_QA":
            errors.append("pre-promotion batch families have an unsafe admission state")
        if global_batch_rows:
            errors.append("pre-promotion global registry already contains batch families")
        state = (
            "READY_FOR_PROMOTION"
            if human.get("final_decision") == "APPROVE_REVIEWED_RESULTS" and not errors
            else "READY_FOR_HUMAN_FINAL_QA"
        )
        return errors, state, len(approved)

    if stage != "PAPER_ELIGIBILITY_CERTIFIED":
        errors.append(f"unsupported qualification stage: {stage!r}")
        return errors, "INVALID", 0
    if not certificate_file.exists() or not admission_file.exists():
        errors.append("certified state requires certificate and admission manifest")
        return errors, "CERTIFIED", len(approved)

    certificate = load(certificate_file)
    admission = load(admission_file)
    batch_token = batch.batch_id.replace("_", "")
    expected_reviewer = {
        "name": human.get("reviewer", {}).get("name"),
        "role_or_qualification": human.get("reviewer", {}).get("role_or_qualification"),
        "review_date": human.get("reviewer", {}).get("review_date"),
    }
    if certificate.get("certificate_contract") != f"GATE_EE_{batch_token}_PAPER_ELIGIBILITY_CERTIFICATE_V1":
        errors.append("certificate contract mismatch")
    if certificate.get("batch_id") != batch.batch_id:
        errors.append("certificate batch mismatch")
    if certificate.get("source_sha256") != source_sha:
        errors.append("certificate source checksum mismatch")
    if certificate.get("formatter_evidence_sha256") != formatter_sha:
        errors.append("certificate Formatter checksum mismatch")
    if certificate.get("independent_ai_qa_sha256") != qa_sha:
        errors.append("certificate independent-QA checksum mismatch")
    if certificate.get("human_signoff_sha256") != signoff_sha:
        errors.append("certificate human-signoff checksum mismatch")
    if certificate.get("completed_pdf_sha256") != human.get("pdf_evidence", {}).get("sha256"):
        errors.append("certificate completed-PDF checksum mismatch")
    if certificate.get("reviewer") != expected_reviewer:
        errors.append("certificate reviewer mismatch")
    if certificate.get("approved_question_ids") != approved:
        errors.append("certificate approved IDs do not match human PASS decisions")
    if certificate.get("revise_question_ids") != revise:
        errors.append("certificate revision IDs do not match human REVISE decisions")
    if certificate.get("rejected_question_ids") != reject:
        errors.append("certificate rejected IDs do not match human REJECT decisions")
    if certificate.get("paper_eligible_count") != len(approved) or certificate.get("decision") != "CERTIFIED":
        errors.append("certificate decision/count mismatch")

    if admission.get("manifest_contract") != f"GATE_EE_CORPUS_V1_{batch_token}_ADMISSION_V1":
        errors.append("admission contract mismatch")
    if admission.get("batch_id") != batch.batch_id:
        errors.append("admission batch mismatch")
    if admission.get("source_sha256") != source_sha:
        errors.append("admission source checksum mismatch")
    if admission.get("paper_eligibility_certificate_sha256") != sha256(certificate_file):
        errors.append("admission certificate checksum mismatch")
    if admission.get("admitted_question_ids") != approved:
        errors.append("admission IDs do not match certified IDs")
    if admission.get("held_for_revision_question_ids") != revise:
        errors.append("admission revision IDs mismatch")
    if admission.get("rejected_question_ids") != reject:
        errors.append("admission rejected IDs mismatch")
    if admission.get("admitted_count") != len(approved) or admission.get("status") != "ADMITTED_TO_CORPUS_V1":
        errors.append("admission status/count mismatch")

    if candidate.get("human_final_qa") != "COMPLETE":
        errors.append("candidate human-QA state mismatch")
    if candidate.get("prerequisites", {}).get("human_final_qa") != "COMPLETE":
        errors.append("candidate human-QA prerequisite state mismatch")
    if candidate.get("human_signoff_sha256") != signoff_sha:
        errors.append("candidate human-signoff checksum mismatch")
    if candidate.get("certified_paper_eligible_question_ids") != approved:
        errors.append("candidate certified IDs mismatch")
    if candidate.get("paper_eligible_count") != len(approved):
        errors.append("candidate paper-eligible count mismatch")
    if candidate.get("release_gate") != "PAPER_ELIGIBILITY_CERTIFIED":
        errors.append("candidate certification gate mismatch")

    human_summary = summary.get("human_final_qa", {})
    if summary.get("paper_eligible_count") != len(approved):
        errors.append("qualification-summary eligible count mismatch")
    if human_summary.get("status") != "COMPLETE" or human_summary.get("passed") != len(approved):
        errors.append("qualification-summary human-QA status/pass mismatch")
    if human_summary.get("revise") != len(revise) or human_summary.get("reject") != len(reject):
        errors.append("qualification-summary non-pass counts mismatch")
    if summary.get("release_gate") != "BLOCKED_NO_COMPLETE_65_QUESTION_SET":
        errors.append("qualification summary must keep paper release blocked")
    if manifest.get("status") != "PAPER_ELIGIBILITY_CERTIFIED_AND_ADMITTED":
        errors.append("certified source manifest status mismatch")
    if manifest.get("paper_eligible_count") != len(approved):
        errors.append("certified source manifest count mismatch")
    if family_file.get("admission_status") != "ADMITTED_TO_CORPUS_V1":
        errors.append("batch-family admission state mismatch")

    approved_set = set(approved)
    expected_family_map = {
        row.get("family_id"): [
            qid for qid in row.get("question_ids", []) if qid in approved_set
        ]
        for row in batch_family_rows
        if any(qid in approved_set for qid in row.get("question_ids", []))
    }
    found_family_map = {
        row.get("family_id"): row.get("question_ids") for row in global_batch_rows
    }
    if found_family_map != expected_family_map:
        errors.append("global family registry does not match certified batch families")
    return errors, "CERTIFIED", len(approved)


def main() -> int:
    registry = load(FAMILY_REGISTRY)
    rows = registry.get("families", [])
    family_ids = [row.get("family_id") for row in rows]
    question_ids = [qid for row in rows for qid in row.get("question_ids", [])]
    errors: list[str] = []
    results: list[tuple[str, str, int]] = []
    if len(family_ids) != len(set(family_ids)):
        errors.append("global family registry contains duplicate family IDs")
    if len(question_ids) != len(set(question_ids)):
        errors.append("global family registry contains duplicate question IDs")
    if registry.get("admitted_question_count") != len(question_ids):
        errors.append("global admitted-question count is inconsistent")

    for batch_id in sorted(BATCHES):
        batch_errors, state, count = validate_batch(BATCHES[batch_id], rows)
        errors.extend(f"{batch_id}: {error}" for error in batch_errors)
        results.append((batch_id, state, count))

    if errors:
        print("GATE EE BATCHES 004-005 PAPER-ELIGIBILITY CERTIFICATION: BLOCKED")
        for error in errors:
            print("-", error)
        return 1

    for batch_id, state, count in results:
        print(f"{batch_id} PAPER-ELIGIBILITY STATE: {state}")
        print(f"Certified/approved count: {count}")
    if all(state == "CERTIFIED" for _, state, _ in results):
        print("GATE EE BATCHES 004-005 PAPER-ELIGIBILITY CERTIFICATION: PASSED")
        print(f"Corpus V1 admitted total: {registry['admitted_question_count']}")
        print("Paper release gate: BLOCKED (manifest and final paper QA pending)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
