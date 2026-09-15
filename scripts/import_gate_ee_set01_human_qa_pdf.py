#!/usr/bin/env python3
"""Import a completed Set 01 human-QA PDF without authorizing commercial release."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re

from pypdf import PdfReader

from gate_ee_set01 import HUMAN_QA, ROOT, content_sha256, load_json, pretty_bytes, relative, sha256
from render_gate_ee_set01_review_artifacts import REQUIRED_ATTESTATION
from validate_gate_ee_set01_review_artifacts import expected_qa_fields


DEFAULT_COMPLETED_PDF = ROOT / "output/pdf/GATE_EE_SET_01_HUMAN_FINAL_QA_COMPLETED.pdf"
DEFAULT_OUTPUT = ROOT / "GATE_EE/corpus_v1/review_manifests/GATE_EE_SET_01_HUMAN_FINAL_QA_COMPLETED.json"


def normalized(value: object) -> str:
    return " ".join(str(value or "").split())


def value(fields: dict, name: str) -> object:
    return fields.get(name, {}).get("/V")


def checked(fields: dict, name: str) -> bool:
    return str(value(fields, name) or "") not in ("", "/Off", "Off", "False", "0")


def decision(fields: dict, prefix: str) -> tuple[str, list[str]]:
    selected = [
        label.upper()
        for label in ("pass", "revise", "reject")
        if checked(fields, f"{prefix}_decision_{label}")
    ]
    return (selected[0] if len(selected) == 1 else "INVALID", selected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path, nargs="?", default=DEFAULT_COMPLETED_PDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if not args.pdf.is_file():
        print("GATE EE SET 01 HUMAN-QA IMPORT: BLOCKED")
        print("- completed PDF not found:", args.pdf)
        return 1
    template = load_json(HUMAN_QA)
    reader = PdfReader(args.pdf)
    fields = reader.get_fields() or {}
    errors: list[str] = []
    if set(fields) != expected_qa_fields():
        errors.append("completed PDF field contract differs from the issued blank template")

    reviewer_name = normalized(value(fields, "reviewer_name"))
    reviewer_qualification = normalized(value(fields, "reviewer_qualification"))
    review_date = normalized(value(fields, "review_date"))
    reviewer_identifier = normalized(value(fields, "reviewer_identifier"))
    attestation = normalized(value(fields, "reviewer_attestation"))
    signature = normalized(value(fields, "reviewer_signature"))
    qualification_notes = normalized(value(fields, "batch001_qualification_notes"))
    final_comments = normalized(value(fields, "final_comments"))

    if not reviewer_name:
        errors.append("reviewer name is blank")
    if not reviewer_qualification:
        errors.append("reviewer role/qualification is blank")
    try:
        date.fromisoformat(review_date)
    except ValueError:
        errors.append("review date must be a valid YYYY-MM-DD date")
    if attestation != normalized(REQUIRED_ATTESTATION):
        errors.append("required attestation was not typed exactly")
    if not signature:
        errors.append("reviewer typed signature is blank")
    if not checked(fields, "batch001_qualification_reconfirmed"):
        errors.append("Batch 001 reviewer-qualification inconsistency was not reconfirmed")
    if not qualification_notes:
        errors.append("reviewer-qualification correction/confirmation note is blank")

    completed_questions = []
    for row in template["questions"]:
        position = row["position"]
        prefix = f"q{position:03d}"
        content_pass = checked(fields, f"{prefix}_content_pass")
        answer_solution_pass = checked(fields, f"{prefix}_answer_solution_pass")
        visual_pass = checked(fields, f"{prefix}_visual_pass")
        item_decision, selected = decision(fields, prefix)
        notes = normalized(value(fields, f"{prefix}_notes"))
        if item_decision == "INVALID":
            errors.append(f"Q{position}: select exactly one PASS/REVISE/REJECT decision; found {selected}")
        if item_decision == "PASS" and not (content_pass and answer_solution_pass and visual_pass):
            errors.append(f"Q{position}: PASS requires all three prerequisite checks")
        if item_decision in {"REVISE", "REJECT"} and not notes:
            errors.append(f"Q{position}: {item_decision} requires notes")
        completed_questions.append({
            **{key: row[key] for key in ("position", "question_id", "revision", "type", "marks")},
            "content_rendering": "PASS" if content_pass else "FAIL",
            "answer_solution_alignment": "PASS" if answer_solution_pass else "FAIL",
            "visual_layout": "PASS" if visual_pass else "FAIL",
            "decision": item_decision,
            "notes": notes,
        })

    all_pass = all(row["decision"] == "PASS" for row in completed_questions)
    final_checked = checked(fields, "final_approve_reviewed_results")
    if final_checked and not all_pass:
        errors.append("final approval cannot be selected while any question is not PASS")
    if all_pass and not final_checked:
        errors.append("all questions are PASS but final approval is not selected")
    if errors:
        print("GATE EE SET 01 HUMAN-QA IMPORT: BLOCKED")
        for error in errors:
            print("-", error)
        return 1

    payload = {
        **template,
        "status": "COMPLETE_PAPER_QA_APPROVED" if all_pass else "COMPLETE_PAPER_QA_RETURNED_FOR_REVISION",
        "completed_pdf": {"path": relative(args.pdf) if args.pdf.is_relative_to(ROOT) else str(args.pdf), "sha256": sha256(args.pdf)},
        "reviewer": {
            "name": reviewer_name,
            "role_or_qualification": reviewer_qualification,
            "review_date": review_date,
            "reviewer_identifier": reviewer_identifier,
            "attestation": attestation,
            "signature": signature,
        },
        "reviewer_metadata_reconfirmation": {
            **template["reviewer_metadata_reconfirmation"],
            "status": "RECONFIRMED_BY_NAMED_REVIEWER",
            "reconfirmed": True,
            "notes": qualification_notes,
        },
        "questions": completed_questions,
        "final_decision": "APPROVE_REVIEWED_RESULTS" if all_pass else "RETURN_FOR_REVISION",
        "final_comments": final_comments,
        "release_authorized": False,
        "sale_authorized": False,
    }
    payload["signoff_content_sha256"] = content_sha256(payload, "signoff_content_sha256")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pretty_bytes(payload))
    print("GATE EE SET 01 HUMAN-QA IMPORT: PASSED")
    print("Decision:", payload["final_decision"])
    print("Completed signoff:", relative(args.output) if args.output.is_relative_to(ROOT) else args.output)
    print("Release and sale gates remain BLOCKED pending certification and website integration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
