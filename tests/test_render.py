from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDER_FIXTURES = ROOT / "tests" / "fixtures" / "render"

from agent_work_snapshot.render import render_snapshot
from agent_work_snapshot.validation import validate_snapshot


def _load(name: str) -> dict:
    return json.loads((RENDER_FIXTURES / name).read_text())


def _cli_render(filename: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "agent_work_snapshot", "render", filename],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class RenderUnitTest(unittest.TestCase):
    """Unit tests for render_snapshot()."""

    def test_working_snapshot_contains_key_fields(self) -> None:
        snapshot = _load("working.json")
        output = render_snapshot(snapshot)
        self.assertIn("snap_render_working_0001", output)
        self.assertIn("example-render-agent", output)
        self.assertIn("task_render_0001", output)
        self.assertIn("`working`", output)
        self.assertIn("2 / 4 completed", output)
        self.assertIn("Implement core logic", output)
        self.assertIn("src/example.py", output)

    def test_empty_blockers_shows_none(self) -> None:
        snapshot = _load("working.json")
        output = render_snapshot(snapshot)
        self.assertIn("**Blockers:**\n\nNone", output)

    def test_empty_outputs_shows_none(self) -> None:
        snapshot = _load("multiline_text.json")
        output = render_snapshot(snapshot)
        self.assertIn("**Outputs:**\n\nNone", output)

    def test_completed_candidate_shows_disclaimer(self) -> None:
        snapshot = _load("completed_candidate.json")
        output = render_snapshot(snapshot)
        self.assertIn("`completed_candidate`", output)
        self.assertIn("is not a command to close the parent task", output)

    def test_working_status_has_no_disclaimer(self) -> None:
        snapshot = _load("working.json")
        output = render_snapshot(snapshot)
        self.assertNotIn("is not a command to close the parent task", output)

    def test_null_current_focus_shows_none(self) -> None:
        snapshot = _load("completed_candidate.json")
        output = render_snapshot(snapshot)
        self.assertIn("**Current Focus:** None", output)

    def test_null_next_checkpoint_shows_none(self) -> None:
        snapshot = _load("completed_candidate.json")
        output = render_snapshot(snapshot)
        self.assertIn("**Next Checkpoint:** None", output)

    def test_host_id_appears_when_present(self) -> None:
        snapshot = _load("blocked_with_markdown.json")
        output = render_snapshot(snapshot)
        self.assertIn("example-host-a", output)

    def test_host_id_absent_when_not_present(self) -> None:
        snapshot = _load("working.json")
        output = render_snapshot(snapshot)
        self.assertNotIn("Host", output)

    def test_markdown_special_chars_escaped_in_focus(self) -> None:
        snapshot = _load("blocked_with_markdown.json")
        output = render_snapshot(snapshot)
        # ** around "settings" must be escaped so it doesn't render as bold
        focus_line = [l for l in output.splitlines() if "Current Focus" in l][0]
        self.assertNotIn("**settings**", focus_line)
        self.assertIn("settings", focus_line)

    def test_markdown_special_chars_escaped_in_blockers(self) -> None:
        snapshot = _load("blocked_with_markdown.json")
        output = render_snapshot(snapshot)
        # [ and ] must be escaped so they don't create a link
        blocker_lines = [l for l in output.splitlines() if "spec" in l]
        self.assertTrue(any(r"\[spec\]" in l or "spec" in l for l in blocker_lines))
        for line in blocker_lines:
            self.assertNotIn("[spec](", line)

    def test_multiline_focus_normalized_to_single_line(self) -> None:
        snapshot = _load("multiline_text.json")
        output = render_snapshot(snapshot)
        self.assertIn("Line one Line two Line three", output)

    def test_multiline_blocker_normalized_to_single_line(self) -> None:
        snapshot = _load("multiline_text.json")
        output = render_snapshot(snapshot)
        self.assertIn("First line Second line", output)

    def test_extra_whitespace_normalized(self) -> None:
        snapshot = _load("working.json")
        snapshot["current_focus"] = "Implement   core\tlogic"
        output = render_snapshot(snapshot)
        self.assertIn("**Current Focus:** Implement core logic", output)

    def test_deterministic_output(self) -> None:
        snapshot = _load("working.json")
        self.assertEqual(render_snapshot(snapshot), render_snapshot(snapshot))

    def test_provider_examples_renderable(self) -> None:
        for example in sorted((ROOT / "examples").glob("*.json")):
            snapshot = json.loads(example.read_text())
            result = validate_snapshot(snapshot, strict_paths=True)
            if result.is_valid:
                output = render_snapshot(snapshot)
                self.assertIn("## Snapshot:", output, f"failed for {example.name}")


class RenderCliTest(unittest.TestCase):
    """CLI-level tests for the render subcommand."""

    def test_valid_snapshot_returns_zero_and_markdown(self) -> None:
        result = _cli_render("tests/fixtures/render/working.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Snapshot:", result.stdout)

    def test_absolute_path_returns_one(self) -> None:
        result = _cli_render("tests/fixtures/render/absolute_path.json")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("[ERROR]", result.stderr)

    def test_invalid_json_returns_two(self) -> None:
        result = _cli_render("tests/fixtures/invalid/malformed.json")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("[ERROR] [invalid_json]", result.stderr)

    def test_schema_violation_returns_one(self) -> None:
        result = _cli_render("tests/fixtures/invalid/missing-agent-id.json")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("[ERROR]", result.stderr)

    def test_completed_candidate_cli_output(self) -> None:
        result = _cli_render("tests/fixtures/render/completed_candidate.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("completed_candidate", result.stdout)
        self.assertIn("is not a command to close the parent task", result.stdout)

    def test_existing_validate_still_works(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agent_work_snapshot", "validate",
             "examples/codex.snapshot.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
