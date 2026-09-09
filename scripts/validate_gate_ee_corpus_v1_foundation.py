from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"
errors: list[str] = []


def load(path: Path) -> dict:
    if not path.exists():
        errors.append(f"MISSING: {path.relative_to(ROOT)}")
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


topic = load(BASE / "TOPIC_MAP_V1.json")
blueprint = load(ROOT / "blueprints/GATE_EE_SET_01_V1.json")
schema = load(ROOT / "schemas/GATE_EE_CORPUS_V1.schema.json")
family_registry = load(BASE / "families/FAMILY_REGISTRY.json")
review = load(BASE / "review_manifests/REVIEW_TEMPLATE.json")

if topic and sum(row["target"] for row in topic["domains"]) != topic["target_questions"]:
    errors.append("Topic-map allocation does not equal corpus target.")
if topic and topic.get("target_questions") != 220:
    errors.append("Corpus target must be 220.")
if blueprint and blueprint.get("paper") != {"questions": 65, "marks": 100, "duration_minutes": 180}:
    errors.append("Set 01 paper contract mismatch.")
if blueprint and blueprint.get("release_gate") != "HUMAN_FINAL_QA_REQUIRED":
    errors.append("Human final QA gate missing.")
if schema and "family_id" not in schema.get("required", []):
    errors.append("family_id missing from schema.")
if review and "originality_checked" not in review.get("checks", {}):
    errors.append("Originality review gate missing.")
if family_registry and family_registry.get("corpus") != "GATE_EE_CORPUS_V1":
    errors.append("Family registry corpus mismatch.")

expected_families: dict[str, dict] = {}
all_admitted_ids: list[str] = []
admission_paths = sorted((BASE / "manifests").glob("BATCH_*_CORPUS_ADMISSION.json"))
for admission_path in admission_paths:
    admission = load(admission_path)
    batch_id = admission.get("batch_id")
    if not isinstance(batch_id, str):
        errors.append(f"{admission_path.name}: missing batch_id")
        continue
    families_path = BASE / "families" / f"{batch_id}_FAMILIES.json"
    batch_families = load(families_path)
    admitted_ids = admission.get("admitted_question_ids", [])
    if admission.get("status") != "ADMITTED_TO_CORPUS_V1":
        errors.append(f"{batch_id}: admission status mismatch")
    if admission.get("admitted_count") != len(admitted_ids):
        errors.append(f"{batch_id}: admission count mismatch")
    if len(admitted_ids) != len(set(admitted_ids)):
        errors.append(f"{batch_id}: duplicate admitted question ID")
    all_admitted_ids.extend(admitted_ids)

    coverage: list[str] = []
    admitted_set = set(admitted_ids)
    for row in batch_families.get("families", []):
        selected_ids = [qid for qid in row.get("question_ids", []) if qid in admitted_set]
        coverage.extend(selected_ids)
        if not selected_ids:
            continue
        family_id = row.get("family_id")
        if family_id in expected_families:
            errors.append(f"{batch_id}: family {family_id!r} collides with an earlier admission")
            continue
        expected_families[family_id] = {
            "question_ids": selected_ids,
            "admission_batch": batch_id,
        }
    if sorted(coverage) != sorted(admitted_ids):
        errors.append(f"{batch_id}: family map does not cover every admitted ID exactly once")

global_rows = family_registry.get("families", [])
global_family_ids = [row.get("family_id") for row in global_rows]
if len(global_family_ids) != len(set(global_family_ids)):
    errors.append("Duplicate family IDs in the global family registry.")
global_map = {
    row.get("family_id"): {
        "question_ids": row.get("question_ids"),
        "admission_batch": row.get("admission_batch"),
    }
    for row in global_rows
}
if global_map != expected_families:
    errors.append("Global family registry does not exactly match all Corpus V1 admissions.")
registered_ids = [qid for row in global_rows for qid in row.get("question_ids", [])]
if len(registered_ids) != len(set(registered_ids)):
    errors.append("A question ID appears more than once in the global family registry.")
if sorted(registered_ids) != sorted(all_admitted_ids):
    errors.append("Global family registry does not cover every admitted question ID.")
if family_registry.get("admitted_question_count") != len(all_admitted_ids):
    errors.append("Global admitted-question count mismatch.")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("GATE EE CORPUS V1 FOUNDATION: PASSED")
print("Master pool target: 220")
print("Set 01 contract: 65 questions / 100 marks / 180 minutes")
print("Human final QA gate: REQUIRED")
print(f"Corpus V1 admitted questions: {len(all_admitted_ids)}")
