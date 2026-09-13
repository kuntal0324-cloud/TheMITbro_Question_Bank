"""Shared configuration for the Set 01 core-EE recovery batches."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "GATE_EE/corpus_v1"


@dataclass(frozen=True)
class RecoveryBatch:
    batch_id: str
    number: str
    code: str
    domain: str
    source_name: str
    markdown_name: str
    expected_count: int
    expected_one_mark: int
    expected_two_mark: int
    expected_visual: int
    allowed_subtopics: frozenset[str]
    carried_from_day: int

    @property
    def source(self) -> Path:
        return BASE / "source_batches" / self.source_name

    @property
    def markdown(self) -> Path:
        return BASE / "source_batches" / self.markdown_name

    @property
    def manifest(self) -> Path:
        return BASE / "manifests" / f"{self.batch_id}_MANIFEST.json"

    @property
    def handoff(self) -> Path:
        return BASE / "formatter_handoff" / f"{self.batch_id}_FORMATTER_V2_HANDOFF.json"

    @property
    def families(self) -> Path:
        return BASE / "families" / f"{self.batch_id}_FAMILIES.json"

    @property
    def formatter_evidence(self) -> Path:
        return BASE / "qualification" / f"{self.batch_id}_FORMATTER_FINAL_EVIDENCE.json"

    @property
    def independent_qa(self) -> Path:
        return BASE / "qualification" / f"{self.batch_id}_INDEPENDENT_AI_QA.json"

    @property
    def technical_review(self) -> Path:
        return BASE / "qualification" / f"{self.batch_id}_TECHNICAL_REVIEW.json"

    @property
    def summary(self) -> Path:
        return BASE / "qualification" / f"{self.batch_id}_QUALIFICATION_SUMMARY.json"

    @property
    def candidate(self) -> Path:
        return BASE / "qualification" / f"{self.batch_id}_PAPER_ELIGIBILITY_CANDIDATE.json"

    @property
    def human_qa(self) -> Path:
        return BASE / "review_manifests" / f"{self.batch_id}_HUMAN_FINAL_QA.json"

    @property
    def review_packet(self) -> Path:
        return BASE / "review_manifests" / f"{self.batch_id}_HUMAN_REVIEW_PACKET.md"

    @property
    def pdf(self) -> Path:
        return ROOT / "output/pdf" / f"GATE_EE_{self.batch_id.replace('_', '')}_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf"

    @property
    def attestation(self) -> str:
        label = self.batch_id.replace("BATCH_", "Batch ")
        return (
            f"I independently reviewed the {label} questions, answers and solutions "
            "and approve only the question IDs marked PASS below."
        )


BATCHES: dict[str, RecoveryBatch] = {
    "BATCH_004": RecoveryBatch(
        batch_id="BATCH_004",
        number="004",
        code="SS",
        domain="Signals and Systems",
        source_name="BATCH_004_SIGNALS_AND_SYSTEMS.jsonl",
        markdown_name="BATCH_004_SIGNALS_AND_SYSTEMS.md",
        expected_count=15,
        expected_one_mark=8,
        expected_two_mark=7,
        expected_visual=3,
        allowed_subtopics=frozenset({
            "Continuous and Discrete Signals",
            "LTI Systems and Convolution",
            "Fourier Analysis",
            "Laplace Transform",
            "Z Transform",
            "Sampling",
        }),
        carried_from_day=4,
    ),
    "BATCH_005": RecoveryBatch(
        batch_id="BATCH_005",
        number="005",
        code="EMFT",
        domain="Electromagnetic Fields",
        source_name="BATCH_005_ELECTROMAGNETIC_FIELDS.jsonl",
        markdown_name="BATCH_005_ELECTROMAGNETIC_FIELDS.md",
        expected_count=12,
        expected_one_mark=6,
        expected_two_mark=6,
        expected_visual=3,
        allowed_subtopics=frozenset({
            "Electrostatics",
            "Magnetostatics",
            "Magnetic Circuits",
            "Electromagnetic Induction",
        }),
        carried_from_day=4,
    ),
}


ORACLE: dict[str, tuple[Any, str]] = {
    "TMB-GATE-EE-SS-001": ("C", "The component angular frequencies have greatest common divisor $2\\,\\mathrm{rad/s}$, giving $T_0=\\pi\\,\\mathrm{s}$."),
    "TMB-GATE-EE-SS-002": (1.333, "The squared sequence is $(1/4)^n u[n]$, whose geometric sum is $4/3=1.333$."),
    "TMB-GATE-EE-SS-003": (["A", "C", "D"], "Multiplication by $t$ is linear, memoryless and causal, but a time shift does not commute with the multiplier."),
    "TMB-GATE-EE-SS-004": ("C", "Even symmetry gives $2\\int_0^2(2-t)^2dt=16/3$."),
    "TMB-GATE-EE-SS-005": (0.25, "Direct convolution gives $e^{-t}-e^{-2t}$ for $t\\geq0$ and hence $1/4$ at $t=\\ln2$."),
    "TMB-GATE-EE-SS-006": (3, "The LTI frequency-response magnitude at $2\\,\\mathrm{rad/s}$ is $3$, so the output amplitude is $3$."),
    "TMB-GATE-EE-SS-007": ("C", "At $n=2$, three overlapping unit samples contribute to the convolution."),
    "TMB-GATE-EE-SS-008": (["A", "B", "C"], "Weighted averaging gives $-1$; constant squared magnitude gives RMS $2$ and power $4$."),
    "TMB-GATE-EE-SS-009": (27, "Orthogonal output components contribute $1^2+4^2/2+6^2/2=27$."),
    "TMB-GATE-EE-SS-010": ("C", "The right-sided term requires $\\operatorname{Re}(s)>-2$ and the left-sided term requires $\\operatorname{Re}(s)<3$."),
    "TMB-GATE-EE-SS-011": (0.667, "The final-value theorem gives $\\lim_{s\\to0}(s+4)/[(s+2)(s+3)]=2/3=0.667$."),
    "TMB-GATE-EE-SS-012": ("A", "The ROC outside both poles makes both inverse-Z components right sided."),
    "TMB-GATE-EE-SS-013": (["A", "B", "C"], "Only the annular ROC contains the unit circle; outer and inner ROCs are causal and anti-causal respectively and both unstable."),
    "TMB-GATE-EE-SS-014": (8, "The highest occupied frequency is $4\\,\\mathrm{kHz}$, so conventional Nyquist sampling requires $8\\,\\mathrm{kHz}$."),
    "TMB-GATE-EE-SS-015": ("B", "Sampling at $4\\,\\mathrm{kHz}$ folds $2.6\\,\\mathrm{kHz}$ to $1.4\\,\\mathrm{kHz}$ while preserving $1\\,\\mathrm{kHz}$."),
    "TMB-GATE-EE-EMFT-001": ("C", "Gauss law for $\\mathbf{D}$ makes the closed-surface flux equal to enclosed free charge $Q$."),
    "TMB-GATE-EE-EMFT-002": (9.994, "The line-charge field $\\lambda/(2\\pi\\varepsilon_0\\rho)$ evaluates to $9.994\\,\\mathrm{kV/m}$."),
    "TMB-GATE-EE-EMFT-003": (["A", "B", "C"], "Charge-free boundary conditions preserve normal $D$ and tangential $E$, giving $E_{2n}=1.2\\,\\mathrm{V/m}$."),
    "TMB-GATE-EE-EMFT-004": ("B", "Integrating the radial field between $a$ and $b$ gives $C=4\\pi\\varepsilon ab/(b-a)$."),
    "TMB-GATE-EE-EMFT-005": (359.5, "The centre-to-surface potential difference $Q/(8\\pi\\varepsilon_0a)$ evaluates to $359.5\\,\\mathrm{V}$."),
    "TMB-GATE-EE-EMFT-006": (2, "The air and dielectric half-area capacitances add in parallel to twice the all-air value."),
    "TMB-GATE-EE-EMFT-007": ("C", "At the midpoint the two right-hand-rule fields add to $30\\,\\mu\\mathrm{T}$."),
    "TMB-GATE-EE-EMFT-008": (["A", "B", "C"], "Ampere law, zero magnetic divergence and the surface-current jump in tangential $H$ are valid; normal $B$ is continuous."),
    "TMB-GATE-EE-EMFT-009": (0.0838, "The core and gap reluctance drops give $B=\\mu_0NI/(l_g+l_c/\\mu_r)=0.0838\\,\\mathrm{T}$."),
    "TMB-GATE-EE-EMFT-010": ("C", "Differentiating $(4t^2+2t)\\,\\mathrm{mWb}$ at $t=0.5\\,\\mathrm{s}$ gives $6\\,\\mathrm{mV}$."),
    "TMB-GATE-EE-EMFT-011": (320, "Motional emf is $1.6\\,\\mathrm{V}$, current is $0.8\\,\\mathrm{A}$ and $BIl=0.32\\,\\mathrm{N}=320\\,\\mathrm{mN}$."),
    "TMB-GATE-EE-EMFT-012": ("C", "For $r>a$, Faraday law gives $E=a^2|dB/dt|/(2r)=0.05\\,\\mathrm{V/m}$."),
}


def get_batch(batch_id: str) -> RecoveryBatch:
    try:
        return BATCHES[batch_id.upper()]
    except KeyError as exc:
        raise ValueError(f"Unknown recovery batch: {batch_id}") from exc


def load_questions(batch: RecoveryBatch) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in batch.source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
