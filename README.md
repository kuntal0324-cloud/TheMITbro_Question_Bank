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

As of 2026-09-14 (calendar Day 7), Batches 001-005 contribute 87 checksum-bound, named-human-certified, paper-eligible and Corpus V1-admitted records: 20 Engineering Mathematics, 20 Electric Circuits, 20 General Aptitude, 15 Signals and Systems and 12 Electromagnetic Fields. Batches 004 and 005 record 27/27 strict Formatter PASS, 27/27 independent-recomputation PASS and 27/27 named-human final-QA PASS. No paper is complete or released.

Batch 002 promotion is reproducible with `scripts/promote_gate_ee_batch_002_paper_eligibility.py` and enforced by `scripts/validate_gate_ee_batch_002_paper_eligibility.py`. The completed signoff remains checksum-bound in `GATE_EE/corpus_v1/review_manifests/BATCH_002_HUMAN_FINAL_QA.json`.

Batch 003 promotion is reproducible with `scripts/promote_gate_ee_batch_003_paper_eligibility.py` and enforced by `scripts/validate_gate_ee_batch_003_paper_eligibility.py`. Its completed signoff remains checksum-bound in `GATE_EE/corpus_v1/review_manifests/BATCH_003_HUMAN_FINAL_QA.json`.

Batches 004 and 005 are promoted together with `scripts/promote_gate_ee_recovery_paper_eligibility.py` and enforced by `scripts/validate_gate_ee_recovery_paper_eligibility.py`. Their completed signoffs remain checksum-bound in `GATE_EE/corpus_v1/review_manifests/`. `blueprints/GATE_EE_SET_01_CAPACITY_PREFLIGHT.json` now proves that all 65 selected records are `PAPER_ELIGIBLE`; it remains a preflight, not a paper manifest or release authorization.

The next gate is controlled Set 01 manifest assembly from the exact 65-record preflight selection, followed by blueprint validation, final PDF rendering and named-human technical and visual signoff. Catalog publication, sale and release remain blocked until those gates pass.
