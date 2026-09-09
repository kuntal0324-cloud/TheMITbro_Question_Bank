#!/usr/bin/env python3
"""Build the XeLaTeX-rendered, fillable Batch 002 human final-QA packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
)


CHECKS = (
    ("technical", "Technical correctness"),
    ("answer", "Answer correctness"),
    ("solution", "Solution correctness"),
    ("clarity", "Clarity / ambiguity"),
    ("originality", "Originality-conflict check"),
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
FORMATTER = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_FORMATTER_FINAL_EVIDENCE.json"
INDEPENDENT_QA = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_INDEPENDENT_AI_QA.json"
DEFAULT_OUTPUT = ROOT / "output/pdf/GATE_EE_BATCH002_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf"
REQUIRED_ATTESTATION = (
    "I independently reviewed the Batch 002 questions, answers and solutions "
    "and approve only the question IDs marked PASS below."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def answer_text(answer: object) -> str:
    if isinstance(answer, list):
        return ", ".join(str(item) for item in answer)
    return str(answer)


def raw_tex(text: str) -> str:
    """Wrap trusted LaTeX form/layout fragments for Pandoc passthrough."""
    return f"```{{=latex}}\n{text}\n```"


def form_table(prefix: str) -> str:
    rows = []
    for short, label in CHECKS:
        rows.append(
            rf"{label} & \CheckBox[name={prefix}_{short}_pass,width=4mm,height=4mm,bordercolor={{0.15 0.35 0.55}}]{{}}"
            rf" & \CheckBox[name={prefix}_{short}_fail,width=4mm,height=4mm,bordercolor={{0.65 0.15 0.15}}]{{}} \\ \hline"
        )
    return "\n".join(
        [
            r"\renewcommand{\arraystretch}{1.35}",
            r"\begin{tabularx}{\linewidth}{|>{\raggedright\arraybackslash}X|c|c|}",
            r"\hline",
            r"\textbf{Check} & \textbf{PASS} & \textbf{FAIL} \\ \hline",
            *rows,
            r"\end{tabularx}",
            r"\vspace{2mm}",
            rf"\textbf{{Decision (select exactly one):}}\quad PASS\,\CheckBox[name={prefix}_decision_pass,width=4mm,height=4mm]{{}}",
            rf"\quad REVISE\,\CheckBox[name={prefix}_decision_revise,width=4mm,height=4mm]{{}}",
            rf"\quad REJECT\,\CheckBox[name={prefix}_decision_reject,width=4mm,height=4mm]{{}}",
            r"\par\vspace{2mm}\textbf{Notes / independent calculation summary:}\par",
            rf"\TextField[multiline=true,name={prefix}_notes,width=\linewidth,height=18mm,bordercolor={{0.35 0.35 0.35}}]{{}}",
        ]
    )


def build_markdown(questions: list[dict], evidence: dict[str, str]) -> str:
    if len(questions) != 20 or len(evidence) != 20:
        raise RuntimeError(f"Expected 20 questions and evidence rows, found {len(questions)} and {len(evidence)}")

    yaml = r"""---
title: "GATE EE Batch 002"
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
    \usepackage{array,tabularx,xcolor,fancyhdr}
    \definecolor{themitblue}{HTML}{173B57}
    \definecolor{themitlight}{HTML}{EAF2F7}
    \pagestyle{fancy}
    \fancyhf{}
    \lhead{TheMITbro - Batch 002 Human Final QA}
    \rhead{Reviewer copy}
    \cfoot{\thepage}
    \setlength{\headheight}{13pt}
    \setlength{\parindent}{0pt}
    \setlength{\parskip}{4pt}
---
"""
    body: list[str] = [yaml]
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
            "This packet contains 20 checksum-bound Batch 002 Electric Circuits questions. Revision 2 replaces the rejected ASCII-style formulas with canonical LaTeX and renders them through XeLaTeX.",
            "",
            f"Canonical source SHA-256: `{sha256(SOURCE)}`",
            "",
            f"Strict Formatter report SHA-256: `{sha256(FORMATTER)}`",
            "",
            "Automated prerequisite: **20 PASS / 0 REVIEW / 0 invalid**. This does not replace your human judgment.",
            "",
            "## Required procedure",
            "",
            "1. For each item, solve the question independently before relying on the declared answer.",
            "2. Select exactly one of PASS or FAIL for each of the five checks.",
            "3. Select exactly one final decision: PASS, REVISE, or REJECT.",
            "4. Explain every REVISE or REJECT decision in Notes.",
            "5. Save this filled PDF and return it for conversion into the checksum-bound certification JSON.",
            "",
            f"**Required attestation:** {REQUIRED_ATTESTATION}",
            "",
            "For the qualification field, state your actual background accurately; no diploma or job title is required unless it is genuinely yours.",
        ]
    )

    for index, q in enumerate(questions, start=1):
        prefix = f"q{index:03d}"
        body.extend(
            [
                raw_tex(r"\clearpage"),
                f"# {q['id']} - revision {q['revision']}",
                "",
                f"**Question {index} of {len(questions)}**  ",
                f"**Route:** {q['subject']} -> {q['topic']} -> {q['subtopic']}  ",
                f"**Type / marks / difficulty:** {q['type']} / {q['marks']} / {q['difficulty']}",
                "",
                "## Question",
                "",
                q["stem"],
                "",
            ]
        )
        options = q.get("options") or []
        if options:
            body.extend(["## Options", ""])
            for option_index, option in enumerate(options):
                body.append(f"- {chr(65 + option_index)}. {option}")
            body.append("")
        body.extend(
            [
                "## Verification reference",
                "",
                "**Declared answer:** " + answer_text(q["answer"]),
                "",
                "**Independent recomputation evidence:** " + evidence[q["id"]],
                "",
                "**Canonical solution:**",
                "",
                q["solution"],
                "",
                "## Human decision",
                "",
                "Select exactly one box in each row. PASS for the item is valid only when all five checks are PASS.",
                "",
                raw_tex(form_table(prefix)),
            ]
        )

    body.extend(
        [
            raw_tex(r"\clearpage"),
            "# Review completion",
            "",
            "Complete this page only after reviewing all 20 questions.",
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
                        r"\textit{Paper eligibility remains blocked until the completed human record is validated and only explicitly approved IDs are promoted.}",
                        r"\end{Form}",
                    ]
                )
            ),
        ]
    )
    return "\n".join(body) + "\n"


def _appearance_stream(width: float, height: float, content: str) -> DecodedStreamObject:
    stream = DecodedStreamObject()
    stream.set_data(content.encode("ascii"))
    stream[NameObject("/Type")] = NameObject("/XObject")
    stream[NameObject("/Subtype")] = NameObject("/Form")
    stream[NameObject("/FormType")] = FloatObject(1)
    stream[NameObject("/BBox")] = ArrayObject(
        [FloatObject(0), FloatObject(0), FloatObject(width), FloatObject(height)]
    )
    stream[NameObject("/Resources")] = DictionaryObject()
    return stream


def ensure_widget_appearances(pdf_path: Path) -> None:
    """Supply explicit blank and checked appearances for reliable mobile rendering."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    for page in writer.pages:
        for annotation_ref in page.get("/Annots", []):
            widget = annotation_ref.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            rect = [float(value) for value in widget["/Rect"]]
            width = max(rect[2] - rect[0], 1.0)
            height = max(rect[3] - rect[1], 1.0)
            field_type = widget.get("/FT")
            if field_type == "/Btn":
                mk = widget.get("/MK", {})
                border = [float(v) for v in mk.get("/BC", [0.2, 0.2, 0.2])]
                while len(border) < 3:
                    border.append(border[-1] if border else 0.2)
                r, g, b = border[:3]
                base = (
                    f"q 1 1 1 rg 0 0 {width:.3f} {height:.3f} re f "
                    f"{r:.3f} {g:.3f} {b:.3f} RG 0.9 w "
                    f"0.45 0.45 {max(width - 0.9, 0.1):.3f} {max(height - 0.9, 0.1):.3f} re S"
                )
                off_stream = _appearance_stream(width, height, base + " Q")
                yes_stream = _appearance_stream(
                    width,
                    height,
                    base
                    + f" 0.05 0.40 0.16 RG 1.5 w "
                    + f"{0.20 * width:.3f} {0.52 * height:.3f} m "
                    + f"{0.43 * width:.3f} {0.27 * height:.3f} l "
                    + f"{0.82 * width:.3f} {0.78 * height:.3f} l S Q",
                )
                widget[NameObject("/AP")] = DictionaryObject(
                    {
                        NameObject("/N"): DictionaryObject(
                            {
                                NameObject("/Off"): writer._add_object(off_stream),
                                NameObject("/Yes"): writer._add_object(yes_stream),
                            }
                        )
                    }
                )
                widget[NameObject("/AS")] = NameObject("/Off")
                widget[NameObject("/V")] = NameObject("/Off")
            elif field_type == "/Tx":
                blank_stream = _appearance_stream(
                    width,
                    height,
                    f"q 1 1 1 rg 0 0 {width:.3f} {height:.3f} re f "
                    f"0.45 0.45 0.45 RG 0.7 w "
                    f"0.35 0.35 {max(width - 0.7, 0.1):.3f} {max(height - 0.7, 0.1):.3f} re S Q",
                )
                widget[NameObject("/AP")] = DictionaryObject(
                    {NameObject("/N"): writer._add_object(blank_stream)}
                )

    acroform = writer.root_object.get("/AcroForm")
    if acroform:
        acroform.get_object()[NameObject("/NeedAppearances")] = BooleanObject(False)

    repaired = pdf_path.with_suffix(".appearance-ready.pdf")
    with repaired.open("wb") as stream:
        writer.write(stream)
    repaired.replace(pdf_path)


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, nargs="?", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    questions = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip()]
    qa = json.loads(INDEPENDENT_QA.read_text(encoding="utf-8"))
    evidence = {row["question_id"]: row["derivation_summary"] for row in qa.get("questions", [])}

    with tempfile.TemporaryDirectory(prefix="themitbro-human-qa-") as temp_dir:
        staging = Path(temp_dir)
        markdown_path = staging / "BATCH_002_HUMAN_FINAL_QA_MOBILE.md"
        markdown_path.write_text(build_markdown(questions, evidence), encoding="utf-8")
        command = [
            "pandoc",
            str(markdown_path),
            "--from=markdown+raw_tex",
            "--pdf-engine=xelatex",
            "--metadata=linkcolor:themitblue",
            "--output",
            str(args.output.resolve()),
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        if completed.returncode:
            raise RuntimeError(f"Pandoc failed:\n{completed.stdout}\n{completed.stderr}")
        if not args.output.exists() or args.output.stat().st_size < 10_000:
            raise RuntimeError("PDF output is missing or unexpectedly small")
        ensure_widget_appearances(args.output.resolve())


if __name__ == "__main__":
    run()
