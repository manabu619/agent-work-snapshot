# PyPI Publication Evaluation

Status: deferred. This document does not authorize package publication.

The GitHub repository and tagged releases are currently the public
distribution source. Publishing the Python CLI to PyPI may improve onboarding,
but it creates an additional release channel that needs explicit ownership and
maintenance rules.

## Decision

Do not publish a package yet.

Before any first publish, a maintainer must approve the release channel,
confirm project ownership, verify the package name immediately before use, and
choose an authenticated publication method. Do not store registry credentials
in this repository.

## Ownership

Before publication, record the following in private maintainer operations
notes:

- PyPI project owner
- backup owner or recovery contact
- approved publication method
- credential rotation or revocation path
- account recovery procedure

The public repository should contain process documentation only, not account
identifiers, tokens, recovery details, or credentials.

## Publication Gate

Every package publication requires an explicit human approval record:

```text
package_publish: approved
version:
tag:
artifact_review: passed
test_install: passed
dependency_review: passed
sanitation_review: passed
```

Approval for a GitHub Release does not imply approval for a PyPI publish.

## Candidate Release Procedure

After approval:

1. Confirm the version and Git tag match.
2. Build wheel and source distribution artifacts from a clean checkout.
3. Inspect artifact contents and package metadata.
4. Install the wheel into an isolated environment.
5. Run `agent-work-snapshot --version` and validate a provider-neutral example.
6. Re-run tests, dependency review, and sanitation review.
7. Publish through the separately approved authenticated method.
8. Confirm the registry page and a fresh install from the registry.
9. Record the release evidence without storing credentials.

## Rollback

Published versions must be treated as immutable.

If a release is defective:

1. Stop promoting the affected version.
2. Yank the affected version in the registry when appropriate.
3. Publish a corrected patch version after the normal approval gate.
4. Revoke or rotate credentials immediately if exposure is suspected.
5. Document the incident and recovery evidence without copying secret values.

## Open Questions

- Is PyPI distribution needed before external users request it?
- Who will be the primary and backup project owners?
- Which authenticated publication method will be approved?
- Should the first package publish wait for the next maintenance release?
