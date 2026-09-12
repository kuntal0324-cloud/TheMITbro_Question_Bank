# Batch 003 Human Final-QA Certification Guide

Batch 003 contains 20 original General Aptitude candidates covering Verbal, Quantitative, Analytical and Spatial Aptitude. Strict Formatter v2.0 reports 20 PASS / 0 REVIEW / 0 invalid, and independent recomputation reports 20/20 PASS. Named human final QA was the mandatory promotion gate and was completed on 2026-09-10 with 20 PASS / 0 REVISE / 0 REJECT.

## Review procedure used

1. Download `output/pdf/GATE_EE_BATCH003_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf` after the Question Bank pull request is merged.
2. Open the downloaded file in Adobe Acrobat Reader or another PDF viewer that saves AcroForm fields. Do not fill the GitHub preview.
3. Enter the reviewer name, actual role or qualification, review date and the exact attestation printed on page 1.
4. Independently solve each of the 20 questions before relying on its declared answer or supplied solution.
5. For each item, select exactly one PASS or FAIL value for all five checks, then select exactly one final decision: PASS, REVISE or REJECT.
6. A PASS decision requires five PASS checks. Every REVISE, REJECT or failed check requires a precise note.
7. On page 22, approve the reviewed results, enter the typed signature, save the completed form under a new filename and return that completed PDF for the promotion checkpoint.

## Import validation

The completed form can be checked from the repository root without changing the committed pending template:

```bash
python -m pip install -r requirements-pdf.txt
python scripts/import_gate_ee_batch_003_human_qa_pdf.py \
  "/path/to/completed-review.pdf" \
  --output /tmp/BATCH_003_HUMAN_FINAL_QA.json
```

The importer rejects incomplete reviewer identity, an altered attestation, ambiguous checkbox pairs, inconsistent PASS decisions, and missing notes for failed, REVISE or REJECT outcomes.

## Gate discipline used

- Do not overwrite the repository's pending human-QA JSON until the completed PDF has been returned and independently checked.
- Do not edit paper-eligibility or admission counters manually.
- Only IDs explicitly marked PASS may enter a later certificate and Corpus V1 admission manifest.
- Batch 003 alone does not complete a 65-question paper, so the commercial release gate remains blocked.

## Certification result - 2026-09-10

- Named reviewer: KUNTAL DAS, Diploma in Electrical Engineering.
- Human final QA: 20 PASS / 0 REVISE / 0 REJECT.
- Completed-PDF SHA-256: `b18ec0bd1eb62f2c9151a8ba726857cb227cda1544660d5008ba82275a0de9e8`.
- All 20 approved IDs are paper-eligibility certified and admitted to Corpus V1.
- Program inventory: 60 candidates / 60 Formatter PASS / 60 paper-eligible / 60 admitted.
- Complete and released papers remain 0 / 0.
