# Batch 001 Human QA certification guide

Human final QA is currently **blocked** because strict Formatter qualification is 0 PASS / 20 REVIEW.

When and only when the qualification summary reaches `READY_FOR_HUMAN_FINAL_QA` with current checksum-linked evidence showing 20 PASS / 0 REVIEW:

1. Generate a fresh detailed review packet from the canonical JSONL.
2. Independently check each question, answer, solution, clarity and originality-conflict risk.
3. Record named reviewer identity, qualification, date and exact attestation.
4. Mark each check PASS or FAIL and each decision PASS, REVISE or REJECT.
5. Run the human-signoff validator and promotion command.

The promotion script independently checks the current Formatter evidence and eligibility-candidate list. A human signoff cannot override unresolved Formatter reviews.
