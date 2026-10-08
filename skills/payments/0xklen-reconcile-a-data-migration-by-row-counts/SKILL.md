---
name: reconcile-a-data-migration-by-row-counts
description: Use when moving or reshaping data between tables or stores — reconcile source and target by count, key set and checksum so no row is silently dropped or doubled.
---

# Reconcile a data migration by row counts

A migration that "completed without error" can still lose or duplicate rows. Reconcile source against target by count, key set and checksum, and refuse to cut over until the deltas are zero.

## Procedure

1. Snapshot the source baseline before the run:
```sql
SELECT count(*) AS n, coalesce(sum(amount_cents),0) AS total,
       md5(string_agg(id::text, ',' ORDER BY id)) AS keyhash
FROM orders WHERE created_at < '2026-01-01';
```
2. Run with a checkpoint table so a crash resumes instead of restarting — bookmark by the last processed id:
```sql
INSERT INTO mig_checkpoint(last_id, batch) VALUES (:last_id, :batch)
ON CONFLICT (batch) DO UPDATE SET last_id = EXCLUDED.last_id;
```
3. Count the target with the same frozen predicate:
```sql
SELECT count(*), coalesce(sum(amount_cents),0), md5(string_agg(id::text, ',' ORDER BY id)) FROM orders_new;
```
4. Compare three things in order: row counts equal; key sets equal; value checksum equal.
```sql
(SELECT id FROM orders EXCEPT SELECT id FROM orders_new)
UNION ALL
(SELECT id FROM orders_new EXCEPT SELECT id FROM orders);
```
Required: 0 rows.
5. Interpret sums: a lower target total means dropped rows, a higher total means duplication. Quantify `target_n - source_n`.
6. For a huge source, spot-check the transform on a sample — pick 1000 random ids and compare full rows field by field.
7. Cut over only when every delta is zero; otherwise diff a specific id to find the transform bug.

## Pitfalls

- `SELECT count(*)` alone misses duplicates compensated by drops. Always compare the key set with `EXCEPT`.
- The source keeps changing during the run. Freeze the predicate window (`created_at < cutoff`) or read from a snapshot.
- Hash order matters: use `string_agg(..., ORDER BY id)` on both sides or the hashes never match.
- A NULL vs empty-string difference changes no counts but is a real transform bug — compare the transformed values, not only keys.

## Verification

```
psql -c "SELECT (SELECT count(*) FROM orders) AS src, (SELECT count(*) FROM orders_new) AS dst"
```
Passes = `src` equals `dst` and the `EXCEPT` query returns 0 rows. Report: "orders→orders_new reconciled: 2,431,882 == 2,431,882, key diff 0, sum amount_cents equal."
