from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    pattern = load_json("references/GATE_2027/GATE_2027_EE_PATTERN.json")
    syllabus = load_json("references/GATE_2027/GATE_2027_EE_SYLLABUS.json")
    ga = load_json("references/GATE_2027/GATE_2027_GA_SYLLABUS.json")
    blueprint = load_json("blueprints/GATE_EE_SET_01_V1.json")
    program = load_json("blueprints/GATE_EE_50_SET_PROGRAM_V1.json")
    topic_map = load_json("GATE_EE/corpus_v1/TOPIC_MAP_V1.json")

    if (pattern["total_questions"], pattern["total_marks"], pattern["duration_minutes"]) != (65, 100, 180):
        errors.append("Official paper totals must be 65 questions, 100 marks and 180 minutes.")
    if pattern["section_contract"]["General Aptitude"] != {
        "questions": 10, "marks": 15, "one_mark_questions": 5, "two_mark_questions": 5
    }:
        errors.append("General Aptitude contract mismatch.")
    selected = pattern["section_contract"]["Selected Subject"]
    if (selected["questions"], selected["marks"], selected["one_mark_questions"], selected["two_mark_questions"]) != (55, 85, 25, 30):
        errors.append("Selected-subject contract mismatch.")
    if selected["includes"] != {"Engineering Mathematics": 13, "Electrical Engineering": 72}:
        errors.append("EE mark distribution mismatch.")
    if pattern["derived_whole_paper_mark_counts"] != {
        "one_mark_questions": 30,
        "two_mark_questions": 35,
        "derivation": "With 65 questions carrying only 1 or 2 marks and totaling 100 marks, the exact counts are 30 one-mark and 35 two-mark questions."
    }:
        errors.append("Whole-paper one/two-mark counts mismatch.")

    section_names = [section["name"] for section in syllabus["sections"]]
    expected_sections = [
        "Engineering Mathematics", "Electric Circuits", "Electromagnetic Fields",
        "Signals and Systems", "Electrical Machines", "Power Systems",
        "Control Systems", "Electrical and Electronic Measurements",
        "Analog and Digital Electronics", "Power Electronics",
    ]
    if section_names != expected_sections:
        errors.append("EE syllabus section sequence mismatch.")
    em_topics = set(syllabus["sections"][0]["topics"])
    if "Numerical Methods" in em_topics:
        errors.append("XE0 Numerical Methods leaked into the GATE EE syllabus.")
    if len(ga["sections"]) != 4:
        errors.append("GA syllabus must contain four official sections.")
    if blueprint.get("reference") != "blueprints/GATE_EE_2027_REFERENCE.json":
        errors.append("Set 01 does not point to the GATE 2027 reference.")

    if program["set_count"] * program["questions_per_set"] != program["question_slots"]:
        errors.append("50-set slot calculation mismatch.")
    if sum(program["qualified_pool_allocation"].values()) != program["recommended_qualified_pool"]:
        errors.append("50-set qualified-pool allocation mismatch.")
    if sum(program["eight_day_draft_throughput"]) != program["recommended_qualified_pool"]:
        errors.append("Eight-day draft quota mismatch.")
    if sum(item["target"] for item in topic_map["domains"]) != topic_map["target_questions"]:
        errors.append("Corpus V1 allocation mismatch.")

    allowed_by_subject = {
        "Engineering Mathematics": em_topics,
    }
    source = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
    questions = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    for question in questions:
        allowed = allowed_by_subject.get(question.get("subject"))
        if allowed is None or question.get("topic") not in allowed:
            errors.append(f"{question.get('id', '?')}: topic is outside the official GATE 2027 EE scope.")

    manifest = load_json("GATE_EE/corpus_v1/manifests/BATCH_001_MANIFEST.json")
    actual_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    if manifest.get("jsonl_sha256") != actual_sha:
        errors.append("Batch 001 manifest checksum is stale.")

    if errors:
        print("GATE 2027 EE CONTRACT: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GATE 2027 EE CONTRACT: PASSED")
    print("Official pattern: 65 questions / 100 marks / 180 minutes")
    print("Sections: 10 GA questions + 55 selected-subject questions")
    print("Marks: 15 GA + 13 Engineering Mathematics + 72 core EE")
    print("50-set requirement: 3250 unique slots; 3575 with 10% reserve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

