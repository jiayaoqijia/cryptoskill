---
name: dedupe-rows-by-natural-key
description: Use when a pipeline ingest produces duplicate rows from retries or multi-source overlap. Removes duplicates by a deterministic natural key with a defined winner rule.
---

# Dedupe Rows by Natural Key

Duplicates arrive from at-least-once delivery, overlapping extracts, or the same entity from two sources. Deduplicate by a stable natural key with an explicit tie-break, so the result is deterministic and stable across runs.

## Procedure

1. Define the natural key: the columns that truly identify one row (`(user_id, event_ts, event_type)`). Not the surrogate `id`, because a duplicate has a new id.
2. Define the winner rule explicitly and make it deterministic: highest `updated_at`, then highest ingestion sequence, then a hash. Never keep an arbitrary row.
3. Size the problem first: `SELECT k, count(*) FROM t GROUP BY k HAVING count(*)>1;`
4. Dedupe with a window function keeping `rn=1`:
   `SELECT * FROM (SELECT *, row_number() OVER (PARTITION BY k ORDER BY updated_at DESC, ingest_seq DESC) rn FROM t) WHERE rn=1`
   BigQuery: `QUALIFY row_number() OVER (...) = 1`.
5. For streaming, keep a keyed state store with the last-seen version and drop older arrivals.
6. Prefer preventing duplicates with an idempotent upsert over deduping after the fact. Dedupe is cleanup, not design.
7. Scope the dedupe to the affected partitions, not the whole history, so it stays affordable.
8. Re-check after dedupe: the same duplicate query must return zero rows.
9. Preserve a merge record (which rows were collapsed and why) so an audit can reconstruct the decision.
10. Add a uniqueness test to CI so the key's uniqueness is asserted continuously, not just cleaned up each night.

## Pitfalls

- Deduping on a key that is not unique in reality (two genuine events share a timestamp) deletes real data; verify the key identifies.
- A non-deterministic winner (bare `row_number()` with no ORDER BY) picks different rows each run and flips results.
- Deduping the whole history every run is O(all rows); scope to affected partitions.
- Nulls in key columns: engines disagree on whether NULLs are equal, so coalesce before grouping.
- Keeping first versus last changes the answer; state which the business expects.
- Deduping a table with downstream consumers changes their history silently.
- A winner rule that references `ingest_seq` fails when the sequence resets on restart, collapsing distinct rows.
- Removing duplicates without recording what was removed makes a later dispute unresolvable.

## Verification

```sh
psql -c "SELECT k, count(*) c FROM t GROUP BY k HAVING c>1"   # expect 0 rows
psql -c "SELECT count(*) FROM t"                              # stable across two runs
```

Zero duplicate groups, and the total row count is unchanged when the dedupe re-runs. Report the natural key, winner rule, rows removed, and the duplicate source (retry versus overlap).