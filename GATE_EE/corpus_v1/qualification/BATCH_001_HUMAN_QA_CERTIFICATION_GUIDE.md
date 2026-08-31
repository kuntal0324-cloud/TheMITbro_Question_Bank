# Batch 001 Human Final QA → Paper-Eligibility Certification

Current state: 20 Formatter PASS / 0 REVIEW; 20 independent-AI QA PASS; 0 certified paper-eligible.

A real human reviewer must complete `GATE_EE/corpus_v1/review_manifests/BATCH_001_HUMAN_FINAL_QA.json`.

## Procedure
1. Use `BATCH_001_HUMAN_REVIEW_PACKET.md`.
2. Independently check each question, answer, solution, clarity and originality-conflict risk.
3. For every required check, set `PASS` or `FAIL`.
4. Set `decision` to `PASS`, `REVISE`, or `REJECT`.
5. Fill reviewer name, role/qualification, date (`YYYY-MM-DD`) and exact attestation.
6. Set `final_decision` to `APPROVE_REVIEWED_RESULTS`.
7. Run `python scripts/validate_gate_ee_batch_001_human_signoff.py`.
8. Run `python scripts/promote_gate_ee_batch_001_paper_eligibility.py`.
9. Run `python scripts/validate_gate_ee_batch_001_paper_eligibility.py`.

Do not alter the canonical JSONL after signoff. The review and certificate are checksum-bound to `2c218be6055cfa977da0842a6bdbc1edb61fe1712bf88794dc461052ae050b9e`.
