---
name: schema-migrations
domain: software-engineering/schema-migrations
trigger: "\"add a column with no downtime\", \"rename this column\", \"backfill a table\", \"drop this table safely\", \"the migration locked the database\"."
anti_trigger: "First design of the schema (subskills/data-modeling.md); retiring an API surface and moving consumers; restore from backup; feature removal."
scope: "Changing a live schema or data with no downtime: expand-migrate-contract"
status: "seedling"
---

# Schema Migrations

## Standard

- **Expand/contract** (Hodgson "Parallel Change", 2014; https://martinfowler.com/bliki/ParallelChange.html): expand with an additive change, migrate data and reads, then contract after zero readers remain. Each phase deploys and reverts on its own.
- **Never edit an applied migration.** Add a new one. Tools enforce a checksum on the history table.
- **Additive-only discipline**: new columns are nullable or carry a non-volatile default; indexes build CONCURRENTLY; constraints are added NOT VALID then VALIDATE.
- **Full rewrites under AccessExclusiveLock**: ADD NOT NULL without default on a populated table, a validated foreign key in one step, ALTER TYPE to an incompatible type.
- **Rollback reality**: down-migrations rot because they run once. Forward-fix by reverting the read path; expand/contract is the rollback strategy.
- **Rollback is not a backup.** A drop is recovered only by a restore.

## Decision rules

1. A rename or a drop is never one release: expand, dual-write, backfill, cutover, then contract.
2. Migrate in a low-traffic window, with lock and statement timeouts set first.
3. Backfill in batches with a checkpoint cursor, throttled on replication lag. An unbounded single-transaction copy starves production.
4. Every backfill is idempotent: upsert or `WHERE new_col IS NULL`.
5. Shadow-read the new shape and log mismatches. Target under 0.1 % before cutover.
6. Hold a 24–72 hour rollback window before contract. ⚠️ The window length is practitioner convention.
7. A schema drop, a table drop and a data deletion are **human-gated**.
8. Lint the generated SQL, not the ORM source.

## Procedure

1. Write the change as three migrations: expand, backfill, contract.
2. Lint: `squawk migrations/V42__add_status.sql` (concurrent index creation, constraint NOT VALID, no drop column, no NOT NULL without default).
3. Test the chain on a production-sized copy, asserting the catalog state after the migration and that the previous schema still upgrades.
4. Apply expand to production. Old code keeps running.
5. Deploy the dual-write. The old column stays the source of truth.
6. Backfill in throttled batches; record progress in a cursor table.
7. Shadow-read and log mismatches. Wait out the window.
8. Flip reads by flag, then stop the dual-write.
9. After zero readers, apply contract. A human approves the drop.
10. Record the rollback plan in the PR: which flag flips, and until when.

## Anti-patterns

- A rename in a single release.
- Editing an applied migration to fix a typo.
- A single-transaction backfill on a large table.
- A down-migration nobody has run.
- An ORM default that fills a column at read time instead of the database.
- A drop scheduled the same week the last reader ships.

## Done checklist

- [ ] Change split into expand, backfill and contract.
- [ ] Migration lint passes.
- [ ] Chain tested from the previous schema on production-sized data.
- [ ] Backfill idempotent, batched and checkpointed.
- [ ] Rollback window stated with the flag that flips it.
- [ ] Human approved any contract step.

## Sources

- <https://youngju.dev/blog/database/2026-06-16-schema-migration-tools-comparison.en>
- https://martinfowler.com/bliki/ParallelChange.html
