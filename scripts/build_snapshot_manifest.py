#!/usr/bin/env python3
"""Build or check the complete SHA-256 inventory for the public snapshot."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "frozen" / "SNAPSHOT_SHA256.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): digest(path)
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and ".git" not in path.parts and path != OUTPUT
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="compare the current tree with the checked-in inventory")
    args = parser.parse_args()
    current = inventory()
    if args.check:
        expected = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if current != expected:
            missing = sorted(set(expected) - set(current))
            added = sorted(set(current) - set(expected))
            changed = sorted(k for k in set(current) & set(expected)
                             if current[k] != expected[k])
            raise SystemExit(
                f"snapshot mismatch: added={added}, missing={missing}, changed={changed}"
            )
        print(f"SNAPSHOT MATCH: {len(current)} files")
        return
    OUTPUT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {OUTPUT.relative_to(ROOT)}: {len(current)} files")


if __name__ == "__main__":
    main()
