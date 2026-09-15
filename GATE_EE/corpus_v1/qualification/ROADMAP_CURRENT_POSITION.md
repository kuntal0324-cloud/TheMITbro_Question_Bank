# GATE EE Corpus V1 — Current Roadmap Position

## Current position — 2026-09-14

**Calendar checkpoint:** Day 7 of the fixed eight-day contract is in progress.

**Qualification checkpoint:** Batches 001–005 are checksum-bound, named-human-certified, paper-eligible and admitted to Corpus V1.

**Set 01 checkpoint:** the exact 65 `PAPER_ELIGIBLE` revisions are frozen in an immutable review manifest. The 65-question / 100-mark / 180-minute structure, 15/13/72 mark split, balance ranges and every source/evidence checksum pass. Review-only question, solution and fillable whole-paper QA PDFs have been rendered and validated.

**Release checkpoint:** blocked; the complete rendered paper has not received named-human technical and visual signoff. Historical reviewer-qualification metadata also requires explicit reconfirmation before release certification.

Batch 001 contributes 20 Engineering Mathematics records, Batch 002 contributes 20 Electric Circuits records and Batch 003 contributes 20 General Aptitude records.

Batch 004 contributes 15 Signals and Systems records bound to source SHA-256 `0d0eb24d9f82f1f511f8dcb879dd78d5684fa73c444a8319d6bc01bdd7961b66`. Its completed review PDF is bound to SHA-256 `4a7697cd3a3b1d641eb9c62d9aeb54d4105e5bb4d809cd0bc76d135b0bacdf98`; named-human final QA records 15 PASS / 0 REVISE / 0 REJECT.

Batch 005 contributes 12 Electromagnetic Fields records bound to source SHA-256 `f30c6d8b1a522d75effdc46b147c87a723e57ecc0a43ef74624daa9da25fb89e`. Its completed review PDF is bound to SHA-256 `dfe7bc900f7878e7cd9eee00a349c199e78af57de947e03f9479d220a486fd7f`; named-human final QA records 12 PASS / 0 REVISE / 0 REJECT.

## Eight-day contract position

| Measure | Current | Contract target | Position |
|---|---:|---:|---|
| Day-1 new drafts | 20 | 447 | Closed 427 below target |
| Day-2 new drafts | 20 | 447 | Closed 427 below target |
| Day-3 new drafts | 0 | 447 | Closed 447 below target |
| Day-4 new drafts | 0 | 447 | Closed 447 below target |
| Day-5 new drafts | 27 | 447 | Closed below target; Day-4 SS/EMFT recovery |
| Day-6 new drafts | 0 | 447 | Closed 447 below target |
| Day-7 new drafts | 0 | 447 | In progress; allocation unfilled |
| Eight-day sprint drafts | 67 | 3,575 | 1.87% complete |
| Total program candidates | 87 | 3,595 including opening inventory | 20 opening + 67 sprint |
| Formatter-passed candidates | 87 | — | Batches 001–005 |
| Human-final-QA PASS | 87 | — | Batches 001–005 |
| Paper-eligible / admitted | 87 / 87 | 3,250 minimum unique slots | All current candidates admitted |
| Complete 65-question papers | 0 | 50 | Release blocked |

The original schedule has not been reset. Its accumulated shortfall remains visible, so the roadmap is behind the original 447-drafts-per-day pace even though the first-paper structural deficit is closed.

## Exact next gates

1. **Complete:** freeze the exact 65-record selection in an immutable review manifest using only `PAPER_ELIGIBLE` revisions and one question per family.
2. **Complete:** validate the official structure, 15/13/72 mark split, balance ranges and every source/evidence checksum.
3. **Complete:** deterministically render and mechanically validate the review question paper, paired solutions and blank whole-paper QA form.
4. Have a named reviewer complete the exact checksum-bound form, including the reviewer-qualification metadata reconfirmation, and import it without altering the issued PDFs.
5. Resolve every `REVISE` or `REJECT`, rerender if needed, and repeat complete-paper QA until all 65 positions pass.
6. Only then create a separate immutable release certificate and integrate the certified artifacts with the website. No sale or release is currently authorized.

The authoring lane remains behind the larger 3,575-draft / 50-set contract and must continue independently of this first-paper recovery lane. The authoritative machine-readable counter is `production/EIGHT_DAY_PROGRESS.json`.
