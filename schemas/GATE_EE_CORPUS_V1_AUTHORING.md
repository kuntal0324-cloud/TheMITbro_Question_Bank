# GATE EE Corpus V1 — Production Authoring Contract

Every commercial question is original TheMITbro content. Public exam patterns/syllabi may guide scope, but question wording, data, distractors and solutions must be independently authored.

## Required metadata
`id`, `exam`, `subject`, `topic`, `subtopic`, `concept`, `difficulty`, `type`, `marks`, `estimated_time_seconds`, `family_id`, `revision`, `status`, `provenance`.

## Required content
Question stem; four options for MCQ/MSQ; answer; complete worked solution; NAT tolerance where applicable; diagram specification/asset where applicable.

## Production lifecycle
DRAFT → TECHNICAL_REVIEW → ANSWER_VERIFIED → SOLUTION_VERIFIED → FORMATTER_VALIDATED → APPROVED → PAPER_ELIGIBLE → RELEASED

`APPROVED` and later states require human review. Formatter success alone never constitutes publication approval.

## Family rule
Questions sharing the same underlying construction, numerical skeleton, diagram topology, or near-equivalent reasoning pattern receive the same `family_id`. A production paper may contain at most one member of a family.

## Revision rule
Never silently overwrite a released question. Increment `revision`; preserve the release manifest that identifies the sold version.
