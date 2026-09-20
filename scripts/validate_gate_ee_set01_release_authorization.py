#!/usr/bin/env python3
"""Validate a completed RC1 release authorization when present."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from gate_ee_set01 import (
    RELEASE_AUTHORIZATION_COMPLETED,
    RELEASE_CANDIDATE,
    ROOT,
    content_sha256,
    load_json,
    sha256,
)
from import_gate_ee_set01_release_authorization_pdf import CHECK_FIELDS
from render_gate_ee_set01_release_candidate import REQUIRED_RELEASE_ATTESTATION


def resolve_path(recorded: object) -> Path | None:
    if not isinstance(recorded, str) or not recorded.strip():
        return None
    path = Path(recorded)
    if path.is_absolute():
        return path
    candidate = (ROOT / path).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    if not RELEASE_AUTHORIZATION_COMPLETED.is_file():
        print("GATE EE SET 01 RELEASE AUTHORIZATION: PENDING")
        print("Exact-artifact RC1 authorization has not been imported.")
        print("Release, sale and storefront activation: BLOCKED")
        return 1 if args.require_complete else 0

    candidate = load_json(RELEASE_CANDIDATE)
    payload = load_json(RELEASE_AUTHORIZATION_COMPLETED)
    errors: list[str] = []
    expected = (
        payload.get("authorization_contract"), payload.get("candidate_id"),
        payload.get("paper_id"), payload.get("candidate_content_sha256"),
    )
    if expected != (
        "GATE_EE_SET01_EXACT_ARTIFACT_RELEASE_AUTHORIZATION_V1",
        candidate.get("candidate_id"), candidate.get("paper_id"),
        candidate.get("candidate_content_sha256"),
    ):
        errors.append("authorization identity/candidate binding mismatch")
    if payload.get("authorization_content_sha256") != content_sha256(payload, "authorization_content_sha256"):
        errors.append("authorization self-hash is invalid")
    for key in ("question_pdf", "solution_pdf", "learner_pack_pdf"):
        if payload.get("authorized_artifacts", {}).get(key) != {
            "path": candidate["artifacts"][key]["path"],
            "sha256": candidate["artifacts"][key]["sha256"],
        }:
            errors.append(f"authorization {key} binding mismatch")
    completed_pdf = payload.get("completed_pdf", {})
    completed_path = resolve_path(completed_pdf.get("path"))
    if completed_path is None or not completed_path.is_file():
        errors.append("completed authorization PDF is missing or non-portable")
    elif completed_pdf.get("sha256") != sha256(completed_path):
        errors.append("completed authorization PDF checksum mismatch")
    reviewer = payload.get("reviewer", {})
    for field in ("name", "role_or_qualification", "review_date", "signature"):
        if not str(reviewer.get(field, "")).strip():
            errors.append(f"reviewer {field} is blank")
    try:
        date.fromisoformat(str(reviewer.get("review_date", "")))
    except ValueError:
        errors.append("review date must use YYYY-MM-DD")
    if " ".join(str(reviewer.get("attestation", "")).split()) != " ".join(REQUIRED_RELEASE_ATTESTATION.split()):
        errors.append("reviewer attestation differs from the required statement")
    if payload.get("checks") != {field: "PASS" for field in CHECK_FIELDS}:
        errors.append("one or more exact-artifact checks are not PASS")
    if payload.get("status") != "EXACT_ARTIFACT_RELEASE_AUTHORIZED" or payload.get("release_authorized") is not True:
        errors.append("release authorization status is invalid")
    for field in ("price_set", "storefront_activated", "sale_authorized"):
        if payload.get(field) is not False:
            errors.append(f"release authorization improperly sets {field}")

    if errors:
        print("GATE EE SET 01 RELEASE AUTHORIZATION: BLOCKED")
        for error in errors:
            print("-", error)
        return 1
    print("GATE EE SET 01 RELEASE AUTHORIZATION: PASSED")
    print("Exact RC1 learner artifacts are authorized for release.")
    print("Pricing, sale and storefront activation remain BLOCKED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
