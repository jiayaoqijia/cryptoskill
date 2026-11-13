---
name: database-model-generation
domain: software-engineering/database-model-generation
trigger: "Generating models or query layers from a live database schema."
anti_trigger: "Not for schema migration design, and not for hand-tuning queries."
scope: "Generating query and model layers from the database."
status: seedling
---

# Database model generation

## Standard

The database is a source of truth a generator can read: tables, columns, types, and constraints become model classes and query builders. The freshness problem is more delicate than with a contract file, because a live database changes through migrations rather than through an edit to a checked-in artifact — the generator's input is not in the repository, and the generated layer can silently lag changes that have already shipped to the database.

The control is to generate against a database whose state is itself pinned: a migration-determined schema in CI, the same one the tests run against. Generation then reproduces from a known state, and its output becomes a honest reflection of what the migrations build. Generated against a developer's local database, the same step produces output that describes one machine's current table state — which may be neither what CI has nor what production will have.

Primary source: <https://www.postgresql.org/docs/>.

## Decision rules

- Record whether generation targets models, queries, or both.
- Generate in CI against a schema created by the migrations that tests also build.
- Treat reliably passing migrations through generation — the pinned chain — as the authoritative input.
- Fail generation when the schema it read contains objects it does not understand.
- Invalidate the output layer committed to regenerate when a migration is added.
- Verify that a breaking migration produces a visible generation diff, not a silent no-op for the generated layer.

## Procedure

1. Determine what the generator reads: a live schema connection or a schema file.
2. Wire generation in CI to run after the migration chain creates a schema.
3. Confirm what it emits on an unknown type or unsupported structure — failure, not silence.
4. Add a migration that changes a column and confirm the output visibly changes.
5. Wire the drift check so a new migration without regenerated output fails.
6. Document the input state this generation derives from.

## Anti-patterns

- Generating against a developer's local database.
- A generated layer that does not change visibly when its input did.
- A migration chain that ships without regenerating derived models.
- Muffling generation warnings on unknown types.
- Expecting the generator to encode intent — it encodes the current shape only.

## Done checklist

- [ ] Generation input state identified and pinned.
- [ ] Generation runs after the migration chain.
- [ ] Unknown input structure fails loudly.
- [ ] Migration-to-output visibility verified.
- [ ] Drift check wired and proven.
- [ ] Input provenance documented.

## Sources

- PostgreSQL schema introspection: <https://www.postgresql.org/docs/>
- Schema migration practices: <https://sqitch.org/>
- Reproducibility of derived artifacts: <https://reproducible-builds.org/>
