#!/usr/bin/env python3
"""Validate a completed Set 01 whole-paper human-QA record, when present."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from gate_ee_set01 import (
    HUMAN_QA,
    ROOT,
    content_sha256,
    load_json,
    sha256,
    validate_manifest_and_handoff,
)
from render_gate_ee_set01_review_artifacts import REQUIRED_ATTESTATION


COMPLETED_SIGNOFF = (
    ROOT / "GATE_EE/corpus_v1/review_manifests/"
    "GATE_EE_SET_01_HUMAN_FINAL_QA_COMPLETED.json"
)


def resolve_completed_pdf(recorded_path: object) -> Path | None:
    if not isinstance(recorded_path, str) or not recorded_path.strip():
        return None
    path = Path(recorded_path)
    if path.is_absolute():
        return path
    candidate = (ROOT / path).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def validate_completed_signoff(payload: dict, template: dict) -> tuple[list[str], bool]:
    errors: list[str] = []
    static_fields = (
        "signoff_contract",
        "paper_id",
        "manifest_content_sha256",
        "formatter_handoff_content_sha256",
        "question_pdf_sha256",
        "solution_pdf_sha256",
        "required_attestation",
    )
    for field in static_fields:
        if payload.get(field) != template.get(field):
            errors.append(f"completed signoff {field} differs from the issued template")

    if payload.get("signoff_content_sha256") != content_sha256(payload, "signoff_content_sha256"):
        errors.append("completed signoff self-hash is invalid")
    if payload.get("release_authorized") is not False:
        errors.append("completed human QA must not authorize release")
    if payload.get("sale_authorized") is not False:
        errors.append("completed human QA must not authorize sale")

    completed_pdf = payload.get("completed_pdf", {})
    completed_pdf_path = resolve_completed_pdf(completed_pdf.get("path"))
    if completed_pdf_path is None or not completed_pdf_path.is_file():
        errors.append("completed signoff PDF is missing or its path is not portable")
    elif completed_pdf.get("sha256") != sha256(completed_pdf_path):
        errors.append("completed signoff PDF checksum mismatch")

    reviewer = payload.get("reviewer", {})
    for field in ("name", "role_or_qualification", "review_date", "signature"):
        if not str(reviewer.get(field, "")).strip():
            errors.append(f"reviewer {field} is blank")
    try:
        date.fromisoformat(str(reviewer.get("review_date", "")))
    except ValueError:
        errors.append("review date must use YYYY-MM-DD")
    if " ".join(str(reviewer.get("attestation", "")).split()) != " ".join(REQUIRED_ATTESTATION.split()):
        errors.append("reviewer attestation differs from the required statement")

    reconfirmation = payload.get("reviewer_metadata_reconfirmation", {})
    if reconfirmation.get("reconfirmed") is not True:
        errors.append("reviewer qualification metadata has not been reconfirmed")
    if reconfirmation.get("status") != "RECONFIRMED_BY_NAMED_REVIEWER":
        errors.append("reviewer metadata reconfirmation status is invalid")
    if not str(reconfirmation.get("notes", "")).strip():
        errors.append("reviewer metadata reconfirmation note is blank")

    expected_rows = template.get("questions", [])
    actual_rows = payload.get("questions", [])
    if len(actual_rows) != 65:
        errors.append(f"completed signoff must contain 65 question rows, found {len(actual_rows)}")
    for expected, actual in zip(expected_rows, actual_rows):
        for field in ("position", "question_id", "revision", "type", "marks"):
            if actual.get(field) != expected.get(field):
                errors.append(f"Q{expected.get('position')}: {field} differs from the issued template")
        decision = actual.get("decision")
        if decision not in {"PASS", "REVISE", "REJECT"}:
            errors.append(f"Q{expected.get('position')}: invalid decision {decision!r}")
        checks = (
            actual.get("content_rendering"),
            actual.get("answer_solution_alignment"),
            actual.get("visual_layout"),
        )
        if any(value not in {"PASS", "FAIL"} for value in checks):
            errors.append(f"Q{expected.get('position')}: invalid prerequisite check value")
        if decision == "PASS" and checks != ("PASS", "PASS", "PASS"):
            errors.append(f"Q{expected.get('position')}: PASS requires all prerequisite checks")
        if decision in {"REVISE", "REJECT"} and not str(actual.get("notes", "")).strip():
            errors.append(f"Q{expected.get('position')}: {decision} requires notes")

    all_pass = len(actual_rows) == 65 and all(row.get("decision") == "PASS" for row in actual_rows)
    expected_status = (
        "COMPLETE_PAPER_QA_APPROVED"
        if all_pass
        else "COMPLETE_PAPER_QA_RETURNED_FOR_REVISION"
    )
    expected_decision = "APPROVE_REVIEWED_RESULTS" if all_pass else "RETURN_FOR_REVISION"
    if payload.get("status") != expected_status:
        errors.append("completed signoff status does not match its question decisions")
    if payload.get("final_decision") != expected_decision:
        errors.append("completed signoff final decision does not match its question decisions")
    return errors, all_pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    try:
        validate_manifest_and_handoff()
        template = load_json(HUMAN_QA)
    except (KeyError, TypeError, ValueError) as error:
        print("GATE EE SET 01 HUMAN-QA SIGNOFF: BLOCKED")
        print("-", error)
        return 1

    if not COMPLETED_SIGNOFF.is_file():
        print("GATE EE SET 01 HUMAN-QA SIGNOFF: PENDING")
        print("Completed whole-paper signoff has not been imported.")
        print("Release and sale gates: BLOCKED")
        return 1 if args.require_complete else 0

    payload = load_json(COMPLETED_SIGNOFF)
    errors, all_pass = validate_completed_signoff(payload, template)
    if errors:
        print("GATE EE SET 01 HUMAN-QA SIGNOFF: BLOCKED")
        for error in errors:
            print("-", error)
        return 1
    if all_pass:
        print("GATE EE SET 01 HUMAN-QA SIGNOFF: PASSED")
        print("65/65 complete-paper decisions: PASS")
        print("This human-QA record alone does not authorize release or sale; validate later gates separately.")
        return 0
    print("GATE EE SET 01 HUMAN-QA SIGNOFF: VALID RETURN FOR REVISION")
    print("Release and sale gates: BLOCKED")
    return 1 if args.require_complete else 0


if __name__ == "__main__":
    raise SystemExit(main())
