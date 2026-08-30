from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f"MISSING: {rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

topic=load("GATE_EE/corpus_v1/TOPIC_MAP_V1.json")
bp=load("blueprints/GATE_EE_SET_01_V1.json")
schema=load("schemas/GATE_EE_CORPUS_V1.schema.json")
family=load("GATE_EE/corpus_v1/families/FAMILY_REGISTRY.json")
review=load("GATE_EE/corpus_v1/review_manifests/REVIEW_TEMPLATE.json")

if topic and sum(x["target"] for x in topic["domains"]) != topic["target_questions"]:
    errors.append("Topic-map allocation does not equal corpus target.")
if topic and topic.get("target_questions") != 220:
    errors.append("Corpus target must be 220.")
if bp and bp.get("paper") != {"questions":65,"marks":100,"duration_minutes":180}:
    errors.append("Set 01 paper contract mismatch.")
if bp and bp.get("release_gate") != "HUMAN_FINAL_QA_REQUIRED":
    errors.append("Human final QA gate missing.")
if schema and "family_id" not in schema.get("required",[]):
    errors.append("family_id missing from schema.")
if review and "originality_checked" not in review.get("checks",{}):
    errors.append("Originality review gate missing.")
if family and family.get("corpus") != "GATE_EE_CORPUS_V1":
    errors.append("Family registry corpus mismatch.")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("GATE EE CORPUS V1 FOUNDATION: PASSED")
print("Master pool target: 220")
print("Set 01 contract: 65 questions / 100 marks / 180 minutes")
print("Human final QA gate: REQUIRED")
