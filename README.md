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

As of 2026-09-13 (calendar Day 6), Batches 001-003 contribute 60 checksum-bound, named-human-certified, paper-eligible and Corpus V1-admitted records: 20 Engineering Mathematics, 20 Electric Circuits and 20 General Aptitude. Batches 004 and 005 add 27 core-EE candidates—15 Signals and Systems plus 12 Electromagnetic Fields—with 27/27 strict Formatter and independent-recomputation PASS. Their named human final QA is pending, so they contribute zero paper-eligible records. The validated counters are 87 program candidates, 87 Formatter passes and 60 paper-eligible/admitted records; no paper is complete or released.

Batch 002 promotion is reproducible with `scripts/promote_gate_ee_batch_002_paper_eligibility.py` and enforced by `scripts/validate_gate_ee_batch_002_paper_eligibility.py`. The completed signoff remains checksum-bound in `GATE_EE/corpus_v1/review_manifests/BATCH_002_HUMAN_FINAL_QA.json`.

Batch 003 promotion is reproducible with `scripts/promote_gate_ee_batch_003_paper_eligibility.py` and enforced by `scripts/validate_gate_ee_batch_003_paper_eligibility.py`. Its completed signoff remains checksum-bound in `GATE_EE/corpus_v1/review_manifests/BATCH_003_HUMAN_FINAL_QA.json`.

Batches 004 and 005 are validated together with `scripts/validate_gate_ee_recovery_batches.py`. `blueprints/GATE_EE_SET_01_CAPACITY_PREFLIGHT.json` proves that their 27 records close the structural Set 01 deficit, but the preflight explicitly selects 27 human-QA-pending records and is not a paper manifest or release authorization.

Reviewers use `output/pdf/GATE_EE_BATCH004_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf` and `output/pdf/GATE_EE_BATCH005_HUMAN_FINAL_QA_MOBILE_FILLABLE.pdf`. After each form is completed, import it with `scripts/import_gate_ee_recovery_human_qa_pdf.py --batch BATCH_004|BATCH_005 <completed.pdf>` and validate it with `scripts/validate_gate_ee_recovery_human_signoff.py --batch BATCH_004|BATCH_005`. Blank or partially completed forms are rejected.
