from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
MARKDOWN = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_002_ELECTRIC_CIRCUITS.md"
MANIFEST = ROOT / "GATE_EE/corpus_v1/manifests/BATCH_002_MANIFEST.json"
HANDOFF = ROOT / "GATE_EE/corpus_v1/formatter_handoff/BATCH_002_FORMATTER_V2_HANDOFF.json"
FAMILIES = ROOT / "GATE_EE/corpus_v1/families/BATCH_002_FAMILIES.json"
GLOBAL_FAMILIES = ROOT / "GATE_EE/corpus_v1/families/FAMILY_REGISTRY.json"
TOPIC_MAP = ROOT / "GATE_EE/corpus_v1/TOPIC_MAP_V1.json"
FORMATTER_EVIDENCE = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_FORMATTER_FINAL_EVIDENCE.json"
INDEPENDENT_QA = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_INDEPENDENT_AI_QA.json"
CERTIFICATE = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_PAPER_ELIGIBILITY_CERTIFICATE.json"
ADMISSION = ROOT / "GATE_EE/corpus_v1/manifests/BATCH_002_CORPUS_ADMISSION.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


errors: list[str] = []
questions: list[dict] = []
for line_number, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
        continue
    try:
        questions.append(json.loads(line))
    except json.JSONDecodeError as exc:
        errors.append(f"line {line_number}: invalid JSON: {exc}")

required = {
    "id", "exam", "subject", "topic", "subtopic", "concept", "difficulty",
    "type", "marks", "estimated_time_seconds", "stem", "answer", "solution",
    "family_id", "revision", "status", "provenance", "review",
}
ids: list[str] = []
families: list[str] = []
topic_map = load(TOPIC_MAP)
nt_domain = next((row for row in topic_map.get("domains", []) if row.get("code") == "NT"), {})
allowed_subtopics = set(nt_domain.get("topics", []))


ASCII_MATH_PATTERNS = (
    ("ASCII unit name", re.compile(r"\b(?:microfarads?|kilo-ohms?|ohms?)\b", re.I)),
    ("ASCII math function", re.compile(r"\b(?:sqrt|sin|cos|tan|ln|exp)\s*\(", re.I)),
    ("ASCII multiplication", re.compile(r"(?<=\d)\s+x\s+(?=\d)", re.I)),
    ("ASCII fraction", re.compile(r"\b\d+\s*/\s*\d+\b")),
    ("undelimited subscript/power", re.compile(r"[A-Za-z0-9][_^][A-Za-z0-9({-]")),
    ("undelimited electrical value", re.compile(r"\b\d+(?:\.\d+)?\s*(?:V|A|H|F|W|J|kW|kVA|kVAr|mH|mJ|rad/s)\b")),
)


def math_source_violations(question: dict) -> tuple[int, list[str]]:
    values = [str(question.get("stem", "")), str(question.get("solution", ""))]
    values.extend(str(option) for option in question.get("options", []))
    math_segments = 0
    violations: list[str] = []
    for value in values:
        parts = re.split(r"(?<!\\)\$", value)
        if len(parts) % 2 == 0:
            violations.append("unbalanced inline-math delimiter")
            continue
        math_segments += (len(parts) - 1) // 2
        outside_math = " ".join(parts[::2])
        for label, pattern in ASCII_MATH_PATTERNS:
            if pattern.search(outside_math):
                violations.append(label)
    return math_segments, sorted(set(violations))

for question in questions:
    qid = question.get("id", "?")
    missing = sorted(required - question.keys())
    if missing:
        errors.append(f"{qid}: missing fields {', '.join(missing)}")
    if not re.fullmatch(r"TMB-GATE-EE-NT-\d{3}", str(qid)):
        errors.append(f"{qid}: invalid Batch 002 ID")
    ids.append(str(qid))
    families.append(str(question.get("family_id", "")))
    if question.get("exam") != "GATE_EE": errors.append(f"{qid}: wrong exam")
    if question.get("subject") != "Electrical Engineering": errors.append(f"{qid}: wrong subject")
    if question.get("topic") != "Electric Circuits": errors.append(f"{qid}: wrong topic")
    if question.get("subtopic") not in allowed_subtopics: errors.append(f"{qid}: out-of-map subtopic")
    if question.get("difficulty") not in {"Easy", "Medium", "Hard"}: errors.append(f"{qid}: invalid difficulty")
    if question.get("type") not in {"MCQ", "MSQ", "NAT"}: errors.append(f"{qid}: invalid type")
    if question.get("marks") not in {1, 2}: errors.append(f"{qid}: invalid marks")
    if question.get("status") != "DRAFT": errors.append(f"{qid}: source must remain DRAFT")
    if question.get("revision") != 2: errors.append(f"{qid}: render-quality revision must be 2")
    if question.get("provenance", {}).get("originality") != "ORIGINAL_THEMITBRO":
        errors.append(f"{qid}: originality provenance missing")

    qtype = question.get("type")
    answer = question.get("answer")
    options = question.get("options")
    if qtype == "MCQ":
        if not isinstance(options, list) or len(options) != 4: errors.append(f"{qid}: MCQ requires four options")
        if answer not in {"A", "B", "C", "D"}: errors.append(f"{qid}: invalid MCQ answer")
    elif qtype == "MSQ":
        if not isinstance(options, list) or len(options) != 4: errors.append(f"{qid}: MSQ requires four options")
        if not isinstance(answer, list) or not answer or len(answer) != len(set(answer)) or any(x not in "ABCD" for x in answer):
            errors.append(f"{qid}: invalid MSQ answer")
    elif qtype == "NAT":
        if "options" in question: errors.append(f"{qid}: NAT must not contain options")
        if not isinstance(answer, (int, float)): errors.append(f"{qid}: NAT answer must be numeric")
        if not isinstance(question.get("nat_tolerance"), (int, float)) or question.get("nat_tolerance", -1) < 0:
            errors.append(f"{qid}: NAT tolerance is missing or invalid")

    markers = re.findall(r"(?m)^Final answer:\s*([^\n]+)$", str(question.get("solution", "")))
    expected = ", ".join(answer) if isinstance(answer, list) else str(answer)
    if markers != [expected]: errors.append(f"{qid}: final-answer marker does not match structured answer")
    math_segments, math_violations = math_source_violations(question)
    if math_violations:
        errors.append(f"{qid}: canonical mathematics contract failed: {', '.join(math_violations)}")
    question["_math_segment_count"] = math_segments

expected_ids = [f"TMB-GATE-EE-NT-{index:03d}" for index in range(1, 21)]
if len(questions) != 20: errors.append(f"expected 20 questions, found {len(questions)}")
if ids != expected_ids: errors.append("Batch 002 ID sequence mismatch")
if len(families) != len(set(families)): errors.append("duplicate family inside Batch 002")
if sum(question.get("_math_segment_count", 0) > 0 for question in questions) < 19:
    errors.append("Batch 002 must contain canonical LaTeX mathematics in at least 19 questions")

source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
manifest = load(MANIFEST)
handoff = load(HANDOFF)
batch_family = load(FAMILIES)
global_family = load(GLOBAL_FAMILIES)

if manifest.get("question_count") != len(questions): errors.append("manifest question count mismatch")
if manifest.get("jsonl_sha256") != source_sha: errors.append("manifest checksum mismatch")
certificate_exists = CERTIFICATE.exists()
admission_exists = ADMISSION.exists()
if certificate_exists != admission_exists:
    errors.append("Batch 002 certificate and admission manifest must exist together")
eligible_count = 0
admitted_ids: list[str] = []
if certificate_exists and admission_exists:
    certificate = load(CERTIFICATE)
    admission = load(ADMISSION)
    eligible_count = certificate.get("paper_eligible_count", 0)
    admitted_ids = admission.get("admitted_question_ids", [])
    if certificate.get("source_sha256") != source_sha: errors.append("certificate source checksum mismatch")
    if admission.get("source_sha256") != source_sha: errors.append("admission source checksum mismatch")
    if admitted_ids != certificate.get("approved_question_ids"):
        errors.append("admission IDs do not match the paper-eligibility certificate")
    if admission.get("admitted_count") != eligible_count:
        errors.append("admission count does not match the paper-eligibility certificate")
    if manifest.get("status") != "PAPER_ELIGIBILITY_CERTIFIED_AND_ADMITTED":
        errors.append("certified Batch 002 manifest status is stale")
else:
    if manifest.get("status") != "READY_FOR_HUMAN_FINAL_QA":
        errors.append("pre-promotion Batch 002 manifest status mismatch")
if manifest.get("paper_eligible_count") != eligible_count:
    errors.append("manifest paper-eligible count does not match certification state")
if handoff.get("source_sha256") != source_sha: errors.append("Formatter handoff checksum mismatch")
if handoff.get("question_count") != len(questions): errors.append("Formatter handoff count mismatch")
if handoff.get("formatter_required_version") != "2.0.0": errors.append("Formatter version contract mismatch")

expected_counts = {
    "type_counts": dict(Counter(str(q["type"]) for q in questions)),
    "marks_counts": dict(Counter(str(q["marks"]) for q in questions)),
    "difficulty_counts": dict(Counter(str(q["difficulty"]) for q in questions)),
    "subtopics": dict(Counter(str(q["subtopic"]) for q in questions)),
}
for field, expected in expected_counts.items():
    if manifest.get(field) != expected: errors.append(f"manifest {field} mismatch")

family_map = {
    row.get("family_id"): row.get("question_ids")
    for row in batch_family.get("families", [])
}
if set(family_map) != set(families): errors.append("Batch 002 family file does not match source families")
for question in questions:
    if family_map.get(question["family_id"]) != [question["id"]]:
        errors.append(f"{question['id']}: family mapping mismatch")
admitted_families = {row.get("family_id") for row in global_family.get("families", [])}
collision = admitted_families.intersection(families)
if certificate_exists and admission_exists:
    approved_set = set(admitted_ids)
    expected_admitted_family_map = {
        row.get("family_id"): [qid for qid in row.get("question_ids", []) if qid in approved_set]
        for row in batch_family.get("families", [])
        if any(qid in approved_set for qid in row.get("question_ids", []))
    }
    found_admitted_family_map = {
        row.get("family_id"): row.get("question_ids")
        for row in global_family.get("families", [])
        if row.get("admission_batch") == "BATCH_002"
    }
    if found_admitted_family_map != expected_admitted_family_map:
        errors.append("admitted Batch 002 families do not match the global family registry")
else:
    if collision: errors.append(f"Batch 002 collides with admitted families: {sorted(collision)}")

markdown = MARKDOWN.read_text(encoding="utf-8")
if any(markdown.count(qid) != 1 for qid in expected_ids):
    errors.append("deterministic Markdown view does not contain every Batch 002 ID exactly once")

if FORMATTER_EVIDENCE.exists():
    evidence = load(FORMATTER_EVIDENCE)
    if evidence.get("source_sha256") != source_sha: errors.append("Formatter evidence checksum mismatch")
    if evidence.get("question_count") != 20: errors.append("Formatter evidence count mismatch")
    if manifest.get("formatter_evidence_sha256") != hashlib.sha256(FORMATTER_EVIDENCE.read_bytes()).hexdigest():
        errors.append("manifest Formatter-evidence checksum mismatch")
if INDEPENDENT_QA.exists():
    independent = load(INDEPENDENT_QA)
    if independent.get("source_sha256") != source_sha: errors.append("independent-QA checksum mismatch")
    if manifest.get("independent_ai_qa_sha256") != hashlib.sha256(INDEPENDENT_QA.read_bytes()).hexdigest():
        errors.append("manifest independent-QA evidence checksum mismatch")
    if manifest.get("status") not in {
        "READY_FOR_HUMAN_FINAL_QA",
        "PAPER_ELIGIBILITY_CERTIFIED_AND_ADMITTED",
    }:
        errors.append("manifest status does not reflect the supported qualification lifecycle")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("GATE EE PRODUCTION BATCH 002: PASSED")
print("Questions: 20")
print("Domain: Electric Circuits")
print("IDs: TMB-GATE-EE-NT-001..020")
print(f"Source SHA-256: {source_sha}")
print(f"Paper-eligible: {eligible_count}")
print("Manifest, family and Formatter handoff consistency: PASSED")
