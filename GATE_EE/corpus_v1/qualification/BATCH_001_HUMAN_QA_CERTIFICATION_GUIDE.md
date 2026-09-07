# Batch 001 Human QA certification guide

Batch 001 is now ready for named human final QA against canonical source `cf815b061af0d357df02796f34021b69c3e2465835a1ab1caab7d1ae16d61256`.

The strict Formatter result is 20 PASS / 0 REVIEW / 0 invalid, and independent AI recomputation is 20/20 PASS. Neither result is a substitute for a qualified human reviewer.

1. Review every item in `../review_manifests/BATCH_001_HUMAN_REVIEW_PACKET.md`.
2. Independently check each question, answer, solution, clarity and originality-conflict risk.
3. Record reviewer name, qualification, date and the exact required attestation in `BATCH_001_HUMAN_FINAL_QA.json`.
4. Mark all five checks PASS or FAIL and each decision PASS, REVISE or REJECT.
5. Run the human-signoff validator.
6. Run the promotion command only after valid signoff; it promotes only question IDs explicitly marked PASS.

The website release and commerce gates remain blocked throughout this stage.
