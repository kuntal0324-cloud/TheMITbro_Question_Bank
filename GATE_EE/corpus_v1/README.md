# GATE EE Production Corpus V1

This directory is the canonical production workspace for the first scalable TheMITbro GATE Electrical Engineering master corpus.

## Foundation contract
- Master-pool target: **220 original questions**
- Commercial source of truth: this Question Bank repository
- Processing engine: frozen Formatter v2.0
- First production paper: `blueprints/GATE_EE_SET_01_V1.json`
- Publication requires human final QA
- Released question revisions are immutable through release manifests

## Workflow
Author source batch → technical/answer/solution review → diagram/originality checks → Formatter v2.0 validation → duplicate/family check → quality gate → PAPER_ELIGIBLE → blueprint selection → paper QA → immutable release.

## Foundation files
- `TOPIC_MAP_V1.json`
- `CORPUS_ALLOCATION_V1.md`
- `source_batches/BATCH_TEMPLATE.md`
- `review_manifests/REVIEW_TEMPLATE.json`
- `families/FAMILY_REGISTRY.json`
- `../../blueprints/GATE_EE_SET_01_V1.json`
- `../../schemas/GATE_EE_CORPUS_V1.schema.json`

This foundation intentionally does **not** declare the existing pilot questions commercially approved.

## Current inventory

As of 2026-09-13, Batches 001, 002 and 003 each contribute 20 checksum-bound, named-human-certified questions. Corpus V1 therefore contains 60 admitted questions: 20 Engineering Mathematics, 20 Electric Circuits and 20 General Aptitude.

Batches 004 and 005 add 27 original, Formatter-passed and independently recomputed candidates: 15 Signals and Systems and 12 Electromagnetic Fields. They remain outside the admitted family registry and have `paper_eligible_count: 0` until named human final QA is completed. The program inventory is 87 candidates / 87 Formatter PASS / 60 paper-eligible and admitted. The Set 01 capacity preflight is structurally complete, but no actual paper manifest or release exists.
