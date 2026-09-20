#!/usr/bin/env python3
"""Import a completed RC1 exact-artifact authorization without enabling sale."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from pypdf import PdfReader

from gate_ee_set01 import (
    RELEASE_AUTHORIZATION_COMPLETED,
    RELEASE_AUTHORIZATION_COMPLETED_PDF,
    RELEASE_CANDIDATE,
    ROOT,
    content_sha256,
    load_json,
    pretty_bytes,
    relative,
    sha256,
)
from render_gate_ee_set01_release_candidate import REQUIRED_RELEASE_ATTESTATION
from validate_gate_ee_set01_release_candidate import EXPECTED_AUTHORIZATION_FIELDS


CHECK_FIELDS = (
    "question_hash_match", "solution_hash_match", "learner_pack_hash_match",
    "clean_learner_copy", "visual_layout_pass", "question_solution_alignment",
)


def normalized(value: object) -> str:
    return " ".join(str(value or "").split())


def value(fields: dict, name: str) -> object:
    return fields.get(name, {}).get("/V")


def checked(fields: dict, name: str) -> bool:
    return str(value(fields, name) or "") not in ("", "/Off", "Off", "False", "0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path, nargs="?", default=RELEASE_AUTHORIZATION_COMPLETED_PDF)
    parser.add_argument("--output", type=Path, default=RELEASE_AUTHORIZATION_COMPLETED)
    args = parser.parse_args()
    if not args.pdf.is_file():
        print("GATE EE SET 01 RELEASE AUTHORIZATION IMPORT: BLOCKED")
        print("- completed PDF not found:", args.pdf)
        return 1
    candidate = load_json(RELEASE_CANDIDATE)
    reader = PdfReader(args.pdf)
    fields = reader.get_fields() or {}
    errors: list[str] = []
    if set(fields) != EXPECTED_AUTHORIZATION_FIELDS:
        errors.append("completed PDF field contract differs from the issued authorization form")

    reviewer_name = normalized(value(fields, "reviewer_name"))
    reviewer_qualification = normalized(value(fields, "reviewer_qualification"))
    review_date = normalized(value(fields, "review_date"))
    reviewer_identifier = normalized(value(fields, "reviewer_identifier"))
    attestation = normalized(value(fields, "release_attestation"))
    signature = normalized(value(fields, "release_signature"))
    comments = normalized(value(fields, "final_comments"))
    if not reviewer_name:
        errors.append("reviewer name is blank")
    if not reviewer_qualification:
        errors.append("reviewer role/qualification is blank")
    try:
        date.fromisoformat(review_date)
    except ValueError:
        errors.append("review date must be a valid YYYY-MM-DD date")
    if attestation != normalized(REQUIRED_RELEASE_ATTESTATION):
        errors.append("required release attestation was not typed exactly")
    if not signature:
        errors.append("reviewer typed signature is blank")
    for field in CHECK_FIELDS:
        if not checked(fields, field):
            errors.append(f"required exact-artifact check is not selected: {field}")
    if not checked(fields, "final_authorize_release"):
        errors.append("final release authorization is not selected")
    if errors:
        print("GATE EE SET 01 RELEASE AUTHORIZATION IMPORT: BLOCKED")
        for error in errors:
            print("-", error)
        return 1

    payload = {
        "authorization_contract": "GATE_EE_SET01_EXACT_ARTIFACT_RELEASE_AUTHORIZATION_V1",
        "candidate_id": candidate["candidate_id"],
        "paper_id": candidate["paper_id"],
        "candidate_content_sha256": candidate["candidate_content_sha256"],
        "authorized_artifacts": {
            key: {
                "path": candidate["artifacts"][key]["path"],
                "sha256": candidate["artifacts"][key]["sha256"],
            }
            for key in ("question_pdf", "solution_pdf", "learner_pack_pdf")
        },
        "completed_pdf": {
            "path": relative(args.pdf) if args.pdf.is_relative_to(ROOT) else str(args.pdf),
            "sha256": sha256(args.pdf),
        },
        "reviewer": {
            "name": reviewer_name,
            "role_or_qualification": reviewer_qualification,
            "review_date": review_date,
            "reviewer_identifier": reviewer_identifier,
            "attestation": attestation,
            "signature": signature,
        },
        "checks": {field: "PASS" for field in CHECK_FIELDS},
        "final_comments": comments,
        "status": "EXACT_ARTIFACT_RELEASE_AUTHORIZED",
        "release_authorized": True,
        "price_set": False,
        "storefront_activated": False,
        "sale_authorized": False,
    }
    payload["authorization_content_sha256"] = content_sha256(payload, "authorization_content_sha256")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pretty_bytes(payload))
    print("GATE EE SET 01 RELEASE AUTHORIZATION IMPORT: PASSED")
    print("Release candidate authorization: RECORDED")
    print("Pricing, sale and storefront activation remain BLOCKED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

