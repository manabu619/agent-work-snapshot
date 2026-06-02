from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .render import render_snapshot
from .validation import validate_file, validate_snapshot


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

    render = subparsers.add_parser("render", help="render a snapshot JSON file as Markdown")
    render.add_argument("file", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "validate":
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

    if args.command == "render":
        try:
            raw = args.file.read_text(encoding="utf-8")
        except OSError as error:
            print(f"[ERROR] [file_io] {args.file}: {error}", file=sys.stderr)
            return 2

        try:
            snapshot = json.loads(raw)
        except json.JSONDecodeError as error:
            print(f"[ERROR] [invalid_json] {args.file}: {error}", file=sys.stderr)
            return 2

        # render always uses strict_paths=True
        result = validate_snapshot(snapshot, strict_paths=True)
        for error in result.errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        if not result.is_valid:
            return 1

        print(render_snapshot(snapshot), end="")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
