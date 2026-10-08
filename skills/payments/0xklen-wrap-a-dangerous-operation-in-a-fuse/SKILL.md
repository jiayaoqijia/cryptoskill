---
name: wrap-a-dangerous-operation-in-a-fuse
description: Use when a single operation (drop, mass delete, backfill, force-push) can destroy more than intended in one call — fronts it with a dry-run count, an explicit bound and a confirmation token so the default is "nothing happens".
---

# Wrap a dangerous operation in a fuse

Some operations fail catastrophically rather than partially: `DROP TABLE`, an unbounded `DELETE`, a backfill with a wrong `WHERE`. The job of a fuse is to make the dangerous thing impossible to trigger by accident and bounded even when triggered on purpose.

## Procedure

1. Always run the *count* first and print it, as a separate step, before the mutation exists:
       SELECT count(*) FROM events WHERE created_at < '2025-01-01';   -- the blast radius
   An operator who has seen "4,120,000 rows" decides differently from one who typed the query blind.

2. Require a bound on the mutation itself, so even a bad `WHERE` cannot affect everything. Postgres does not allow `LIMIT` on `DELETE`, so use a bounded CTE (or a tight loop) and refuse if the count disagrees:
       WITH d AS (SELECT id FROM events WHERE created_at < '2025-01-01' LIMIT 1000)
       DELETE FROM events WHERE id IN (SELECT id FROM d);

3. Gate the operation behind a confirmation token derived from the *data*, not the clock, so a stale plan cannot be run against a changed table:
       token = sha256(f"{table}|{where}|{expected_count}")
       if args.token != token: refuse("dry-run count drifted; re-run the count")

4. Require an explicit bound argument and refuse the default: no `--limit` means do not run; `--limit 0` is not "unlimited" but "nothing". Make the destructive default the no-op.

5. Take a recovery path *before* the mutation: a snapshot, an `EXPLAIN`-into-a-`CREATE TABLE ... AS SELECT` of the rows about to be touched, or a soft-delete column. A fuse that cannot be reversed is just a slower accident. Verify the backup restores in a scratch DB.

6. Run it transactionally and in batches for large operations, committing per batch so a crash stops at a known point rather than rolling back an hour of work — and log the batch size and rows affected per commit.

7. Emit an audit record per invocation: who, token, table, predicate, count, rows affected, timestamp. The record is how the next operator knows what the last one did.

## Pitfalls

- A dry-run that computes the count with a *different* predicate than the mutation, so the guard approves an operation it never measured.
- `DELETE FROM t` with a `WHERE` built by string concatenation from user input — an empty filter deletes the table.
- Dumping a "backup" table into the same database/filesystem as the source, so a corruption or disk-full takes both.
- Running unbounded in one giant transaction on a live table: long locks, replication lag, and a WAL that can fill the disk and take the primary down.

## Verification

    # the dry run must refuse when the count is larger than the declared bound
    psql "$DB" -c "SELECT count(*) FROM events WHERE created_at < '2025-01-01';"
    python tools/mass_delete.py --table events --where "created_at < '2025-01-01'" --expected 1000
    # expect exit 1: "count 4120000 != expected 1000, refusing"
    python tools/mass_delete.py --table events --where "created_at < '2025-01-01'" --expected 4120000 --limit 1000 --dry-run
    # expect a plan, a token, and zero rows changed

Report: the pre-count, the bound and how the tool refuses a mismatch, the recovery artefact and that it restores, and the per-batch rows-affected log.
