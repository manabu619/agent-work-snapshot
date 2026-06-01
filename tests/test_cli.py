from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTest(unittest.TestCase):
    def test_version_returns_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agent_work_snapshot", "--version"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "agent-work-snapshot 0.1.1")

    def test_valid_example_returns_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agent_work_snapshot", "validate", "examples/codex.snapshot.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_json_returns_two(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agent_work_snapshot", "validate", "tests/fixtures/invalid/malformed.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("[ERROR] [invalid_json]", result.stderr)

    def test_missing_file_returns_two(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agent_work_snapshot", "validate", "tests/fixtures/missing.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("[ERROR] [file_io]", result.stderr)


if __name__ == "__main__":
    unittest.main()
