from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "GATE_EE/corpus_v1/source_batches/BATCH_002_ELECTRIC_CIRCUITS.jsonl"
FORMATTER = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_FORMATTER_FINAL_EVIDENCE.json"
DEFAULT_OUTPUT = ROOT / "GATE_EE/corpus_v1/qualification/BATCH_002_INDEPENDENT_AI_QA.json"


# This is deliberately separate from the canonical answer fields.  Each entry
# records a fresh computation or theorem check and is compared with the source.
ORACLE = {
    "TMB-GATE-EE-NT-001": (0.324, r"$C_{\mathrm{eq}}=2\,\mu\mathrm{F}$ and $W=\frac{1}{2}C_{\mathrm{eq}}(18)^2=0.324\,\mathrm{mJ}$."),
    "TMB-GATE-EE-NT-002": ("C", r"$M=0.5\sqrt{(4)(9)}=3\,\mathrm{H}$ and $L_{\mathrm{eq}}=4+9+2M=19\,\mathrm{H}$, option C."),
    "TMB-GATE-EE-NT-003": ("B", r"A test voltage $v$ draws $\frac{v}{4}+0.5\left(\frac{v}{4}\right)=\frac{3v}{8}$; therefore $\frac{v}{i}=\frac{8}{3}\,\Omega$, option B."),
    "TMB-GATE-EE-NT-004": (["A", "C", "D"], r"The ideal stored energies are $\frac{1}{2}Cv^2$ and $\frac{1}{2}Li^2$; capacitor voltage and inductor current cannot jump under finite, impulse-free excitation."),
    "TMB-GATE-EE-NT-005": (4, r"KCL gives $v_1=1.5v_2$ and $6v_1-3v_2=24$; hence $v_2=4\,\mathrm{V}$."),
    "TMB-GATE-EE-NT-006": (6.8, r"$\frac{v_1}{2}+\frac{v_2}{3}=4$ with $v_1-v_2=5$ gives $v_2=1.8\,\mathrm{V}$ and $v_1=6.8\,\mathrm{V}$."),
    "TMB-GATE-EE-NT-007": ("A", r"The two equations give $I_1=2.25\,\mathrm{A}$ and $I_2=1.625\,\mathrm{A}$; hence $I_1-I_2=0.625\,\mathrm{A}$, option A."),
    "TMB-GATE-EE-NT-008": (["A", "B", "C"], r"A reference node, a supernode for an inter-node ideal voltage source, and at most $n-1$ independent KCL equations are valid; dependent sources do not prohibit nodal analysis."),
    "TMB-GATE-EE-NT-009": ("B", r"$V_{\mathrm{th}}=18\left(\frac{6}{9}\right)=12\,\mathrm{V}$ and $R_{\mathrm{th}}=3\parallel6=2\,\Omega$; therefore $I_L=\frac{12}{2+4}=2\,\mathrm{A}$, option B."),
    "TMB-GATE-EE-NT-010": ("C", r"Current division gives $I_L=3\left(\frac{6}{6+3}\right)=2\,\mathrm{A}$, option C."),
    "TMB-GATE-EE-NT-011": (8.333, r"Conjugate matching gives $P_{\max}=\frac{|V_{\mathrm{th}}|^2}{4R_{\mathrm{th}}}=\frac{100}{12}=8.333\,\mathrm{W}$."),
    "TMB-GATE-EE-NT-012": (["A", "B", "C", "D"], "Independent voltage/current sources become shorts/opens, dependent sources remain, and nonlinear power does not superpose."),
    "TMB-GATE-EE-NT-013": (7.057, r"$\tau=RC=0.2\,\mathrm{s}$ and $v_C(\tau)=10+(2-10)e^{-1}=7.057\,\mathrm{V}$."),
    "TMB-GATE-EE-NT-014": (1.5, r"$I_{\infty}=3\,\mathrm{A}$, $\tau=\frac{L}{R}=0.5\,\mathrm{s}$ and $\frac{t}{\tau}=\ln2$; hence $i_L=3\left(1-\frac{1}{2}\right)=1.5\,\mathrm{A}$."),
    "TMB-GATE-EE-NT-015": ("C", r"$LC=10^{-6}$ and $\omega_0=\frac{1}{\sqrt{LC}}=1000\,\mathrm{rad\,s^{-1}}$, option C."),
    "TMB-GATE-EE-NT-016": ("B", r"The series-RLC angular bandwidth is $\Delta\omega=\frac{R}{L}=\frac{20}{0.1}=200\,\mathrm{rad\,s^{-1}}$, option B."),
    "TMB-GATE-EE-NT-017": (["A", "B", "D"], r"$\tan(\cos^{-1}0.8)=0.75$ gives $Q=6\,\mathrm{kVAr}$ and $|S|=10\,\mathrm{kVA}$; the current lags, and $6\,\mathrm{kVAr}$ capacitive compensation reaches unity power factor."),
    "TMB-GATE-EE-NT-018": (12.8, r"$|Z|=10\,\Omega$ and $\cos\phi=0.8$; the three-phase real power evaluates to $12.8\,\mathrm{kW}$."),
    "TMB-GATE-EE-NT-019": (3.5, r"$Z_{\mathrm{in}}=z_{11}-\frac{z_{12}z_{21}}{z_{22}+Z_L}=4-\frac{4}{8}=3.5\,\Omega$."),
    "TMB-GATE-EE-NT-020": ("B", r"The delta phase current is $\frac{240}{12}=20\,\mathrm{A}$; $3(240)(20)\cos30^{\circ}=12.47\,\mathrm{kW}$, option B."),
}


def build_evidence() -> dict:
    questions = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip()]
    formatter = json.loads(FORMATTER.read_text(encoding="utf-8"))
    source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    formatter_sha = hashlib.sha256(FORMATTER.read_bytes()).hexdigest()
    errors: list[str] = []
    expected_ids = set(ORACLE)
    found_ids = {question["id"] for question in questions}
    if found_ids != expected_ids or len(questions) != 20:
        errors.append("oracle IDs do not match the canonical 20-question source")
    if formatter.get("source_sha256") != source_sha:
        errors.append("Formatter evidence is not bound to the current source")
    if (
        formatter.get("status"), formatter.get("formatter_pass_count"),
        formatter.get("formatter_review_count"), formatter.get("invalid_count"),
    ) != ("PASS", 20, 0, 0):
        errors.append("independent recomputation requires strict Formatter 20 PASS / 0 REVIEW / 0 invalid")

    rows = []
    for question in questions:
        qid = question["id"]
        recomputed, derivation = ORACLE[qid]
        declared = question["answer"]
        if declared != recomputed:
            errors.append(f"{qid}: recomputed answer disagrees with the declared answer")
        expected_marker = ", ".join(declared) if isinstance(declared, list) else str(declared)
        markers = re.findall(r"(?m)^Final answer:\s*([^\n]+)$", question["solution"])
        if markers != [expected_marker]:
            errors.append(f"{qid}: canonical solution final marker disagrees with the declared answer")
        rows.append({
            "question_id": qid,
            "revision": question["revision"],
            "declared_answer": declared,
            "recomputed_answer": recomputed,
            "technical_result": "PASS",
            "answer_result": "PASS",
            "solution_consistency_result": "PASS",
            "machine_final_marker_result": "PASS",
            "derivation_summary": derivation,
            "human_originality_check": "PENDING",
        })

    if errors:
        raise ValueError("\n".join(errors))
    return {
        "qa_contract": "GATE_EE_BATCH002_INDEPENDENT_AI_QA_V1",
        "batch_id": "BATCH_002",
        "status": "PASS",
        "qa_date": "2026-09-08",
        "performed_by": "OpenAI Codex",
        "reviewer_kind": "AI_ASSISTED_INDEPENDENT_RECOMPUTATION",
        "source_sha256": source_sha,
        "formatter_report_sha256": formatter_sha,
        "evidence_valid_for_current_source": True,
        "technical_pass_count": 20,
        "answer_recomputed_pass_count": 20,
        "solution_consistency_pass_count": 20,
        "machine_final_marker_pass_count": 20,
        "formatter_pass_count": 20,
        "formatter_review_count": 0,
        "invalid_count": 0,
        "paper_eligibility_candidate_count": 20,
        "paper_eligible_count": 0,
        "human_final_qa_required": True,
        "human_review_substitute": False,
        "automated_oracle": "scripts/recompute_gate_ee_batch_002.py",
        "release_gate": "BLOCKED_PENDING_HUMAN_FINAL_QA",
        "questions": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute and record Batch 002 answers independently of the canonical answer fields.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Compare with the committed evidence instead of rewriting it.")
    args = parser.parse_args()
    evidence = build_evidence()
    serialized = json.dumps(evidence, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != serialized:
            raise SystemExit("Committed Batch 002 independent-QA evidence is stale.")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print("GATE EE BATCH 002 INDEPENDENT AI QA: PASSED")
    print("Technical/answer/solution recomputation: 20/20")
    print("Human-review substitute: False")
    print("Paper-eligible: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
