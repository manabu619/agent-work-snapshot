# Contributing

Keep changes focused on the small snapshot contract and validator.

Before submitting a change:

```bash
python -m unittest discover -s tests -v
python scripts/validate_examples.py
python scripts/validate_fixtures.py
```

Do not add real host names, personal information, secrets, transcripts, or
absolute local paths to fixtures or documentation.
