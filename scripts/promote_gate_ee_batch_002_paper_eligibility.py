from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_gate_ee_batch_002_human_signoff import validate


BASE = ROOT / "GATE_EE/corpus_v1"
SOURCE = BASE / "source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
FORMATTER = BASE / "qualification/BATCH_002_FORMATTER_FINAL_EVIDENCE.json"
QA = BASE / "qualification/BATCH_002_INDEPENDENT_AI_QA.json"
HUMAN = BASE / "review_manifests/BATCH_002_HUMAN_FINAL_QA.json"
CANDIDATE = BASE / "qualification/BATCH_002_PAPER_ELIGIBILITY_CANDIDATE.json"
SUMMARY = BASE / "qualification/BATCH_002_QUALIFICATION_SUMMARY.json"
CERTIFICATE = BASE / "qualification/BATCH_002_PAPER_ELIGIBILITY_CERTIFICATE.json"
ADMISSION = BASE / "manifests/BATCH_002_CORPUS_ADMISSION.json"
MANIFEST = BASE / "manifests/BATCH_002_MANIFEST.json"
BATCH_FAMILIES = BASE / "families/BATCH_002_FAMILIES.json"
FAMILY_REGISTRY = BASE / "families/FAMILY_REGISTRY.json"
PROGRESS = BASE / "production/EIGHT_DAY_PROGRESS.json"
BATCH1_CERTIFICATE = BASE / "qualification/BATCH_001_PAPER_ELIGIBILITY_CERTIFICATE.json"
BATCH1_ADMISSION = BASE / "manifests/BATCH_001_CORPUS_ADMISSION.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def serialized(payload: dict) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def block(errors: list[str]) -> None:
    print("BATCH 002 PAPER-ELIGIBILITY PROMOTION: BLOCKED")
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


def main() -> int:
    errors, approved, revise, reject, source_sha = validate(require_complete=True)
    if errors:
        block(errors)

    human = load(HUMAN)
    candidate = load(CANDIDATE)
    summary = load(SUMMARY)
    manifest = load(MANIFEST)
    batch_families = load(BATCH_FAMILIES)
    family_registry = load(FAMILY_REGISTRY)
    progress = load(PROGRESS)
    questions = [
        json.loads(line)
        for line in SOURCE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected_ids = [question["id"] for question in questions]

    preflight: list[str] = []
    if summary.get("current_stage") != "READY_FOR_HUMAN_FINAL_QA":
        preflight.append("promotion requires current_stage READY_FOR_HUMAN_FINAL_QA")
    if CERTIFICATE.exists() or ADMISSION.exists():
        preflight.append("certificate/admission already exists; refusing to overwrite a certification event")
    if sorted(approved + revise + reject) != sorted(expected_ids):
        preflight.append("human decisions do not partition the canonical source IDs")
    if candidate.get("candidate_question_ids") != expected_ids:
        preflight.append("paper-eligibility candidate list is stale")
    if preflight:
        block(preflight)

    batch_rows = batch_families.get("families", [])
    batch_family_ids = [row.get("family_id") for row in batch_rows]
    batch_question_ids = [qid for row in batch_rows for qid in row.get("question_ids", [])]
    if len(batch_family_ids) != len(set(batch_family_ids)):
        preflight.append("Batch 002 family file contains duplicate family IDs")
    if sorted(batch_question_ids) != sorted(expected_ids):
        preflight.append("Batch 002 family file does not cover the canonical source exactly once")

    global_rows = family_registry.get("families", [])
    global_family_ids = {row.get("family_id") for row in global_rows}
    global_question_ids = {qid for row in global_rows for qid in row.get("question_ids", [])}
    family_collision = sorted(global_family_ids.intersection(batch_family_ids))
    question_collision = sorted(global_question_ids.intersection(expected_ids))
    if family_collision: preflight.append(f"family collision with Corpus V1: {family_collision}")
    if question_collision: preflight.append(f"question-ID collision with Corpus V1: {question_collision}")
    if family_registry.get("admitted_question_count") != len(global_question_ids):
        preflight.append("existing global admitted-question count is inconsistent")
    if len(global_question_ids) != sum(len(row.get("question_ids", [])) for row in global_rows):
        preflight.append("existing global family registry contains a duplicate admitted question ID")
    if preflight:
        block(preflight)

    signoff_sha = hashlib.sha256(HUMAN.read_bytes()).hexdigest()
    formatter_sha = hashlib.sha256(FORMATTER.read_bytes()).hexdigest()
    qa_sha = hashlib.sha256(QA.read_bytes()).hexdigest()
    review_date = human["reviewer"]["review_date"]

    candidate.update(
        {
            "human_final_qa": "COMPLETE",
            "certified_paper_eligible_question_ids": approved,
            "paper_eligible_count": len(approved),
            "release_gate": "PAPER_ELIGIBILITY_CERTIFIED",
            "human_signoff_sha256": signoff_sha,
        }
    )

    certificate = {
        "certificate_contract": "GATE_EE_BATCH002_PAPER_ELIGIBILITY_CERTIFICATE_V1",
        "batch_id": "BATCH_002",
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
        "manifest_contract": "GATE_EE_CORPUS_V1_BATCH002_ADMISSION_V1",
        "batch_id": "BATCH_002",
        "source_sha256": source_sha,
        "paper_eligibility_certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "admitted_question_ids": approved,
        "held_for_revision_question_ids": revise,
        "rejected_question_ids": reject,
        "admitted_count": len(approved),
        "status": "ADMITTED_TO_CORPUS_V1",
    }

    summary.update(
        {
            "qualification_version": "1.1.0",
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
                "Use admitted questions only for controlled blueprint selection; continue Day-1 "
                "authoring until a complete 65-question, 100-mark paper can satisfy every section gate."
            ),
        }
    )

    manifest.update(
        {
            "manifest_version": "1.1.0",
            "status": "PAPER_ELIGIBILITY_CERTIFIED_AND_ADMITTED",
            "paper_eligible_count": len(approved),
            "qualification_note": (
                f"Revision 2. Strict Formatter: 20 PASS / 0 REVIEW / 0 invalid. Independent AI "
                f"technical/answer/solution recomputation: 20/20 PASS and not a human substitute. "
                f"Named human final QA: {len(approved)} PASS / {len(revise)} REVISE / "
                f"{len(reject)} REJECT. Approved IDs are certificate-bound and admitted to Corpus "
                "V1; no complete paper is released."
            ),
        }
    )

    batch_families["registry_version"] = "1.1.0"
    batch_families["admission_status"] = "ADMITTED_TO_CORPUS_V1"
    approved_set = set(approved)
    admitted_family_rows: list[dict] = []
    for row in batch_rows:
        admitted_ids = [qid for qid in row["question_ids"] if qid in approved_set]
        if admitted_ids:
            admitted_family_rows.append(
                {
                    "family_id": row["family_id"],
                    "question_ids": admitted_ids,
                    "admission_batch": "BATCH_002",
                }
            )
    family_registry["registry_version"] = "1.1.0"
    family_registry["families"] = global_rows + admitted_family_rows
    family_registry["admitted_question_count"] = sum(
        len(row.get("question_ids", [])) for row in family_registry["families"]
    )

    batch1_certificate = load(BATCH1_CERTIFICATE)
    batch1_admission = load(BATCH1_ADMISSION)
    total_eligible = batch1_certificate.get("paper_eligible_count", 0) + len(approved)
    total_admitted = batch1_admission.get("admitted_count", 0) + len(approved)
    progress["as_of"] = review_date
    progress["program_inventory"].update(
        {
            "human_final_qa_passed": total_eligible,
            "paper_eligible": total_eligible,
            "corpus_admitted": total_admitted,
            "complete_65_question_sets": 0,
            "released_sets": 0,
        }
    )
    progress["next_gate"] = (
        "Continue the remaining Day-1 draft allocation and admit only independently reviewed, "
        "checksum-bound questions; Set 01 remains blocked until its exact blueprint is complete."
    )

    outputs = {
        CANDIDATE: serialized(candidate),
        CERTIFICATE: certificate_bytes,
        ADMISSION: serialized(admission),
        SUMMARY: serialized(summary),
        MANIFEST: serialized(manifest),
        BATCH_FAMILIES: serialized(batch_families),
        FAMILY_REGISTRY: serialized(family_registry),
        PROGRESS: serialized(progress),
    }
    for path, data in outputs.items():
        atomic_bytes_write(path, data)

    print("BATCH 002 PAPER-ELIGIBILITY PROMOTION: PASSED")
    print(f"Certified paper-eligible: {len(approved)}")
    print(f"Held for revision: {len(revise)}")
    print(f"Rejected: {len(reject)}")
    print(f"Corpus V1 admitted total: {family_registry['admitted_question_count']}")
    print("Complete/released papers: 0/0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
