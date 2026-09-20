#!/usr/bin/env python3
"""Build the non-public Set 01 RC1 learner artifacts and release-authorization form."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from gate_ee_set01 import (
    COMPLETED_SIGNOFF,
    FORMATTER_RELEASE_EVIDENCE,
    HANDOFF,
    MANIFEST,
    RELEASE_AUTHORIZATION_PDF,
    RELEASE_CANDIDATE,
    RELEASE_LEARNER_PACK_PDF,
    RELEASE_QUESTION_PDF,
    RELEASE_SOLUTION_PDF,
    ROOT,
    content_sha256,
    load_json,
    pretty_bytes,
    relative,
    sha256,
    validate_manifest_and_handoff,
)
from render_gate_ee_set01_review_artifacts import (
    _checkbox,
    _draw_wrapped,
    _page_header,
    _register_fonts,
    _textfield,
    answer_text,
    convert_diagrams,
    diagram_block,
    grouped_hash,
    pdf_summary,
    raw_tex,
    run_pandoc,
    section_title,
)
from validate_gate_ee_set01_human_signoff import validate_completed_signoff


FIXED_SOURCE_DATE_EPOCH = "1789776000"  # 2026-09-19T00:00:00Z
REQUIRED_RELEASE_ATTESTATION = (
    "I verified the exact Set 01 RC1 question, solution and learner-pack PDFs identified "
    "by these checksums and authorize this candidate for release, subject to separate "
    "pricing and storefront activation."
)


def learner_yaml_header(title: str, subtitle: str, running_header: str, right_header: str) -> str:
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
    \\rhead{{{right_header}}}
    \\cfoot{{\\thepage}}
    \\setlength{{\\headheight}}{{14pt}}
    \\setlength{{\\parindent}}{{0pt}}
    \\setlength{{\\parskip}}{{4pt}}
    \\setlist[itemize]{{leftmargin=7mm,itemsep=1pt,topsep=2pt}}
---
'''


def question_markdown(handoff: dict, diagrams: dict[str, Path]) -> str:
    paper = handoff["paper"]
    body = [
        learner_yaml_header(
            "GATE 2027 Electrical Engineering",
            "Independent Practice Mock Set 01 — Question Paper",
            "TheMITbro · GATE 2027 EE · Set 01",
            "Question paper",
        ),
        raw_tex(r"\begin{center}{\small\bfseries\color{themitgray} INDEPENDENT PRACTICE MATERIAL — NOT AN OFFICIAL GATE PAPER}\end{center}"),
        "",
        "**Questions / marks / duration:** 65 / 100 / 180 minutes",
        "",
        "## Instructions",
        "",
        "- Questions 1–10 are General Aptitude; Questions 11–65 are Electrical Engineering, including Engineering Mathematics.",
        "- Each question carries either 1 mark or 2 marks, as printed beside it.",
        "- For MCQ, select exactly one option. A wrong 1-mark MCQ attracts 1/3 negative mark; a wrong 2-mark MCQ attracts 2/3 negative mark.",
        "- MSQ and NAT questions have no negative marking. This practice-paper contract awards no partial marks for MSQ.",
        "- For NAT, enter only the numerical answer in the permitted answer box on the examination interface.",
        "",
        raw_tex(r"\clearpage"),
    ]
    last_section = None
    for question in paper["questions"]:
        if question["section"] != last_section:
            body.extend([f"# {section_title(question)}", ""])
            last_section = question["section"]
        body.extend([
            raw_tex(r"\Needspace{72mm}"),
            f"## Q{question['number']}. [{question['marks']} mark{'s' if question['marks'] != 1 else ''}; {question['type']}]",
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
        "The answer key and worked solutions begin in the separate solutions document or after this section in the learner pack.",
    ])
    return "\n".join(body).rstrip() + "\n"


def solution_markdown(handoff: dict, diagrams: dict[str, Path]) -> str:
    paper = handoff["paper"]
    body = [
        learner_yaml_header(
            "GATE 2027 Electrical Engineering",
            "Independent Practice Mock Set 01 — Answer Key and Solutions",
            "TheMITbro · GATE 2027 EE · Set 01",
            "Solutions",
        ),
        raw_tex(r"\begin{center}{\small\bfseries\color{themitgray} INDEPENDENT PRACTICE MATERIAL — NOT AN OFFICIAL GATE PAPER}\end{center}"),
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
            raw_tex(r"\Needspace{92mm}"),
            f"## Q{question['number']}. [{question['marks']} mark{'s' if question['marks'] != 1 else ''}; {question['type']}]",
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
            f"**Answer:** {answer_text(question['answer'])}",
            "",
            "**Solution:**",
            "",
            question["solution"],
            "",
            raw_tex(r"\vspace{2mm}\hrule\vspace{3mm}"),
            "",
        ])
    return "\n".join(body).rstrip() + "\n"


def combine_pdfs(question_path: Path, solution_path: Path, output: Path) -> None:
    writer = PdfWriter()
    for source in (question_path, solution_path):
        reader = PdfReader(source)
        for page in reader.pages:
            writer.add_page(page)
    writer.add_metadata({
        "/Title": "GATE 2027 EE Independent Practice Mock Set 01 — Learner Pack RC1",
        "/Author": "TheMITbro",
        "/Subject": "Question paper followed by answer key and solutions",
        "/Creator": "TheMITbro deterministic release-candidate pipeline",
        "/Producer": "pypdf",
        "/CreationDate": "D:20260919000000+00'00'",
        "/ModDate": "D:20260919000000+00'00'",
    })
    with output.open("wb") as stream:
        writer.write(stream)


def render_release_authorization(candidate_hashes: dict[str, str], output: Path) -> None:
    _register_fonts()
    width, height = A4
    c = canvas.Canvas(str(output), pagesize=A4, pageCompression=1, invariant=1)
    c.setTitle("GATE EE Set 01 RC1 Exact-Artifact Release Authorization")
    c.setAuthor("TheMITbro")
    _page_header(c, 1, "GATE EE Set 01 RC1 — Exact-Artifact Release Authorization")
    c.setFont("DejaVuSans-Bold", 18)
    c.setFillColor(colors.HexColor("#173B57"))
    c.drawString(42, height - 78, "Release Authorization — Mobile Fillable")
    c.setFillColor(colors.HexColor("#9B1C1C"))
    c.setFont("DejaVuSans-Bold", 10)
    c.drawString(42, height - 101, "CANDIDATE ONLY — SALE AND STOREFRONT ACTIVATION REMAIN BLOCKED")
    c.setFillColor(colors.black)
    y = height - 129
    y = _draw_wrapped(c, "Authorize only the exact learner-facing PDFs identified below. If any checksum differs, stop and regenerate the candidate.", 42, y, 94, size=8.5, leading=11)
    y -= 5
    for label, key in (
        ("Question PDF", "question_pdf"),
        ("Solution PDF", "solution_pdf"),
        ("Learner pack", "learner_pack_pdf"),
    ):
        c.setFont("DejaVuSans-Bold", 7.5)
        c.drawString(42, y, label + " SHA-256:")
        digest = candidate_hashes[key]
        c.setFont("DejaVuSans", 7.2)
        c.drawString(160, y, grouped_hash(digest[:32]))
        c.drawString(160, y - 9, grouped_hash(digest[32:]))
        y -= 22
    c.setFont("DejaVuSans-Bold", 8.5)
    c.drawString(42, y, "Reviewer name")
    _textfield(c, "reviewer_name", 155, y - 5, 385, 19)
    y -= 31
    c.drawString(42, y, "Role / qualification")
    _textfield(c, "reviewer_qualification", 155, y - 5, 385, 19)
    y -= 31
    c.drawString(42, y, "Review date (YYYY-MM-DD)")
    _textfield(c, "review_date", 190, y - 5, 150, 19)
    c.drawString(360, y, "Reviewer ID")
    _textfield(c, "reviewer_identifier", 440, y - 5, 100, 19)
    y -= 37
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(42, y, "Required exact-artifact checks")
    y -= 19
    checks = (
        ("question_hash_match", "Question PDF opens and its checksum matches."),
        ("solution_hash_match", "Solution PDF opens and its checksum matches."),
        ("learner_pack_hash_match", "Combined learner pack opens and its checksum matches."),
        ("clean_learner_copy", "No review-only warning, internal audit ID or raw source markup is visible."),
        ("visual_layout_pass", "All pages, equations, options and figures are legible and unclipped."),
        ("question_solution_alignment", "Question numbering, answer key and detailed solutions align for all 65 positions."),
    )
    for name, label in checks:
        _checkbox(c, name, 42, y, label, size=11)
        y -= 22
    y -= 3
    c.setFont("DejaVuSans-Bold", 8.5)
    c.drawString(42, y, "Required attestation (type exactly):")
    y -= 14
    y = _draw_wrapped(c, REQUIRED_RELEASE_ATTESTATION, 42, y, 94, size=7.7, leading=9.5)
    _textfield(c, "release_attestation", 42, y - 57, 498, 55, multiline=True)
    y -= 75
    c.setFont("DejaVuSans-Bold", 8.5)
    c.drawString(42, y, "Typed signature")
    _textfield(c, "release_signature", 145, y - 5, 395, 20)
    y -= 34
    _checkbox(c, "final_authorize_release", 42, y, "AUTHORIZE THIS EXACT RC1 CANDIDATE FOR RELEASE", size=12)
    y -= 31
    c.setFont("DejaVuSans-Bold", 8)
    c.drawString(42, y, "Final comments (optional)")
    _textfield(c, "final_comments", 42, y - 52, 498, 46, multiline=True)
    y -= 69
    c.setFillColor(colors.HexColor("#9B1C1C"))
    c.setFont("DejaVuSans-Bold", 8)
    c.drawString(42, y, "This authorization does not set a price, enable checkout, or authorize sale.")
    c.save()


def validate_upstream() -> tuple[dict, dict, dict, dict]:
    manifest, handoff = validate_manifest_and_handoff()
    completed = load_json(COMPLETED_SIGNOFF)
    template = load_json(ROOT / "GATE_EE/corpus_v1/review_manifests/GATE_EE_SET_01_HUMAN_FINAL_QA.json")
    signoff_errors, all_pass = validate_completed_signoff(completed, template)
    if signoff_errors or not all_pass:
        raise ValueError("completed Set 01 human QA is not an exact all-PASS signoff: " + "; ".join(signoff_errors))
    formatter = load_json(FORMATTER_RELEASE_EVIDENCE)
    expected_formatter = (
        formatter.get("evidence_contract"), formatter.get("paper_id"),
        formatter.get("question_count"), formatter.get("formatter_pass_count"),
        formatter.get("formatter_blocked_count"), formatter.get("status"),
        formatter.get("release_authorized"), formatter.get("sale_authorized"),
    )
    if expected_formatter != (
        "GATE_EE_SET01_FORMATTER_RELEASE_CANDIDATE_EVIDENCE_V1",
        "GATE_2027_EE_SET_01", 65, 65, 0, "PASS", False, False,
    ):
        raise ValueError("Set 01 aggregate Formatter release evidence is not an exact all-PASS non-authorizing result")
    if formatter.get("evidence_content_sha256") != content_sha256(formatter, "evidence_content_sha256"):
        raise ValueError("Set 01 aggregate Formatter evidence self-hash is invalid")
    if formatter.get("review_manifest_content_sha256") != manifest["manifest_content_sha256"]:
        raise ValueError("Formatter evidence is not bound to this review manifest")
    if formatter.get("review_handoff_content_sha256") != handoff["handoff_content_sha256"]:
        raise ValueError("Formatter evidence is not bound to this review handoff")
    return manifest, handoff, completed, formatter


def build_candidate(manifest: dict, handoff: dict, completed: dict, formatter: dict) -> dict:
    payload = {
        "candidate_contract": "GATE_EE_SET01_LEARNER_RELEASE_CANDIDATE_V1",
        "candidate_id": "GATE_2027_EE_SET_01_RC1",
        "paper_id": manifest["paper_id"],
        "generated_on": "2026-09-19",
        "status": "RELEASE_CANDIDATE_AWAITING_EXACT_ARTIFACT_AUTHORIZATION",
        "source_review_manifest": {
            "path": relative(MANIFEST),
            "file_sha256": sha256(MANIFEST),
            "content_sha256": manifest["manifest_content_sha256"],
        },
        "source_formatter_handoff": {
            "path": relative(HANDOFF),
            "file_sha256": sha256(HANDOFF),
            "content_sha256": handoff["handoff_content_sha256"],
        },
        "complete_paper_human_qa": {
            "path": relative(COMPLETED_SIGNOFF),
            "file_sha256": sha256(COMPLETED_SIGNOFF),
            "content_sha256": completed["signoff_content_sha256"],
            "completed_pdf_sha256": completed["completed_pdf"]["sha256"],
            "status": completed["status"],
            "pass_count": 65,
        },
        "formatter_release_evidence": {
            "path": relative(FORMATTER_RELEASE_EVIDENCE),
            "file_sha256": sha256(FORMATTER_RELEASE_EVIDENCE),
            "content_sha256": formatter["evidence_content_sha256"],
            "status": formatter["status"],
            "pass_count": formatter["formatter_pass_count"],
        },
        "artifacts": {
            "question_pdf": pdf_summary(RELEASE_QUESTION_PDF),
            "solution_pdf": pdf_summary(RELEASE_SOLUTION_PDF),
            "learner_pack_pdf": pdf_summary(RELEASE_LEARNER_PACK_PDF),
            "release_authorization_pdf": pdf_summary(RELEASE_AUTHORIZATION_PDF),
        },
        "learner_copy_contract": {
            "independent_practice_disclaimer": True,
            "internal_audit_ids_removed": True,
            "review_only_markings_removed": True,
            "question_count": 65,
            "marks": 100,
            "duration_minutes": 180,
        },
        "gate_state": {
            "complete_paper_human_qa": "PASS_65_OF_65",
            "formatter_release_qualification": "PASS_65_OF_65",
            "learner_artifact_validation": "PENDING_INDEPENDENT_VALIDATOR",
            "exact_artifact_release_authorization": "PENDING",
            "release_authorized": False,
            "price_set": False,
            "storefront_activated": False,
            "sale_authorized": False,
        },
    }
    payload["candidate_content_sha256"] = content_sha256(payload, "candidate_content_sha256")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when committed candidate artifacts differ from a fresh render")
    args = parser.parse_args()
    manifest, handoff, completed, formatter = validate_upstream()
    outputs = (
        RELEASE_QUESTION_PDF, RELEASE_SOLUTION_PDF, RELEASE_LEARNER_PACK_PDF,
        RELEASE_AUTHORIZATION_PDF, RELEASE_CANDIDATE,
    )
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
    prior = {path: path.read_bytes() for path in outputs if path.is_file()} if args.check else {}
    staging = ROOT / "build/set01-release-candidate"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    old_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    os.environ["SOURCE_DATE_EPOCH"] = FIXED_SOURCE_DATE_EPOCH
    try:
        questions = handoff["paper"]["questions"]
        diagrams = convert_diagrams(questions, staging)
        run_pandoc(
            question_markdown(handoff, diagrams), RELEASE_QUESTION_PDF, staging,
            "question-paper-rc1", source_date_epoch=FIXED_SOURCE_DATE_EPOCH,
        )
        run_pandoc(
            solution_markdown(handoff, diagrams), RELEASE_SOLUTION_PDF, staging,
            "solutions-rc1", source_date_epoch=FIXED_SOURCE_DATE_EPOCH,
        )
        combine_pdfs(RELEASE_QUESTION_PDF, RELEASE_SOLUTION_PDF, RELEASE_LEARNER_PACK_PDF)
        hashes = {
            "question_pdf": sha256(RELEASE_QUESTION_PDF),
            "solution_pdf": sha256(RELEASE_SOLUTION_PDF),
            "learner_pack_pdf": sha256(RELEASE_LEARNER_PACK_PDF),
        }
        render_release_authorization(hashes, RELEASE_AUTHORIZATION_PDF)
        RELEASE_CANDIDATE.write_bytes(pretty_bytes(build_candidate(manifest, handoff, completed, formatter)))
    finally:
        if old_epoch is None:
            os.environ.pop("SOURCE_DATE_EPOCH", None)
        else:
            os.environ["SOURCE_DATE_EPOCH"] = old_epoch
        shutil.rmtree(staging, ignore_errors=True)

    if args.check:
        changed = [path for path in outputs if path not in prior or path.read_bytes() != prior[path]]
        if changed:
            print("GATE EE SET 01 RELEASE-CANDIDATE DETERMINISM: FAILED")
            for path in changed:
                print("-", relative(path))
            return 1
    print("GATE EE SET 01 RELEASE CANDIDATE RC1: RENDERED")
    print(f"Question PDF: {pdf_summary(RELEASE_QUESTION_PDF)['pages']} pages")
    print(f"Solution PDF: {pdf_summary(RELEASE_SOLUTION_PDF)['pages']} pages")
    print(f"Learner pack: {pdf_summary(RELEASE_LEARNER_PACK_PDF)['pages']} pages")
    print("Release authorization: PENDING; sale and storefront activation: BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
