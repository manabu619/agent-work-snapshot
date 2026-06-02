# Markdown Handoff Renderer

The `render` command converts a validated snapshot JSON file into a short
Markdown checkpoint summary suitable for handoff documents, pull request
descriptions, or status updates.

## Usage

```bash
agent-work-snapshot render snapshot.json
```

Output is written to stdout. Redirect to a file if needed:

```bash
agent-work-snapshot render snapshot.json > checkpoint.md
```

## Output Format

The renderer produces a deterministic Markdown document with the following
sections:

- A heading with the snapshot identifier
- A table of core fields (agent, task, status, observed time, source,
  progress, TTL, and optional host)
- Current focus
- Blockers (or `None`)
- Outputs (or `None`)
- Next checkpoint time
- A disclaimer when status is `completed_candidate`

## Example

Given `examples/codex.snapshot.json`:

```bash
agent-work-snapshot render examples/codex.snapshot.json
```

Produces:

```markdown
## Snapshot: snap_codex_0001

| | |
|---|---|
| **Agent** | `example-codex-agent` |
| **Task** | `task_example_0001` |
| **Status** | `working` |
| **Observed** | 2026-01-01T00:00:00Z |
| **Source** | local_file |
| **Progress** | 1 / 3 completed, 0 blocked |
| **TTL** | 3600s |

**Current Focus:** Add validation tests

**Blockers:**

None

**Outputs:**

- tests/test_validation.py

**Next Checkpoint:** 2026-01-01T01:00:00Z
```

## Validation

The renderer always applies strict path validation. Snapshots that contain
absolute local paths are rejected with a non-zero exit code.

The renderer does not write to files, call external services, or perform
any operation beyond reading the snapshot and writing Markdown to stdout.

## Safety

Free-text fields (`current_focus`, `blockers`, `outputs`) are:

- Normalized: newlines and extra whitespace are collapsed to a single space
- Escaped: Markdown special characters are escaped to prevent unintended
  rendering

`completed_candidate` is accompanied by a disclaimer noting that it is a
report, not a command to close the parent task.

See [privacy model](privacy-model.md) for guidance on what should and should
not appear in snapshot fields.
