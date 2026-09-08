#!/usr/bin/env python3
"""Import a completed Batch 002 AcroForm into the canonical human-QA JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
SOURCE = BASE / "source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
TEMPLATE = BASE / "review_manifests/BATCH_002_HUMAN_FINAL_QA.json"
DEFAULT_OUTPUT = TEMPLATE

FORM_TO_JSON = {
    "technical": "technical_correctness",
    "answer": "answer_correctness",
    "solution": "solution_correctness",
    "clarity": "clarity_ambiguity",
    "originality": "originality_conflict_check",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    return text[1:] if text.startswith("/") else text


def field_values(path: Path) -> dict[str, str]:
    reader = PdfReader(path)
    fields = reader.get_fields() or {}
    return {name: normalize(field.get("/V")).strip() for name, field in fields.items()}


def build_payload(pdf_path: Path) -> dict[str, Any]:
    values = field_values(pdf_path)
    source_rows = [
        json.loads(line)
        for line in SOURCE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    errors: list[str] = []

    if template.get("source_sha256") != sha256(SOURCE):
        errors.append("repository template is not locked to the current Batch 002 source")

    reviewer = {
        "name": values.get("reviewer_name", ""),
        "role_or_qualification": values.get("reviewer_qualification", ""),
        "review_date": values.get("review_date", ""),
        "attestation": values.get("reviewer_attestation", ""),
    }
    identifier = values.get("reviewer_identifier", "")
    if identifier:
        reviewer["identifier"] = identifier
    for key in ("name", "role_or_qualification", "review_date", "attestation"):
        if not reviewer[key]:
            errors.append(f"missing reviewer field: {key}")
    if reviewer["review_date"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewer["review_date"]):
        errors.append("review date must use YYYY-MM-DD")
    if reviewer["attestation"] != template.get("required_attestation"):
        errors.append("reviewer attestation must exactly match the required text printed on page 1")

    questions: list[dict[str, Any]] = []
    for index, source in enumerate(source_rows, 1):
        prefix = f"q{index:03d}"
        row: dict[str, Any] = {
            "question_id": source["id"],
            "revision": source["revision"],
        }
        checks: list[str] = []
        for form_suffix, json_key in FORM_TO_JSON.items():
            result = values.get(f"{prefix}_{form_suffix}", "")
            row[json_key] = result
            checks.append(result)
            if result not in {"PASS", "FAIL"}:
                errors.append(f"{source['id']}: select PASS or FAIL for {json_key}")
        decision = values.get(f"{prefix}_decision", "")
        notes = values.get(f"{prefix}_notes", "")
        row["decision"] = decision
        row["notes"] = notes
        if decision not in {"PASS", "REVISE", "REJECT"}:
            errors.append(f"{source['id']}: select PASS, REVISE or REJECT")
        elif decision == "PASS" and any(result != "PASS" for result in checks):
            errors.append(f"{source['id']}: PASS requires all five checks to be PASS")
        elif decision in {"REVISE", "REJECT"} and not notes:
            errors.append(f"{source['id']}: {decision} requires a note")
        if "FAIL" in checks and decision == "PASS":
            errors.append(f"{source['id']}: a failed check cannot have a PASS decision")
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
        "format": "ACROFORM_V1",
    }
    return template


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a completed Batch 002 fillable PDF into canonical human-QA JSON."
    )
    parser.add_argument("completed_pdf", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    pdf_path = args.completed_pdf.resolve()
    if not pdf_path.is_file():
        raise SystemExit(f"Completed PDF not found: {pdf_path}")
    try:
        payload = build_payload(pdf_path)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    counts = {decision: 0 for decision in ("PASS", "REVISE", "REJECT")}
    for row in payload["questions"]:
        counts[row["decision"]] += 1
    print(f"Created {args.output}")
    print(f"PASS: {counts['PASS']} | REVISE: {counts['REVISE']} | REJECT: {counts['REJECT']}")
    print("Next: python scripts/validate_gate_ee_batch_002_human_signoff.py")


if __name__ == "__main__":
    main()
