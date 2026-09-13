#!/usr/bin/env python3
"""Generate a XeLaTeX-rendered, mobile-fillable Batch 004/005 QA packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from gate_ee_recovery_batches import BATCHES, ROOT, get_batch, load_questions
from generate_gate_ee_batch_003_human_qa_pdf import (
    answer_text,
    ensure_widget_appearances,
    form_table,
    raw_tex,
    sha256,
)


def yaml_header(batch_id: str, domain: str) -> str:
    label = batch_id.replace("BATCH_", "Batch ")
    return f'''---
title: "GATE EE {label}"
subtitle: "Human Final QA - Mobile Fillable Review Packet"
date: ""
documentclass: article
papersize: a4
fontsize: 10pt
geometry:
  - top=12mm
  - bottom=14mm
  - left=13mm
  - right=13mm
mainfont: "DejaVu Sans"
sansfont: "DejaVu Sans"
monofont: "DejaVu Sans Mono"
mathfont: "Latin Modern Math"
colorlinks: true
header-includes:
  - |
    \\usepackage{{array,tabularx,xcolor,fancyhdr,graphicx}}
    \\definecolor{{themitblue}}{{HTML}}{{173B57}}
    \\pagestyle{{fancy}}
    \\fancyhf{{}}
    \\lhead{{TheMITbro - {label} Human Final QA}}
    \\rhead{{Reviewer copy}}
    \\cfoot{{\\thepage}}
    \\setlength{{\\headheight}}{{13pt}}
    \\setlength{{\\parindent}}{{0pt}}
    \\setlength{{\\parskip}}{{4pt}}
---
'''


def convert_diagrams(questions: list[dict], staging: Path) -> dict[str, Path]:
    rendered: dict[str, Path] = {}
    for question in questions:
        diagram = question.get("diagram")
        if not diagram:
            continue
        source = ROOT / diagram["asset"]
        target = staging / f"{question['id']}.png"
        completed = subprocess.run(
            [
                "inkscape", str(source), "--export-type=png",
                f"--export-filename={target}", "--export-width=1400",
            ],
            text=True,
            capture_output=True,
        )
        if completed.returncode or not target.is_file():
            raise RuntimeError(
                f"Diagram conversion failed for {question['id']}:\n"
                f"{completed.stdout}\n{completed.stderr}"
            )
        rendered[question["id"]] = target
    return rendered


def build_markdown(batch_id: str, questions: list[dict], evidence: dict[str, str], diagrams: dict[str, Path]) -> str:
    batch = get_batch(batch_id)
    if len(questions) != batch.expected_count or len(evidence) != batch.expected_count:
        raise RuntimeError(
            f"Expected {batch.expected_count} questions/evidence rows, found "
            f"{len(questions)}/{len(evidence)}"
        )
    label = batch_id.replace("BATCH_", "Batch ")
    body: list[str] = [yaml_header(batch_id, batch.domain)]
    body.append(
        raw_tex(
            "\n".join(
                [
                    r"\begin{Form}",
                    r"\begin{center}",
                    r"{\Large\bfseries\color{themitblue} Human reviewer record}\par",
                    r"\end{center}",
                    r"\vspace{2mm}",
                    r"\textbf{Name:}\quad \TextField[name=reviewer_name,width=0.68\linewidth,height=5mm]{}\par\vspace{2mm}",
                    r"\textbf{Role or qualification:}\quad \TextField[name=reviewer_qualification,width=0.55\linewidth,height=5mm]{}\par\vspace{2mm}",
                    r"\textbf{Review date (YYYY-MM-DD):}\quad \TextField[name=review_date,width=0.32\linewidth,height=5mm]{}\par\vspace{2mm}",
                    r"\textbf{Reviewer identifier (optional):}\quad \TextField[name=reviewer_identifier,width=0.48\linewidth,height=5mm]{}\par\vspace{2mm}",
                    r"\textbf{Type the attestation exactly as printed below:}\par",
                    r"\TextField[multiline=true,name=reviewer_attestation,width=\linewidth,height=16mm]{}\par\vspace{2mm}",
                ]
            )
        )
    )
    body.extend(
        [
            f"This packet contains {len(questions)} checksum-bound {label} {batch.domain} questions. Mathematical expressions are canonical LaTeX; declared SVG diagrams are checksum-bound and rendered below their stems.",
            "",
            f"Canonical source SHA-256: `{sha256(batch.source)}`",
            "",
            f"Strict Formatter report SHA-256: `{sha256(batch.formatter_evidence)}`",
            "",
            f"Automated prerequisite: **{len(questions)} PASS / 0 REVIEW / 0 invalid**. This does not replace your human judgment.",
            "",
            "## Required procedure",
            "",
            "1. Solve each question independently before relying on the declared answer.",
            "2. Inspect every displayed diagram and all labels when a figure is present.",
            "3. Select exactly one of PASS or FAIL for each of the five checks.",
            "4. Select exactly one final decision: PASS, REVISE, or REJECT.",
            "5. Explain every REVISE or REJECT decision in Notes.",
            "6. Save this filled PDF and return it for checksum-bound import and validation.",
            "",
            f"**Required attestation:** {batch.attestation}",
            "",
            "State your actual background accurately in the qualification field; do not invent a title or credential.",
        ]
    )

    for index, question in enumerate(questions, 1):
        prefix = f"q{index:03d}"
        body.extend(
            [
                raw_tex(r"\clearpage"),
                f"# {question['id']} - revision {question['revision']}",
                "",
                f"**Question {index} of {len(questions)}**  ",
                f"**Route:** {question['subject']} -> {question['topic']} -> {question['subtopic']}  ",
                f"**Type / marks / difficulty:** {question['type']} / {question['marks']} / {question['difficulty']}",
                "",
                "## Question",
                "",
                question["stem"],
                "",
            ]
        )
        diagram = question.get("diagram")
        if diagram:
            image_path = diagrams[question["id"]]
            body.extend(
                [
                    raw_tex(
                        "\n".join(
                            [
                                r"\begin{center}",
                                rf"\includegraphics[width=0.60\linewidth,height=30mm,keepaspectratio]{{{image_path.as_posix()}}}",
                                r"\end{center}",
                            ]
                        )
                    ),
                    "",
                    f"**Figure:** {diagram['caption']}  ",
                    f"*Diagram description:* {diagram['alt_text']}",
                    "",
                ]
            )
        options = question.get("options") or []
        if options:
            body.extend(["## Options", ""])
            body.extend(f"- {chr(65 + option_index)}. {option}" for option_index, option in enumerate(options))
            body.append("")
        body.extend(
            [
                "## Verification reference",
                "",
                "**Declared answer:** " + answer_text(question["answer"]),
                "",
                "**Independent recomputation evidence:** " + evidence[question["id"]],
                "",
                "**Canonical solution:**",
                "",
                question["solution"],
                "",
                "## Human decision",
                "",
                "Select exactly one box in each row. PASS for the item is valid only when all five checks are PASS.",
                "",
                raw_tex(form_table(prefix, notes_height_mm=10 if diagram else 18)),
            ]
        )

    body.extend(
        [
            raw_tex(r"\clearpage"),
            "# Review completion",
            "",
            f"Complete this page only after reviewing all {len(questions)} questions.",
            "",
            raw_tex(
                "\n".join(
                    [
                        r"\textbf{Final reviewed-results decision:}\quad APPROVE REVIEWED RESULTS\,\CheckBox[name=final_approve_reviewed_results,width=4mm,height=4mm]{}",
                        r"\par\vspace{5mm}",
                        r"\textbf{Reviewer typed signature:}\quad \TextField[name=reviewer_signature,width=0.55\linewidth,height=5mm]{}",
                        r"\par\vspace{4mm}",
                        r"\textbf{Final comments:}\par",
                        r"\TextField[multiline=true,name=final_comments,width=\linewidth,height=35mm]{}",
                        r"\par\vfill",
                        r"\textit{Paper eligibility remains blocked until this completed record is validated and only explicitly approved IDs are promoted.}",
                        r"\end{Form}",
                    ]
                )
            ),
        ]
    )
    return "\n".join(body) + "\n"


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True, choices=sorted(BATCHES))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    batch = get_batch(args.batch)
    output = args.output or batch.pdf
    output.parent.mkdir(parents=True, exist_ok=True)

    questions = load_questions(batch)
    qa = json.loads(batch.independent_qa.read_text(encoding="utf-8"))
    evidence = {row["question_id"]: row["derivation_summary"] for row in qa.get("questions", [])}

    with tempfile.TemporaryDirectory(prefix=f"themitbro-{batch.number}-human-qa-") as temp_dir:
        staging = Path(temp_dir)
        diagrams = convert_diagrams(questions, staging)
        markdown_path = staging / f"{batch.batch_id}_HUMAN_FINAL_QA_MOBILE.md"
        markdown_path.write_text(build_markdown(batch.batch_id, questions, evidence, diagrams), encoding="utf-8")
        command = [
            "pandoc", str(markdown_path), "--from=markdown+raw_tex+link_attributes",
            "--pdf-engine=xelatex", "--metadata=linkcolor:themitblue",
            "--output", str(output.resolve()),
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        if completed.returncode:
            raise RuntimeError(f"Pandoc failed:\n{completed.stdout}\n{completed.stderr}")
        if not output.is_file() or output.stat().st_size < 10_000:
            raise RuntimeError("PDF output is missing or unexpectedly small")
        ensure_widget_appearances(output.resolve())
    print(f"Wrote {output}")


if __name__ == "__main__":
    run()
