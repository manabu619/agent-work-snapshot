# Changelog

## Unreleased

- Add `render` command: converts a validated snapshot JSON to a Markdown
  checkpoint summary.
- Free-text fields are normalized (newlines collapsed) and Markdown-escaped.
- Absolute local paths are always rejected by the renderer (strict mode).
- `completed_candidate` output includes a disclaimer that it is not a close command.

- Add a WBS-driven AI Work Control concept document and README link that
  position Agent Work Snapshot as a small, human-supervised checkpoint
  contract.
- Record the post-release CI integration and private vulnerability-reporting
  guidance refinements.

## 0.1.2 - 2026-06-01

- Add a schema conformance fixture matrix with representative valid and invalid
  snapshots.
- Add stable validation finding categories for automation-friendly CLI
  integration.
- Document the extension-field compatibility policy for the closed `v1`
  contract.
- Document the separate approval gate for any future PyPI publication.

## 0.1.1 - 2026-05-31

- Add CLI `--version`.
- Add a clone-based Quick Start and CI integration example.
- Add a stable public schema URL.
- Add Windows activation guidance, an implementation glossary, and schema
  compatibility guidance for contributors.
- Make the Claude Code example identifier explicitly synthetic.

## 0.1.0 - 2026-05-31

- Add `agent-work-snapshot/v1` JSON Schema.
- Add Python validation CLI.
- Add provider-neutral examples and policy tests.
- Add privacy, migration, pilot, dependency, and roadmap documentation.
