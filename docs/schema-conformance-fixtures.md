# Schema Conformance Fixtures

The fixture suite documents representative contract boundaries and is enforced
in CI by `python scripts/validate_fixtures.py`.

## Valid Fixtures

| Fixture | Coverage |
|---|---|
| `tests/fixtures/valid/minimal.json` | Required fields, optional `host_id` omitted, nullable checkpoint fields, minimum TTL |
| `tests/fixtures/valid/ttl-maximum.json` | Optional pseudonymous `host_id`, `completed_candidate`, maximum TTL |

## Invalid Fixtures

| Fixture | Coverage |
|---|---|
| `tests/fixtures/invalid/additional-property.json` | Unknown top-level fields |
| `tests/fixtures/invalid/absolute-local-path.json` | macOS absolute local path in strict mode |
| `tests/fixtures/invalid/completed-greater-than-total.json` | Relational progress check |
| `tests/fixtures/invalid/file-users-local-path.json` | `file:///Users/` local path in strict mode |
| `tests/fixtures/invalid/inconsistent-progress.json` | Combined completed and blocked progress exceeds total |
| `tests/fixtures/invalid/invalid-observed-at.json` | Invalid `date-time` format |
| `tests/fixtures/invalid/invalid-snapshot-id.json` | Snapshot ID pattern |
| `tests/fixtures/invalid/malformed.json` | Malformed JSON |
| `tests/fixtures/invalid/missing-agent-id.json` | Missing required field |
| `tests/fixtures/invalid/ttl-too-large.json` | TTL maximum bound |
| `tests/fixtures/invalid/ttl-too-small.json` | TTL minimum bound |
| `tests/fixtures/invalid/unknown-status.json` | Status enum |
| `tests/fixtures/invalid/windows-local-path.json` | Windows user path in strict mode |

## Scope

The fixture suite is intentionally representative rather than exhaustive.
Unit tests cover recursive secret-like keys and warning behavior for local
paths when strict mode is disabled.
