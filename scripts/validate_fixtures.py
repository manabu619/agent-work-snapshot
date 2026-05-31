#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from agent_work_snapshot.validation import validate_snapshot

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    failed = False
    valid_count = 0
    invalid_count = 0

    for path in sorted((ROOT / "tests" / "fixtures" / "valid").glob("*.json")):
        valid_count += 1
        snapshot = json.loads(path.read_text(encoding="utf-8"))
        result = validate_snapshot(snapshot, strict_paths=True)
        if result.is_valid:
            print(f"[OK] accepted: {path.relative_to(ROOT)}")
        else:
            failed = True
            for error in result.errors:
                print(f"[ERROR] valid fixture rejected: {path.relative_to(ROOT)}: {error}")

    for path in sorted((ROOT / "tests" / "fixtures" / "invalid").glob("*.json")):
        invalid_count += 1
        try:
            snapshot = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"[OK] rejected malformed JSON: {path.relative_to(ROOT)}")
            continue
        result = validate_snapshot(snapshot, strict_paths=True)
        if result.is_valid:
            failed = True
            print(f"[ERROR] invalid fixture passed: {path.relative_to(ROOT)}")
        else:
            print(f"[OK] rejected: {path.relative_to(ROOT)}")

    print(f"[SUMMARY] valid={valid_count} invalid={invalid_count}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
