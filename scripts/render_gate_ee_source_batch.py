from __future__ import annotations

import argparse
import json
from pathlib import Path


def render_question(question: dict) -> str:
    answer = question["answer"]
    if isinstance(answer, list):
        answer = ", ".join(answer)

    lines = [
        f"## {question['id']} — revision {question['revision']}",
        "",
        f"**Route:** {question['subject']} → {question['topic']} → {question['subtopic']}",
        f"**Type / marks / difficulty:** {question['type']} / {question['marks']} / {question['difficulty']}",
        f"**Family:** `{question['family_id']}`",
        "",
        "### Question",
        "",
        question["stem"],
        "",
    ]
    if question.get("options"):
        lines.extend(["### Options", ""])
        for label, value in zip("ABCD", question["options"]):
            lines.append(f"- {label}. {value}")
        lines.append("")
    lines.extend([
        "### Declared answer",
        "",
        str(answer),
        "",
        "### Canonical solution",
        "",
        question["solution"],
        "",
        "### Review state",
        "",
        "Technical, answer, solution, originality, duplicate-family and Formatter checks are pending unless superseded by a checksum-bound qualification artifact.",
        "",
        "---",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a deterministic GATE EE source-batch review document.")
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    questions = [
        json.loads(line)
        for line in args.jsonl.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    body = [
        f"# {args.title}",
        "",
        "**Status:** DRAFT — NOT PAPER-ELIGIBLE",
        f"**Questions:** {len(questions)}",
        "",
        "This is a deterministic view of the canonical JSONL source. Review decisions belong in checksum-bound review artifacts, not in this generated document.",
        "",
        "---",
        "",
    ]
    body.extend(render_question(question) for question in questions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
