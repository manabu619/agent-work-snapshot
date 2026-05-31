from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .validation import validate_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-work-snapshot",
        description="Validate a small, read-only AI agent work snapshot.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a snapshot JSON file")
    validate.add_argument("file", type=Path)
    validate.add_argument(
        "--strict-paths",
        action="store_true",
        help="reject absolute local paths instead of reporting warnings",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "validate":
        return 2

    try:
        result = validate_file(args.file, strict_paths=args.strict_paths)
    except json.JSONDecodeError as error:
        print(f"[ERROR] [invalid_json] {args.file}: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"[ERROR] [file_io] {args.file}: {error}", file=sys.stderr)
        return 2

    for warning in result.warnings:
        print(f"[WARNING] {warning}", file=sys.stderr)
    for error in result.errors:
        print(f"[ERROR] {error}", file=sys.stderr)
    if not result.is_valid:
        return 1

    print(f"[OK] valid snapshot: {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
