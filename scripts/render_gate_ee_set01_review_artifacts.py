#!/usr/bin/env python3
"""Render the checksum-bound Set 01 question, solution and human-QA PDFs."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
from textwrap import wrap

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from gate_ee_set01 import (
    HANDOFF,
    HUMAN_QA,
    HUMAN_QA_PDF,
    MANIFEST,
    QUESTION_PDF,
    RENDER_EVIDENCE,
    ROOT,
    SOLUTION_PDF,
    content_sha256,
    load_json,
    pretty_bytes,
    relative,
    sha256,
    validate_manifest_and_handoff,
)


FIXED_SOURCE_DATE_EPOCH = "1789344000"  # 2026-09-14T00:00:00Z
REQUIRED_ATTESTATION = (
    "I independently reviewed the complete Set 01 question paper and solution PDF "
    "identified by the printed checksums and approve only the question positions marked PASS."
)


def raw_tex(value: str) -> str:
    return f"```{{=latex}}\n{value}\n```"


def grouped_hash(value: str) -> str:
    return " ".join(value[index:index + 16] for index in range(0, len(value), 16))


def yaml_header(title: str, subtitle: str, running_header: str) -> str:
    return f'''---
title: "{title}"
subtitle: "{subtitle}"
date: ""
documentclass: article
papersize: a4
fontsize: 10pt
geometry:
  - top=15mm
  - bottom=16mm
  - left=16mm
  - right=16mm
mainfont: "DejaVu Sans"
sansfont: "DejaVu Sans"
monofont: "DejaVu Sans Mono"
mathfont: "Latin Modern Math"
colorlinks: true
header-includes:
  - |
    \\usepackage{{array,booktabs,enumitem,fancyhdr,graphicx,needspace,xcolor}}
    \\definecolor{{themitblue}}{{HTML}}{{173B57}}
    \\definecolor{{themitgray}}{{HTML}}{{4B5563}}
    \\pagestyle{{fancy}}
    \\fancyhf{{}}
    \\lhead{{{running_header}}}
    \\rhead{{Review copy}}
    \\cfoot{{\\thepage}}
    \\setlength{{\\headheight}}{{14pt}}
    \\setlength{{\\parindent}}{{0pt}}
    \\setlength{{\\parskip}}{{4pt}}
    \\setlist[itemize]{{leftmargin=7mm,itemsep=1pt,topsep=2pt}}
---
'''


def convert_diagrams(questions: list[dict], staging: Path) -> dict[str, Path]:
    converted: dict[str, Path] = {}
    for question in questions:
        diagram = question.get("diagram")
        if not diagram:
            continue
        source = ROOT / diagram["asset"]
        target = staging / f"{question['id']}.png"
        run = subprocess.run(
            [
                "inkscape", str(source), "--export-type=png",
                f"--export-filename={target}", "--export-width=1600",
            ],
            text=True,
            capture_output=True,
        )
        if run.returncode or not target.is_file():
            raise RuntimeError(
                f"diagram conversion failed for {question['id']}:\n{run.stdout}\n{run.stderr}"
            )
        converted[question["id"]] = target
    return converted


def diagram_block(question: dict, diagrams: dict[str, Path], *, width: str = "0.66\\linewidth") -> list[str]:
    diagram = question.get("diagram")
    if not diagram:
        return []
    path = diagrams[question["id"]].as_posix()
    return [
        raw_tex(
            "\n".join([
                r"\begin{center}",
                rf"\includegraphics[width={width},height=48mm,keepaspectratio]{{{path}}}",
                r"\end{center}",
            ])
        ),
        "",
        f"*Figure: {diagram['caption']}*  ",
        f"*Accessible description: {diagram['alt_text']}*",
        "",
    ]


def section_title(question: dict) -> str:
    subject = question["section"]
    if subject == "General Aptitude":
        return "Section A — General Aptitude (10 questions, 15 marks)"
    if subject == "Engineering Mathematics":
        return "Section B — Engineering Mathematics (8 questions, 13 marks)"
    return "Section C — Electrical Engineering (47 questions, 72 marks)"


def question_markdown(handoff: dict, manifest_hash: str, diagrams: dict[str, Path]) -> str:
    paper = handoff["paper"]
    body = [
        yaml_header(paper["title"], "Set 01 Question Paper — Human-QA Review Copy", "TheMITbro GATE 2027 EE — Set 01"),
        raw_tex(r"\begin{center}{\Large\bfseries\color{themitblue} NOT FOR SALE OR RELEASE}\end{center}"),
        "",
        "This PDF is a checksum-bound review artifact. It is not an official GATE paper and has not yet passed complete-paper human QA.",
        "",
        f"**Paper ID:** `{handoff['paper_id']}`  ",
        f"**Manifest content SHA-256:** `{grouped_hash(manifest_hash)}`  ",
        "**Questions / marks / duration:** 65 / 100 / 180 minutes",
        "",
        "## Instructions",
        "",
        "- Questions 1–10 are General Aptitude; Questions 11–65 are the selected subject.",
        "- Each question carries either 1 mark or 2 marks, as printed beside it.",
        "- For MCQ, select exactly one option. A wrong 1-mark MCQ attracts 1/3 negative mark; a wrong 2-mark MCQ attracts 2/3 negative mark.",
        "- MSQ and NAT questions have no negative marking. This project reference specifies no partial marks for MSQ.",
        "- For NAT, enter only the numerical answer in the permitted answer box on the examination interface.",
        "- Internal audit IDs appear only because this is a review copy; they must be removed from the commercial learner copy.",
        "",
        raw_tex(r"\clearpage"),
    ]
    last_section = None
    for question in paper["questions"]:
        if question["section"] != last_section:
            body.extend([f"# {section_title(question)}", ""])
            last_section = question["section"]
        body.extend([
            raw_tex(r"\Needspace{75mm}"),
            f"## Q{question['number']}. [{question['marks']} mark{'s' if question['marks'] != 1 else ''}; {question['type']}]",
            "",
            f"*Audit ID: {question['id']} · revision {question['revision']} · {question['difficulty']}*",
            "",
            question["text"],
            "",
        ])
        if question.get("options"):
            for index, option in enumerate(question["options"]):
                body.append(f"- **{chr(65 + index)}.** {option}")
            body.append("")
        else:
            body.extend(["**NAT response:** ____________________", ""])
        body.extend(diagram_block(question, diagrams))
        body.extend([raw_tex(r"\vspace{2mm}\hrule\vspace{3mm}"), ""])
    body.extend([
        raw_tex(r"\Needspace{18mm}"),
        "# End of question paper",
        "",
        "Release remains blocked until this exact question PDF and its paired solution PDF pass named-human complete-paper technical and visual QA.",
    ])
    return "\n".join(body).rstrip() + "\n"


def answer_text(answer: object) -> str:
    if isinstance(answer, list):
        return ", ".join(str(value) for value in answer)
    return str(answer)


def solution_markdown(handoff: dict, manifest_hash: str, diagrams: dict[str, Path]) -> str:
    paper = handoff["paper"]
    body = [
        yaml_header(paper["title"], "Set 01 Answer Key and Solutions — Human-QA Review Copy", "TheMITbro GATE 2027 EE — Solutions"),
        raw_tex(r"\begin{center}{\Large\bfseries\color{themitblue} CONFIDENTIAL REVIEW COPY}\end{center}"),
        "",
        "This answer-and-solution PDF is paired only with the checksum-bound Set 01 review question paper. It is not authorized for release.",
        "",
        f"**Paper ID:** `{handoff['paper_id']}`  ",
        f"**Manifest content SHA-256:** `{grouped_hash(manifest_hash)}`",
        "",
        "# Compact answer key",
        "",
    ]
    for start in range(0, len(paper["questions"]), 10):
        chunk = paper["questions"][start:start + 10]
        body.append(" · ".join(f"**{q['number']}.** {answer_text(q['answer'])}" for q in chunk))
        body.append("")
    body.extend([raw_tex(r"\clearpage"), "# Detailed solutions", ""])
    last_section = None
    for question in paper["questions"]:
        if question["section"] != last_section:
            body.extend([f"# {section_title(question)}", ""])
            last_section = question["section"]
        body.extend([
            raw_tex(r"\Needspace{95mm}"),
            f"## Q{question['number']}. {question['id']} [{question['marks']} mark{'s' if question['marks'] != 1 else ''}; {question['type']}]",
            "",
            question["text"],
            "",
        ])
        if question.get("options"):
            for index, option in enumerate(question["options"]):
                body.append(f"- **{chr(65 + index)}.** {option}")
            body.append("")
        body.extend(diagram_block(question, diagrams, width="0.55\\linewidth"))
        body.extend([
            f"**Verified answer:** {answer_text(question['answer'])}",
            "",
            "**Solution:**",
            "",
            question["solution"],
            "",
            raw_tex(r"\vspace{2mm}\hrule\vspace{3mm}"),
            "",
        ])
    return "\n".join(body).rstrip() + "\n"


def run_pandoc(markdown: str, output: Path, staging: Path, stem: str) -> None:
    source = staging / f"{stem}.md"
    tex = staging / f"{stem}.tex"
    source.write_text(markdown, encoding="utf-8")
    env = os.environ.copy()
    env.update({"SOURCE_DATE_EPOCH": FIXED_SOURCE_DATE_EPOCH, "TZ": "UTC"})
    pandoc_command = [
        "pandoc", str(source), "--from=markdown+raw_tex+tex_math_dollars+link_attributes",
        "--standalone", "--metadata=linkcolor:themitblue", "--output", str(tex),
    ]
    completed = subprocess.run(pandoc_command, cwd=ROOT, env=env, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(f"Pandoc failed for {output.name}:\n{completed.stdout}\n{completed.stderr}")
    xelatex_command = [
        "xelatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
        "-file-line-error", f"-jobname={stem}", tex.name,
    ]
    for _ in range(2):
        completed = subprocess.run(
            xelatex_command, cwd=staging, env=env, text=True, capture_output=True
        )
        if completed.returncode:
            raise RuntimeError(
                f"XeLaTeX failed for {output.name}:\n{completed.stdout}\n{completed.stderr}"
            )
    rendered = staging / f"{stem}.pdf"
    if not rendered.is_file():
        raise RuntimeError(f"XeLaTeX did not create {rendered.name}")
    shutil.copyfile(rendered, output)
    if not output.is_file() or output.stat().st_size < 20_000:
        raise RuntimeError(f"{output.name} is missing or unexpectedly small")


def _register_fonts() -> None:
    for name, path in (
        ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ):
        if name not in pdfmetrics.getRegisteredFontNames() and Path(path).is_file():
            pdfmetrics.registerFont(TTFont(name, path))


def _draw_wrapped(c: canvas.Canvas, value: str, x: float, y: float, width_chars: int, *, font: str = "DejaVuSans", size: float = 8.5, leading: float = 11) -> float:
    c.setFont(font, size)
    for line in wrap(value, width_chars, break_long_words=True, break_on_hyphens=False) or [""]:
        c.drawString(x, y, line)
        y -= leading
    return y


def _checkbox(c: canvas.Canvas, name: str, x: float, y: float, label: str, *, size: float = 10) -> None:
    c.acroForm.checkbox(
        name=name, x=x, y=y - 2, size=size, checked=False, buttonStyle="check",
        borderWidth=1, borderColor=colors.HexColor("#355B75"),
        fillColor=colors.white, textColor=colors.HexColor("#173B57"), forceBorder=True,
    )
    c.setFont("DejaVuSans", 7.5)
    c.drawString(x + size + 3, y, label)


def _textfield(c: canvas.Canvas, name: str, x: float, y: float, width: float, height: float, *, multiline: bool = False) -> None:
    flags = 4096 if multiline else 0
    c.acroForm.textfield(
        name=name, x=x, y=y, width=width, height=height, value="",
        fontName="Helvetica", fontSize=8, fieldFlags=flags,
        borderWidth=1, borderColor=colors.HexColor("#6B7280"),
        fillColor=colors.white, textColor=colors.black, forceBorder=True,
    )


def _page_header(c: canvas.Canvas, page_number: int, title: str) -> None:
    width, height = A4
    c.setFillColor(colors.HexColor("#173B57"))
    c.setFont("DejaVuSans-Bold", 10)
    c.drawString(36, height - 32, title)
    c.setFont("DejaVuSans", 8)
    c.drawRightString(width - 36, height - 32, f"Page {page_number}")
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(36, height - 39, width - 36, height - 39)
    c.setFillColor(colors.black)


def render_human_qa_pdf(template: dict, output: Path) -> None:
    _register_fonts()
    width, height = A4
    c = canvas.Canvas(str(output), pagesize=A4, pageCompression=1, invariant=1)
    c.setTitle("GATE EE Set 01 Complete-Paper Human Final QA")
    c.setAuthor("TheMITbro")
    page_number = 1
    _page_header(c, page_number, "GATE EE Set 01 — Complete-Paper Human Final QA")
    c.setFont("DejaVuSans-Bold", 19)
    c.setFillColor(colors.HexColor("#173B57"))
    c.drawString(42, height - 80, "Human Final QA — Mobile Fillable")
    c.setFillColor(colors.HexColor("#9B1C1C"))
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(42, height - 104, "REVIEW GATE ONLY — RELEASE AND SALE BLOCKED")
    c.setFillColor(colors.black)
    y = height - 135
    y = _draw_wrapped(c, "This form is valid only for the exact question and solution PDFs identified below. Review both PDFs before completing any decision.", 42, y, 92, size=9.5, leading=13)
    y -= 8
    for label, value in (
        ("Paper ID", template["paper_id"]),
        ("Manifest SHA-256", grouped_hash(template["manifest_content_sha256"])),
        ("Question PDF SHA-256", grouped_hash(template["question_pdf_sha256"])),
        ("Solution PDF SHA-256", grouped_hash(template["solution_pdf_sha256"])),
    ):
        c.setFont("DejaVuSans-Bold", 8)
        c.drawString(42, y, label + ":")
        y = _draw_wrapped(c, value, 174, y, 48, size=7.5, leading=9)
        y -= 3
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(42, y, "Reviewer name")
    _textfield(c, "reviewer_name", 160, y - 5, 380, 18)
    y -= 31
    c.drawString(42, y, "Role / qualification")
    _textfield(c, "reviewer_qualification", 160, y - 5, 380, 18)
    y -= 31
    c.drawString(42, y, "Review date (YYYY-MM-DD)")
    _textfield(c, "review_date", 190, y - 5, 150, 18)
    c.drawString(355, y, "Reviewer ID (optional)")
    _textfield(c, "reviewer_identifier", 455, y - 5, 85, 18)
    y -= 38
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(42, y, "Required attestation (type exactly):")
    y -= 15
    y = _draw_wrapped(c, REQUIRED_ATTESTATION, 42, y, 92, size=8, leading=10)
    _textfield(c, "reviewer_attestation", 42, y - 42, 498, 42, multiline=True)
    y -= 62
    c.setFillColor(colors.HexColor("#7C2D12"))
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(42, y, "Reviewer-metadata inconsistency requiring resolution")
    c.setFillColor(colors.black)
    y -= 15
    issue = (
        "Batch 001 records 'Masters in Electrical Engineering'; Batches 002–005 record "
        "'Diploma in Electrical Engineering'. Verify your true qualification. Do not select "
        "the box until the value typed above is accurate; explain the correction below."
    )
    y = _draw_wrapped(c, issue, 42, y, 92, size=8, leading=10)
    _checkbox(c, "batch001_qualification_reconfirmed", 42, y - 3, "I reconfirmed the accurate qualification and resolve the inconsistent historical metadata.")
    y -= 31
    c.setFont("DejaVuSans-Bold", 8)
    c.drawString(42, y, "Correction / confirmation note")
    _textfield(c, "batch001_qualification_notes", 42, y - 44, 498, 40, multiline=True)
    y -= 58
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(42, y, "Per-question procedure")
    y -= 14
    instructions = [
        "Content: stem, options, marks, type, numbering and section are complete and readable.",
        "Answer/Solution: the solution PDF matches the question and gives the certified answer.",
        "Visual: notation, page layout and any figure are legible and not clipped or overlapped.",
        "Select exactly one decision. Explain every REVISE or REJECT in Notes.",
    ]
    for item in instructions:
        y = _draw_wrapped(c, "• " + item, 48, y, 88, size=8, leading=10)
        y -= 1
    c.showPage()

    questions = template["questions"]
    for offset in range(0, len(questions), 5):
        page_number += 1
        _page_header(c, page_number, "Set 01 per-question technical and visual decisions")
        y = height - 62
        for item in questions[offset:offset + 5]:
            prefix = f"q{item['position']:03d}"
            c.setFillColor(colors.HexColor("#EAF2F7"))
            c.roundRect(36, y - 120, width - 72, 119, 4, fill=1, stroke=0)
            c.setFillColor(colors.black)
            c.setFont("DejaVuSans-Bold", 9)
            heading = f"Q{item['position']} · {item['question_id']} · {item['type']} · {item['marks']} mark{'s' if item['marks'] != 1 else ''}"
            c.drawString(43, y - 14, heading)
            _checkbox(c, f"{prefix}_content_pass", 43, y - 34, "Content PASS")
            _checkbox(c, f"{prefix}_answer_solution_pass", 150, y - 34, "Answer/Solution PASS")
            _checkbox(c, f"{prefix}_visual_pass", 310, y - 34, "Visual/Layout PASS")
            c.setFont("DejaVuSans-Bold", 7.5)
            c.drawString(43, y - 55, "Decision:")
            _checkbox(c, f"{prefix}_decision_pass", 96, y - 57, "PASS")
            _checkbox(c, f"{prefix}_decision_revise", 160, y - 57, "REVISE")
            _checkbox(c, f"{prefix}_decision_reject", 238, y - 57, "REJECT")
            c.setFont("DejaVuSans", 7.5)
            c.drawString(310, y - 54, "Notes (required for REVISE/REJECT)")
            _textfield(c, f"{prefix}_notes", 43, y - 108, 492, 37, multiline=True)
            y -= 137
        c.showPage()

    page_number += 1
    _page_header(c, page_number, "Set 01 final complete-paper decision")
    y = height - 75
    c.setFont("DejaVuSans-Bold", 16)
    c.setFillColor(colors.HexColor("#173B57"))
    c.drawString(42, y, "Review completion")
    c.setFillColor(colors.black)
    y -= 32
    y = _draw_wrapped(c, "Complete this page only after all 65 positions have exactly one decision and every REVISE/REJECT has an explanatory note.", 42, y, 92, size=9, leading=12)
    y -= 12
    _checkbox(c, "final_approve_reviewed_results", 42, y, "APPROVE REVIEWED RESULTS (only if all 65 decisions are PASS)", size=12)
    y -= 40
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(42, y, "Reviewer typed signature")
    _textfield(c, "reviewer_signature", 185, y - 5, 355, 20)
    y -= 42
    c.drawString(42, y, "Final comments")
    _textfield(c, "final_comments", 42, y - 115, 498, 105, multiline=True)
    y -= 145
    c.setFillColor(colors.HexColor("#9B1C1C"))
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(42, y, "Completing this form does not itself publish, price, sell or release the paper.")
    c.setFillColor(colors.black)
    c.save()


def pdf_summary(path: Path) -> dict:
    reader = PdfReader(path)
    metadata = reader.metadata or {}
    return {
        "path": relative(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "pages": len(reader.pages),
        "producer": str(metadata.get("/Producer", "")),
    }


def build_human_qa_template(manifest: dict, handoff: dict) -> dict:
    payload = {
        "signoff_contract": "GATE_EE_SET01_COMPLETE_PAPER_HUMAN_FINAL_QA_V1",
        "paper_id": manifest["paper_id"],
        "status": "PENDING_NAMED_HUMAN_COMPLETE_PAPER_QA",
        "manifest_content_sha256": manifest["manifest_content_sha256"],
        "formatter_handoff_content_sha256": handoff["handoff_content_sha256"],
        "question_pdf_sha256": sha256(QUESTION_PDF),
        "solution_pdf_sha256": sha256(SOLUTION_PDF),
        "required_attestation": REQUIRED_ATTESTATION,
        "reviewer": {
            "name": "", "role_or_qualification": "", "review_date": "",
            "reviewer_identifier": "", "attestation": "", "signature": "",
        },
        "reviewer_metadata_reconfirmation": {
            "status": "PENDING",
            "issue": manifest["reviewer_metadata_consistency"],
            "reconfirmed": False,
            "notes": "",
        },
        "questions": [
            {
                "position": row["position"], "question_id": row["question_id"],
                "revision": row["revision"], "type": row["type"], "marks": row["marks"],
                "content_rendering": "PENDING", "answer_solution_alignment": "PENDING",
                "visual_layout": "PENDING", "decision": "PENDING", "notes": "",
            }
            for row in manifest["questions"]
        ],
        "final_decision": "PENDING",
        "final_comments": "",
        "release_authorized": False,
        "sale_authorized": False,
    }
    return payload


def renderer_version(command: str) -> str:
    run = subprocess.run([command, "--version"], text=True, capture_output=True)
    return (run.stdout or run.stderr).splitlines()[0].strip() if run.returncode == 0 else "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed artifacts differ from a fresh deterministic render")
    args = parser.parse_args()
    manifest, handoff = validate_manifest_and_handoff()
    outputs = (QUESTION_PDF, SOLUTION_PDF, HUMAN_QA_PDF, HUMAN_QA, RENDER_EVIDENCE)
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)

    prior = {path: path.read_bytes() for path in outputs if path.is_file()} if args.check else {}
    staging = ROOT / "build/set01-review"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    try:
        questions = handoff["paper"]["questions"]
        diagrams = convert_diagrams(questions, staging)
        run_pandoc(question_markdown(handoff, manifest["manifest_content_sha256"], diagrams), QUESTION_PDF, staging, "question-paper")
        run_pandoc(solution_markdown(handoff, manifest["manifest_content_sha256"], diagrams), SOLUTION_PDF, staging, "solutions")
    finally:
        shutil.rmtree(staging, ignore_errors=True)

    template = build_human_qa_template(manifest, handoff)
    HUMAN_QA.write_bytes(pretty_bytes(template))
    render_human_qa_pdf(template, HUMAN_QA_PDF)
    evidence = {
        "render_evidence_contract": "GATE_EE_SET01_REVIEW_RENDER_EVIDENCE_V1",
        "paper_id": manifest["paper_id"],
        "rendered_on": manifest["assembled_on"],
        "manifest": {
            "path": relative(MANIFEST), "file_sha256": sha256(MANIFEST),
            "content_sha256": manifest["manifest_content_sha256"],
        },
        "formatter_handoff": {
            "path": relative(HANDOFF), "file_sha256": sha256(HANDOFF),
            "content_sha256": handoff["handoff_content_sha256"],
        },
        "renderer": {
            "contract": handoff["render_contract"],
            "pandoc": renderer_version("pandoc"),
            "xelatex": renderer_version("xelatex"),
            "source_date_epoch": FIXED_SOURCE_DATE_EPOCH,
            "math_font": "Latin Modern Math",
        },
        "artifacts": {
            "question_pdf": pdf_summary(QUESTION_PDF),
            "solution_pdf": pdf_summary(SOLUTION_PDF),
            "human_qa_pdf": pdf_summary(HUMAN_QA_PDF),
            "human_qa_json": {
                "path": relative(HUMAN_QA), "sha256": sha256(HUMAN_QA),
                "bytes": HUMAN_QA.stat().st_size,
            },
        },
        "gate_state": {
            "manifest_validation": "PASS",
            "render_validation": "PENDING_INDEPENDENT_VALIDATOR",
            "complete_paper_human_qa": "PENDING",
            "release_authorized": False,
            "sale_authorized": False,
        },
    }
    evidence["evidence_content_sha256"] = content_sha256(evidence, "evidence_content_sha256")
    RENDER_EVIDENCE.write_bytes(pretty_bytes(evidence))

    if args.check:
        changed = [path for path in outputs if path not in prior or path.read_bytes() != prior[path]]
        if changed:
            print("GATE EE SET 01 DETERMINISTIC RENDER CHECK: FAILED")
            for path in changed:
                print("-", relative(path))
            return 1
    print("GATE EE SET 01 REVIEW ARTIFACTS: RENDERED")
    print(f"Question paper: {QUESTION_PDF.name} ({pdf_summary(QUESTION_PDF)['pages']} pages)")
    print(f"Solutions: {SOLUTION_PDF.name} ({pdf_summary(SOLUTION_PDF)['pages']} pages)")
    print(f"Human QA form: {HUMAN_QA_PDF.name} ({pdf_summary(HUMAN_QA_PDF)['pages']} pages)")
    print("Release and sale gates: BLOCKED pending named-human complete-paper QA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
