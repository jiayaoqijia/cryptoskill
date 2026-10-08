---
name: expand-contract-a-database-column
description: Use when renaming or retyping a column that live code still reads — use the expand/migrate/contract pattern so old and new app versions run against the same database during deploy.
---

# Expand/contract a database column

A column rename breaks running code the instant it deploys. Split it into expand (add), migrate (dual-write and backfill) and contract (drop) across releases, so every deploy step is compatible with the version before it.

## Procedure

1. **Expand** — add the new column beside the old; release A writes both, reads the old:
```sql
ALTER TABLE users ADD COLUMN email_address text;   -- nullable first
-- release A: writes email + email_address, reads email
```
2. **Backfill** in batched updates to avoid a long lock:
```sql
UPDATE users SET email_address = email
WHERE email_address IS NULL AND id IN
  (SELECT id FROM users WHERE email_address IS NULL LIMIT 5000);
-- repeat until 0 rows affected
```
3. Verify the backfill is complete before flipping reads:
```sql
SELECT count(*) FROM users WHERE email_address IS NULL;   -- must be 0
```
4. **Migrate** — release B reads the new column while still writing both:
```
release A: write {old,new}  read {old}
release B: write {old,new}  read {new}
```
5. **Contract** — release C stops writing the old column; a later release drops it:
```sql
ALTER TABLE users DROP COLUMN email;
```
6. Add NOT NULL/unique only in the contract phase, after step 3 proves no nulls:
```sql
ALTER TABLE users ALTER COLUMN email_address SET NOT NULL;
```
7. Keep each migration reversible per `make-a-schema-migration-reversible`, and test the mixed state: old app + new DB and new app + new DB.

## Pitfalls

- Adding a column with `NOT NULL DEFAULT` on older Postgres rewrites the table under an exclusive lock. Add NULL, backfill, then constrain.
- Skipping the dual-write during backfill loses writes that land after it. The dual-write window must cover the whole backfill.
- Dropping the old column before every reader has moved breaks rollback to the prior release. Contract only after the old version is fully retired.
- A backfill in one `UPDATE` on a large table holds a lock long enough to stall production. Always batch.

## Verification

```
psql -c "SELECT count(*) FROM users WHERE email_address IS NULL" && psql -c "SELECT count(*) FROM users WHERE email <> email_address"
```
Passes = both queries return `0` before the contract phase. Report: "email→email_address expanded, backfilled 2.4M rows in 5000-row batches, 0 nulls and 0 mismatches, contract queued for release C."
