# Set 01 Recovery Plan — RC1 Authorization Checkpoint

## Purpose

This plan accelerates the first valid paper without changing the eight-day 3,575-draft contract or treating machine checks as human approval.

## Current inventory

- 20 admitted Engineering Mathematics questions.
- 20 admitted Electric Circuits questions.
- 20 admitted General Aptitude questions.
- 15 admitted Signals and Systems and 12 admitted Electromagnetic Fields questions with strict Formatter, independent-recomputation and named-human final-QA PASS.
- 1 complete whole-paper-QA-approved paper; 0 released papers.

## Why raw inventory count is insufficient

Set 01 requires exactly 10 GA questions for 15 marks and 55 selected-subject questions for 85 marks. Within the selected-subject section, Engineering Mathematics must contribute 13 marks and core EE must contribute 72 marks.

The current mathematics pool contains only four one-mark questions. Therefore a feasible 13-mark selection uses eight questions (three one-mark plus five two-mark). Set 01 then needs 47 core-EE questions. The 20 admitted Electric Circuits records plus all 27 admitted Batch 004/005 records provide exactly those 47 core-EE questions and 72 marks.

`blueprints/GATE_EE_SET_01_CAPACITY_PREFLIGHT.json` proves the complete structural candidate: 65 questions, 100 marks, 30 one-mark and 35 two-mark questions; exact GA/selected-subject and 13/72 mark splits; 15 Easy, 33 Medium and 17 Hard; 28 MCQ, 17 MSQ and 20 NAT; six visual questions; and 9,005 estimated seconds. All 65 selected records are now `PAPER_ELIGIBLE`. It is deliberately not a release manifest.

## Recovery sequence

1. **Complete:** named human final QA for Batches 004 and 005 using the checksum-bound fillable PDFs.
2. **Complete:** promote and admit only explicit PASS records; all 27 records passed.
3. **Complete:** re-run the capacity preflight; all 65 selected records are admitted and eligible.
4. **Complete:** select the exact 65-question immutable review manifest and validate every question, mark, type, difficulty, family, visual, timing and evidence-binding constraint.
5. **Complete:** render and mechanically validate the checksum-bound review question paper, paired solutions and mobile-fillable 65-question QA form.
6. **Complete:** named-human complete-paper technical and visual QA; all 65 positions passed and the reviewer-qualification metadata inconsistency was explicitly resolved.
7. **Complete:** aggregate all 65 Formatter results, render clean learner-facing RC1 question/solution/combined-pack PDFs, remove internal review markings, and validate exact checksums and page concatenation.
8. **Current gate:** complete and import the RC1 exact-artifact release-authorization form. A later promotion must separately create the immutable release manifest, set the price and activate storefront delivery.

This is a first-paper recovery lane. It does not replace the larger 50-set production contract.
