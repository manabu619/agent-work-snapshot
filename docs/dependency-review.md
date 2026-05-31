# Dependency Review

## Runtime Dependency

| Package | Constraint | Purpose | License |
|---|---|---|---|
| `jsonschema` | `>=4.23,<5` | Draft 2020-12 validation | MIT |
| `rfc3339-validator` | `>=0.1.4,<1` | `date-time` format checking | MIT |

The wider `jsonschema[format-nongpl]` extra was evaluated but is not required
for this small contract. A direct `rfc3339-validator` dependency keeps the
runtime dependency set smaller.

Before release, record the resolved dependency list from an isolated
environment and review package metadata.

## Resolved RC Environment

| Package | Resolved version | License metadata |
|---|---|---|
| `jsonschema` | `4.26.0` | MIT |
| `attrs` | `26.1.0` | MIT |
| `jsonschema-specifications` | `2025.9.1` | MIT |
| `referencing` | `0.37.0` | MIT |
| `rpds-py` | `2026.5.1` | MIT |
| `rfc3339-validator` | `0.1.4` | MIT |
| `six` | `1.17.0` | MIT |
| `typing-extensions` | `4.15.0` | PSF-2.0 |

This is an RC environment snapshot, not a lock file. Re-run the metadata review
before publishing a release.
