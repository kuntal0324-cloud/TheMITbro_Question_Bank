#!/usr/bin/env python3
"""Build deterministic pre-human artifacts for Batches 004 and 005."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from gate_ee_recovery_batches import BATCHES, ORACLE, ROOT, RecoveryBatch, get_batch, load_questions


BUILD_DATE = "2026-09-12"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def expected_marker(answer: Any) -> str:
    return ", ".join(answer) if isinstance(answer, list) else str(answer)


def build_static(batch: RecoveryBatch, questions: list[dict[str, Any]]) -> tuple[str, list[dict[str, str]]]:
    source_sha = sha256(batch.source)
    diagram_assets: list[dict[str, str]] = []
    for question in questions:
        diagram = question.get("diagram")
        if not diagram:
            continue
        asset = ROOT / diagram["asset"]
        diagram_assets.append({
            "question_id": question["id"],
            "path": diagram["asset"],
            "sha256": sha256(asset),
        })

    write_json(batch.families, {
        "registry_version": "1.2.0",
        "batch": batch.batch_id,
        "corpus": "GATE_EE_CORPUS_V1",
        "admission_status": "NOT_ADMITTED_PENDING_HUMAN_FINAL_QA",
        "families": [
            {"family_id": question["family_id"], "question_ids": [question["id"]]}
            for question in questions
        ],
    })
    write_json(batch.handoff, {
        "handoff_version": "1.0.0",
        "handoff_id": f"GATE_EE_{batch.batch_id}_TO_FORMATTER_V2",
        "source_repository": "TheMITbro_Question_Bank",
        "target_repository": "TheMITBro_Formatter",
        "formatter_required_version": "2.0.0",
        "batch_id": batch.batch_id,
        "corpus": "GATE_EE_CORPUS_V1",
        "domain": batch.domain,
        "question_count": len(questions),
        "source_jsonl": f"GATE_EE/corpus_v1/source_batches/{batch.source.name}",
        "source_markdown": f"GATE_EE/corpus_v1/source_batches/{batch.markdown.name}",
        "source_sha256": source_sha,
        "official_scope_reference": "references/GATE_2027/GATE_2027_EE_SYLLABUS.json",
        "required_formatter_checks": [
            "schema/ingestion compatibility",
            "question intelligence classification",
            "answer/solution structural validation",
            "duplicate/family detection",
            "quality scoring",
            "canonical LaTeX mathematics source contract",
            "declared-diagram and visual-reference consistency",
            "professional rendering smoke test",
            "mobile human-review PDF rendering",
        ],
        "math_render_contract": {
            "canonical_source": "LaTeX math delimited with $...$",
            "pdf_engine": "Pandoc + XeLaTeX",
            "math_font": "Latin Modern Math",
            "ascii_formula_fallback_allowed": False,
        },
        "diagram_assets": diagram_assets,
        "promotion_rule": "Formatter PASS and independent technical recomputation are machine evidence only. Named human final QA is required before PAPER_ELIGIBLE promotion.",
        "release_gate": "BLOCKED",
    })
    return source_sha, diagram_assets


def build_machine_qualified(
    batch: RecoveryBatch,
    questions: list[dict[str, Any]],
    source_sha: str,
    diagram_assets: list[dict[str, str]],
) -> None:
    formatter = json.loads(batch.formatter_evidence.read_text(encoding="utf-8"))
    formatter_sha = sha256(batch.formatter_evidence)
    strict = (
        formatter.get("status") == "PASS"
        and formatter.get("source_sha256") == source_sha
        and formatter.get("question_count") == len(questions)
        and formatter.get("formatter_pass_count") == len(questions)
        and formatter.get("formatter_review_count") == 0
        and formatter.get("invalid_count") == 0
    )
    if not strict:
        raise ValueError(f"{batch.batch_id}: strict Formatter evidence is not complete")

    rows: list[dict[str, Any]] = []
    for question in questions:
        qid = question["id"]
        if qid not in ORACLE:
            raise ValueError(f"{qid}: independent oracle is missing")
        recomputed, derivation = ORACLE[qid]
        if recomputed != question["answer"]:
            raise ValueError(f"{qid}: independent oracle disagrees with the declared answer")
        markers = re.findall(r"(?m)^Final answer:\s*([^\n]+)$", question["solution"])
        if markers != [expected_marker(question["answer"])]:
            raise ValueError(f"{qid}: solution final-answer marker mismatch")
        rows.append({
            "question_id": qid,
            "revision": question["revision"],
            "declared_answer": question["answer"],
            "recomputed_answer": recomputed,
            "technical_result": "PASS",
            "answer_result": "PASS",
            "solution_consistency_result": "PASS",
            "machine_final_marker_result": "PASS",
            "derivation_summary": derivation,
            "human_originality_check": "PENDING",
        })

    independent = {
        "qa_contract": f"GATE_EE_{batch.batch_id.replace('_', '')}_INDEPENDENT_AI_QA_V1",
        "batch_id": batch.batch_id,
        "status": "PASS",
        "qa_date": BUILD_DATE,
        "performed_by": "OpenAI Codex",
        "reviewer_kind": "AI_ASSISTED_INDEPENDENT_RECOMPUTATION",
        "source_sha256": source_sha,
        "formatter_report_sha256": formatter_sha,
        "evidence_valid_for_current_source": True,
        "technical_pass_count": len(questions),
        "answer_recomputed_pass_count": len(questions),
        "solution_consistency_pass_count": len(questions),
        "machine_final_marker_pass_count": len(questions),
        "formatter_pass_count": len(questions),
        "formatter_review_count": 0,
        "invalid_count": 0,
        "paper_eligibility_candidate_count": len(questions),
        "paper_eligible_count": 0,
        "human_final_qa_required": True,
        "human_review_substitute": False,
        "automated_oracle": "scripts/gate_ee_recovery_batches.py",
        "release_gate": "BLOCKED_PENDING_HUMAN_FINAL_QA",
        "questions": rows,
    }
    write_json(batch.independent_qa, independent)
    independent_sha = sha256(batch.independent_qa)

    write_json(batch.technical_review, {
        "review_contract": f"GATE_EE_{batch.batch_id.replace('_', '')}_TECHNICAL_REVIEW_V1",
        "batch_id": batch.batch_id,
        "source_sha256": source_sha,
        "stage": "READY_FOR_HUMAN_FINAL_QA",
        "independent_ai_technical_recomputation_passed": len(questions),
        "independent_ai_technical_recomputation_pending": 0,
        "formatter_passed": len(questions),
        "formatter_review": 0,
        "invalid_count": 0,
        "paper_eligible_count": 0,
        "independent_human_review_required": True,
        "human_technical_review_status": "PENDING",
        "release_gate": "BLOCKED_PENDING_HUMAN_FINAL_QA",
    })

    write_json(batch.candidate, {
        "candidate_contract": f"GATE_EE_{batch.batch_id.replace('_', '')}_PAPER_ELIGIBILITY_CANDIDATE_V1",
        "batch_id": batch.batch_id,
        "domain": batch.domain,
        "source_sha256": source_sha,
        "paper_eligibility_candidate_count": len(questions),
        "paper_eligible_count": 0,
        "candidate_question_ids": [question["id"] for question in questions],
        "prerequisites": {
            "formatter": f"{len(questions)}_PASS_0_REVIEW_0_INVALID",
            "independent_ai_recomputation": f"{len(questions)}_PASS",
            "human_final_qa": "PENDING",
        },
        "release_gate": "BLOCKED_PENDING_HUMAN_FINAL_QA",
    })

    human_questions = [
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
    ]
    write_json(batch.human_qa, {
        "signoff_contract": f"GATE_EE_{batch.batch_id}_HUMAN_FINAL_QA_V1",
        "batch_id": batch.batch_id,
        "source_sha256": source_sha,
        "formatter_report_sha256": formatter_sha,
        "prerequisites": {
            "formatter": f"{len(questions)}_PASS_0_REVIEW_0_INVALID",
            "independent_ai_recomputation": f"{len(questions)}_PASS",
        },
        "reviewer": {
            "name": "",
            "role_or_qualification": "",
            "review_date": "",
            "attestation": "",
        },
        "required_attestation": batch.attestation,
        "final_decision": "PENDING",
        "questions": human_questions,
    })

    write_json(batch.summary, {
        "qualification_version": "1.1.0",
        "batch_id": batch.batch_id,
        "domain": batch.domain,
        "current_stage": "READY_FOR_HUMAN_FINAL_QA",
        "source_sha256": source_sha,
        "formatter_evidence_sha256": formatter_sha,
        "questions_total": len(questions),
        "formatter_v2_qualification": {
            "status": "PASS",
            "passed": len(questions),
            "review": 0,
            "invalid": 0,
            "render_passed": len(questions),
        },
        "independent_ai_technical_recomputation": {
            "status": "PASS",
            "passed": len(questions),
            "evidence_sha256": independent_sha,
            "human_review_substitute": False,
        },
        "human_final_qa": {"status": "PENDING", "passed": 0, "revise": 0, "reject": 0},
        "paper_eligible_count": 0,
        "release_gate": "BLOCKED_PENDING_HUMAN_FINAL_QA",
        "next_action": f"Complete named human final QA for all {len(questions)} checksum-bound {batch.domain} candidates; promote only explicit PASS records.",
        "remaining_gates": ["Named human final QA", "Paper-eligibility promotion", "Corpus V1 admission"],
    })

    type_counts = dict(Counter(str(question["type"]) for question in questions))
    marks_counts = dict(Counter(str(question["marks"]) for question in questions))
    difficulty_counts = dict(Counter(str(question["difficulty"]) for question in questions))
    topic_counts = dict(Counter(str(question["topic"]) for question in questions))
    subtopics = dict(Counter(str(question["subtopic"]) for question in questions))
    write_json(batch.manifest, {
        "manifest_version": "1.1.0",
        "batch_id": batch.batch_id,
        "corpus": "GATE_EE_CORPUS_V1",
        "domain": batch.domain,
        "question_count": len(questions),
        "status": "READY_FOR_HUMAN_FINAL_QA",
        "paper_eligible_count": 0,
        "type_counts": type_counts,
        "marks_counts": marks_counts,
        "difficulty_counts": difficulty_counts,
        "topic_counts": topic_counts,
        "subtopics": subtopics,
        "visual_question_count": len(diagram_assets),
        "source_files": [
            f"GATE_EE/corpus_v1/source_batches/{batch.markdown.name}",
            f"GATE_EE/corpus_v1/source_batches/{batch.source.name}",
        ],
        "diagram_assets": diagram_assets,
        "jsonl_sha256": source_sha,
        "formatter_evidence_sha256": formatter_sha,
        "independent_ai_qa_sha256": independent_sha,
        "qualification_note": f"{batch.domain} {batch.batch_id}. Strict Formatter: {len(questions)} PASS / 0 REVIEW / 0 invalid. Independent AI technical/answer/solution recomputation: {len(questions)}/{len(questions)} PASS and not a human substitute. Named human final QA remains pending; no record is PAPER_ELIGIBLE and no paper is released.",
    })

    batch.review_packet.write_text(
        "\n".join([
            f"# {batch.batch_id} Human Review Packet",
            "",
            "**Stage:** READY_FOR_HUMAN_FINAL_QA",
            f"**Domain:** {batch.domain}",
            f"**Questions:** {len(questions)}",
            f"**Source SHA-256:** `{source_sha}`",
            f"**Formatter evidence SHA-256:** `{formatter_sha}`",
            "",
            f"Strict Formatter and independent recomputation both pass all {len(questions)} records. These machine checks are not human approval.",
            "",
            "Use the mobile-fillable PDF in `output/pdf`, solve every item independently, complete all five checks, and select PASS, REVISE, or REJECT for each question.",
            "",
            f"Required attestation: {batch.attestation}",
            "",
            "Paper eligibility and release remain blocked until the completed form is imported, validated, and promoted.",
        ]) + "\n",
        encoding="utf-8",
    )


def write_pre_formatter_manifest(
    batch: RecoveryBatch,
    questions: list[dict[str, Any]],
    source_sha: str,
    diagram_assets: list[dict[str, str]],
) -> None:
    write_json(batch.manifest, {
        "manifest_version": "1.1.0",
        "batch_id": batch.batch_id,
        "corpus": "GATE_EE_CORPUS_V1",
        "domain": batch.domain,
        "question_count": len(questions),
        "status": "READY_FOR_FORMATTER",
        "paper_eligible_count": 0,
        "visual_question_count": len(diagram_assets),
        "jsonl_sha256": source_sha,
        "qualification_note": "Source, family and handoff artifacts are ready. Formatter and independent recomputation evidence are pending.",
    })


def build(batch: RecoveryBatch, *, static_only: bool = False) -> None:
    questions = load_questions(batch)
    source_sha, diagram_assets = build_static(batch, questions)
    if batch.formatter_evidence.exists() and not static_only:
        build_machine_qualified(batch, questions, source_sha, diagram_assets)
    else:
        write_pre_formatter_manifest(batch, questions, source_sha, diagram_assets)
    print(f"Built {batch.batch_id}: {len(questions)} questions, source {source_sha}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="append", choices=sorted(BATCHES))
    parser.add_argument("--static-only", action="store_true", help="Rebuild source-bound handoffs before fresh Formatter evidence exists.")
    args = parser.parse_args()
    for batch_id in args.batch or sorted(BATCHES):
        build(get_batch(batch_id), static_only=args.static_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
