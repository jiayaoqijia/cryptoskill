---
name: type-generation
domain: software-engineering/type-generation
trigger: "Deriving types from a schema and catching when they drift."
anti_trigger: "Not for designing the schema itself, and not for hand-authored types."
scope: "Deriving types from schemas and detecting drift."
status: seedling
---

# Type generation

## Standard

Type generation derives definitions from a source of truth — an OpenAPI document, a protobuf schema, a database schema — so that the producer's contract and the consumer's expectations come from one artifact instead of two that agree by effort. The value is elimination: a field the producer adds appears to the consumer as a real field, and a field the producer removes becomes a visible compile error rather than a silent runtime surprise.

Drift is the failure this wiring must catch. A schema can change, and unless the derived types are regenerated and the diff reviewed, consumers compile against a truth the producer has already abandoned. The control is CI: regenerate, diff against the committed types, and fail on any difference, so the drift is detected the moment it exists rather than the moment it bites.

Primary source: <https://www.openapis.org/>.

## Decision rules

- Record each schema that types are derived from and the generator version used.
- Pin the generator version; a generator upgrade can change output without any input changing.
- Commit the derived types and add a CI drift check: regenerate and diff.
- Review generator upgrades as output-affecting changes even when no input changed.
- Record which language targets are generated and their compatibility assumptions.
- Bind the generated types to the contract tests so the shape is validated, not just compiled.

## Procedure

1. List schemas, generators, versions, and output targets.
2. Pin generator versions.
3. Commit outputs and wire the regenerate-and-diff CI check.
4. Change one schema field and confirm the diff check fires.
5. Upgrade a generator deliberately and review the output-only diff.
6. Record the pipeline and what each check catches.

## Anti-patterns

- Generating fresh each build with no record of generator version.
- Unpinned generators, where output changes from under the contract.
- Editing generated types to make a compile pass.
- A drift check that regenerates but ignores the diff result.
- Assuming a compiled type means a validated contract.

## Done checklist

- [ ] Schemas and generator versions pinned and recorded.
- [ ] Outputs committed.
- [ ] Regenerate-and-diff wired in CI.
- [ ] Drift check proven to fire.
- [ ] Generator upgrade reviewed as output-affecting.
- [ ] Pipeline documented.

A subtlety worth recording is the difference between optional in the schema and nullable in the target language: the two are often confused by naive mappings, and a generated type that marks a field optional when it is merely nullable pushes null-handling bugs into every consumer. Checking the mapping of these two concepts per target is a one-time review that prevents a recurring class of defect.

## Sources

- OpenAPI specification: <https://www.openapis.org/>
- Protocol Buffers schema guide: <https://protobuf.dev/overview/>
- Reproducible generation diffs: <https://reproducible-builds.org/>
