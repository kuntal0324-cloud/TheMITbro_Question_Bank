#!/usr/bin/env python3
"""Generate the interactive, mobile-readable Batch 002 human final-QA packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
INDEPENDENT_QA = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_INDEPENDENT_AI_QA.json"
OUTPUT = ROOT / "output/pdf/GATE_EE_BATCH002_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf"
REQUIRED_ATTESTATION = (
    "I independently reviewed the Batch 002 questions, answers and solutions "
    "and approve only the question IDs marked PASS below."
)

PAGE_W, PAGE_H = A4
MARGIN = 38
NAVY = colors.HexColor("#12233F")
BLUE = colors.HexColor("#2457A6")
LIGHT_BLUE = colors.HexColor("#EAF1FB")
PALE = colors.HexColor("#F5F7FA")
MID = colors.HexColor("#596579")
GREEN = colors.HexColor("#087F5B")
RED = colors.HexColor("#B42318")
LINE = colors.HexColor("#CBD3DF")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pick(item: dict[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        if key in item and item[key] not in (None, "", []):
            return item[key]
    return default


def plain(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float, str)):
        return str(value)
    if isinstance(value, list):
        return "; ".join(plain(part) for part in value)
    if isinstance(value, dict):
        return "; ".join(f"{key}: {plain(val)}" for key, val in value.items())
    return str(value)


def lines_for(text: str, font: str, size: float, width: float) -> list[str]:
    text = " ".join(str(text).replace("\n", " ").split())
    if not text:
        return ["-"]
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if stringWidth(candidate, font, size) <= width:
            current = candidate
            continue
        if current:
            lines.append(current)
        if stringWidth(word, font, size) <= width:
            current = word
            continue
        fragment = ""
        for char in word:
            if stringWidth(fragment + char, font, size) <= width:
                fragment += char
            else:
                if fragment:
                    lines.append(fragment)
                fragment = char
        current = fragment
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    font: str = "Helvetica",
    size: float = 8.6,
    leading: float = 10.7,
    color: colors.Color = NAVY,
) -> float:
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for line in lines_for(text, font, size, width):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def section(
    pdf: canvas.Canvas,
    label: str,
    value: Any,
    x: float,
    y: float,
    width: float,
    *,
    size: float = 8.6,
) -> float:
    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 8.7)
    pdf.drawString(x, y, label.upper())
    y -= 12
    return draw_wrapped(pdf, plain(value), x, y, width, size=size) - 7


def page_frame(pdf: canvas.Canvas, title: str, page_number: int) -> None:
    pdf.setFillColor(NAVY)
    pdf.rect(0, PAGE_H - 52, PAGE_W, 52, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(MARGIN, PAGE_H - 32, title)
    pdf.setFillColor(MID)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawRightString(PAGE_W - MARGIN, 18, f"Batch 002 human final QA | page {page_number}")


def text_field(
    pdf: canvas.Canvas,
    name: str,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    multiline: bool = False,
) -> None:
    pdf.acroForm.textfield(
        name=name,
        x=x,
        y=y,
        width=width,
        height=height,
        fontName="Helvetica",
        fontSize=9,
        textColor=NAVY,
        fillColor=colors.white,
        borderColor=LINE,
        borderWidth=1,
        forceBorder=True,
        fieldFlags=4096 if multiline else 0,
    )


def radio(
    pdf: canvas.Canvas,
    group: str,
    value: str,
    x: float,
    y: float,
    *,
    color: colors.Color,
) -> None:
    pdf.acroForm.radio(
        name=group,
        value=value,
        selected=False,
        x=x,
        y=y,
        buttonStyle="check",
        shape="square",
        size=11,
        borderColor=color,
        fillColor=colors.white,
        textColor=color,
        forceBorder=True,
    )


def draw_labeled_field(
    pdf: canvas.Canvas,
    label: str,
    name: str,
    x: float,
    y: float,
    width: float,
) -> None:
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(x, y + 23, label)
    text_field(pdf, name, x, y, width, 19)


def question_value(item: dict[str, Any]) -> str:
    direct = pick(item, "question", "question_text", "stem", "prompt")
    if isinstance(direct, dict):
        return plain(pick(direct, "text", "stem", "prompt", "question", default=direct))
    return plain(direct)


def options_value(item: dict[str, Any]) -> str:
    options = pick(item, "options", "choices", default=[])
    if isinstance(options, dict):
        return "    ".join(f"{key}. {plain(value)}" for key, value in options.items())
    if isinstance(options, list):
        rendered = []
        for index, option in enumerate(options):
            if isinstance(option, dict):
                label = pick(option, "label", "id", "key", default=chr(65 + index))
                value = pick(option, "text", "value", "option", default=option)
                rendered.append(f"{label}. {plain(value)}")
            else:
                rendered.append(f"{chr(65 + index)}. {plain(option)}")
        return "    ".join(rendered)
    return plain(options)


def route_value(item: dict[str, Any]) -> str:
    route = pick(item, "route", "taxonomy_route", "syllabus_route")
    if isinstance(route, list):
        return " > ".join(plain(part) for part in route)
    if route:
        return plain(route)
    return " > ".join(
        plain(item.get(key))
        for key in ("topic", "subtopic", "concept")
        if item.get(key)
    )


def draw_review_controls(pdf: canvas.Canvas, qkey: str, top_y: float) -> None:
    x0 = MARGIN
    width = PAGE_W - 2 * MARGIN
    pdf.setFillColor(LIGHT_BLUE)
    pdf.roundRect(x0, top_y - 244, width, 244, 6, fill=1, stroke=0)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(x0 + 12, top_y - 18, "HUMAN DECISION FIELDS")
    pdf.setFont("Helvetica-Bold", 7.7)
    pdf.drawString(x0 + 12, top_y - 39, "CHECK")
    pdf.drawCentredString(x0 + 331, top_y - 39, "PASS")
    pdf.drawCentredString(x0 + 387, top_y - 39, "FAIL")

    checks = [
        ("technical", "Technical correctness"),
        ("answer", "Answer correctness"),
        ("solution", "Solution correctness"),
        ("clarity", "Clarity / ambiguity"),
        ("originality", "Originality-conflict check"),
    ]
    y = top_y - 61
    for slug, label in checks:
        pdf.setStrokeColor(LINE)
        pdf.line(x0 + 10, y - 5, x0 + width - 10, y - 5)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 8.7)
        pdf.drawString(x0 + 12, y + 3, label)
        radio(pdf, f"{qkey}_{slug}", "PASS", x0 + 325, y - 1, color=GREEN)
        radio(pdf, f"{qkey}_{slug}", "FAIL", x0 + 381, y - 1, color=RED)
        y -= 24

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(x0 + 12, y + 5, "Decision")
    choices = [("PASS", GREEN), ("REVISE", colors.HexColor("#A15C00")), ("REJECT", RED)]
    x = x0 + 96
    for value, color in choices:
        radio(pdf, f"{qkey}_decision", value, x, y, color=color)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 7.5)
        pdf.drawString(x + 16, y + 2, value)
        x += 87

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(x0 + 12, y - 22, "Notes (required for REVISE or REJECT)")
    text_field(pdf, f"{qkey}_notes", x0 + 12, top_y - 236, width - 24, 28, multiline=True)


def build_pdf(items: Iterable[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    records = list(items)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    pdf.setTitle("GATE EE Batch 002 Human Final QA")
    pdf.setAuthor("TheMITbro")
    pdf.setSubject("Interactive human final-QA packet for Batch 002 Electric Circuits")

    page_frame(pdf, "GATE EE BATCH 002 - HUMAN FINAL QA", 1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(MARGIN, PAGE_H - 94, "Mobile-fillable review packet")
    pdf.setFillColor(MID)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(MARGIN, PAGE_H - 116, "20 Electric Circuits candidates | human release gate")

    y = PAGE_H - 157
    intro = [
        "Download this PDF and open it in Adobe Acrobat Reader or a PDF viewer that saves AcroForm fields.",
        "For every question, select exactly one PASS or FAIL value for each of the five checks, then one final decision.",
        "If any check fails, choose REVISE or REJECT and record a precise correction in Notes.",
        "Save the completed PDF with a new name, then run the included PDF importer. The pipeline remains blocked until its JSON output validates.",
    ]
    for index, instruction in enumerate(intro, 1):
        pdf.setFillColor(BLUE)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(MARGIN, y, f"{index}.")
        y = draw_wrapped(pdf, instruction, MARGIN + 18, y, PAGE_W - 2 * MARGIN - 18, size=9, leading=12) - 7

    pdf.setFillColor(PALE)
    pdf.roundRect(MARGIN, 360, PAGE_W - 2 * MARGIN, 210, 7, fill=1, stroke=0)
    draw_labeled_field(pdf, "Reviewer full name", "reviewer_name", MARGIN + 14, 516, 236)
    draw_labeled_field(pdf, "Qualification / role", "reviewer_qualification", MARGIN + 267, 516, 252)
    draw_labeled_field(pdf, "Review date (YYYY-MM-DD)", "review_date", MARGIN + 14, 470, 236)
    draw_labeled_field(pdf, "Reviewer email or identifier", "reviewer_identifier", MARGIN + 267, 470, 252)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(MARGIN + 14, 446, "Reviewer attestation")
    text_field(pdf, "reviewer_attestation", MARGIN + 14, 379, PAGE_W - 2 * MARGIN - 28, 61, multiline=True)
    pdf.setFillColor(MID)
    pdf.setFont("Helvetica-Oblique", 7.4)
    draw_wrapped(
        pdf,
        f"Type exactly: {REQUIRED_ATTESTATION}",
        MARGIN + 14,
        367,
        PAGE_W - 2 * MARGIN - 28,
        font="Helvetica-Oblique",
        size=7.2,
        leading=8.5,
        color=MID,
    )

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(MARGIN, 325, "Source lock")
    source_line = f"BATCH_002_ELECTRIC_CIRCUITS.jsonl | SHA-256 {sha256(SOURCE)}"
    draw_wrapped(pdf, source_line, MARGIN, 311, PAGE_W - 2 * MARGIN, size=7.8, leading=10)
    pdf.setFillColor(RED)
    pdf.setFont("Helvetica-Bold", 8.3)
    pdf.drawString(MARGIN, 279, "This form records review evidence; it does not itself promote or release questions.")
    pdf.showPage()

    total = len(records)
    for index, item in enumerate(records, 1):
        qid = plain(pick(item, "id", "question_id", default=f"BATCH002-{index:03d}"))
        revision = plain(pick(item, "revision", "version", default="1"))
        qkey = f"q{index:03d}"
        page_frame(pdf, f"{qid} - revision {revision}", index + 1)

        meta = " | ".join(
            part
            for part in [
                route_value(item),
                plain(pick(item, "type", "question_type")),
                f"{plain(pick(item, 'marks'))} mark(s)",
                plain(pick(item, "difficulty")),
            ]
            if part and part != " mark(s)"
        )
        y = PAGE_H - 75
        y = draw_wrapped(pdf, meta, MARGIN, y, PAGE_W - 2 * MARGIN, font="Helvetica-Bold", size=7.5, leading=9, color=MID) - 8
        y = section(pdf, "Question", question_value(item), MARGIN, y, PAGE_W - 2 * MARGIN)
        options = options_value(item)
        if options and options != "-":
            y = section(pdf, "Options", options, MARGIN, y, PAGE_W - 2 * MARGIN, size=8.2)
        y = section(
            pdf,
            "Declared answer",
            pick(item, "answer", "declared_answer", "correct_answer", "final_answer"),
            MARGIN,
            y,
            PAGE_W - 2 * MARGIN,
        )
        evidence = pick(
            item,
            "independent_recomputation_evidence",
            "_independent_recomputation_evidence",
            "independent_recomputation",
            "recomputation_evidence",
            "verification",
            default="Recompute independently before recording a decision.",
        )
        y = section(pdf, "Independent recomputation evidence", evidence, MARGIN, y, PAGE_W - 2 * MARGIN, size=8.2)
        solution = pick(item, "solution", "canonical_solution", "explanation", "worked_solution")
        y = section(pdf, "Canonical solution", solution, MARGIN, y, PAGE_W - 2 * MARGIN, size=8.2)

        review_top = 303
        if y < review_top + 5:
            # The source is intentionally concise; this guard makes any future
            # overflow obvious instead of silently painting over review fields.
            pdf.setFillColor(RED)
            pdf.setFont("Helvetica-Bold", 7.5)
            pdf.drawRightString(PAGE_W - MARGIN, review_top + 7, "CONTENT DENSE - inspect carefully")
        draw_review_controls(pdf, qkey, review_top)
        pdf.setFillColor(MID)
        pdf.setFont("Helvetica", 7)
        pdf.drawRightString(PAGE_W - MARGIN, 31, f"Question {index} of {total}")
        pdf.showPage()

    pdf.save()


def main() -> None:
    records = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(records) != 20:
        raise SystemExit(f"Expected 20 Batch 002 questions, found {len(records)}")
    qa = json.loads(INDEPENDENT_QA.read_text(encoding="utf-8"))
    evidence_by_id = {
        item["question_id"]: item.get("derivation_summary", "")
        for item in qa.get("questions", [])
    }
    for record in records:
        record["_independent_recomputation_evidence"] = evidence_by_id.get(record["id"], "")
    build_pdf(records)
    print(f"Created {OUTPUT}")
    print(f"Questions: {len(records)}")
    print(f"Source SHA-256: {sha256(SOURCE)}")


if __name__ == "__main__":
    main()
