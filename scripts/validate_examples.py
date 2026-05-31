#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from agent_work_snapshot.validation import validate_snapshot

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    failed = False
    for path in sorted((ROOT / "examples").glob("*.snapshot.json")):
        snapshot = json.loads(path.read_text(encoding="utf-8"))
        result = validate_snapshot(snapshot, strict_paths=True)
        if result.is_valid:
            print(f"[OK] {path.relative_to(ROOT)}")
        else:
            failed = True
            for error in result.errors:
                print(f"[ERROR] {path.relative_to(ROOT)}: {error}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

