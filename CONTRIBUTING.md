# Contributing

Keep changes focused on the small snapshot contract and validator.

## What We Welcome

- Validation error improvements
- Focused conformance fixtures
- Documentation fixes and CI examples
- Privacy guardrail improvements

For a behavior change, open an issue before sending a pull request. This keeps
the core contract small and makes the compatibility impact explicit.

## Schema Compatibility

`agent-work-snapshot/v1` changes should remain backward-compatible. Additive,
optional fields require a documented use case. A breaking schema change needs a
new contract version and must not silently change the meaning of an existing
field.

## Validation

Before submitting a change:

```bash
python -m unittest discover -s tests -v
python scripts/validate_examples.py
python scripts/validate_fixtures.py
```

Do not add real host names, personal information, secrets, transcripts, or
absolute local paths to fixtures or documentation.
