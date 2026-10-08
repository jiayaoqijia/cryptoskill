---
name: denormalise-to-avoid-a-hot-join
description: Use when a hot read path joins many tables on every request — add a maintained counter or materialized copy, and prove the write path keeps it correct with a reconciliation query.
---

# Denormalise to avoid a hot join

A join over five tables on every read of the front page costs more than the read is worth. A precomputed row or counter column removes the join, but only if the write path keeps the copy correct. Transform read cost into write cost deliberately.

## Procedure

1. Prove the join is the cost before denormalising: `EXPLAIN (ANALYZE, BUFFERS)` the read path and confirm the join nodes dominate. Never denormalise a query that is slow for another reason.
2. Choose the shape: a counter column for aggregates (`comment_count`), a materialized view with a refresh policy for read-mostly analytics, or a copy table updated on write for a feed page.
3. Maintain the copy in the same transaction as the write so a crash between statements cannot let it drift:
```sql
BEGIN;
INSERT INTO comments(post_id, body) VALUES ($1, $2);
UPDATE posts SET comment_count = comment_count + 1 WHERE id = $1;
COMMIT;
```
4. Or use a trigger when writes arrive from many code paths you cannot audit:
```sql
CREATE TRIGGER bump AFTER INSERT ON comments FOR EACH ROW
EXECUTE FUNCTION posts_bump_comment_count();
```
5. For a materialized view, `REFRESH MATERIALIZED VIEW CONCURRENTLY` (needs a unique index) refreshes without locking reads; schedule it off peak.
6. Add a reconciliation check that compares the denormalized value to the source aggregate and alarms on divergence — the copy is now a second source of truth.
7. Index the denormalized column so the read becomes a single index scan.

## Pitfalls

- Maintaining the copy outside the write transaction, so a mid-way failure leaves it permanently stale.
- A trigger that assumes one row per statement but is defined `FOR EACH ROW` or vice versa.
- `REFRESH MATERIALIZED VIEW` without `CONCURRENTLY` takes an exclusive lock and blocks all reads for the refresh.
- Denormalising before proving the join is the bottleneck; the added write complexity buys nothing.
- Counter drift when an `UPDATE ... n = n + 1` is rolled back with its parent transaction.
- No reconciliation job, so drift is discovered by a user instead of an alarm.

## Verification

    psql -c "SELECT p.id, p.comment_count,
                    (SELECT count(*) FROM comments c WHERE c.post_id=p.id) AS real
             FROM posts p
             WHERE p.comment_count <> (SELECT count(*) FROM comments c WHERE c.post_id=p.id)
             LIMIT 10;"
    # pass: zero diverging rows; the refresh/reconcile job runs clean

Report the join removed, the denormalized shape chosen, how the write path maintains it, and the reconciliation query result.
