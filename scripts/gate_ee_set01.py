#!/usr/bin/env python3
"""Shared, deterministic Set 01 manifest and review-artifact contracts."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
BLUEPRINT = ROOT / "blueprints/GATE_EE_SET_01_V1.json"
PREFLIGHT = ROOT / "blueprints/GATE_EE_SET_01_CAPACITY_PREFLIGHT.json"
MANIFEST = BASE / "paper_manifests/GATE_EE_SET_01_V1.json"
HANDOFF = BASE / "formatter_handoff/GATE_EE_SET_01_V1_FORMATTER_HANDOFF.json"
RENDER_EVIDENCE = BASE / "qualification/GATE_EE_SET_01_RENDER_EVIDENCE.json"
HUMAN_QA = BASE / "review_manifests/GATE_EE_SET_01_HUMAN_FINAL_QA.json"
QUESTION_PDF = ROOT / "output/pdf/GATE_EE_SET_01_QUESTION_PAPER_REVIEW.pdf"
SOLUTION_PDF = ROOT / "output/pdf/GATE_EE_SET_01_SOLUTIONS_REVIEW.pdf"
HUMAN_QA_PDF = ROOT / "output/pdf/GATE_EE_SET_01_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf"
COMPLETED_SIGNOFF = BASE / "review_manifests/GATE_EE_SET_01_HUMAN_FINAL_QA_COMPLETED.json"
FORMATTER_RELEASE_EVIDENCE = BASE / "formatter_handoff/GATE_EE_SET_01_FORMATTER_RELEASE_EVIDENCE.json"
RELEASE_CANDIDATE = BASE / "release_candidates/GATE_EE_SET_01_RC1.json"
RELEASE_QUESTION_PDF = ROOT / "output/pdf/GATE_EE_SET_01_QUESTION_PAPER_RC1.pdf"
RELEASE_SOLUTION_PDF = ROOT / "output/pdf/GATE_EE_SET_01_SOLUTIONS_RC1.pdf"
RELEASE_LEARNER_PACK_PDF = ROOT / "output/pdf/GATE_EE_SET_01_LEARNER_PACK_RC1.pdf"
RELEASE_AUTHORIZATION_PDF = ROOT / "output/pdf/GATE_EE_SET_01_RELEASE_AUTHORIZATION_MOBILE_FILLABLE.pdf"
RELEASE_AUTHORIZATION_COMPLETED = BASE / "review_manifests/GATE_EE_SET_01_RC1_RELEASE_AUTHORIZATION_COMPLETED.json"
RELEASE_AUTHORIZATION_COMPLETED_PDF = ROOT / "output/pdf/GATE_EE_SET_01_RELEASE_AUTHORIZATION_COMPLETED.pdf"

SOURCES = {
    "BATCH_001": BASE / "source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl",
    "BATCH_002": BASE / "source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl",
    "BATCH_003": BASE / "source_batches/BATCH_003_GENERAL_APTITUDE.jsonl",
    "BATCH_004": BASE / "source_batches/BATCH_004_SIGNALS_AND_SYSTEMS.jsonl",
    "BATCH_005": BASE / "source_batches/BATCH_005_ELECTROMAGNETIC_FIELDS.jsonl",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def pretty_bytes(payload: Any) -> bytes:
    return (
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode("utf-8")


def content_sha256(payload: dict[str, Any], field: str) -> str:
    unsigned = dict(payload)
    unsigned.pop(field, None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def evidence_paths(batch_id: str) -> dict[str, Path]:
    return {
        "source": SOURCES[batch_id],
        "formatter_final_evidence": BASE / "qualification" / f"{batch_id}_FORMATTER_FINAL_EVIDENCE.json",
        "independent_ai_qa": BASE / "qualification" / f"{batch_id}_INDEPENDENT_AI_QA.json",
        "human_final_qa": BASE / "review_manifests" / f"{batch_id}_HUMAN_FINAL_QA.json",
        "paper_eligibility_certificate": BASE / "qualification" / f"{batch_id}_PAPER_ELIGIBILITY_CERTIFICATE.json",
        "corpus_admission_manifest": BASE / "manifests" / f"{batch_id}_CORPUS_ADMISSION.json",
    }


def source_index() -> tuple[dict[str, dict[str, Any]], dict[str, tuple[str, int]]]:
    by_id: dict[str, dict[str, Any]] = {}
    location: dict[str, tuple[str, int]] = {}
    for batch_id, path in SOURCES.items():
        for line_number, question in enumerate(load_jsonl(path), 1):
            question_id = question["id"]
            if question_id in by_id:
                raise ValueError(f"duplicate source question ID: {question_id}")
            by_id[question_id] = question
            location[question_id] = (batch_id, line_number)
    return by_id, location


def selected_questions() -> list[tuple[dict[str, Any], dict[str, Any]]]:
    preflight = load_json(PREFLIGHT)
    by_id, _ = source_index()
    selected = []
    for row in preflight["selection"]:
        question = by_id.get(row["question_id"])
        if question is None:
            raise ValueError(f"preflight question is absent from canonical sources: {row['question_id']}")
        selected.append((row, question))
    return selected


def _stats(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "questions": len(rows),
        "marks": sum(int(row["marks"]) for row in rows),
        "one_mark_questions": sum(int(row["marks"]) == 1 for row in rows),
        "two_mark_questions": sum(int(row["marks"]) == 2 for row in rows),
    }


def _validate_batch_evidence(batch_id: str, selected_ids: set[str]) -> dict[str, Any]:
    paths = evidence_paths(batch_id)
    for label, path in paths.items():
        if not path.is_file():
            raise ValueError(f"{batch_id}: missing {label}: {relative(path)}")

    source_hash = sha256(paths["source"])
    formatter = load_json(paths["formatter_final_evidence"])
    independent = load_json(paths["independent_ai_qa"])
    human = load_json(paths["human_final_qa"])
    certificate = load_json(paths["paper_eligibility_certificate"])
    admission = load_json(paths["corpus_admission_manifest"])

    expected_count = len(load_jsonl(paths["source"]))
    if formatter.get("source_sha256") != source_hash:
        raise ValueError(f"{batch_id}: Formatter evidence/source checksum mismatch")
    formatter_tuple = (
        formatter.get("status"),
        formatter.get("question_count"),
        formatter.get("formatter_pass_count"),
        formatter.get("formatter_review_count"),
        formatter.get("invalid_count"),
    )
    if formatter_tuple != ("PASS", expected_count, expected_count, 0, 0):
        raise ValueError(f"{batch_id}: Formatter evidence is not an exact all-PASS result")
    if human.get("source_sha256") != source_hash:
        raise ValueError(f"{batch_id}: human signoff/source checksum mismatch")
    if human.get("final_decision") != "APPROVE_REVIEWED_RESULTS":
        raise ValueError(f"{batch_id}: human final QA is incomplete")
    human_pass = {
        row["question_id"]
        for row in human.get("questions", [])
        if row.get("decision") == "PASS"
    }
    approved = set(certificate.get("approved_question_ids", []))
    admitted = set(admission.get("admitted_question_ids", []))
    if certificate.get("source_sha256") != source_hash:
        raise ValueError(f"{batch_id}: certificate/source checksum mismatch")
    if certificate.get("decision") != "CERTIFIED" or approved != human_pass:
        raise ValueError(f"{batch_id}: certificate does not match human PASS decisions")
    if certificate.get("human_signoff_sha256") != sha256(paths["human_final_qa"]):
        raise ValueError(f"{batch_id}: certificate/human signoff checksum mismatch")
    if admission.get("source_sha256") != source_hash or admitted != approved:
        raise ValueError(f"{batch_id}: admission manifest does not match certificate")
    if admission.get("paper_eligibility_certificate_sha256") != sha256(paths["paper_eligibility_certificate"]):
        raise ValueError(f"{batch_id}: admission/certificate checksum mismatch")
    if not selected_ids <= approved or not selected_ids <= admitted:
        raise ValueError(f"{batch_id}: one or more selected IDs are not certified and admitted")

    independent_rows = independent.get("questions", [])
    independently_passed = {
        row.get("question_id")
        for row in independent_rows
        if all(
            row.get(field) == "PASS"
            for field in (
                "technical_result", "answer_result",
                "solution_consistency_result", "machine_final_marker_result",
            )
        )
    }
    if independent.get("status") != "PASS" or not selected_ids <= independently_passed:
        raise ValueError(f"{batch_id}: selected IDs lack independent-QA PASS evidence")

    return {
        label: {"path": relative(path), "sha256": sha256(path)}
        for label, path in paths.items()
    }


def build_manifest_payload() -> dict[str, Any]:
    blueprint = load_json(BLUEPRINT)
    preflight = load_json(PREFLIGHT)
    _, locations = source_index()
    selected = selected_questions()
    if preflight.get("status") != "READY_FOR_CONTROLLED_MANIFEST_ASSEMBLY":
        raise ValueError("Set 01 capacity preflight is not ready for manifest assembly")
    if len(selected) != 65:
        raise ValueError(f"Set 01 must select 65 questions, found {len(selected)}")

    selected_by_batch: dict[str, set[str]] = {batch_id: set() for batch_id in SOURCES}
    manifest_rows: list[dict[str, Any]] = []
    for row, question in selected:
        question_id = question["id"]
        batch_id, line_number = locations[question_id]
        selected_by_batch[batch_id].add(question_id)
        for key, source_key in (
            ("revision", "revision"), ("family_id", "family_id"),
            ("subject", "subject"), ("topic", "topic"), ("marks", "marks"),
            ("type", "type"), ("difficulty", "difficulty"),
            ("estimated_time_seconds", "estimated_time_seconds"),
        ):
            if row.get(key) != question.get(source_key):
                raise ValueError(f"{question_id}: preflight/source {key} mismatch")
        diagram = question.get("diagram")
        visual = diagram is not None
        if bool(row.get("visual")) != visual:
            raise ValueError(f"{question_id}: preflight/source visual flag mismatch")
        diagram_binding = None
        if diagram:
            asset = ROOT / diagram["asset"]
            if not asset.is_file():
                raise ValueError(f"{question_id}: missing diagram asset {diagram['asset']}")
            diagram_binding = {
                "path": relative(asset),
                "sha256": sha256(asset),
                "alt_text": diagram["alt_text"],
                "caption": diagram["caption"],
            }
        manifest_rows.append({
            "position": int(row["position"]),
            "question_id": question_id,
            "revision": int(question["revision"]),
            "family_id": question["family_id"],
            "batch_id": batch_id,
            "source_path": relative(SOURCES[batch_id]),
            "source_line_number": line_number,
            "source_record_sha256": hashlib.sha256(canonical_bytes(question)).hexdigest(),
            "subject": question["subject"],
            "topic": question["topic"],
            "subtopic": question["subtopic"],
            "marks": int(question["marks"]),
            "type": question["type"],
            "difficulty": question["difficulty"],
            "estimated_time_seconds": int(question["estimated_time_seconds"]),
            "visual": visual,
            "diagram": diagram_binding,
            "eligibility_state": "PAPER_ELIGIBLE",
        })

    batch_evidence = {
        batch_id: _validate_batch_evidence(batch_id, selected_by_batch[batch_id])
        for batch_id in SOURCES
    }
    human_qualifications = {
        batch_id: load_json(evidence_paths(batch_id)["human_final_qa"])
        .get("reviewer", {})
        .get("role_or_qualification", "")
        for batch_id in SOURCES
    }
    qualification_values = sorted({value for value in human_qualifications.values() if value})

    ga = [row for row in manifest_rows if row["subject"] == "General Aptitude"]
    math = [row for row in manifest_rows if row["subject"] == "Engineering Mathematics"]
    core = [row for row in manifest_rows if row["subject"] == "Electrical Engineering"]
    structure = {
        "paper": _stats(manifest_rows),
        "General Aptitude": _stats(ga),
        "Selected Subject": _stats(math + core),
        "Engineering Mathematics": _stats(math),
        "Electrical Engineering": _stats(core),
    }
    balance = {
        "difficulty": dict(sorted(Counter(row["difficulty"] for row in manifest_rows).items())),
        "question_type": dict(sorted(Counter(row["type"] for row in manifest_rows).items())),
        "visual_questions": sum(row["visual"] for row in manifest_rows),
        "nonvisual_questions": sum(not row["visual"] for row in manifest_rows),
        "estimated_time_seconds": sum(row["estimated_time_seconds"] for row in manifest_rows),
    }

    payload: dict[str, Any] = {
        "manifest_contract": "GATE_EE_SET01_IMMUTABLE_REVIEW_MANIFEST_V1",
        "paper_id": "GATE_2027_EE_SET_01",
        "manifest_version": "1.0.0-review.1",
        "assembled_on": preflight["generated_on"],
        "status": "ASSEMBLED_FOR_COMPLETE_PAPER_HUMAN_QA",
        "purpose": "Freezes the exact 65 PAPER_ELIGIBLE revisions used for Set 01 review rendering. It is not a commercial release manifest.",
        "blueprint": {"path": relative(BLUEPRINT), "sha256": sha256(BLUEPRINT)},
        "capacity_preflight": {"path": relative(PREFLIGHT), "sha256": sha256(PREFLIGHT)},
        "structure": structure,
        "balance": balance,
        "batch_evidence": batch_evidence,
        "questions": manifest_rows,
        "reviewer_metadata_consistency": {
            "status": "RECONFIRMATION_REQUIRED_BEFORE_RELEASE" if len(qualification_values) > 1 else "CONSISTENT",
            "recorded_by_batch": human_qualifications,
            "distinct_recorded_values": qualification_values,
            "affected_selected_batch_001_questions": len(selected_by_batch["BATCH_001"]),
            "resolution": "The named reviewer must state the accurate qualification in the complete-paper QA form; no signed historical record is silently rewritten.",
        },
        "gate_state": {
            "manifest_assembled": True,
            "blueprint_validation": "PASS",
            "selected_paper_eligible": "PASS_65_OF_65",
            "unique_question_ids": "PASS",
            "unique_family_ids": "PASS",
            "rendered_question_pdf": "PENDING",
            "rendered_solution_pdf": "PENDING",
            "complete_paper_human_qa": "PENDING",
            "release_authorized": False,
            "sale_authorized": False,
        },
    }
    payload["manifest_content_sha256"] = content_sha256(payload, "manifest_content_sha256")
    _assert_structure(payload, blueprint, preflight)
    return payload


def _assert_structure(manifest: dict[str, Any], blueprint: dict[str, Any], preflight: dict[str, Any]) -> None:
    rows = manifest["questions"]
    if [row["position"] for row in rows] != list(range(1, 66)):
        raise ValueError("Set 01 positions must be the contiguous range 1..65")
    if [row["question_id"] for row in rows] != [row["question_id"] for row in preflight["selection"]]:
        raise ValueError("manifest selection/order differs from the approved capacity preflight")
    if len({row["question_id"] for row in rows}) != 65:
        raise ValueError("Set 01 question IDs are not unique")
    if len({row["family_id"] for row in rows}) != 65:
        raise ValueError("Set 01 family IDs are not unique")
    paper = blueprint["paper"]
    if manifest["structure"]["paper"] != {
        "questions": paper["questions"], "marks": paper["marks"],
        "one_mark_questions": 30, "two_mark_questions": 35,
    }:
        raise ValueError("Set 01 paper totals violate the blueprint")
    section = blueprint["section_contract"]
    for name in ("General Aptitude", "Selected Subject"):
        if manifest["structure"][name] != section[name]:
            raise ValueError(f"Set 01 {name} structure violates the blueprint")
    for name in ("Engineering Mathematics", "Electrical Engineering"):
        if manifest["structure"][name]["marks"] != section[name]["marks"]:
            raise ValueError(f"Set 01 {name} marks violate the blueprint")
    for axis in ("difficulty", "question_type"):
        for label, bounds in blueprint["balance_targets"][axis].items():
            value = manifest["balance"][axis].get(label, 0)
            if not bounds["min"] <= value <= bounds["max"]:
                raise ValueError(f"Set 01 {axis}/{label} balance is outside its range")
    for name in ("visual_questions", "estimated_time_seconds"):
        bounds = blueprint["balance_targets"][name]
        if not bounds["min"] <= manifest["balance"][name] <= bounds["max"]:
            raise ValueError(f"Set 01 {name} balance is outside its range")


def build_handoff_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    by_id, _ = source_index()
    questions = []
    for row in manifest["questions"]:
        source = by_id[row["question_id"]]
        questions.append({
            "number": row["position"],
            "id": source["id"],
            "revision": source["revision"],
            "section": source["subject"],
            "topic": source["topic"],
            "subtopic": source["subtopic"],
            "type": source["type"],
            "marks": source["marks"],
            "difficulty": source["difficulty"],
            "text": source["stem"],
            "options": source.get("options", []),
            "answer": source["answer"],
            "nat_tolerance": source.get("nat_tolerance"),
            "solution": source["solution"],
            "diagram": source.get("diagram"),
            "source_record_sha256": row["source_record_sha256"],
        })
    payload: dict[str, Any] = {
        "handoff_contract": "GATE_EE_SET01_FORMATTER_REVIEW_HANDOFF_V1",
        "paper_id": manifest["paper_id"],
        "manifest_content_sha256": manifest["manifest_content_sha256"],
        "render_contract": "XELATEX_CANONICAL_MATH_WITH_CHECKSUM_BOUND_SVG_ASSETS_V1",
        "release_mode": "REVIEW_ONLY",
        "paper": {
            "title": "TheMITbro GATE 2027 Electrical Engineering — Set 01",
            "exam": "GATE_EE",
            "duration_minutes": 180,
            "total_marks": 100,
            "question_count": 65,
            "questions": questions,
        },
        "gate_state": {
            "source_formatter_qualification": "PASS_65_OF_65",
            "complete_paper_human_qa": "PENDING",
            "release_authorized": False,
            "sale_authorized": False,
        },
    }
    payload["handoff_content_sha256"] = content_sha256(payload, "handoff_content_sha256")
    return payload


def validate_manifest_and_handoff() -> tuple[dict[str, Any], dict[str, Any]]:
    expected_manifest = build_manifest_payload()
    if not MANIFEST.is_file():
        raise ValueError(f"missing Set 01 manifest: {relative(MANIFEST)}")
    actual_manifest = load_json(MANIFEST)
    if actual_manifest != expected_manifest:
        raise ValueError("Set 01 manifest differs from the deterministic evidence-bound build")
    expected_hash = content_sha256(actual_manifest, "manifest_content_sha256")
    if actual_manifest.get("manifest_content_sha256") != expected_hash:
        raise ValueError("Set 01 manifest self-hash is invalid")

    expected_handoff = build_handoff_payload(actual_manifest)
    if not HANDOFF.is_file():
        raise ValueError(f"missing Formatter handoff: {relative(HANDOFF)}")
    actual_handoff = load_json(HANDOFF)
    if actual_handoff != expected_handoff:
        raise ValueError("Set 01 Formatter handoff differs from the deterministic manifest build")
    if actual_handoff.get("handoff_content_sha256") != content_sha256(actual_handoff, "handoff_content_sha256"):
        raise ValueError("Set 01 Formatter handoff self-hash is invalid")
    return actual_manifest, actual_handoff


def write_manifest_and_handoff() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = build_manifest_payload()
    handoff = build_handoff_payload(manifest)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    HANDOFF.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_bytes(pretty_bytes(manifest))
    HANDOFF.write_bytes(pretty_bytes(handoff))
    return manifest, handoff
