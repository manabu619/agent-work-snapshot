"""Render a validated agent work snapshot as a Markdown checkpoint."""

from __future__ import annotations

import re
from typing import Any

# Characters that need escaping in Markdown paragraph / table-cell text.
# Hyphens are excluded: they only act as list markers at line start,
# which cannot happen inside a table cell or a field-value line.
_MD_ESCAPE_RE = re.compile(r"([\\`*_{}\[\]()#+!|])")


def _escape(text: str) -> str:
    """Escape Markdown special characters in inline free-text."""
    return _MD_ESCAPE_RE.sub(r"\\\1", text)


def _normalize(text: str) -> str:
    """Collapse newlines and extra whitespace in free-text fields."""
    return " ".join(text.splitlines()).strip()


def _inline(value: str | None) -> str:
    """Normalize and escape a nullable free-text value for inline display."""
    if value is None:
        return "None"
    normalized = _normalize(value)
    return _escape(normalized) if normalized else "None"


def _list_section(items: list[Any]) -> str:
    """Render a list field as Markdown bullet points, or 'None'."""
    if not items:
        return "None"
    lines = []
    for item in items:
        normalized = _normalize(str(item))
        lines.append(f"- {_escape(normalized)}")
    return "\n".join(lines)


def render_snapshot(snapshot: dict[str, Any]) -> str:
    """Return a deterministic Markdown string for a validated snapshot dict."""
    snapshot_id = str(snapshot.get("snapshot_id", ""))
    agent_id = str(snapshot.get("agent_id", ""))
    host_id = snapshot.get("host_id")
    parent_task_id = str(snapshot.get("parent_task_id", ""))
    status = str(snapshot.get("status", ""))
    observed_at = str(snapshot.get("observed_at", ""))
    source = str(snapshot.get("source", ""))
    ttl_seconds = snapshot.get("ttl_seconds", "")

    progress = snapshot.get("progress", {})
    total = progress.get("total", 0)
    completed = progress.get("completed", 0)
    blocked_count = progress.get("blocked", 0)

    current_focus = _inline(snapshot.get("current_focus"))
    blockers = _list_section(snapshot.get("blockers") or [])
    outputs = _list_section(snapshot.get("outputs") or [])
    next_checkpoint_at = snapshot.get("next_checkpoint_at") or "None"

    lines: list[str] = []
    lines.append(f"## Snapshot: {snapshot_id}")
    lines.append("")

    # IDs and enum values go into backtick code spans — no Markdown escaping needed.
    table_rows: list[tuple[str, str]] = [
        ("Agent", f"`{agent_id}`"),
        ("Task", f"`{parent_task_id}`"),
        ("Status", f"`{status}`"),
        ("Observed", observed_at),
        ("Source", source),
        ("Progress", f"{completed} / {total} completed, {blocked_count} blocked"),
        ("TTL", f"{ttl_seconds}s"),
    ]
    if host_id is not None:
        table_rows.insert(1, ("Host", f"`{host_id}`"))

    lines.append("| | |")
    lines.append("|---|---|")
    for label, value in table_rows:
        lines.append(f"| **{label}** | {value} |")
    lines.append("")

    lines.append(f"**Current Focus:** {current_focus}")
    lines.append("")
    lines.append("**Blockers:**")
    lines.append("")
    lines.append(blockers)
    lines.append("")
    lines.append("**Outputs:**")
    lines.append("")
    lines.append(outputs)
    lines.append("")
    lines.append(f"**Next Checkpoint:** {next_checkpoint_at}")

    if status == "completed_candidate":
        lines.append("")
        lines.append(
            "> `completed_candidate` is a report that work may satisfy completion "
            "criteria. It is not a command to close the parent task."
        )

    lines.append("")
    return "\n".join(lines)
