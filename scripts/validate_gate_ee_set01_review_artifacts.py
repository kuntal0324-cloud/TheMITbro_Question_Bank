#!/usr/bin/env python3
"""Validate Set 01 review PDFs, their checksums and the blank QA-form contract."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

from gate_ee_set01 import (
    HANDOFF,
    HUMAN_QA,
    HUMAN_QA_PDF,
    MANIFEST,
    QUESTION_PDF,
    RENDER_EVIDENCE,
    SOLUTION_PDF,
    content_sha256,
    load_json,
    relative,
    sha256,
    validate_manifest_and_handoff,
)
from render_gate_ee_set01_review_artifacts import build_human_qa_template


RAW_SOURCE_MARKUP = re.compile(r"\\(?:frac|dfrac|tfrac|mathrm|mathbf|begin|end|sqrt|operatorname)\b|\$")


def extracted_text(path: Path) -> str:
    try:
        run = subprocess.run(["pdftotext", "-layout", str(path), "-"], text=True, capture_output=True)
    except FileNotFoundError as error:
        raise ValueError("pdftotext is required; install poppler-utils") from error
    if run.returncode:
        raise ValueError(f"pdftotext failed for {path.name}: {run.stderr.strip()}")
    return run.stdout


def font_names(reader: PdfReader) -> set[str]:
    names: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources", {})
        for reference in (resources.get("/Font", {}) if resources else {}).values():
            names.add(str(reference.get_object().get("/BaseFont", "")))
    return names


def expected_qa_fields() -> set[str]:
    names = {
        "reviewer_name", "reviewer_qualification", "review_date", "reviewer_identifier",
        "reviewer_attestation", "batch001_qualification_reconfirmed",
        "batch001_qualification_notes", "final_approve_reviewed_results",
        "reviewer_signature", "final_comments",
    }
    for position in range(1, 66):
        prefix = f"q{position:03d}"
        names.update({
            f"{prefix}_content_pass", f"{prefix}_answer_solution_pass",
            f"{prefix}_visual_pass", f"{prefix}_decision_pass",
            f"{prefix}_decision_revise", f"{prefix}_decision_reject",
            f"{prefix}_notes",
        })
    return names


def field_is_blank(field: dict) -> bool:
    value = field.get("/V")
    return value in (None, "", "/Off")


def validate_pdf_structure(
    path: Path, expected_pages: range, *, require_math: bool
) -> tuple[PdfReader | None, str, list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return None, "", [f"missing {relative(path)}"]
    reader = PdfReader(path)
    if len(reader.pages) not in expected_pages:
        errors.append(f"{path.name}: unexpected page count {len(reader.pages)}")
    metadata = reader.metadata or {}
    if require_math:
        if "xdvipdfmx" not in str(metadata.get("/Producer", "")):
            errors.append(f"{path.name}: not produced by the XeLaTeX/xdvipdfmx pipeline")
        if not any("LatinModernMath" in name for name in font_names(reader)):
            errors.append(f"{path.name}: Latin Modern Math is not embedded")
    text = extracted_text(path)
    if RAW_SOURCE_MARKUP.search(text):
        errors.append(f"{path.name}: learner-facing text exposes raw source math markup")
    return reader, text, errors


def main() -> int:
    errors: list[str] = []
    try:
        manifest, handoff = validate_manifest_and_handoff()
    except (KeyError, TypeError, ValueError) as error:
        print("GATE EE SET 01 REVIEW ARTIFACT VALIDATION: FAILED")
        print("-", error)
        return 1

    question_reader, question_text, question_errors = validate_pdf_structure(
        QUESTION_PDF, range(14, 31), require_math=True
    )
    solution_reader, solution_text, solution_errors = validate_pdf_structure(
        SOLUTION_PDF, range(18, 46), require_math=True
    )
    qa_reader, qa_text, qa_errors = validate_pdf_structure(
        HUMAN_QA_PDF, range(15, 16), require_math=False
    )
    errors.extend(question_errors + solution_errors + qa_errors)

    manifest_hash = manifest["manifest_content_sha256"]
    for label, text in (
        ("question PDF", question_text), ("solution PDF", solution_text), ("human-QA PDF", qa_text),
    ):
        if manifest_hash not in re.sub(r"\s+", "", text):
            errors.append(f"{label}: manifest content hash is not visibly recoverable")
    for row in manifest["questions"]:
        question_id = row["question_id"]
        if question_text.count(question_id) != 1:
            errors.append(f"question PDF: {question_id} must appear exactly once")
        if solution_text.count(question_id) != 1:
            errors.append(f"solution PDF: {question_id} must appear exactly once")
        if qa_text.count(question_id) != 1:
            errors.append(f"human-QA PDF: {question_id} must appear exactly once")

    if "Verified answer:" in question_text or "Final answer:" in question_text or "Detailed solutions" in question_text:
        errors.append("question PDF exposes answer/solution content")
    for required in (
        "65 / 100 / 180 minutes", "Section A", "Section B", "Section C",
        "NOT FOR SALE OR RELEASE", "End of question paper",
    ):
        if required not in question_text:
            errors.append(f"question PDF: missing visible contract text: {required}")
    for required in ("Compact answer key", "Detailed solutions", "CONFIDENTIAL REVIEW COPY"):
        if required not in solution_text:
            errors.append(f"solution PDF: missing visible contract text: {required}")

    fields = qa_reader.get_fields() if qa_reader is not None else {}
    fields = fields or {}
    expected_fields = expected_qa_fields()
    if set(fields) != expected_fields:
        errors.append(
            "human-QA PDF field contract mismatch; "
            f"missing={sorted(expected_fields - set(fields))}, unexpected={sorted(set(fields) - expected_fields)}"
        )
    widgets = 0
    missing_appearances = 0
    for page in qa_reader.pages if qa_reader is not None else []:
        for reference in page.get("/Annots", []):
            widget = reference.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            widgets += 1
            if not widget.get("/AP", {}).get("/N"):
                missing_appearances += 1
    if widgets != 465:
        errors.append(f"human-QA PDF: expected 465 widgets, found {widgets}")
    if missing_appearances:
        errors.append(f"human-QA PDF: {missing_appearances} widgets lack normal appearance streams")
    nonblank = sorted(name for name, field in fields.items() if not field_is_blank(field))
    if nonblank:
        errors.append(f"human-QA PDF template contains pre-filled decisions/values: {nonblank}")
    qa_normalized = " ".join(qa_text.split())
    for required in (
        "RELEASE AND SALE BLOCKED", "Reviewer-metadata inconsistency requiring resolution",
        "Masters in Electrical Engineering", "Diploma in Electrical Engineering",
        "APPROVE REVIEWED RESULTS",
    ):
        if required not in qa_normalized:
            errors.append(f"human-QA PDF: missing visible gate text: {required}")

    if not HUMAN_QA.is_file():
        errors.append(f"missing {relative(HUMAN_QA)}")
        template = {}
    else:
        template = load_json(HUMAN_QA)
        expected_template = build_human_qa_template(manifest, handoff)
        if template != expected_template:
            errors.append("human-QA JSON template is stale or differs from the rendered artifact bindings")
        if template.get("release_authorized") is not False or template.get("sale_authorized") is not False:
            errors.append("human-QA JSON template improperly authorizes release or sale")

    if not RENDER_EVIDENCE.is_file():
        errors.append(f"missing {relative(RENDER_EVIDENCE)}")
    else:
        evidence = load_json(RENDER_EVIDENCE)
        if evidence.get("evidence_content_sha256") != content_sha256(evidence, "evidence_content_sha256"):
            errors.append("render evidence self-hash is invalid")
        if evidence.get("manifest", {}).get("file_sha256") != sha256(MANIFEST):
            errors.append("render evidence manifest file hash mismatch")
        if evidence.get("formatter_handoff", {}).get("file_sha256") != sha256(HANDOFF):
            errors.append("render evidence Formatter handoff file hash mismatch")
        expected_artifacts = {
            "question_pdf": QUESTION_PDF,
            "solution_pdf": SOLUTION_PDF,
            "human_qa_pdf": HUMAN_QA_PDF,
            "human_qa_json": HUMAN_QA,
        }
        for label, path in expected_artifacts.items():
            row = evidence.get("artifacts", {}).get(label, {})
            if row.get("path") != relative(path) or row.get("sha256") != sha256(path):
                errors.append(f"render evidence {label} path/hash mismatch")
        gate = evidence.get("gate_state", {})
        if gate.get("complete_paper_human_qa") != "PENDING":
            errors.append("render evidence must keep complete-paper human QA pending")
        if gate.get("release_authorized") is not False or gate.get("sale_authorized") is not False:
            errors.append("render evidence improperly authorizes release or sale")

    if errors:
        print("GATE EE SET 01 REVIEW ARTIFACT VALIDATION: FAILED")
        for error in errors:
            print("-", error)
        return 1
    print("GATE EE SET 01 REVIEW ARTIFACT VALIDATION: PASSED")
    print(f"Question PDF: {len(question_reader.pages)} pages | {sha256(QUESTION_PDF)}")
    print(f"Solution PDF: {len(solution_reader.pages)} pages | {sha256(SOLUTION_PDF)}")
    print(f"Human-QA PDF: {len(qa_reader.pages)} pages | 465/465 fields and widgets | missing appearances: 0")
    print("All 65 IDs, manifest binding, fonts, visible gate text and blank-form state: PASSED")
    print("Release and sale gates: BLOCKED pending named-human complete-paper QA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
