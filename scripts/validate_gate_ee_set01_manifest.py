#!/usr/bin/env python3
"""Independently enforce the immutable Set 01 review-manifest contract."""

from __future__ import annotations

from gate_ee_set01 import validate_manifest_and_handoff


def main() -> int:
    try:
        manifest, handoff = validate_manifest_and_handoff()
    except (KeyError, TypeError, ValueError) as error:
        print("GATE EE SET 01 MANIFEST VALIDATION: FAILED")
        print("-", error)
        return 1
    print("GATE EE SET 01 MANIFEST VALIDATION: PASSED")
    print(f"Manifest: {manifest['manifest_content_sha256']}")
    print(f"Formatter handoff: {handoff['handoff_content_sha256']}")
    print("Exact blueprint, source, evidence, eligibility and admission bindings: PASSED")
    if manifest["reviewer_metadata_consistency"]["status"] != "CONSISTENT":
        print("Reviewer qualification metadata: RECONFIRMATION REQUIRED BEFORE RELEASE")
    print("Release and sale gates: BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
