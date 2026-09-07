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
