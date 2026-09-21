# Set 01 post-authorization state-sync handoff

## Result

The latest completed exact-artifact authorization is now reflected in the live production ledger and roadmap documentation.

- Set 01 whole-paper human QA: 65/65 PASS.
- Formatter release qualification: 65/65 PASS.
- Exact RC1 learner-artifact authorization: PASS.
- Release-authorized sets: 1.
- Commercially released sets: 0.
- Pricing, sale and storefront activation: BLOCKED.

## Authoritative bindings

- Candidate content SHA-256: `3c719fe424b564ca4843b334588046be3e3ba428ce62cf58b5c615dddad2346e`
- Authorization JSON file SHA-256: `68b4c5f41c3d832123dd18946c8d8ae55319fc1f5af6928f554f931b836402bd`
- Authorization content SHA-256: `5b3a1adebf05b47d78012fe90ca328d1a20073dfaa64cd37debeabc10bb130b9`
- Completed authorization PDF SHA-256: `9f9551f861b512457d13dc0c3e971e1f33826fe798a4e2bb73aac719157188ad`
- Question PDF SHA-256: `5479e90058e363f3c67494753c3c860540177ef2e84713eb9bec13595c2f9491`
- Solution PDF SHA-256: `8ba106686bbb7b405de96dfb9ab6308bdf4e93b958882cafb67360a7fb4e1f19`
- Learner-pack PDF SHA-256: `f6526a7ed7a16e12339f12206a8ca4ec88c5177f159f9a276ef3f2ef4298be58`

## Validation

Run from the repository root:

```bash
python -m pip install -r requirements-pdf.txt
sudo apt-get update && sudo apt-get install -y poppler-utils
python scripts/validate_gate_ee_set01_human_signoff.py --require-complete
python scripts/validate_gate_ee_set01_release_candidate.py
python scripts/validate_gate_ee_set01_release_authorization.py --require-complete
python scripts/validate_gate_ee_eight_day_progress.py
python scripts/validate_gate_ee_set01_manifest.py
git diff --check
```

This checkpoint does not set a price, authorize a sale, activate the storefront or modify the authorized learner PDFs.
