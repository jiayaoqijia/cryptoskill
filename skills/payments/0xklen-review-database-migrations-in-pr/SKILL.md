---
name: review-database-migrations-in-pr
description: Use when a PR ships a schema change alongside code. Verifies the migration is backward-compatible with the running app and will not lock a large table.
---

# Review database migrations in a PR

A migration that drops a column the old deploy still reads takes the site down for the length of a rollout. Review the migration for compatibility with both the old and new code, and for the lock it takes on a live table.

## Procedure

1. Locate the migration and read it as a sequence of DDL, not as an afterthought: `gh pr diff 482 -- '*migrations*'` or `git diff origin/main...HEAD -- '**/migrations/**'`.
2. Require the expand/contract pattern for any rename or type change:
   - expand: add the new nullable column, backfill in batches, make the app write both,
   - contract: after the old code is gone, drop the old column in a later release.
3. Reject a destructive change in the same PR as the code that stops using the field — those must be separate deploys.
4. Check the lock each statement takes. On Postgres, `ALTER TABLE ... ADD COLUMN ... DEFAULT x` is fast since 11, but `SET NOT NULL` and `ALTER COLUMN TYPE` take an `ACCESS EXCLUSIVE` lock and rewrite the table; on a table over a few million rows that is a production stall.
5. For indexes, require `CREATE INDEX CONCURRENTLY` on Postgres (outside a transaction) so writers are not blocked.
6. Confirm the backfill is batched with a limit and a sleep, not a single `UPDATE` over the whole table.
7. Verify the down migration exists and actually reverses the change, or document why forward-only is intended.

## Pitfalls

- Adding a `NOT NULL` column with no default to a populated table, which fails outright.
- A migration that runs inside the same transaction as the index build, so `CONCURRENTLY` is rejected.
- Renaming a column in place, breaking the previous app version mid-rollout.
- A backfill that runs unbounded and holds row locks for minutes under load.

## Verification

    gh pr diff 482 -- '**/migrations/**'
    # Dry-run against a production-sized copy:
    alembic upgrade head --sql | grep -iE 'ACCESS EXCLUSIVE|NOT NULL|CONCURRENTLY'

Report the DDL statements, the lock level each takes, and whether the change is expand-only or contains a contract step. A contract step bundled with the consuming code is blocking.

## Worked example

A PR renames `users.name` to `users.full_name` and updates the query in the same commit. Mid-rollout the old pods still read `name`, which no longer exists, and return 500s. The expand/contract fix: release 1 adds `full_name` nullable, backfills in batches of 1,000, and writes both columns; release 2 switches reads to `full_name`; release 3 drops `name`.
