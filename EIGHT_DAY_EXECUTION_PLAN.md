# GATE 2027 EE — Eight-Day Draft Production Sprint

## Delivery definition

The eight-day target is **3,575 original draft candidates**, enough for 3,250 unique paper slots plus a 10% reserve. It is not permission to release unreviewed papers. A set exists commercially only after all 65 selected records are `PAPER_ELIGIBLE`, its exact blueprint passes, and its final PDF receives human technical and visual signoff.

## Daily authoring allocation

| Day | Candidate allocation | Daily total |
|---|---|---:|
| 1 | GA 150; Engineering Mathematics 150; Electric Circuits 147 | 447 |
| 2 | GA 150; Engineering Mathematics 150; Electric Circuits 147 | 447 |
| 3 | GA 150; Engineering Mathematics 150; Electromagnetic Fields 147 | 447 |
| 4 | Signals and Systems 260; Electromagnetic Fields 73; Electrical Machines 114 | 447 |
| 5 | Electrical Machines 266; Power Systems 181 | 447 |
| 6 | Power Systems 269; Control Systems 178 | 447 |
| 7 | Control Systems 122; Measurements 180; Analog and Digital Electronics 145 | 447 |
| 8 | Analog and Digital Electronics 95; Power Electronics 180; GA 100; Engineering Mathematics 45; Electric Circuits 26 | 446 |
| **Total** | **All official EE/GA sections** | **3,575** |

## Continuous lanes

1. **Authoring lane:** generate independent families, not cosmetic number variants; attach worked answer evidence.
2. **Ingestion lane:** split uploads, extract structure, route to section/topic/subtopic, and quarantine low-confidence OCR.
3. **Technical lane:** independently recompute the answer and validate the complete solution, units and diagram.
4. **Integrity lane:** check exact/near duplicates, family collisions and external originality conflicts.
5. **Formatter lane:** remove learner-visible markup, inspect every page and record deterministic hashes.
6. **Release lane:** assemble only `PAPER_ELIGIBLE` records, validate the official pattern, obtain named human signoff, then integrate the manifest-backed PDF with the website.

## End-of-day control report

Record candidate count, in-syllabus count, AUTO/REVIEW/FAIL routing, validation status, duplicate/family flags, reviewer throughput, paper-eligible count and blockers. Draft totals must never be reported as qualified totals.

## Capacity requirement

At 447 candidates per day, the human-review load is substantial. A credible eight-day commercial release would require multiple qualified EE reviewers plus a separate final visual-QA role. With one reviewer, use this sprint to build the draft pool and release fully reviewed sets incrementally after day eight.

## Live contract position

The execution clock starts on **2026-09-08** and ends on **2026-09-15** (eight inclusive calendar days). The calendar position is **Day 6 in progress** as of **2026-09-13**. The earlier Day-3 ledger was a recorded checkpoint, not permission to pause or reset the fixed clock.

- New sprint drafts: **67 / 3,575** (Batches 002–005).
- Day 1 closed at **20 / 447**; the Day-1 shortfall carried forward is 427 drafts.
- Day 2 closed at **20 / 447**; 427 remain against the original Day-2 allocation.
- Days 3 and 4 closed at **0 / 447** each.
- Day 5 closed at **27 / 447**: 15 Signals and Systems plus 12 Electromagnetic Fields candidates carried forward from the Day-4 allocation. The original Day-5 Electrical Machines and Power Systems allocation remains unfilled.
- Day-6 progress is **0 / 447**; its Power Systems and Control Systems allocation is still unfilled while Batches 004 and 005 wait at the named-human gate.
- Opening inventory, excluded from Day-1 output: **20** Batch 001 Engineering Mathematics records.
- Current program inventory: **87** unique candidates; **87** Formatter-passed.
- Human-certified, paper-eligible and admitted inventory remains **60**. Batches 004 and 005 are independently recomputed and Formatter-passed, but their 27 records remain `DRAFT` and await named human final QA.
- Complete/released papers: **0 / 50**.

The original 3,575-draft target is therefore **behind schedule**, not cancelled or silently reset. The 27-record Set 01 core-EE capacity gap is now filled structurally: a deterministic preflight satisfies 65 questions, 100 marks, the 15/13/72 section-mark split and all balance ranges. It selects 38 already eligible records plus the 27 pending records, so it is not a paper manifest and release remains blocked. The immediate gate is named human final QA, paper-eligibility promotion and Corpus V1 admission for Batches 004 and 005.

`GATE_EE/corpus_v1/production/EIGHT_DAY_PROGRESS.json` is the validated source of truth. It must be updated in the same change as every new source batch or certification event.
