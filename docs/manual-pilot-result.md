# Manual Pilot Result

Date: 2026-05-31 JST
CLI version: `0.1.0`
Environment: isolated Python 3.12 virtual environment

## Results

| Check | Result |
|---|---|
| Codex-style sample | Passed |
| Claude Code-style sample | Passed |
| Gemini CLI-style sample | Passed |
| Local LLM-style sample | Passed |
| `working`, `blocked`, `checkpoint`, `completed_candidate` examples | Passed |
| Invalid fixture rejection | Passed |
| Unit tests | Passed. 14 tests |

The same Python CLI validates snapshots from four provider-neutral examples.
No transcript, prompt text, secret value, or real local path is required.
