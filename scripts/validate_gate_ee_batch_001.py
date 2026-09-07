from pathlib import Path
from collections import Counter
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
batch=ROOT/"GATE_EE/corpus_v1/source_batches/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
errors=[]
qs=[]
for n,line in enumerate(batch.read_text(encoding="utf-8").splitlines(),1):
    try: q=json.loads(line)
    except Exception as e:
        errors.append(f"line {n}: invalid JSON: {e}"); continue
    qs.append(q)

required=["id","exam","subject","topic","subtopic","concept","difficulty","type","marks",
          "estimated_time_seconds","stem","answer","solution","family_id","revision","status","provenance","review"]
ids=set(); fams=set()
for q in qs:
    for k in required:
        if k not in q: errors.append(f"{q.get('id','?')}: missing {k}")
    qid=q.get("id","")
    if not re.fullmatch(r"TMB-GATE-EE-EM-\d{3}",qid): errors.append(f"{qid}: bad id")
    if qid in ids: errors.append(f"{qid}: duplicate id")
    ids.add(qid)
    fam=q.get("family_id")
    if fam in fams: errors.append(f"{qid}: duplicate family in Batch 001")
    fams.add(fam)
    if q.get("exam")!="GATE_EE": errors.append(f"{qid}: wrong exam")
    if q.get("subject")!="Engineering Mathematics": errors.append(f"{qid}: wrong subject")
    if q.get("type") not in {"MCQ","MSQ","NAT"}: errors.append(f"{qid}: bad type")
    if q.get("marks") not in {1,2}: errors.append(f"{qid}: bad marks")
    if q.get("difficulty") not in {"Easy","Medium","Hard"}: errors.append(f"{qid}: bad difficulty")
    if q.get("status")!="DRAFT": errors.append(f"{qid}: Batch 001 must remain DRAFT until independent review")
    if q.get("provenance",{}).get("originality")!="ORIGINAL_THEMITBRO": errors.append(f"{qid}: originality provenance missing")
    if q.get("type") in {"MCQ","MSQ"} and len(q.get("options",[]))!=4: errors.append(f"{qid}: requires four options")
    if q.get("type")=="NAT" and "options" in q: errors.append(f"{qid}: NAT must not contain options")
    if len(q.get("stem",""))<10 or len(q.get("solution",""))<10: errors.append(f"{qid}: content too short")
    markers=re.findall(r"(?m)^Final answer:\s*([^\n]+)$",q.get("solution",""))
    if len(markers)!=1: errors.append(f"{qid}: solution must contain exactly one Final answer marker")
    elif re.search(r"[$\\{}]",markers[0]): errors.append(f"{qid}: Final answer marker exposes source math markup")
    else:
        expected=", ".join(q.get("answer",[])) if isinstance(q.get("answer"),list) else str(q.get("answer"))
        if markers[0].strip()!=expected: errors.append(f"{qid}: Final answer marker disagrees with structured answer")

if len(qs)!=20: errors.append(f"expected 20 questions, got {len(qs)}")
expected_ids={f"TMB-GATE-EE-EM-{i:03d}" for i in range(1,21)}
if ids != expected_ids: errors.append("question ID sequence mismatch")

manifest=json.loads((ROOT/"GATE_EE/corpus_v1/manifests/BATCH_001_MANIFEST.json").read_text())
if manifest.get("question_count")!=20: errors.append("manifest count mismatch")
if manifest.get("paper_eligible_count")!=0: errors.append("unreviewed batch cannot be paper eligible")
if manifest.get("jsonl_sha256")!=hashlib.sha256(batch.read_bytes()).hexdigest(): errors.append("manifest source checksum mismatch")
expected_counts={
    "type_counts":dict(Counter(str(q["type"]) for q in qs)),
    "marks_counts":dict(Counter(str(q["marks"]) for q in qs)),
    "difficulty_counts":dict(Counter(str(q["difficulty"]) for q in qs)),
    "topics":dict(Counter(str(q["topic"]) for q in qs)),
}
for field,actual in expected_counts.items():
    if manifest.get(field)!=actual: errors.append(f"manifest {field} mismatch")

if errors:
    print("\n".join(errors)); raise SystemExit(1)

print("GATE EE PRODUCTION BATCH 001: PASSED")
print("Questions: 20")
print("Domain: Engineering Mathematics")
print("IDs: TMB-GATE-EE-EM-001..020")
print("Paper-eligible: 0 (independent review required)")
print("Machine-final markers and manifest consistency: PASSED")
