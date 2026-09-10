# GATE EE Corpus V1 — Current Roadmap Position

## Current position — 2026-09-09

**Calendar checkpoint:** Day 2 of the eight-day contract is in progress.

**Qualification checkpoint:** Batch 003 is ready for named human final QA.
**Release checkpoint:** blocked; no complete 65-question paper exists.

Batch 001 contributes 20 admitted Engineering Mathematics records and Batch 002 contributes 20 admitted Electric Circuits records. Both batches are checksum-bound, human-certified and paper-eligible.

Batch 003 adds 20 original General Aptitude candidates across Verbal, Quantitative, Analytical and Spatial Aptitude. Its source is bound to SHA-256 `b00075f2ae17951baccc382ea59d149e8d0df73a21fd6398bc8e2af9038c902b`. Strict Formatter v2.0 reports 20 PASS / 0 REVIEW / 0 invalid, and independent answer/solution recomputation reports 20/20 PASS. Named human final QA is still pending, so Batch 003 contributes zero paper-eligible records at this checkpoint.

## Eight-day contract position

| Measure | Current | Contract target | Position |
|---|---:|---:|---|
| Day-1 new drafts | 20 | 447 | Closed 427 below target |
| Day-2 new drafts | 20 | 447 | In progress; 427 remain |
| Eight-day sprint drafts | 40 | 3,575 | 1.12% complete |
| Total program candidates | 60 | 3,595 including opening inventory | 20 opening + 40 sprint |
| Formatter-passed candidates | 60 | — | Batches 001–003 |
| Human-final-QA PASS | 40 | — | Batch 003 pending |
| Paper-eligible / admitted | 40 / 40 | 3,250 minimum unique slots | Only Batches 001–002 |
| Complete 65-question papers | 0 | 50 | Release blocked |

The original schedule has not been reset. Its Day-1 shortfall remains visible, so the roadmap is currently behind the original 447-drafts-per-day pace.

## Exact next gates

1. Complete the Batch 003 fillable human final-QA packet and import the saved AcroForm.
2. Promote only the Batch 003 IDs explicitly marked PASS; until then they remain drafts.
3. Author the next selected-subject batch for Set 01. Even if all 20 Batch 003 records pass, at least 27 new blueprint-compatible selected-subject records are still required because the 13-mark Engineering Mathematics section can use at most eight of the currently available mathematics questions while the remaining selected-subject slots must come from core EE.
4. Assemble Set 01 only after 10 GA questions, 55 selected-subject questions, 100 marks, the 13/72 section-mark split and every release gate can all be satisfied simultaneously.

The authoritative machine-readable counter is `production/EIGHT_DAY_PROGRESS.json`.
