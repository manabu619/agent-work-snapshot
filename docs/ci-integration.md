# CI Integration Example

Validate a committed snapshot in GitHub Actions with the released Python CLI:

```yaml
name: validate-agent-work-snapshot

on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install "agent-work-snapshot @ git+https://github.com/manabu619/agent-work-snapshot.git@v0.1.0"
      - run: agent-work-snapshot validate --strict-paths path/to/snapshot.json
```

Keep the dependency pinned to a reviewed tag. A snapshot is still a report,
not a command to update canonical task state.

