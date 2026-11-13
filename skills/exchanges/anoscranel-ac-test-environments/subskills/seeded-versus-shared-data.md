---
name: seeded-versus-shared-data
domain: software-engineering/seeded-versus-shared-data
trigger: "Deciding what data tests run against and where it comes from."
anti_trigger: "Not for test case design, and not for production data governance."
scope: "Where test data comes from and why it ages."
status: seedling
---

# Seeded versus shared data

## Standard

Test data comes from three sources, each honest about something different. Synthetic seed data is written to exercise known paths — it tests exactly what its author thought of and nothing else. A masked copy of production brings the real shapes and the real oddities — it tests what actually occurs, and it inherits production's sensitivity, so the masking must be the real work. A shared mutable dataset, whichever way it started, accumulates history: every test that writes to it changes what the next test meets, and the suite's results begin to depend on how many tests ran today.

Aging is the failure both static sources avoid. Seed data written last year no longer resembles the shapes the application now produces; a production snapshot grows stale the moment the schema moves. The discipline is dating and refreshing: record when the data was made, what made it, and how it is refreshed, and treat a data source the way you treat a dependency — pinned, versioned, and replaced deliberately.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Record the source class per dataset: synthetic, masked production, or shared-mutable.
- Never let one suite write to a dataset another suite reads without a reset between.
- For masked production data, record the masking method and the field inventory it covers.
- Record each dataset's creation date and refresh cadence.
- Prefer immutable datasets per run: create, test, drop.
- Keep the masking method under test as carefully as the data it protects.

## Procedure

1. Classify every dataset a suite depends on by source class.
2. Identify writes into shared datasets and add per-run reset or isolation.
3. Date every dataset and define its refresh trigger.
4. Review masked data for fields the masking inventory misses.
5. Move suites toward create-test-drop datasets where feasible.
6. Record the classification, dates, and refresh rules.

## Anti-patterns

- A shared staging database that every team writes into.
- Seed data older than the last schema migration.
- Production copies with only obvious fields masked.
- Masking applied once, never re-tested after schema changes.
- Debugging failing tests by editing the shared dataset by hand.

## Done checklist

- [ ] Datasets classified by source.
- [ ] Shared-write isolation added.
- [ ] Creation dates and refresh recorded.
- [ ] Masking inventory reviewed.
- [ ] Create-test-drop adopted where feasible.
- [ ] Classification documented.

## Sources

- Test data management practice: <https://martinfowler.com/articles/continuousIntegration.html>
- Snapshot and reset patterns: <https://docs.docker.com/>
- Data protection in non-production environments: <https://csrc.nist.gov/>
