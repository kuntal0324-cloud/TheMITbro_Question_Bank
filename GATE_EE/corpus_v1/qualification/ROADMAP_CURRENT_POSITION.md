# GATE EE Corpus V1 — Current Roadmap Position

## Current position — 2026-09-13

**Calendar checkpoint:** Day 6 of the fixed eight-day contract is in progress.

**Qualification checkpoint:** Batches 001–003 are human-certified, paper-eligible and admitted. Batches 004–005 are Formatter-passed and independently recomputed, with named human final QA pending.
**Release checkpoint:** blocked; no complete 65-question paper exists.

Batch 001 contributes 20 admitted Engineering Mathematics records and Batch 002 contributes 20 admitted Electric Circuits records. Both batches are checksum-bound, human-certified and paper-eligible.

Batch 003 adds 20 original General Aptitude records across Verbal, Quantitative, Analytical and Spatial Aptitude. Its source is bound to SHA-256 `b00075f2ae17951baccc382ea59d149e8d0df73a21fd6398bc8e2af9038c902b`. Strict Formatter v2.0 reports 20 PASS / 0 REVIEW / 0 invalid, independent answer/solution recomputation reports 20/20 PASS, and named human final QA records 20 PASS / 0 REVISE / 0 REJECT. All 20 approved IDs are certificate-bound and admitted to Corpus V1.

Batch 004 adds 15 Signals and Systems candidates (source SHA-256 `0d0eb24d9f82f1f511f8dcb879dd78d5684fa73c444a8319d6bc01bdd7961b66`) and Batch 005 adds 12 Electromagnetic Fields candidates (source SHA-256 `f30c6d8b1a522d75effdc46b147c87a723e57ecc0a43ef74624daa9da25fb89e`). Formatter reports 15/15 and 12/12 PASS with no review or invalid rows; independent recomputation agrees on all 27 answers and solutions. Six SVG diagrams are checksum-bound. These are machine-qualified candidates only: their paper-eligible count is zero until named human review is completed.

## Eight-day contract position

| Measure | Current | Contract target | Position |
|---|---:|---:|---|
| Day-1 new drafts | 20 | 447 | Closed 427 below target |
| Day-2 new drafts | 20 | 447 | Closed 427 below target |
| Day-3 new drafts | 0 | 447 | Closed 447 below target |
| Day-4 new drafts | 0 | 447 | Closed 447 below target |
| Day-5 new drafts | 27 | 447 | Closed below target; Day-4 SS/EMFT recovery |
| Day-6 new drafts | 0 | 447 | In progress; PS/Control allocation unfilled |
| Eight-day sprint drafts | 67 | 3,575 | 1.87% complete |
| Total program candidates | 87 | 3,595 including opening inventory | 20 opening + 67 sprint |
| Formatter-passed candidates | 87 | — | Batches 001–005 |
| Human-final-QA PASS | 60 | — | Batches 001-003 |
| Paper-eligible / admitted | 60 / 60 | 3,250 minimum unique slots | 27 additional candidates pending human QA |
| Complete 65-question papers | 0 | 50 | Release blocked |

The original schedule has not been reset. Its Day-1 shortfall remains visible, so the roadmap is currently behind the original 447-drafts-per-day pace.

## Exact next gates

1. Complete the two checksum-bound mobile human-QA forms for Batches 004 and 005. Every question requires five checks plus PASS, REVISE or REJECT; only a named reviewer may complete the attestation.
2. Import and validate the completed forms, then promote only explicit PASS records into the paper-eligible certificate, Corpus V1 admission and global family registry.
3. Re-run `blueprints/GATE_EE_SET_01_CAPACITY_PREFLIGHT.json`. It already proves structural capacity for 65 questions, 100 marks, the 15/13/72 section-mark split and the configured difficulty/type/visual/time ranges, but 27 selected records are still ineligible.
4. Create the actual Set 01 manifest and final PDF only after all 65 selected records satisfy `PAPER_ELIGIBLE`, then obtain final paper technical and visual QA. No sale or release is currently authorized.

The authoritative machine-readable counter is `production/EIGHT_DAY_PROGRESS.json`.
