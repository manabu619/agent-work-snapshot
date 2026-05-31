# Manual Pilot

This pilot confirms that two or more agent environments can emit the same
small contract without sharing transcripts.

## Procedure

1. Create an isolated Python environment and install the package.
2. Validate at least two provider examples.
3. Confirm the same CLI accepts `working`, `blocked`, and
   `completed_candidate` states.
4. Confirm no example contains transcripts, prompt text, secrets, or absolute
   local paths.
5. Run the test suite.

## Commands

```bash
agent-work-snapshot validate examples/codex.snapshot.json
agent-work-snapshot validate examples/claude-code.snapshot.json
agent-work-snapshot validate examples/local-llm.snapshot.json
python -m unittest discover -s tests -v
```

## Expected Result

All examples validate with one provider-independent CLI. No snapshot directly
changes canonical task state.

