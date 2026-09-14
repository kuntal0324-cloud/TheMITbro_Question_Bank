#!/usr/bin/env python3
"""Build the non-releasable Set 01 structural-capacity preflight."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
BLUEPRINT = ROOT / "blueprints/GATE_EE_SET_01_V1.json"
OUTPUT = ROOT / "blueprints/GATE_EE_SET_01_CAPACITY_PREFLIGHT.json"

SOURCES = {
    "BATCH_001": BASE / "source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl",
    "BATCH_002": BASE / "source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl",
    "BATCH_003": BASE / "source_batches/BATCH_003_GENERAL_APTITUDE.jsonl",
    "BATCH_004": BASE / "source_batches/BATCH_004_SIGNALS_AND_SYSTEMS.jsonl",
    "BATCH_005": BASE / "source_batches/BATCH_005_ELECTROMAGNETIC_FIELDS.jsonl",
}

GA_IDS = (
    "TMB-GATE-EE-GA-002", "TMB-GATE-EE-GA-003", "TMB-GATE-EE-GA-004",
    "TMB-GATE-EE-GA-005", "TMB-GATE-EE-GA-008", "TMB-GATE-EE-GA-010",
    "TMB-GATE-EE-GA-013", "TMB-GATE-EE-GA-014", "TMB-GATE-EE-GA-016",
    "TMB-GATE-EE-GA-019",
)
MATH_IDS = (
    "TMB-GATE-EE-EM-001", "TMB-GATE-EE-EM-003", "TMB-GATE-EE-EM-004",
    "TMB-GATE-EE-EM-008", "TMB-GATE-EE-EM-009", "TMB-GATE-EE-EM-013",
    "TMB-GATE-EE-EM-015", "TMB-GATE-EE-EM-018",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build() -> dict:
    blueprint = json.loads(BLUEPRINT.read_text(encoding="utf-8"))
    registry = json.loads((BASE / "families/FAMILY_REGISTRY.json").read_text(encoding="utf-8"))
    progress = json.loads((BASE / "production/EIGHT_DAY_PROGRESS.json").read_text(encoding="utf-8"))
    admitted_ids = {
        qid
        for family in registry.get("families", [])
        for qid in family.get("question_ids", [])
    }
    by_id: dict[str, tuple[str, dict]] = {}
    for batch_id, path in SOURCES.items():
        for question in load_jsonl(path):
            by_id[question["id"]] = (batch_id, question)

    core_ids = tuple(
        question["id"]
        for batch_id in ("BATCH_002", "BATCH_004", "BATCH_005")
        for question in load_jsonl(SOURCES[batch_id])
    )
    selection_ids = GA_IDS + MATH_IDS + core_ids
    rows = []
    for position, qid in enumerate(selection_ids, 1):
        batch_id, question = by_id[qid]
        pending = qid not in admitted_ids
        rows.append({
            "position": position,
            "question_id": qid,
            "revision": question["revision"],
            "family_id": question["family_id"],
            "batch_id": batch_id,
            "subject": question["subject"],
            "topic": question["topic"],
            "marks": question["marks"],
            "type": question["type"],
            "difficulty": question["difficulty"],
            "estimated_time_seconds": question["estimated_time_seconds"],
            "visual": question.get("diagram") is not None,
            "eligibility_state": "READY_FOR_HUMAN_FINAL_QA" if pending else "PAPER_ELIGIBLE",
        })

    def stats(items: list[dict]) -> dict:
        return {
            "questions": len(items),
            "marks": sum(row["marks"] for row in items),
            "one_mark_questions": sum(row["marks"] == 1 for row in items),
            "two_mark_questions": sum(row["marks"] == 2 for row in items),
        }

    ga_rows = [row for row in rows if row["subject"] == "General Aptitude"]
    math_rows = [row for row in rows if row["subject"] == "Engineering Mathematics"]
    core_rows = [row for row in rows if row["subject"] == "Electrical Engineering"]
    eligible = [row for row in rows if row["eligibility_state"] == "PAPER_ELIGIBLE"]
    pending = [row for row in rows if row["eligibility_state"] == "READY_FOR_HUMAN_FINAL_QA"]
    all_eligible = not pending
    status = (
        "READY_FOR_CONTROLLED_MANIFEST_ASSEMBLY"
        if all_eligible else "STRUCTURALLY_COMPLETE_PENDING_HUMAN_FINAL_QA"
    )
    purpose = (
        "Proves that the selected 65 records satisfy the Set 01 structure and are all "
        "PAPER_ELIGIBLE. It is not a paper manifest or release authorization."
        if all_eligible else
        "Proves that the current candidate pool can satisfy the Set 01 structure after "
        "the remaining named-human approvals. It is not a paper manifest or release authorization."
    )
    eligibility_gate = (
        "PASS_65_OF_65"
        if all_eligible else f"BLOCKED_{len(pending)}_PENDING_HUMAN_FINAL_QA"
    )
    remaining_gate = (
        "Create the immutable Set 01 manifest from these 65 PAPER_ELIGIBLE records, validate "
        "the exact blueprint, render the final PDF, and obtain named-human technical and visual QA."
        if all_eligible else
        "Complete named human final QA, paper-eligibility promotion and Corpus V1 admission "
        "for every pending record, followed by controlled assembly and final paper QA."
    )

    payload = {
        "preflight_contract": "GATE_EE_SET01_STRUCTURAL_CAPACITY_PREFLIGHT_V1",
        "generated_on": progress["as_of"],
        "blueprint": str(BLUEPRINT.relative_to(ROOT)),
        "blueprint_sha256": sha256(BLUEPRINT),
        "status": status,
        "purpose": purpose,
        "inventory": {
            "program_candidates": progress["program_inventory"]["unique_candidates"],
            "formatter_passed": progress["program_inventory"]["formatter_passed"],
            "human_certified_paper_eligible_admitted": registry["admitted_question_count"],
            "selected_in_preflight": len(rows),
            "selected_already_paper_eligible": len(eligible),
            "selected_pending_human_final_qa": len(pending),
        },
        "structure": {
            "paper": stats(rows),
            "General Aptitude": stats(ga_rows),
            "Selected Subject": stats(math_rows + core_rows),
            "Engineering Mathematics": stats(math_rows),
            "Electrical Engineering": stats(core_rows),
        },
        "balance": {
            "difficulty": dict(Counter(row["difficulty"] for row in rows)),
            "question_type": dict(Counter(row["type"] for row in rows)),
            "visual_questions": sum(row["visual"] for row in rows),
            "nonvisual_questions": sum(not row["visual"] for row in rows),
            "estimated_time_seconds": sum(row["estimated_time_seconds"] for row in rows),
        },
        "source_checksums": {batch_id: sha256(path) for batch_id, path in SOURCES.items()},
        "selection": rows,
        "gate_state": {
            "structural_blueprint": "PASS",
            "unique_question_ids": "PASS",
            "unique_family_ids": "PASS",
            "formatter_v2": "PASS_65_OF_65",
            "allowed_status_paper_eligible": eligibility_gate,
            "paper_manifest": "NOT_CREATED",
            "final_pdf": "NOT_CREATED",
            "release_authorized": False,
            "sale_authorized": False,
        },
        "remaining_gate": remaining_gate,
    }

    # Evaluate the machine-checkable structural constraints while building.
    paper = blueprint["paper"]
    section = blueprint["section_contract"]
    balance = blueprint["balance_targets"]
    assert payload["structure"]["paper"] == {
        "questions": paper["questions"], "marks": paper["marks"],
        "one_mark_questions": 30, "two_mark_questions": 35,
    }
    for key in ("General Aptitude", "Selected Subject"):
        assert payload["structure"][key] == section[key]
    assert payload["structure"]["Engineering Mathematics"]["marks"] == section["Engineering Mathematics"]["marks"]
    assert payload["structure"]["Electrical Engineering"]["marks"] == section["Electrical Engineering"]["marks"]
    for axis in ("difficulty", "question_type"):
        for label, bounds in balance[axis].items():
            assert bounds["min"] <= payload["balance"][axis][label] <= bounds["max"]
    assert balance["visual_questions"]["min"] <= payload["balance"]["visual_questions"] <= balance["visual_questions"]["max"]
    assert balance["estimated_time_seconds"]["min"] <= payload["balance"]["estimated_time_seconds"] <= balance["estimated_time_seconds"]["max"]
    assert len({row["question_id"] for row in rows}) == len(rows)
    assert len({row["family_id"] for row in rows}) == len(rows)
    assert all(row["batch_id"] in {"BATCH_004", "BATCH_005"} for row in pending)
    assert len(pending) + len(eligible) == 65
    if all_eligible:
        assert len(eligible) == 65
    else:
        assert all(row["batch_id"] in {"BATCH_001", "BATCH_002", "BATCH_003"} for row in eligible)
    for batch_id, source in SOURCES.items():
        formatter_path = BASE / "qualification" / f"{batch_id}_FORMATTER_FINAL_EVIDENCE.json"
        formatter = json.loads(formatter_path.read_text(encoding="utf-8"))
        expected_count = len(load_jsonl(source))
        assert formatter.get("source_sha256") == sha256(source)
        assert (
            formatter.get("status"), formatter.get("question_count"),
            formatter.get("formatter_pass_count"), formatter.get("formatter_review_count"),
            formatter.get("invalid_count"), formatter.get("paper_eligible_count"),
        ) == ("PASS", expected_count, expected_count, 0, 0, 0)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    build_payload = build()
    serialized = json.dumps(build_payload, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != serialized:
            raise SystemExit("Set 01 capacity preflight is stale")
    else:
        OUTPUT.write_text(serialized, encoding="utf-8")
        print(f"Wrote {OUTPUT}")
    print("GATE EE SET 01 CAPACITY PREFLIGHT: PASSED")
    print("65 questions / 100 marks / 180-minute blueprint")
    print(
        f"Selected: {len([row for row in build_payload['selection'] if row['eligibility_state'] == 'PAPER_ELIGIBLE'])} "
        "PAPER_ELIGIBLE + "
        f"{len([row for row in build_payload['selection'] if row['eligibility_state'] != 'PAPER_ELIGIBLE'])} "
        "PENDING_HUMAN_FINAL_QA"
    )
    print("Paper manifest/release: NOT CREATED / BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
