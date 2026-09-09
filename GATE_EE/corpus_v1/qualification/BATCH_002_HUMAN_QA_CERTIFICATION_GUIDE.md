# Batch 002 Human Final-QA Certification Guide

Batch 002 revision 2 is ready for a fresh named human final QA. It is **not** paper-eligible yet. Do not use the withdrawn revision-1 PDF.

## Review

1. Download `output/pdf/GATE_EE_BATCH002_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf`.
2. Open the downloaded file in Adobe Acrobat Reader or another PDF viewer that saves AcroForm fields. Do not fill the GitHub preview.
3. Enter reviewer identity and the exact attestation printed on page 1. In “Role or qualification,” state only your real background. A diploma or job title is not required; for example: `Independent EE reviewer — self-directed B.Tech/M.Tech-level coursework study`.
4. For each of the 20 questions, independently select one PASS or FAIL result for all five checks, then select PASS, REVISE or REJECT.
5. A PASS decision requires five PASS checks. Every REVISE, REJECT or failed check requires a precise note.
6. Save the completed form under a new filename.

## Import and validate

From the repository root:

```bash
python -m pip install -r requirements-pdf.txt
python scripts/import_gate_ee_batch_002_human_qa_pdf.py "/path/to/completed-review.pdf"
python scripts/validate_gate_ee_batch_002_human_signoff.py
```

The importer writes `GATE_EE/corpus_v1/review_manifests/BATCH_002_HUMAN_FINAL_QA.json` only when every required field is complete and internally consistent. It also records the completed PDF filename and SHA-256 digest as evidence.

## Gate discipline

- Formatter PASS and independent-AI recomputation do not replace human review.
- Revision 2 is source-locked to canonical LaTeX and its PDF is rendered with XeLaTeX plus Latin Modern Math. ASCII formula fallback is forbidden by CI.
- Do not edit paper-eligibility counters manually.
- Do not claim a 65-question set or commercial release from this 20-question batch.
- Promotion must be a separate, validator-controlled change after the human-signoff validator passes.
