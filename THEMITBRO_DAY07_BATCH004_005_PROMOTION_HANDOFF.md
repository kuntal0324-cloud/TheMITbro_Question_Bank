# TheMITbro Day 7 — Batches 004–005 Promotion Handoff

Date: 2026-09-14

## Contract position

- Fixed sprint: 2026-09-08 through 2026-09-15; calendar Day 7 is in progress.
- Sprint drafts: 67 / 3,575; program inventory: 87 unique candidates.
- Formatter PASS: 87; named-human PASS, paper-eligible and admitted: 87 / 87.
- Complete/released papers: 0 / 0.
- No release, sale, price, website download or `RELEASED` state is authorized.

The original contract clock and accumulated draft shortfall remain unchanged. This checkpoint promotes only the 27 explicit PASS records from Batches 004 and 005; it does not create a paper or authorize release.

## Checksum-bound certification evidence

| Batch | Domain | Human result | Source SHA-256 | Completed review PDF SHA-256 |
|---|---|---:|---|---|
| 004 | Signals and Systems | 15 PASS / 0 REVISE / 0 REJECT | `0d0eb24d9f82f1f511f8dcb879dd78d5684fa73c444a8319d6bc01bdd7961b66` | `4a7697cd3a3b1d641eb9c62d9aeb54d4105e5bb4d809cd0bc76d135b0bacdf98` |
| 005 | Electromagnetic Fields | 12 PASS / 0 REVISE / 0 REJECT | `f30c6d8b1a522d75effdc46b147c87a723e57ecc0a43ef74624daa9da25fb89e` | `dfe7bc900f7878e7cd9eee00a349c199e78af57de947e03f9479d220a486fd7f` |

The completed PDFs remain external evidence. Their imported AcroForm values, filenames and SHA-256 digests are recorded in the human-final-QA manifests and bound into the new paper-eligibility certificates.

## Install

Create the Question Bank branch from updated `main`, unpack the supplied Question Bank ZIP over the repository, and remove the uploaded installation ZIP from the repository tree. Do not add either completed review PDF to Git.

Recommended branch:

```bash
git switch main
git pull --ff-only
git switch -c gate-2027-ee-batch004-005-paper-eligibility
```

After copying the archive contents into the repository, run:

```bash
python -m pip install -r requirements-pdf.txt
python scripts/validate_gate_ee_2027_contract.py
python scripts/validate_gate_ee_corpus_v1_foundation.py
python scripts/validate_gate_ee_recovery_batches.py
python scripts/validate_gate_ee_recovery_human_signoff.py --require-complete
python scripts/validate_gate_ee_recovery_paper_eligibility.py
python scripts/validate_gate_ee_recovery_pdf.py
python scripts/build_gate_ee_set01_capacity_preflight.py --check
python scripts/validate_gate_ee_eight_day_progress.py
git diff --check
```

Expected terminal state:

- Batches 004–005 recovery validation: PASS; 27 paper-eligible; human QA complete.
- Batches 004–005 paper-eligibility certification: PASS; Corpus V1 admitted total 87.
- Set 01 capacity preflight: 65 `PAPER_ELIGIBLE` + 0 pending; no paper manifest created.
- Production control: Day 7; 87 candidates / 87 Formatter PASS / 87 paper-eligible and admitted / 0 complete / 0 released.

## Commit boundary

Stage the promotion files, review `git diff --cached --check`, and confirm that no completed review PDF or installation ZIP is staged. Suggested commit message:

```text
Certify Batches 004 and 005 paper eligibility
```

After the pull request is green and merged, the next development stage is controlled Set 01 manifest assembly and final paper rendering. Release remains blocked until the complete rendered paper receives named-human technical and visual signoff.
