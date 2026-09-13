#!/usr/bin/env python3
"""Import a completed Batch 004/005 AcroForm into canonical human-QA JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

from gate_ee_recovery_batches import BATCHES, get_batch, load_questions
from import_gate_ee_batch_003_human_qa_pdf import (
    FORM_TO_JSON,
    checkbox_pair,
    decision_checkboxes,
    field_values,
    is_checked,
    lookup,
    sha256,
)


def build_payload(batch_id: str, pdf_path: Path) -> dict[str, Any]:
    batch = get_batch(batch_id)
    values = field_values(pdf_path)
    source_rows = load_questions(batch)
    template = json.loads(batch.human_qa.read_text(encoding="utf-8"))
    errors: list[str] = []

    if template.get("source_sha256") != sha256(batch.source):
        errors.append(f"repository template is not locked to the current {batch.batch_id} source")
    if template.get("formatter_report_sha256") != sha256(batch.formatter_evidence):
        errors.append(f"repository template is not locked to the current {batch.batch_id} Formatter report")

    reviewer = {
        "name": lookup(values, "reviewer_name"),
        "role_or_qualification": lookup(values, "reviewer_qualification"),
        "review_date": lookup(values, "review_date"),
        "attestation": lookup(values, "reviewer_attestation"),
    }
    identifier = lookup(values, "reviewer_identifier")
    if identifier:
        reviewer["identifier"] = identifier
    for key in ("name", "role_or_qualification", "review_date", "attestation"):
        if not reviewer[key]:
            errors.append(f"missing reviewer field: {key}")
    if reviewer["review_date"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewer["review_date"]):
        errors.append("review date must use YYYY-MM-DD")
    if reviewer["attestation"] != template.get("required_attestation"):
        errors.append("reviewer attestation must exactly match the required text printed on page 1")
    if not is_checked(lookup(values, "final_approve_reviewed_results")):
        errors.append("final reviewed-results approval checkbox is not selected")
    signature = lookup(values, "reviewer_signature")
    if not signature:
        errors.append("reviewer typed signature is missing")

    questions: list[dict[str, Any]] = []
    for index, source in enumerate(source_rows, 1):
        prefix = f"q{index:03d}"
        row: dict[str, Any] = {
            "question_id": source["id"],
            "revision": source["revision"],
        }
        checks: list[str] = []
        for form_suffix, json_key in FORM_TO_JSON.items():
            result = checkbox_pair(
                values,
                f"{prefix}_{form_suffix}",
                f"{source['id']} {json_key}",
                errors,
            )
            row[json_key] = result
            checks.append(result)
        decision = decision_checkboxes(values, f"{prefix}_decision", source["id"], errors)
        notes = lookup(values, f"{prefix}_notes")
        row["decision"] = decision
        row["notes"] = notes
        if decision == "PASS" and any(result != "PASS" for result in checks):
            errors.append(f"{source['id']}: PASS requires all five checks to be PASS")
        elif decision in {"REVISE", "REJECT"} and not notes:
            errors.append(f"{source['id']}: {decision} requires a note")
        if "FAIL" in checks and not notes:
            errors.append(f"{source['id']}: a failed check requires a note")
        questions.append(row)

    if errors:
        rendered = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"Completed review form is not valid:\n{rendered}")

    template["reviewer"] = reviewer
    template["final_decision"] = "APPROVE_REVIEWED_RESULTS"
    template["questions"] = questions
    template["pdf_evidence"] = {
        "filename": pdf_path.name,
        "sha256": sha256(pdf_path),
        "format": "XELATEX_ACROFORM_V2",
        "reviewer_signature": signature,
        "final_comments": lookup(values, "final_comments"),
    }
    return template


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a completed Batch 004/005 fillable PDF into canonical human-QA JSON."
    )
    parser.add_argument("--batch", required=True, choices=sorted(BATCHES))
    parser.add_argument("completed_pdf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    batch = get_batch(args.batch)
    pdf_path = args.completed_pdf.resolve()
    output = args.output or batch.human_qa
    if not pdf_path.is_file():
        raise SystemExit(f"Completed PDF not found: {pdf_path}")
    try:
        payload = build_payload(batch.batch_id, pdf_path)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    counts = {decision: 0 for decision in ("PASS", "REVISE", "REJECT")}
    for row in payload["questions"]:
        counts[row["decision"]] += 1
    print(f"Created {output}")
    print(f"PASS: {counts['PASS']} | REVISE: {counts['REVISE']} | REJECT: {counts['REJECT']}")
    print(f"Next: python scripts/validate_gate_ee_recovery_human_signoff.py --batch {batch.batch_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
