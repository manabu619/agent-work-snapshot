# Privacy Model

Agent Work Snapshot is designed to report work state without collecting full
agent conversations.

## Do Not Include

- Full transcripts
- Prompt text
- Chain of thought
- Secrets, tokens, credentials, cookies, or sessions
- Personal information
- Absolute local paths
- Real host names
- Local file contents

Use pseudonymous `agent_id` and optional `host_id` values. Prefer relative
paths or artifact references in `outputs`.

## Validator Boundary

The CLI rejects keys that look secret-related and warns about common absolute
local path patterns. These are guardrails, not DLP. Free-text fields can still
contain sensitive values. Run a separate secret scan and human review before
external transmission or publication.

