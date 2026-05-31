# Sanitation Review

Date: 2026-05-31 JST
Status: Release-candidate scan completed

## Scope

This repository was created as a new allowlist-based working copy. It was not
copied wholesale from an internal repository.

## Scan Notes

- Common secret-shape scan: no findings.
- Forbidden file scan: no committed `.env`, database, or macOS metadata files.
- Internal identifier scan: no real user names, email addresses, internal
  project names, or real host names should be present.
- `/Users/` appears only in the validator rule and anonymized rejection
  fixtures. These are intentional test literals, not real local paths.
- Git history scan after the local release-candidate commit: passed.
- `gitleaks`: not available in the local environment. Common secret-shape scan
  and manual review were used for this release candidate.

## Manual Review Boundary

The validator is not a data-loss-prevention (DLP) tool. A separate secret scan
and human review remain required before publication.
