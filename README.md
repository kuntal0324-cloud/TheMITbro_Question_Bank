# TheMITbro Question Bank - GATE 2027 EE Production Source

This repository is the **authoring and review source of truth** for original TheMITbro questions. The frozen Formatter v2.0 is the processing engine; the website is the storefront.

## Current scope
- Only GATE 2027 Electrical Engineering is active.
- `GATE_EE/` contains original GATE EE content, Engineering Mathematics and the General Aptitude expansion path.
- `references/GATE_2027/` is the machine-readable official syllabus and paper-pattern authority.
- XE0 and XH0 are separate-paper references. Their topics must never be imported into GATE EE merely because they were supplied beside the EE syllabus.
- JEE and other legacy folders are inactive and must not feed current production.

## Future branches
The identity contract is `exam family + exam year + paper code + set number`. Later GATE ME, CE, EC and other branches add their own official syllabus and paper-code data; they do not require a new storefront or a new generic record format.
- `schemas/` — authoring contracts.
- `blueprints/` — mock-paper specifications.
- `production/` — manifests for Formatter-approved releases.
- Existing subject folders are retained as legacy placeholders until their content is migrated.

## Content lifecycle
`DRAFT → TECHNICAL_REVIEW → FORMATTER_VALIDATION → APPROVED → PAPER_ELIGIBLE → RELEASED`

No question becomes sellable merely because automated validation passes. Every paid release requires human review of question statement, answer, solution, units, diagram and originality.

## Scale reality
Fifty non-repeating papers require 3,250 unique paper-eligible questions. The production program targets 3,575 to retain a 10% reserve. An eight-day run can create draft candidates, but a single reviewer cannot credibly complete commercial-grade human QA at that volume.

## Current production position

As of 2026-09-08, Batch 001 contributes 20 human-certified, paper-eligible Engineering Mathematics records to Corpus V1. Batch 002 adds 20 Electric Circuits drafts as Day-1 sprint output, has cleared strict Formatter v2.0 at 20 PASS / 0 REVIEW / 0 invalid, and has 20/20 independent AI recomputation evidence; named human final QA remains pending. The validated live counters are in `GATE_EE/corpus_v1/production/EIGHT_DAY_PROGRESS.json`; no 65-question paper is complete or released.

The Batch 002 human gate is operational on mobile: review `output/pdf/GATE_EE_BATCH002_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf`, save the completed AcroForm, and use `scripts/import_gate_ee_batch_002_human_qa_pdf.py` to generate the checksum-bound signoff JSON. Full instructions are in `GATE_EE/corpus_v1/qualification/BATCH_002_HUMAN_QA_CERTIFICATION_GUIDE.md`.
