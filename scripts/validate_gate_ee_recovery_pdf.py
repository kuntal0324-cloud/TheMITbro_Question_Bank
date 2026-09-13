#!/usr/bin/env python3
"""Validate Batch 004/005 fillable PDF structure, evidence and rendering metadata."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess

from pypdf import PdfReader

from gate_ee_recovery_batches import BATCHES, get_batch, load_questions


def font_names(reader: PdfReader) -> set[str]:
    names: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources", {})
        fonts = resources.get("/Font", {}) if resources else {}
        for reference in fonts.values():
            names.add(str(reference.get_object().get("/BaseFont", "")))
    return names


def expected_field_names(count: int) -> set[str]:
    names = {
        "reviewer_name", "reviewer_qualification", "review_date",
        "reviewer_identifier", "reviewer_attestation",
        "final_approve_reviewed_results", "reviewer_signature", "final_comments",
    }
    for index in range(1, count + 1):
        prefix = f"q{index:03d}"
        for check in ("technical", "answer", "solution", "clarity", "originality"):
            names.add(f"{prefix}_{check}_pass")
            names.add(f"{prefix}_{check}_fail")
        for decision in ("pass", "revise", "reject"):
            names.add(f"{prefix}_decision_{decision}")
        names.add(f"{prefix}_notes")
    # XeLaTeX/hyperref removes underscores from AcroForm field names.
    return {name.replace("_", "") for name in names}


def validate(batch_id: str) -> list[str]:
    batch = get_batch(batch_id)
    questions = load_questions(batch)
    errors: list[str] = []
    if not batch.pdf.is_file():
        return [f"missing review PDF: {batch.pdf}"]
    reader = PdfReader(batch.pdf)
    fields = reader.get_fields() or {}
    widgets = 0
    missing_appearances = 0
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            widget = reference.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            widgets += 1
            normal = widget.get("/AP", {}).get("/N")
            if not normal:
                missing_appearances += 1

    expected_fields = expected_field_names(len(questions))
    if len(reader.pages) != len(questions) + 2:
        errors.append(f"expected {len(questions) + 2} pages, found {len(reader.pages)}")
    if set(fields) != expected_fields:
        errors.append(
            f"field contract mismatch; missing={sorted(expected_fields - set(fields))}, "
            f"unexpected={sorted(set(fields) - expected_fields)}"
        )
    expected_widgets = 14 * len(questions) + 8
    if widgets != expected_widgets:
        errors.append(f"expected {expected_widgets} widgets, found {widgets}")
    if missing_appearances:
        errors.append(f"{missing_appearances} widgets lack normal appearance streams")
    if not any("LatinModernMath" in name for name in font_names(reader)):
        errors.append("Latin Modern Math is not embedded")
    metadata = reader.metadata or {}
    if "xdvipdfmx" not in str(metadata.get("/Producer", "")):
        errors.append("PDF was not produced by the XeLaTeX pipeline")

    # Poppler's layout extraction is used for visible-text assertions.  It is
    # substantially more faithful than pypdf for long hyphenated identifiers
    # rendered through XeLaTeX; pypdf remains authoritative for form objects.
    extracted_run = subprocess.run(
        ["pdftotext", "-layout", str(batch.pdf), "-"],
        text=True,
        capture_output=True,
    )
    if extracted_run.returncode:
        errors.append(f"pdftotext failed: {extracted_run.stderr.strip()}")
        extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        extracted = extracted_run.stdout
    source_sha = hashlib.sha256(batch.source.read_bytes()).hexdigest()
    formatter_sha = hashlib.sha256(batch.formatter_evidence.read_bytes()).hexdigest()
    if source_sha not in extracted:
        errors.append("PDF does not display the canonical source checksum")
    if formatter_sha not in extracted:
        errors.append("PDF does not display the Formatter evidence checksum")
    for question in questions:
        if extracted.count(question["id"]) != 1:
            errors.append(f"PDF must display {question['id']} exactly once")
        diagram = question.get("diagram")
        if diagram:
            # Typeset math can extract with arbitrary spacing.  Require the
            # stable prose portion of every declared caption instead.
            caption_prose = re.sub(r"\$[^$]*\$", "", str(diagram["caption"]))
            caption_prose = " ".join(caption_prose.split()).strip(" .:-")
            if caption_prose and caption_prose not in extracted:
                errors.append(f"{question['id']}: diagram caption is not recoverable from the PDF")
    normalized_text = " ".join(extracted.split())
    if (
        "APPROVE REVIEWED RESULTS" not in normalized_text
        or " ".join(batch.attestation.split()) not in normalized_text
    ):
        errors.append("review completion controls or attestation text are missing")
    for label, pattern in {
        "ASCII sqrt": r"\bsqrt\s*\(",
        "ASCII subscript": r"\b[A-Za-z]+_[A-Za-z0-9]+\b",
        "ASCII power": r"\b[A-Za-z0-9)]+\^[({-]?[0-9]",
        "spelled electrical unit": r"\b(?:microfarads?|kilo-ohms?|ohms?)\b",
    }.items():
        if re.search(pattern, extracted, re.I):
            errors.append(f"learner-facing PDF exposes {label}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="append", choices=sorted(BATCHES))
    args = parser.parse_args()
    errors: list[str] = []
    selected = args.batch or sorted(BATCHES)
    for batch_id in selected:
        batch_errors = validate(batch_id)
        if batch_errors:
            errors.extend(f"{batch_id}: {error}" for error in batch_errors)
            continue
        batch = get_batch(batch_id)
        count = batch.expected_count
        print(f"{batch_id} PDF VALIDATION: PASSED")
        print(f"Pages: {count + 2} | fields/widgets: {14 * count + 8}/{14 * count + 8} | missing appearances: 0")
    if errors:
        print("GATE EE RECOVERY PDF VALIDATION: FAILED")
        for error in errors:
            print("-", error)
        return 1
    print("Engine: XeLaTeX/xdvipdfmx | math font: Latin Modern Math")
    print("Question IDs, diagrams and evidence checksums: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
