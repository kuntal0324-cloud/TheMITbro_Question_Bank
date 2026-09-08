from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


FIELDS = (
    ("technical_correctness", "Technical correctness"),
    ("answer_correctness", "Answer correctness"),
    ("solution_correctness", "Solution correctness"),
    ("clarity_ambiguity", "Clarity / ambiguity"),
    ("originality_conflict_check", "Originality-conflict check"),
)


def box(selected: bool) -> str:
    return "☑" if selected else "☐"


def escape_table(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def initial_signoff(batch_id: str, source: Path, formatter: Path, questions: list[dict]) -> dict:
    label = batch_id.replace("_", " ").title()
    attestation = f"I independently reviewed the {label} questions, answers and solutions and approve only the question IDs marked PASS below."
    return {
        "signoff_contract": f"GATE_EE_{batch_id}_HUMAN_FINAL_QA_V1",
        "batch_id": batch_id,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "formatter_report_sha256": hashlib.sha256(formatter.read_bytes()).hexdigest(),
        "prerequisites": {
            "formatter": "20_PASS_0_REVIEW_0_INVALID",
            "independent_ai_recomputation": "20_PASS",
        },
        "reviewer": {
            "name": "",
            "role_or_qualification": "",
            "review_date": "",
            "attestation": "",
        },
        "required_attestation": attestation,
        "final_decision": "PENDING",
        "questions": [
            {
                "question_id": question["id"],
                "revision": question["revision"],
                "technical_correctness": "PENDING",
                "answer_correctness": "PENDING",
                "solution_correctness": "PENDING",
                "clarity_ambiguity": "PENDING",
                "originality_conflict_check": "PENDING",
                "decision": "PENDING",
                "notes": "",
            }
            for question in questions
        ],
    }


def render_packet(title: str, source: Path, formatter: Path, evidence: Path, signoff: dict) -> str:
    questions = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    qa = json.loads(evidence.read_text(encoding="utf-8"))
    qa_by_id = {row["question_id"]: row for row in qa["questions"]}
    signoff_by_id = {row["question_id"]: row for row in signoff["questions"]}
    formatter_payload = json.loads(formatter.read_text(encoding="utf-8"))
    reviewer = signoff["reviewer"]
    pending = signoff.get("final_decision") == "PENDING"

    lines = [
        f"# {title}", "",
        f"Canonical source SHA-256: `{hashlib.sha256(source.read_bytes()).hexdigest()}`",
        f"Strict Formatter report SHA-256: `{hashlib.sha256(formatter.read_bytes()).hexdigest()}`",
        f"Strict result: **{formatter_payload['formatter_pass_count']} PASS / {formatter_payload['formatter_review_count']} REVIEW / {formatter_payload['invalid_count']} invalid**",
        f"Independent AI recomputation: **{qa['technical_pass_count']}/20 PASS (not a human-review substitute)**",
        "Paper eligible: **0 — promotion remains blocked pending named human signoff**" if pending else "Human signoff has been recorded; rely on the certification validator for eligibility state.",
        "", "> **Editing note:** the `☐` and `☑` symbols in this Markdown packet are display-only. For Batch 002, use `output/pdf/GATE_EE_BATCH002_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf`, then import the saved form with `scripts/import_gate_ee_batch_002_human_qa_pdf.py`.",
        "", "## Reviewer identity and attestation", "",
        f"- Name: {reviewer.get('name') or '______________________________'}",
        f"- Role or qualification: {reviewer.get('role_or_qualification') or '______________________________'}",
        f"- Review date (YYYY-MM-DD): {reviewer.get('review_date') or '______________________________'}",
        f"- Required attestation: “{signoff['required_attestation']}”", "",
        "For every question, independently check the mathematics, declared answer, complete solution, clarity, and originality-conflict risk. Do not copy the AI result as the human decision.", "", "---", "",
    ]

    for question in questions:
        row = signoff_by_id[question["id"]]
        qa_row = qa_by_id[question["id"]]
        answer = ", ".join(question["answer"]) if isinstance(question["answer"], list) else question["answer"]
        lines.extend([
            f"## {question['id']} — revision {question['revision']}", "",
            f"**Route:** {question['subject']} → {question['topic']} → {question['subtopic']}",
            f"**Type / marks / difficulty:** {question['type']} / {question['marks']} / {question['difficulty']}", "",
            "### Question", "", question["stem"], "",
        ])
        if question.get("options"):
            lines.extend(["### Options", ""])
            for label, option in zip("ABCD", question["options"]):
                lines.append(f"- {label}. {option}")
            lines.append("")
        lines.extend([
            "### Declared answer", "", str(answer), "",
            "### Independent recomputation evidence", "", qa_row["derivation_summary"], "",
            "### Canonical solution", "", question["solution"], "",
            "### Human decision fields", "",
            "| Check | PASS | FAIL |",
            "|---|:---:|:---:|",
        ])
        for key, label in FIELDS:
            value = row.get(key)
            lines.append(f"| {label} | {box(value == 'PASS')} | {box(value == 'FAIL')} |")
        decision = row.get("decision")
        lines.extend([
            "",
            f"Decision: {box(decision == 'PASS')} PASS  {box(decision == 'REVISE')} REVISE  {box(decision == 'REJECT')} REJECT",
            f"Notes: {escape_table(row.get('notes')) or '______________________________'}",
            "", "---", "",
        ])
    lines.extend([
        "## Final certification procedure", "",
        "1. Enter reviewer identity, the exact attestation, all five checks, one decision and notes for every question in the companion human-final-QA JSON.",
        "2. Run the batch human-signoff validator.",
        "3. Promote only explicit PASS decisions after that validator succeeds.",
        "4. Re-run every repository validator before corpus admission or paper assembly.",
    ])
    return "\n".join(str(value) for value in lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or render a checksum-bound GATE EE human-review handoff.")
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--formatter", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--signoff", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--init-signoff", action="store_true")
    args = parser.parse_args()
    questions = [json.loads(line) for line in args.source.read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.init_signoff:
        payload = initial_signoff(args.batch_id, args.source, args.formatter, questions)
        args.signoff.parent.mkdir(parents=True, exist_ok=True)
        args.signoff.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    signoff = json.loads(args.signoff.read_text(encoding="utf-8"))
    args.packet.parent.mkdir(parents=True, exist_ok=True)
    args.packet.write_text(
        render_packet(args.title, args.source, args.formatter, args.evidence, signoff),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
