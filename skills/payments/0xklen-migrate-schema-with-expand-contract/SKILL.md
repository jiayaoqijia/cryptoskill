---
name: migrate-schema-with-expand-contract
description: Use when a column must be renamed, retyped, or dropped in a dataset with live consumers. Runs the change as expand, migrate, then contract so no consumer breaks.
---

# Migrate Schema with Expand/Contract

A destructive schema change breaks consumers mid-flight. Do it in three releases: add the new shape, move consumers, then remove the old. The change is invisible to anyone reading at any moment.

## Procedure

1. Expand: add the new column (or new enum value) alongside the old, nullable or with a default. Keep the old path working, and write both.
2. Backfill the new column for history with an idempotent job: `UPDATE ... SET new_col = f(old_col)` in bounded chunks. Verify counts match.
3. Dual-write: the producer writes old and new for a deprecation window, so a consumer that has not migrated still works.
4. Migrate consumers one at a time, watching each: dashboards, jobs, exports. Announce the deprecation with a date.
5. Verify no reader of the old column remains: check query logs, lineage downstream edges, `information_schema` usage, and `grep -rn old_col`.
6. Contract: after the deprecation date and zero readers, drop the old column in a separate release.
7. For a rename a format cannot express in place (CSV, Parquet), add the new field, migrate, then stop emitting the old field.
8. Keep the expand release and the contract release far enough apart that a consumer weekend deploy cannot straddle both.
9. For a retype, add a new typed column and let the old one age out; never alter in place on a live table.
10. Record the compatibility mode in the contract and let the registry reject a breaking change at publish.

## Pitfalls

- Dropping then adding in one release breaks every consumer between the two deploys.
- A `NOT NULL` new column added with no default fails existing-row validation.
- Dual-write without a defined end date becomes permanent dual-maintenance.
- Backfilling the new column without an idempotent path double-applies on retry.
- Assuming no reader because the dashboard was updated, when the scheduled export was not.
- Retyping (string to int) in place fails on existing rows; add a new typed column and migrate.
- Dropping the old column before the deprecation window closes catches a consumer mid-migration.
- A default that differs from the backfilled value makes new rows disagree with old ones.

## Verification

```sh
psql -c "SELECT count(*) FROM events WHERE old_col IS NOT NULL AND dt > current_date - 1"
grep -rn "old_col" ./jobs ./dashboards   # expect no hits
```

Zero recent writes to the old column and zero code or log references; only then drop it. Report the new column, the dual-write window, readers migrated, and the drop release.