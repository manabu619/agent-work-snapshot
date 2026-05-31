# Glossary

| Term | Meaning |
|---|---|
| Snapshot | A read-only work-state report emitted by an agent or adapter. |
| Verifier | A reviewer, CI job, test, or linter that checks a completion candidate. |
| Reducer | A function that receives a validated, approved event and returns the next canonical state. |
| `queued` | Work has been delegated but has not started. |
| `working` | Work is in progress. |
| `blocked` | Work cannot continue without resolving a blocker. |
| `checkpoint` | Work is in progress and the snapshot records a resumable point. |
| `completed_candidate` | The agent reports that its work may satisfy completion criteria. This is not a close command. |
| `failed` | The current attempt failed. Downstream policy decides whether to retry, reassign, or stop. |
| TTL | The freshness window represented by `ttl_seconds`. |

