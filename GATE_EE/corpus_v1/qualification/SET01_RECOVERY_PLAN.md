# Set 01 Recovery Plan — Day 6 Checkpoint

## Purpose

This plan accelerates the first valid paper without changing the eight-day 3,575-draft contract or treating machine checks as human approval.

## Current inventory

- 20 admitted Engineering Mathematics questions.
- 20 admitted Electric Circuits questions.
- 20 admitted General Aptitude questions.
- 15 Signals and Systems and 12 Electromagnetic Fields candidates with strict Formatter and independent-recomputation PASS, awaiting named human final QA.
- 0 complete or released papers.

## Why raw inventory count is insufficient

Set 01 requires exactly 10 GA questions for 15 marks and 55 selected-subject questions for 85 marks. Within the selected-subject section, Engineering Mathematics must contribute 13 marks and core EE must contribute 72 marks.

The current mathematics pool contains only four one-mark questions. Therefore a feasible 13-mark selection uses eight questions (three one-mark plus five two-mark). Set 01 then needs 47 core-EE questions. The existing 20 admitted Electric Circuits records plus all 27 Batch 004/005 candidates provide exactly those 47 core-EE questions and 72 marks.

`blueprints/GATE_EE_SET_01_CAPACITY_PREFLIGHT.json` proves the complete structural candidate: 65 questions, 100 marks, 30 one-mark and 35 two-mark questions; exact GA/selected-subject and 13/72 mark splits; 15 Easy, 33 Medium and 17 Hard; 28 MCQ, 17 MSQ and 20 NAT; six visual questions; and 9,005 estimated seconds. It selects 38 already paper-eligible questions plus all 27 pending questions. It is deliberately not a release manifest.

## Recovery sequence

1. Complete named human final QA for Batches 004 and 005 using the checksum-bound fillable PDFs.
2. Promote and admit only explicit PASS records; revise or reject any failed item without weakening the gate.
3. Re-run the capacity preflight. If any item is not admitted, replace it with a separately qualified record before assembly.
4. Select the exact 65-question manifest from paper-eligible records and validate every question, mark, type, difficulty, family, visual and timing constraint.
5. Render the paper, complete final human technical and visual QA, then integrate the immutable manifest-backed release with the website.

This is a first-paper recovery lane. It does not replace the larger 50-set production contract.
