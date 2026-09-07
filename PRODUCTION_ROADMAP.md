# Production Roadmap - GATE 2027 EE First

## Stage 1 - Recovery and authoritative contracts
- Freeze the supplied GATE 2027 EE and GA scope as machine-readable references.
- Reject XE0/XH0 contamination and stale exam-year blueprints.
- Quarantine every legacy PDF that has the wrong question count, repeated questions, raw math markup or no release manifest.
- Make Formatter results fail closed: REVIEW is not PASS and automated approval is not human approval.

## Stage 2 - Production ingestion and qualified corpus
- Accept TXT, MD, JPG, JPEG and PNG inputs.
- Split multi-question sources, preserve the original, extract a structured question, and route each question independently.
- Require syllabus, answer, solution, originality, duplicate-family, diagram and render checks.
- Build General Aptitude, Engineering Mathematics and all nine core-EE section pools in parallel.

## Stage 3 - Fifty-set assembly
- Minimum: 3,250 unique PAPER_ELIGIBLE questions for 50 non-repeating papers.
- Recommended: 3,575 qualified questions including a 10% reserve.
- Every set: 65 questions, 100 marks, 180 minutes; 10 GA questions and 55 selected-subject questions; 15 GA, 13 Engineering Mathematics and 72 core-EE marks.
- Produce deterministic manifests and reject any set with repeated IDs/families, wrong marks, wrong section totals or unresolved review flags.

## Stage 4 - Publication and storefront
- Render question paper and separate answer/solution PDF without visible markup.
- Perform page-by-page human visual QA.
- Create an immutable release manifest and checksum.
- Publish only manifest-backed artifacts, then test catalog, payment, download, expiry and recovery paths.

## Eight-day boundary
The 3,575-question quota equals about 447 candidates per day. That is a draft-generation target, not a truthful solo-review target. For a fast public launch, release the first few fully reviewed sets while the remaining draft pool continues through QA. Claiming 50 commercial-grade sets after automated generation alone would be dishonest and risky.
