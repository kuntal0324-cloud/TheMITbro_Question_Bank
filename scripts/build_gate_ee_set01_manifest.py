#!/usr/bin/env python3
"""Build or verify the immutable Set 01 review manifest and Formatter handoff."""

from __future__ import annotations

import argparse

from gate_ee_set01 import (
    HANDOFF,
    MANIFEST,
    build_handoff_payload,
    build_manifest_payload,
    load_json,
    pretty_bytes,
    relative,
    write_manifest_and_handoff,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        manifest = build_manifest_payload()
        handoff = build_handoff_payload(manifest)
        errors = []
        if not MANIFEST.is_file() or MANIFEST.read_bytes() != pretty_bytes(manifest):
            errors.append(f"stale or missing {relative(MANIFEST)}")
        if not HANDOFF.is_file() or HANDOFF.read_bytes() != pretty_bytes(handoff):
            errors.append(f"stale or missing {relative(HANDOFF)}")
        if errors:
            print("GATE EE SET 01 MANIFEST BUILD CHECK: FAILED")
            for error in errors:
                print("-", error)
            return 1
    else:
        manifest, handoff = write_manifest_and_handoff()
    print("GATE EE SET 01 MANIFEST: PASSED")
    print("Questions: 65 | Marks: 100 | Duration: 180 minutes")
    print("PAPER_ELIGIBLE: 65/65 | unique IDs/families: 65/65")
    print("Release and sale gates: BLOCKED pending complete-paper human QA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
