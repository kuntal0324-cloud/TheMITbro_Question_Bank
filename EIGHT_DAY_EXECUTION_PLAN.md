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

The execution clock starts on **2026-09-08** and ends on **2026-09-15** (eight inclusive calendar days). Day 1 is in progress.

- New sprint drafts: **20 / 3,575** (Batch 002 Electric Circuits).
- Day-1 progress: **20 / 447**; 427 remain.
- Opening inventory, excluded from Day-1 output: **20** Batch 001 Engineering Mathematics records.
- Current program inventory: **40** unique candidates, of which **20** are human-certified, paper-eligible and admitted.
- Formatter-passed inventory: **40**; Batch 002 also has 20/20 independent AI recomputation passes, but still requires named human review.
- Complete/released papers: **0 / 50**.

`GATE_EE/corpus_v1/production/EIGHT_DAY_PROGRESS.json` is the validated source of truth. It must be updated in the same change as every new source batch or certification event.
