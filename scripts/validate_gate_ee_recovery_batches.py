#!/usr/bin/env python3
"""Validate the checksum-bound, pre-human lifecycle for Batches 004 and 005."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from gate_ee_recovery_batches import BATCHES, ORACLE, BASE, RecoveryBatch, load_questions


REQUIRED = {
    "id", "exam", "subject", "topic", "subtopic", "concept", "difficulty",
    "type", "marks", "estimated_time_seconds", "stem", "answer", "solution",
    "family_id", "revision", "status", "provenance", "review", "diagram",
}
CHECK_FIELDS = (
    "technical_correctness", "answer_correctness", "solution_correctness",
    "clarity_ambiguity", "originality_conflict_check",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_answer(question: dict, errors: list[str]) -> None:
    qid = question.get("id", "?")
    qtype = question.get("type")
    answer = question.get("answer")
    options = question.get("options")
    if qtype == "MCQ":
        if not isinstance(options, list) or len(options) != 4:
            errors.append(f"{qid}: MCQ requires four options")
        if answer not in {"A", "B", "C", "D"}:
            errors.append(f"{qid}: invalid MCQ answer")
    elif qtype == "MSQ":
        if not isinstance(options, list) or len(options) != 4:
            errors.append(f"{qid}: MSQ requires four options")
        if not isinstance(answer, list) or not answer or len(answer) != len(set(answer)) or any(x not in "ABCD" for x in answer):
            errors.append(f"{qid}: invalid MSQ answer")
    elif qtype == "NAT":
        if "options" in question:
            errors.append(f"{qid}: NAT must not contain options")
        if not isinstance(answer, (int, float)):
            errors.append(f"{qid}: NAT answer must be numeric")
        if not isinstance(question.get("nat_tolerance"), (int, float)) or question.get("nat_tolerance", -1) < 0:
            errors.append(f"{qid}: NAT tolerance is missing or invalid")

    marker = ", ".join(answer) if isinstance(answer, list) else str(answer)
    found = re.findall(r"(?m)^Final answer:\s*([^\n]+)$", str(question.get("solution", "")))
    if found != [marker]:
        errors.append(f"{qid}: final-answer marker mismatch")
    for value in [question.get("stem", ""), question.get("solution", ""), *(question.get("options") or [])]:
        parts = re.split(r"(?<!\\)\$", str(value))
        if len(parts) % 2 == 0:
            errors.append(f"{qid}: unbalanced inline-math delimiter")
            continue
        if any(any(control in segment for control in ("\n", "\r", "\t")) for segment in parts[1::2]):
            errors.append(f"{qid}: control character inside inline math")


def validate_batch(batch: RecoveryBatch, admitted_families: set[str]) -> list[str]:
    errors: list[str] = []
    questions = load_questions(batch)
    source_sha = sha256(batch.source)
    manifest = load(batch.manifest)
    handoff = load(batch.handoff)
    family_file = load(batch.families)
    formatter = load(batch.formatter_evidence)
    independent = load(batch.independent_qa)
    summary = load(batch.summary)
    candidate = load(batch.candidate)
    human = load(batch.human_qa)

    ids: list[str] = []
    families: list[str] = []
    diagrams: list[dict] = []
    for index, question in enumerate(questions, 1):
        qid = str(question.get("id", "?"))
        ids.append(qid)
        families.append(str(question.get("family_id", "")))
        missing = REQUIRED - question.keys()
        if missing:
            errors.append(f"{qid}: missing fields {sorted(missing)}")
        expected_id = f"TMB-GATE-EE-{batch.code}-{index:03d}"
        if qid != expected_id:
            errors.append(f"{qid}: expected ID {expected_id}")
        if question.get("exam") != "GATE_EE" or question.get("subject") != "Electrical Engineering":
            errors.append(f"{qid}: incorrect exam/subject route")
        if question.get("topic") != batch.domain or question.get("subtopic") not in batch.allowed_subtopics:
            errors.append(f"{qid}: out-of-scope topic/subtopic")
        if question.get("difficulty") not in {"Easy", "Medium", "Hard"}:
            errors.append(f"{qid}: invalid difficulty")
        if question.get("type") not in {"MCQ", "MSQ", "NAT"} or question.get("marks") not in {1, 2}:
            errors.append(f"{qid}: invalid type/marks")
        if question.get("status") != "DRAFT" or question.get("revision") != 1:
            errors.append(f"{qid}: source must remain DRAFT revision 1")
        if question.get("provenance", {}).get("originality") != "ORIGINAL_THEMITBRO":
            errors.append(f"{qid}: originality provenance missing")
        validate_answer(question, errors)
        if question.get("answer") != ORACLE.get(qid, (None, ""))[0]:
            errors.append(f"{qid}: independent oracle mismatch")

        diagram = question.get("diagram")
        if diagram:
            diagrams.append(diagram)
            # Asset references are repository-relative; BASE.parents[1] is the
            # Question Bank repository root.
            asset = BASE.parents[1] / str(diagram.get("asset", ""))
            if not asset.is_file():
                errors.append(f"{qid}: declared diagram asset is missing")
            else:
                try:
                    ET.parse(asset)
                except ET.ParseError as exc:
                    errors.append(f"{qid}: invalid SVG: {exc}")
            if not str(diagram.get("alt_text", "")).strip() or not str(diagram.get("caption", "")).strip():
                errors.append(f"{qid}: diagram alt text/caption is missing")

    if len(questions) != batch.expected_count:
        errors.append(f"expected {batch.expected_count} questions, found {len(questions)}")
    if len(ids) != len(set(ids)) or len(families) != len(set(families)):
        errors.append("question IDs and families must be unique inside the batch")
    collision = admitted_families.intersection(families)
    if collision:
        errors.append(f"pending families collide with admitted registry: {sorted(collision)}")
    if Counter(q["marks"] for q in questions) != Counter({1: batch.expected_one_mark, 2: batch.expected_two_mark}):
        errors.append("one-mark/two-mark composition mismatch")
    if len(diagrams) != batch.expected_visual:
        errors.append("visual-question count mismatch")

    expected_counts = {
        "type_counts": dict(Counter(str(q["type"]) for q in questions)),
        "marks_counts": dict(Counter(str(q["marks"]) for q in questions)),
        "difficulty_counts": dict(Counter(str(q["difficulty"]) for q in questions)),
        "topic_counts": dict(Counter(str(q["topic"]) for q in questions)),
        "subtopics": dict(Counter(str(q["subtopic"]) for q in questions)),
    }
    for key, expected in expected_counts.items():
        if manifest.get(key) != expected:
            errors.append(f"manifest {key} mismatch")
    if manifest.get("jsonl_sha256") != source_sha or manifest.get("question_count") != len(questions):
        errors.append("manifest source checksum/count mismatch")
    if manifest.get("status") != "READY_FOR_HUMAN_FINAL_QA" or manifest.get("paper_eligible_count") != 0:
        errors.append("manifest lifecycle state is not safely pre-human")
    if manifest.get("formatter_evidence_sha256") != sha256(batch.formatter_evidence):
        errors.append("manifest Formatter evidence checksum mismatch")
    if manifest.get("independent_ai_qa_sha256") != sha256(batch.independent_qa):
        errors.append("manifest independent-QA checksum mismatch")

    if handoff.get("source_sha256") != source_sha or handoff.get("question_count") != len(questions):
        errors.append("Formatter handoff checksum/count mismatch")
    expected_assets = {
        row["question_id"]: (row["path"], row["sha256"])
        for row in handoff.get("diagram_assets", [])
    }
    for question in questions:
        if not question.get("diagram"):
            continue
        asset_ref = question["diagram"]["asset"]
        asset = BASE.parents[1] / asset_ref
        if expected_assets.get(question["id"]) != (asset_ref, sha256(asset)):
            errors.append(f"{question['id']}: handoff diagram evidence mismatch")

    family_map = {row.get("family_id"): row.get("question_ids") for row in family_file.get("families", [])}
    if set(family_map) != set(families):
        errors.append("batch family registry does not match source")
    for question in questions:
        if family_map.get(question["family_id"]) != [question["id"]]:
            errors.append(f"{question['id']}: family mapping mismatch")
    if family_file.get("admission_status") != "NOT_ADMITTED_PENDING_HUMAN_FINAL_QA":
        errors.append("pending family file has an unsafe admission state")

    strict_tuple = (
        formatter.get("status"), formatter.get("source_sha256"),
        formatter.get("question_count"), formatter.get("formatter_pass_count"),
        formatter.get("formatter_review_count"), formatter.get("invalid_count"),
        formatter.get("paper_eligible_count"), formatter.get("release_gate"),
    )
    expected_strict = ("PASS", source_sha, len(questions), len(questions), 0, 0, 0, "BLOCKED")
    if strict_tuple != expected_strict:
        errors.append("strict Formatter evidence is incomplete or unsafe")
    formatter_rows = {row.get("question_id"): row for row in formatter.get("questions", [])}
    if set(formatter_rows) != set(ids):
        errors.append("Formatter evidence IDs mismatch")
    for qid, row in formatter_rows.items():
        if row.get("formatter_qualification") != "PASS" or row.get("syllabus_match") is not True:
            errors.append(f"{qid}: Formatter row is not a strict PASS")
        if row.get("classification", {}).get("topic") != batch.domain:
            errors.append(f"{qid}: Formatter route mismatch")
        if row.get("diagram_contract", {}).get("declared") and row.get("diagram_contract", {}).get("status") != "PASS":
            errors.append(f"{qid}: Formatter diagram contract failed")

    if (
        independent.get("status"), independent.get("source_sha256"),
        independent.get("formatter_report_sha256"), independent.get("technical_pass_count"),
        independent.get("answer_recomputed_pass_count"), independent.get("human_review_substitute"),
        independent.get("paper_eligible_count"), independent.get("release_gate"),
    ) != (
        "PASS", source_sha, sha256(batch.formatter_evidence), len(questions),
        len(questions), False, 0, "BLOCKED_PENDING_HUMAN_FINAL_QA",
    ):
        errors.append("independent-QA evidence is incomplete or unsafe")
    independent_rows = {row.get("question_id"): row for row in independent.get("questions", [])}
    if set(independent_rows) != set(ids):
        errors.append("independent-QA IDs mismatch")
    for question in questions:
        row = independent_rows.get(question["id"], {})
        if row.get("recomputed_answer") != question["answer"]:
            errors.append(f"{question['id']}: committed recomputation mismatch")

    if summary.get("current_stage") != "READY_FOR_HUMAN_FINAL_QA" or summary.get("paper_eligible_count") != 0:
        errors.append("qualification summary lifecycle mismatch")
    if candidate.get("candidate_question_ids") != ids or candidate.get("paper_eligible_count") != 0:
        errors.append("paper-eligibility candidate artifact mismatch")
    if human.get("final_decision") != "PENDING" or human.get("required_attestation") != batch.attestation:
        errors.append("human-QA template is not clean and pending")
    reviewer = human.get("reviewer", {})
    if any(str(reviewer.get(k, "")).strip() for k in ("name", "role_or_qualification", "review_date", "attestation")):
        errors.append("pending human-QA template contains reviewer data")
    human_rows = human.get("questions", [])
    if [row.get("question_id") for row in human_rows] != ids:
        errors.append("human-QA template IDs mismatch")
    for row in human_rows:
        if row.get("decision") != "PENDING" or any(row.get(field) != "PENDING" for field in CHECK_FIELDS):
            errors.append(f"{row.get('question_id', '?')}: human-QA template contains a premature decision")

    markdown = batch.markdown.read_text(encoding="utf-8")
    if any(markdown.count(qid) != 1 for qid in ids):
        errors.append("deterministic Markdown view does not contain every ID exactly once")
    return errors


def main() -> int:
    global_registry = load(BASE / "families/FAMILY_REGISTRY.json")
    admitted_families = {row.get("family_id") for row in global_registry.get("families", [])}
    errors: list[str] = []
    for batch in BATCHES.values():
        errors.extend(f"{batch.batch_id}: {error}" for error in validate_batch(batch, admitted_families))

    questions = [q for batch in BATCHES.values() for q in load_questions(batch)]
    if len(questions) != 27 or Counter(q["marks"] for q in questions) != Counter({1: 14, 2: 13}):
        errors.append("combined recovery contract must be 27 questions: 14 one-mark and 13 two-mark")
    if sum(q["marks"] for q in questions) != 40:
        errors.append("combined recovery contract must provide exactly 40 marks")
    if errors:
        print("GATE EE CORE-EE RECOVERY VALIDATION: FAILED")
        for error in errors:
            print("-", error)
        return 1
    print("GATE EE CORE-EE RECOVERY VALIDATION: PASSED")
    print("Batch 004: 15 Formatter PASS / 0 REVIEW / 0 invalid")
    print("Batch 005: 12 Formatter PASS / 0 REVIEW / 0 invalid")
    print("Combined: 27 candidates / 40 marks / 6 checksum-bound SVGs")
    print("Paper-eligible: 0 | human final QA: PENDING | release gate: BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
