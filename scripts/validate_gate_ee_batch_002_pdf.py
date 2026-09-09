from __future__ import annotations

import hashlib
from pathlib import Path
import re

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
PDF = ROOT / "output/pdf/GATE_EE_BATCH002_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf"


def font_names(reader: PdfReader) -> set[str]:
    names: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources", {})
        fonts = resources.get("/Font", {}) if resources else {}
        for reference in fonts.values():
            font = reference.get_object()
            names.add(str(font.get("/BaseFont", "")))
    return names


def main() -> int:
    errors: list[str] = []
    if not PDF.is_file():
        raise SystemExit(f"missing Batch 002 review PDF: {PDF}")
    reader = PdfReader(PDF)
    fields = reader.get_fields() or {}
    widgets = 0
    missing_appearances = 0
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            widget = reference.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            widgets += 1
            if not widget.get("/AP") or not widget["/AP"].get("/N"):
                missing_appearances += 1

    if len(reader.pages) != 22: errors.append(f"expected 22 pages, found {len(reader.pages)}")
    if len(fields) != 288: errors.append(f"expected 288 form fields, found {len(fields)}")
    if widgets != 288: errors.append(f"expected 288 widgets, found {widgets}")
    if missing_appearances: errors.append(f"{missing_appearances} widgets lack normal appearance streams")

    fonts = font_names(reader)
    if not any("LatinModernMath" in name for name in fonts):
        errors.append("Latin Modern Math is not embedded")
    metadata = reader.metadata or {}
    if "xdvipdfmx" not in str(metadata.get("/Producer", "")):
        errors.append("PDF was not produced by the XeLaTeX pipeline")

    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if source_sha not in extracted:
        errors.append("PDF does not display the current canonical source checksum")
    raw_patterns = {
        "ASCII sqrt": r"\bsqrt\s*\(",
        "ASCII subscript": r"\b[A-Za-z]+_[A-Za-z0-9]+\b",
        "ASCII power": r"\b[A-Za-z0-9)]+\^[({-]?[0-9]",
        "spelled electrical unit": r"\b(?:microfarads?|kilo-ohms?|ohms?)\b",
    }
    for label, pattern in raw_patterns.items():
        if re.search(pattern, extracted, re.I):
            errors.append(f"learner-facing PDF exposes {label}")

    if errors:
        print("BATCH 002 PDF VALIDATION: FAILED")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("BATCH 002 PDF VALIDATION: PASSED")
    print("Pages: 22 | fields/widgets: 288/288 | missing appearances: 0")
    print("Engine: XeLaTeX/xdvipdfmx | math font: Latin Modern Math")
    print("Learner-facing ASCII formula fallbacks: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
