# Migration Notes

This package uses the public `agent-work-snapshot/v1` identity.

When adapting an internal checkpoint format:

| Internal-style value | Public recommendation |
|---|---|
| Storage-specific `drive_inbox` | `file_inbox` |
| Generic export without transport detail | Use the delivery method, such as `local_file` or `ci_artifact` |
| Required real host name | Omit `host_id` or use a pseudonymous identifier |
| Internal task naming rule | Use any stable identifier matching the public pattern |
| Absolute output path | Use a relative path or artifact reference |

Do not copy full transcripts, approval logs, internal identifiers, or local
paths into a public snapshot.

