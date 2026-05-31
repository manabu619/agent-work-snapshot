# Cowork Review Decisions

## Review 0001

Accepted:

- Add a problem statement near the README entry point.
- Add a Mermaid flow diagram to the README.
- Expand data-loss-prevention (DLP) on first use.
- Define reducer input and output more explicitly.
- Keep `host_id` optional and pseudonymous.
- Clarify provider names are examples, not official integrations.

## Review 0002

Accepted:

- Keep the `v0.1.0` scope small.
- Add reproducible provider-neutral examples, invalid fixtures, privacy notes,
  initial issues, roadmap, and a manual pilot.
- Keep documentation terminology consistent.

Not accepted:

- Node.js and `npx` commands. The approved implementation language is Python.
- `schema_version: "0.1.0"`. The public contract identity is
  `agent-work-snapshot/v1`.
- Free-text `progress`. The approved contract uses relational counts.
- Object-shaped `outputs`. The initial contract uses relative paths or
  artifact-reference strings.
- Rejecting stale snapshots in schema validation. `ttl_seconds` is validated,
  while freshness is evaluated by the downstream collector at observation
  time.

## Review 0003

Accepted:

- Add an explicit clone step and Windows activation note to Quick Start.
- Document the actual `schema_version`, structured `progress`, and string-array
  `outputs` contract in README.
- Make the Claude Code example task identifier explicitly synthetic.
- Expand contributor guidance and add an implementation glossary.

Already satisfied:

- README Mermaid rendering. The repository already uses a `mermaid` fence.

