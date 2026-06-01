# Extension-field Policy

`agent-work-snapshot/v1` is intentionally small and closed. The schema sets
`additionalProperties` to `false`, so validators reject unknown fields.

## v1 Rule

Do not add adapter-private metadata to a public `agent-work-snapshot/v1`
snapshot. Store private metadata in an adapter-owned sidecar file or storage
record that is outside this contract.

Examples of metadata that should remain outside a public snapshot:

- provider-specific request identifiers
- local process or session details
- internal routing hints
- private approval records
- environment-specific diagnostic data

The `source` field is extensible because it is a small delivery identifier. It
is not a container for arbitrary metadata.

## Why v1 Stays Closed

Adding an optional field to the schema file while keeping the
`agent-work-snapshot/v1` identity would create an interoperability trap. A
producer could emit the new field while an existing strict `v1` validator
rejects it.

The repository therefore does not silently widen the `v1` field set.

## Future Shared Metadata

When real usage demonstrates a shared metadata need:

1. Open an issue describing the use case and privacy implications.
2. Confirm that the metadata is safe to export and useful across adapters.
3. Propose a new contract version.
4. Evaluate an optional `extensions` object with namespaced keys in that new
   version.
5. Add fixtures, migration notes, and compatibility tests before release.

A future namespaced key should identify its owner clearly, for example:

```json
{
  "extensions": {
    "org.example.adapter": {
      "example_flag": true
    }
  }
}
```

This example is illustrative only. `extensions` is not a valid
`agent-work-snapshot/v1` field.
