# Agent Instructions

## Scope

Keep this repository small. It provides a read-only JSON checkpoint contract
and validator CLI. Do not add orchestration, database, dashboard, scheduler,
or chat-bot features without an explicit scope decision.

## Validation

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_examples.py
python scripts/validate_fixtures.py
```

## Privacy

Do not commit secrets, personal information, real host names, absolute local
paths, full transcripts, prompts, or chain of thought.
