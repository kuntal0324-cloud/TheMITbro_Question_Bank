#!/usr/bin/env python3
"""Promote human-approved Batches 004 and 005 into Corpus V1 together."""

from __future__ import annotations

from datetime import date
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gate_ee_recovery_batches import BATCHES, BASE, RecoveryBatch, load_questions
from validate_gate_ee_recovery_human_signoff import validate as validate_human_signoff

FAMILY_REGISTRY = BASE / "families/FAMILY_REGISTRY.json"
PROGRESS = BASE / "production/EIGHT_DAY_PROGRESS.json"
DAY_ALLOCATIONS = {
    7: {
        "Control Systems": 122,
        "Electrical and Electronic Measurements": 180,
        "Analog and Digital Electronics": 145,
    },
    8: {
        "Analog and Digital Electronics": 95,
        "Power Electronics": 180,
        "General Aptitude": 100,
        "Engineering Mathematics": 45,
        "Electric Circuits": 26,
    },
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def serialized(payload: dict) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def certificate_path(batch: RecoveryBatch) -> Path:
    return BASE / "qualification" / f"{batch.batch_id}_PAPER_ELIGIBILITY_CERTIFICATE.json"


def admission_path(batch: RecoveryBatch) -> Path:
    return BASE / "manifests" / f"{batch.batch_id}_CORPUS_ADMISSION.json"


def block(errors: list[str]) -> None:
    print("GATE EE BATCHES 004-005 PAPER-ELIGIBILITY PROMOTION: BLOCKED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)


def atomic_bytes_write(path: Path, data: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def advance_calendar(progress: dict, as_of: str) -> None:
    sprint = progress["sprint"]
    start = date.fromisoformat(sprint["start_date"])
    current = date.fromisoformat(as_of)
    current_day = (current - start).days + 1
    if current_day not in range(1, 9):
        block([f"review date {as_of} falls outside the fixed eight-day contract"])

    previous_day = int(sprint["current_day"])
    if current_day < previous_day:
        block(["promotion cannot move the fixed contract clock backwards"])
    for day_number in range(previous_day, current_day):
        day = progress.get(f"day_{day_number}")
        if day and day.get("state") == "IN_PROGRESS":
            day["state"] = "CLOSED_BELOW_TARGET"

    daily_targets = sprint["daily_targets"]
    for day_number in range(previous_day + 1, current_day + 1):
        allocation = DAY_ALLOCATIONS.get(day_number)
        if allocation is None:
            block([f"no production allocation is defined for contract Day {day_number}"])
        target = daily_targets[day_number - 1]
        progress[f"day_{day_number}"] = {
            "target": target,
            "drafts_produced": 0,
            "remaining": target,
            "allocation": {
                domain: {"target": count, "produced": 0}
                for domain, count in allocation.items()
            },
            "source_batches": [],
            "state": "IN_PROGRESS",
        }
    progress["as_of"] = as_of
    sprint["current_day"] = current_day
    sprint["state"] = f"DAY_{current_day:02d}_IN_PROGRESS"


def main() -> int:
    errors: list[str] = []
    states: dict[str, dict] = {}
    all_batch_family_ids: list[str] = []
    all_batch_question_ids: list[str] = []

    for batch_id in sorted(BATCHES):
        batch = BATCHES[batch_id]
        human_errors, approved, revise, reject, source_sha = validate_human_signoff(
            batch_id, require_complete=True
        )
        errors.extend(f"{batch_id}: {error}" for error in human_errors)
        human = load(batch.human_qa)
        candidate = load(batch.candidate)
        summary = load(batch.summary)
        manifest = load(batch.manifest)
        families = load(batch.families)
        questions = load_questions(batch)
        expected_ids = [question["id"] for question in questions]

        if summary.get("current_stage") != "READY_FOR_HUMAN_FINAL_QA":
            errors.append(f"{batch_id}: promotion requires READY_FOR_HUMAN_FINAL_QA")
        if certificate_path(batch).exists() or admission_path(batch).exists():
            errors.append(f"{batch_id}: certificate/admission already exists; refusing overwrite")
        if sorted(approved + revise + reject) != sorted(expected_ids):
            errors.append(f"{batch_id}: human decisions do not partition the source IDs")
        if candidate.get("candidate_question_ids") != expected_ids:
            errors.append(f"{batch_id}: paper-eligibility candidate list is stale")
        if manifest.get("status") != "READY_FOR_HUMAN_FINAL_QA":
            errors.append(f"{batch_id}: source manifest is not ready for promotion")

        family_rows = families.get("families", [])
        family_ids = [row.get("family_id") for row in family_rows]
        family_question_ids = [
            qid for row in family_rows for qid in row.get("question_ids", [])
        ]
        if len(family_ids) != len(set(family_ids)):
            errors.append(f"{batch_id}: duplicate family ID inside the batch")
        if sorted(family_question_ids) != sorted(expected_ids):
            errors.append(f"{batch_id}: family file does not cover the source exactly once")
        all_batch_family_ids.extend(family_ids)
        all_batch_question_ids.extend(expected_ids)
        states[batch_id] = {
            "batch": batch,
            "human": human,
            "candidate": candidate,
            "summary": summary,
            "manifest": manifest,
            "families": families,
            "family_rows": family_rows,
            "approved": approved,
            "revise": revise,
            "reject": reject,
            "source_sha": source_sha,
        }

    if len(all_batch_family_ids) != len(set(all_batch_family_ids)):
        errors.append("Batches 004 and 005 contain a cross-batch family collision")
    if len(all_batch_question_ids) != len(set(all_batch_question_ids)):
        errors.append("Batches 004 and 005 contain a cross-batch question-ID collision")
    if errors:
        block(errors)

    family_registry = load(FAMILY_REGISTRY)
    global_rows = family_registry.get("families", [])
    global_family_ids = {row.get("family_id") for row in global_rows}
    global_question_ids = {
        qid for row in global_rows for qid in row.get("question_ids", [])
    }
    family_collision = sorted(global_family_ids.intersection(all_batch_family_ids))
    question_collision = sorted(global_question_ids.intersection(all_batch_question_ids))
    if family_collision:
        errors.append(f"family collision with Corpus V1: {family_collision}")
    if question_collision:
        errors.append(f"question-ID collision with Corpus V1: {question_collision}")
    global_count = sum(len(row.get("question_ids", [])) for row in global_rows)
    if family_registry.get("admitted_question_count") != global_count:
        errors.append("existing global admitted-question count is inconsistent")
    if global_count != len(global_question_ids):
        errors.append("existing family registry contains duplicate admitted question IDs")
    if errors:
        block(errors)

    outputs: dict[Path, bytes] = {}
    admitted_family_rows: list[dict] = []
    review_dates: list[str] = []
    total_newly_approved = 0

    for batch_id in sorted(states):
        state = states[batch_id]
        batch: RecoveryBatch = state["batch"]
        human = state["human"]
        candidate = state["candidate"]
        summary = state["summary"]
        manifest = state["manifest"]
        families = state["families"]
        approved = state["approved"]
        revise = state["revise"]
        reject = state["reject"]
        source_sha = state["source_sha"]
        review_date = human["reviewer"]["review_date"]
        review_dates.append(review_date)
        total_newly_approved += len(approved)

        signoff_sha = sha256(batch.human_qa)
        formatter_sha = sha256(batch.formatter_evidence)
        qa_sha = sha256(batch.independent_qa)
        candidate.update({
            "human_final_qa": "COMPLETE",
            "certified_paper_eligible_question_ids": approved,
            "paper_eligible_count": len(approved),
            "release_gate": "PAPER_ELIGIBILITY_CERTIFIED",
            "human_signoff_sha256": signoff_sha,
        })
        candidate.setdefault("prerequisites", {})["human_final_qa"] = "COMPLETE"

        batch_token = batch.batch_id.replace("_", "")
        certificate = {
            "certificate_contract": f"GATE_EE_{batch_token}_PAPER_ELIGIBILITY_CERTIFICATE_V1",
            "batch_id": batch.batch_id,
            "source_sha256": source_sha,
            "formatter_evidence_sha256": formatter_sha,
            "independent_ai_qa_sha256": qa_sha,
            "human_signoff_sha256": signoff_sha,
            "completed_pdf_sha256": human["pdf_evidence"]["sha256"],
            "reviewer": {
                "name": human["reviewer"]["name"],
                "role_or_qualification": human["reviewer"]["role_or_qualification"],
                "review_date": review_date,
            },
            "approved_question_ids": approved,
            "revise_question_ids": revise,
            "rejected_question_ids": reject,
            "paper_eligible_count": len(approved),
            "decision": "CERTIFIED",
        }
        certificate_bytes = serialized(certificate)
        admission = {
            "manifest_contract": f"GATE_EE_CORPUS_V1_{batch_token}_ADMISSION_V1",
            "batch_id": batch.batch_id,
            "source_sha256": source_sha,
            "paper_eligibility_certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
            "admitted_question_ids": approved,
            "held_for_revision_question_ids": revise,
            "rejected_question_ids": reject,
            "admitted_count": len(approved),
            "status": "ADMITTED_TO_CORPUS_V1",
        }

        summary.update({
            "qualification_version": "1.2.0",
            "current_stage": "PAPER_ELIGIBILITY_CERTIFIED",
            "human_final_qa": {
                "status": "COMPLETE",
                "review_date": review_date,
                "passed": len(approved),
                "revise": len(revise),
                "reject": len(reject),
            },
            "paper_eligible_count": len(approved),
            "remaining_gates": [],
            "release_gate": "BLOCKED_NO_COMPLETE_65_QUESTION_SET",
            "next_action": (
                "Use admitted records only for controlled Set 01 manifest assembly, then render "
                "the paper and obtain final named-human technical and visual QA."
            ),
        })
        manifest.update({
            "manifest_version": "1.2.0",
            "status": "PAPER_ELIGIBILITY_CERTIFIED_AND_ADMITTED",
            "paper_eligible_count": len(approved),
            "qualification_note": (
                f"{batch.domain} {batch.batch_id}. Strict Formatter: {batch.expected_count} PASS / "
                f"0 REVIEW / 0 invalid. Independent technical/answer/solution recomputation: "
                f"{batch.expected_count}/{batch.expected_count} PASS and not a human substitute. "
                f"Named human final QA: {len(approved)} PASS / {len(revise)} REVISE / "
                f"{len(reject)} REJECT. Approved IDs are certificate-bound and admitted to "
                "Corpus V1; no complete paper is released."
            ),
        })

        families["registry_version"] = "1.3.0"
        families["admission_status"] = "ADMITTED_TO_CORPUS_V1"
        approved_set = set(approved)
        for row in state["family_rows"]:
            admitted_ids = [qid for qid in row["question_ids"] if qid in approved_set]
            if admitted_ids:
                admitted_family_rows.append({
                    "family_id": row["family_id"],
                    "question_ids": admitted_ids,
                    "admission_batch": batch.batch_id,
                })

        outputs.update({
            batch.candidate: serialized(candidate),
            certificate_path(batch): certificate_bytes,
            admission_path(batch): serialized(admission),
            batch.summary: serialized(summary),
            batch.manifest: serialized(manifest),
            batch.families: serialized(families),
        })

    family_registry["registry_version"] = "1.3.0"
    family_registry["families"] = global_rows + admitted_family_rows
    family_registry["admitted_question_count"] = sum(
        len(row.get("question_ids", [])) for row in family_registry["families"]
    )

    progress = load(PROGRESS)
    latest_review_date = max(review_dates)
    advance_calendar(progress, latest_review_date)
    admitted_total = family_registry["admitted_question_count"]
    progress["program_inventory"].update({
        "human_final_qa_passed": admitted_total,
        "paper_eligible": admitted_total,
        "corpus_admitted": admitted_total,
        "complete_65_question_sets": 0,
        "released_sets": 0,
    })
    progress["next_gate"] = (
        "Assemble the exact Set 01 manifest from the 65 preflight-selected PAPER_ELIGIBLE "
        "records, validate the blueprint, render the final PDF, and obtain named-human "
        "technical and visual signoff. Release and sale remain blocked."
    )

    outputs[FAMILY_REGISTRY] = serialized(family_registry)
    outputs[PROGRESS] = serialized(progress)
    for path, data in outputs.items():
        atomic_bytes_write(path, data)

    print("GATE EE BATCHES 004-005 PAPER-ELIGIBILITY PROMOTION: PASSED")
    for batch_id in sorted(states):
        state = states[batch_id]
        print(
            f"{batch_id}: {len(state['approved'])} certified / "
            f"{len(state['revise'])} revise / {len(state['reject'])} reject"
        )
    print(f"Newly certified: {total_newly_approved}")
    print(f"Corpus V1 admitted total: {admitted_total}")
    print("Complete/released papers: 0/0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
