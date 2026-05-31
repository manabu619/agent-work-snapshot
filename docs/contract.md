# Contract Reference

Agent Work Snapshot is a read-only JSON report emitted by an agent or adapter.
It does not instruct a parent system to mutate canonical task state.

Schema URL:
`https://raw.githubusercontent.com/manabu619/agent-work-snapshot/main/schemas/agent-work-snapshot.schema.json`

## Fields

| Field | Required | Purpose |
|---|---:|---|
| `schema_version` | Yes | Contract version. Use `agent-work-snapshot/v1`. |
| `snapshot_id` | Yes | Unique snapshot identifier. |
| `agent_id` | Yes | Pseudonymous agent or adapter identifier. |
| `host_id` | No | Optional pseudonymous execution-environment identifier. |
| `parent_task_id` | Yes | Identifier of the delegated parent task. |
| `observed_at` | Yes | RFC 3339-compatible observation time. |
| `source` | Yes | Extensible transport or delivery identifier. |
| `status` | Yes | Small summary state such as `working`, `blocked`, or `completed_candidate`. |
| `progress` | Yes | Counts for `total`, `completed`, and `blocked`. |
| `current_focus` | Yes | Short current-work summary, or `null`. |
| `blockers` | Yes | Short blocker summaries. |
| `outputs` | Yes | Relative paths or artifact references. |
| `next_checkpoint_at` | Yes | Next planned checkpoint time, or `null`. |
| `ttl_seconds` | Yes | Freshness window from 60 to 604800 seconds. |

## Policy Checks

The CLI enforces relational constraints that JSON Schema does not express:

```text
completed <= total
blocked <= total
completed + blocked <= total
```

It also rejects recursive secret-like keys and reports absolute local paths.

## Validation Categories

Validation findings start with a stable category in square brackets. The
remaining human-readable message may become clearer over time.

| Category | Meaning |
|---|---|
| `schema` | JSON Schema or RFC 3339-compatible format validation failure |
| `secret_like_key` | Recursive key-name policy rejection |
| `progress_relation` | Relational progress policy rejection |
| `absolute_local_path` | Absolute local path warning, or rejection in strict mode |
| `invalid_json` | CLI input is not valid JSON |
| `file_io` | CLI could not read the input file |

## Reconciliation

A collector or control plane can store snapshots as append-only observations.
When a snapshot becomes stale, reports a blocker, or declares
`completed_candidate`, downstream policy decides the next action.

Do not treat a snapshot as a direct mutation command.

A reducer is a function that receives a validated, approved event and returns
the next canonical state. It does not process raw snapshots.
