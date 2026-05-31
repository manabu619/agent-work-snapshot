# Contract Reference

Agent Work Snapshot is a read-only JSON report emitted by an agent or adapter.
It does not instruct a parent system to mutate canonical task state.

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

## Reconciliation

A collector or control plane can store snapshots as append-only observations.
When a snapshot becomes stale, reports a blocker, or declares
`completed_candidate`, downstream policy decides the next action.

Do not treat a snapshot as a direct mutation command.

A reducer is a function that receives a validated, approved event and returns
the next canonical state. It does not process raw snapshots.
