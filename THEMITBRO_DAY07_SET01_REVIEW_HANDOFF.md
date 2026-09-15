# Day 7 — GATE 2027 EE Set 01 Review Handoff

## Outcome

Set 01 is assembled as a deterministic **review checkpoint**: 65 questions, 100 marks and 180 minutes. All selected revisions are individually `PAPER_ELIGIBLE`, unique by question and family, and bound to their canonical source, Formatter, independent-QA, human-QA, eligibility and corpus-admission evidence.

This checkpoint is not a release. Publication, download, payment and sale remain blocked until the complete rendered paper passes named-human QA and receives a separate release certificate.

## Issued review artifacts

| Artifact | SHA-256 |
|---|---|
| `output/pdf/GATE_EE_SET_01_QUESTION_PAPER_REVIEW.pdf` | `97e6c26a9ad0e7638aac19053252c830b2406ed6ff70f7eeddee7f1af1701655` |
| `output/pdf/GATE_EE_SET_01_SOLUTIONS_REVIEW.pdf` | `a3847bfd1d5a490ae65bf8e110a1965e4f0649f187dde00d0fea9a0325a7798a` |
| `output/pdf/GATE_EE_SET_01_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf` | `c30fa91c5305e8f2d3072afab3fd29e418e767b5dcbdc17d7d3a72435bb1beee` |

Manifest content SHA-256: `0a5a9c14cdca6c92db41317239a36afe73da6efda2b5ae642625649a94b03cc8`

## 1. Verify the issued checkpoint

From the Question Bank repository root:

```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
python -m pip install -r requirements-pdf.txt
python scripts/build_gate_ee_set01_manifest.py --check
python scripts/validate_gate_ee_set01_manifest.py
python scripts/validate_gate_ee_set01_review_artifacts.py
python scripts/validate_gate_ee_set01_human_signoff.py
```

The final command should report `PENDING`; that is the correct pre-review state. The other Set 01 commands must pass.

## 2. Perform named-human complete-paper QA

Open the question paper, solutions and fillable QA form together. For every position Q1–Q65:

1. verify statement/content rendering;
2. independently verify the answer and solution alignment;
3. verify diagram and page layout, or confirm that the non-visual item is visually clear;
4. select exactly one final decision: `PASS`, `REVISE` or `REJECT`;
5. add a note for every `REVISE` or `REJECT`.

The reviewer must enter their own truthful name, role/qualification, date, required attestation and typed signature. The historical Batch 001 record says `Masters in Electrical Engineering`, while Batches 002–005 say `Diploma in Electrical Engineering`. The form therefore requires an explicit accurate qualification reconfirmation and explanatory note; historical signed evidence is not silently rewritten.

Do not rename, print-to-PDF, flatten or otherwise regenerate the issued form. Save the completed copy as:

`output/pdf/GATE_EE_SET_01_HUMAN_FINAL_QA_COMPLETED.pdf`

## 3. Import and validate the completed form

```bash
python scripts/import_gate_ee_set01_human_qa_pdf.py
python scripts/validate_gate_ee_set01_human_signoff.py --require-complete
git diff --check
```

If any position is `REVISE` or `REJECT`, the strict completion command must remain blocked. Correct the canonical source, rerun every affected batch and Set 01 check, rerender all three review artifacts, and repeat whole-paper QA against the new checksums.

## 4. Controlled next stage after an all-PASS signoff

An all-PASS human signoff authorizes preparation of a separate immutable release-candidate certificate; it does not itself authorize sale. The release candidate must bind the final manifest, final PDFs, completed QA PDF/JSON and exact repository provenance. Only after that certificate passes may the website checkpoint be updated and one catalog product be considered for release.

The parallel 3,575-draft / 50-set authoring backlog remains behind schedule and must continue independently.
