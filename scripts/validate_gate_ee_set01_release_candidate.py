#!/usr/bin/env python3
"""Validate the exact Set 01 learner release candidate while keeping release/sale blocked."""

from __future__ import annotations

import re

from pypdf import PdfReader

from gate_ee_set01 import (
    COMPLETED_SIGNOFF,
    FORMATTER_RELEASE_EVIDENCE,
    RELEASE_AUTHORIZATION_PDF,
    RELEASE_CANDIDATE,
    RELEASE_LEARNER_PACK_PDF,
    RELEASE_QUESTION_PDF,
    RELEASE_SOLUTION_PDF,
    content_sha256,
    load_json,
    relative,
    sha256,
)
from render_gate_ee_set01_release_candidate import REQUIRED_RELEASE_ATTESTATION, validate_upstream
from validate_gate_ee_set01_review_artifacts import (
    RAW_SOURCE_MARKUP,
    extracted_text,
    field_is_blank,
    font_names,
)


EXPECTED_AUTHORIZATION_FIELDS = {
    "reviewer_name", "reviewer_qualification", "review_date", "reviewer_identifier",
    "question_hash_match", "solution_hash_match", "learner_pack_hash_match",
    "clean_learner_copy", "visual_layout_pass", "question_solution_alignment",
    "release_attestation", "release_signature", "final_authorize_release", "final_comments",
}
FORBIDDEN_LEARNER_TEXT = (
    "Human-QA Review Copy",
    "Review copy",
    "NOT FOR SALE OR RELEASE",
    "CONFIDENTIAL REVIEW COPY",
    "Audit ID:",
    "TMB-GATE-EE-",
    "Release remains blocked",
)


def normalized_page_text(reader: PdfReader) -> list[str]:
    return [" ".join((page.extract_text() or "").split()) for page in reader.pages]


def main() -> int:
    errors: list[str] = []
    try:
        validate_upstream()
    except (KeyError, TypeError, ValueError) as error:
        print("GATE EE SET 01 RELEASE CANDIDATE VALIDATION: FAILED")
        print("-", error)
        return 1

    required_paths = (
        RELEASE_CANDIDATE, RELEASE_QUESTION_PDF, RELEASE_SOLUTION_PDF,
        RELEASE_LEARNER_PACK_PDF, RELEASE_AUTHORIZATION_PDF,
        COMPLETED_SIGNOFF, FORMATTER_RELEASE_EVIDENCE,
    )
    for path in required_paths:
        if not path.is_file():
            errors.append(f"missing {relative(path)}")
    if errors:
        print("GATE EE SET 01 RELEASE CANDIDATE VALIDATION: FAILED")
        for error in errors:
            print("-", error)
        return 1

    candidate = load_json(RELEASE_CANDIDATE)
    if candidate.get("candidate_content_sha256") != content_sha256(candidate, "candidate_content_sha256"):
        errors.append("release candidate self-hash is invalid")
    expected_header = (
        candidate.get("candidate_contract"), candidate.get("candidate_id"),
        candidate.get("paper_id"), candidate.get("status"),
    )
    if expected_header != (
        "GATE_EE_SET01_LEARNER_RELEASE_CANDIDATE_V1",
        "GATE_2027_EE_SET_01_RC1",
        "GATE_2027_EE_SET_01",
        "RELEASE_CANDIDATE_AWAITING_EXACT_ARTIFACT_AUTHORIZATION",
    ):
        errors.append("release candidate identity/status contract mismatch")

    artifact_paths = {
        "question_pdf": RELEASE_QUESTION_PDF,
        "solution_pdf": RELEASE_SOLUTION_PDF,
        "learner_pack_pdf": RELEASE_LEARNER_PACK_PDF,
        "release_authorization_pdf": RELEASE_AUTHORIZATION_PDF,
    }
    readers: dict[str, PdfReader] = {}
    texts: dict[str, str] = {}
    for label, path in artifact_paths.items():
        row = candidate.get("artifacts", {}).get(label, {})
        if row.get("path") != relative(path) or row.get("sha256") != sha256(path):
            errors.append(f"{label}: candidate path/hash binding mismatch")
        if row.get("bytes") != path.stat().st_size:
            errors.append(f"{label}: candidate byte count mismatch")
        reader = PdfReader(path)
        readers[label] = reader
        texts[label] = extracted_text(path)
        if row.get("pages") != len(reader.pages):
            errors.append(f"{label}: candidate page count mismatch")

    question_reader = readers["question_pdf"]
    solution_reader = readers["solution_pdf"]
    pack_reader = readers["learner_pack_pdf"]
    if len(question_reader.pages) not in range(14, 31):
        errors.append(f"question PDF: unexpected page count {len(question_reader.pages)}")
    if len(solution_reader.pages) not in range(18, 46):
        errors.append(f"solution PDF: unexpected page count {len(solution_reader.pages)}")
    if len(pack_reader.pages) != len(question_reader.pages) + len(solution_reader.pages):
        errors.append("learner pack page count is not question pages plus solution pages")
    expected_pack_pages = normalized_page_text(question_reader) + normalized_page_text(solution_reader)
    if normalized_page_text(pack_reader) != expected_pack_pages:
        errors.append("learner pack page text does not exactly concatenate the question and solution PDFs")

    question_text = texts["question_pdf"]
    solution_text = texts["solution_pdf"]
    pack_text = texts["learner_pack_pdf"]
    for label, text in (("question PDF", question_text), ("solution PDF", solution_text), ("learner pack", pack_text)):
        if RAW_SOURCE_MARKUP.search(text):
            errors.append(f"{label}: raw source math markup is visible")
        for forbidden in FORBIDDEN_LEARNER_TEXT:
            if forbidden in text:
                errors.append(f"{label}: forbidden review/internal text is visible: {forbidden}")
        if "INDEPENDENT PRACTICE MATERIAL" not in text or "NOT AN OFFICIAL GATE PAPER" not in text:
            errors.append(f"{label}: independent-material disclaimer is missing")
        names = font_names(PdfReader(artifact_paths[{"question PDF": "question_pdf", "solution PDF": "solution_pdf", "learner pack": "learner_pack_pdf"}[label]]))
        if not any("LatinModernMath" in name for name in names):
            errors.append(f"{label}: Latin Modern Math is not embedded")

    if any(value in question_text for value in ("Compact answer key", "Detailed solutions", "Final answer:")):
        errors.append("question PDF exposes answer or solution content")
    for required in ("65 / 100 / 180 minutes", "Section A", "Section B", "Section C", "End of question paper"):
        if required not in question_text:
            errors.append(f"question PDF: missing visible learner contract text: {required}")
    for required in ("Compact answer key", "Detailed solutions", "Answer:"):
        if required not in solution_text:
            errors.append(f"solution PDF: missing visible learner contract text: {required}")
    if len(re.findall(r"\bQ(?:[1-9]|[1-5][0-9]|6[0-5])\.", question_text)) < 65:
        errors.append("question PDF does not visibly contain all 65 numbered positions")

    auth_reader = readers["release_authorization_pdf"]
    if len(auth_reader.pages) != 1:
        errors.append(f"release-authorization PDF must be one page, found {len(auth_reader.pages)}")
    fields = auth_reader.get_fields() or {}
    if set(fields) != EXPECTED_AUTHORIZATION_FIELDS:
        errors.append(
            "release-authorization field contract mismatch; "
            f"missing={sorted(EXPECTED_AUTHORIZATION_FIELDS - set(fields))}, "
            f"unexpected={sorted(set(fields) - EXPECTED_AUTHORIZATION_FIELDS)}"
        )
    nonblank = sorted(name for name, field in fields.items() if not field_is_blank(field))
    if nonblank:
        errors.append(f"release-authorization template contains pre-filled values: {nonblank}")
    widget_count = 0
    missing_appearances = 0
    for page in auth_reader.pages:
        for reference in page.get("/Annots", []):
            widget = reference.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            widget_count += 1
            if not widget.get("/AP", {}).get("/N"):
                missing_appearances += 1
    if widget_count != 14:
        errors.append(f"release-authorization PDF: expected 14 widgets, found {widget_count}")
    if missing_appearances:
        errors.append(f"release-authorization PDF: {missing_appearances} widgets lack appearance streams")
    auth_normalized = re.sub(r"\s+", "", texts["release_authorization_pdf"])
    for label in ("question_pdf", "solution_pdf", "learner_pack_pdf"):
        digest = candidate["artifacts"][label]["sha256"]
        if digest not in auth_normalized:
            errors.append(f"release-authorization PDF does not visibly bind {label}")
    if " ".join(REQUIRED_RELEASE_ATTESTATION.split()) not in " ".join(texts["release_authorization_pdf"].split()):
        errors.append("release-authorization PDF is missing the exact required attestation")

    gate = candidate.get("gate_state", {})
    if gate.get("complete_paper_human_qa") != "PASS_65_OF_65":
        errors.append("candidate does not record complete-paper human-QA PASS")
    if gate.get("formatter_release_qualification") != "PASS_65_OF_65":
        errors.append("candidate does not record aggregate Formatter PASS")
    if gate.get("exact_artifact_release_authorization") != "PENDING":
        errors.append("candidate must await exact-artifact release authorization")
    for field in ("release_authorized", "price_set", "storefront_activated", "sale_authorized"):
        if gate.get(field) is not False:
            errors.append(f"candidate improperly sets {field}")

    if errors:
        print("GATE EE SET 01 RELEASE CANDIDATE VALIDATION: FAILED")
        for error in errors:
            print("-", error)
        return 1
    print("GATE EE SET 01 RELEASE CANDIDATE VALIDATION: PASSED")
    print(f"Question/Solution/Learner-pack pages: {len(question_reader.pages)}/{len(solution_reader.pages)}/{len(pack_reader.pages)}")
    print("Learner-copy hygiene, embedded math font, exact concatenation and blank 14-field authorization form: PASSED")
    print("Immutable candidate record: PRE-AUTHORIZATION; validate the separate completed authorization for current state.")
    print("Sale and storefront activation: BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
