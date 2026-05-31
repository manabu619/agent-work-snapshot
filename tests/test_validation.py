from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from agent_work_snapshot.validation import load_schema, validate_snapshot
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = json.loads((ROOT / "examples" / "codex.snapshot.json").read_text(encoding="utf-8"))


class ValidationTest(unittest.TestCase):
    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(load_schema())

    def test_provider_examples_are_valid(self) -> None:
        for path in sorted((ROOT / "examples").glob("*.snapshot.json")):
            with self.subTest(path=path.name):
                result = validate_snapshot(json.loads(path.read_text(encoding="utf-8")))
                self.assertTrue(result.is_valid, result.errors)

    def test_rejects_missing_required_field(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        del snapshot["agent_id"]
        self.assertFalse(validate_snapshot(snapshot).is_valid)

    def test_rejects_unknown_field(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["unexpected"] = True
        self.assertFalse(validate_snapshot(snapshot).is_valid)

    def test_rejects_invalid_date_time(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["observed_at"] = "not-a-date"
        self.assertFalse(validate_snapshot(snapshot).is_valid)

    def test_rejects_secret_like_key_recursively(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["progress"]["session_token"] = "redacted"
        errors = validate_snapshot(snapshot).errors
        self.assertTrue(any("secret-like key" in error for error in errors))

    def test_rejects_camel_case_secret_like_key(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["apiKey"] = "redacted"
        errors = validate_snapshot(snapshot).errors
        self.assertTrue(any("secret-like key" in error for error in errors))

    def test_rejects_inconsistent_progress(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["progress"] = {"total": 2, "completed": 2, "blocked": 1}
        errors = validate_snapshot(snapshot).errors
        self.assertTrue(any("completed + blocked" in error for error in errors))

    def test_warns_for_absolute_local_path_by_default(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["outputs"] = ["/Users/example/project/report.json"]
        result = validate_snapshot(snapshot)
        self.assertTrue(result.is_valid)
        self.assertTrue(result.warnings)

    def test_strict_paths_rejects_absolute_local_path(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["outputs"] = ["/home/example/project/report.json"]
        result = validate_snapshot(snapshot, strict_paths=True)
        self.assertFalse(result.is_valid)

    def test_strict_paths_rejects_windows_user_path(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["outputs"] = [r"C:\Users\example\project\report.json"]
        result = validate_snapshot(snapshot, strict_paths=True)
        self.assertFalse(result.is_valid)

    def test_rejects_ttl_out_of_range(self) -> None:
        snapshot = copy.deepcopy(EXAMPLE)
        snapshot["ttl_seconds"] = 59
        self.assertFalse(validate_snapshot(snapshot).is_valid)


if __name__ == "__main__":
    unittest.main()
