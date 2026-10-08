---
name: track-scd-type-2-history
description: Use when downstream needs an entity's state as of a past date, not just its current row. Keeps full history with valid-from/valid-to ranges and a current flag that stays consistent.
---

# Track SCD Type 2 History

Overwriting a dimension row loses the state reports need for "as of last quarter". Type-2 slowly changing dimensions keep every version with validity ranges, and the current row is simply the one with an open end.

## Procedure

1. Add control columns: `valid_from`, `valid_to` (NULL or a sentinel like `9999-12-31` for current), `is_current`, and a version number. Natural key plus `valid_from` is the row's key.
2. Detect a change by comparing the incoming row to the current version on the tracked attributes (`name`, `tier`, `address`), ignoring non-tracked ones (`last_seen`).
3. On a change, in one transaction: close the current row (`valid_to = change_ts`, `is_current = false`) and insert the new version (`valid_from = change_ts`, `valid_to = sentinel`, `is_current = true`).
4. Use a merge/upsert keyed on the natural key so a replay closes the same version rather than creating a duplicate open row.
5. Query as-of with a half-open range: `WHERE valid_from <= :asof AND (valid_to > :asof)`. Index on the natural key and the range.
6. Never delete closed versions; they are the history the table exists to keep.
7. Backfill from a changes log if one exists, deriving versions with lagged timestamps; otherwise history starts now.
8. Enforce the invariant: exactly one `is_current` row per natural key, checked by a nightly test.
9. Use a single `change_ts` for both the close and the open, so adjacent ranges are contiguous with no gap or overlap.
10. Derive `is_current` rather than storing it if your engine allows, to remove a column that can drift.

## Pitfalls

- Two open rows for one key appear when a change is applied twice without closing the prior version first.
- Using the next row's `valid_from` for `valid_to` inconsistently with a sentinel makes the as-of query miss the current row.
- Detecting changes over non-tracked columns (a `last_seen` heartbeat) creates a new version every run.
- No transaction around close and insert leaves a moment with zero or two current rows.
- Comparing with `=` on floats or case-sensitive strings creates spurious versions.
- Deleting closed history to clean up removes the point of the table.
- Backfilling with `valid_from` equal to load time loses the real effective date.
- Overlapping ranges from two concurrent writers make an as-of query return two rows.

## Verification

```sh
psql -c "SELECT natural_key, count(*) FROM dim WHERE is_current GROUP BY 1 HAVING count(*)>1"
psql -c "SELECT * FROM dim WHERE natural_key=:k ORDER BY valid_from"
```

Zero keys with more than one current row, and no gaps or overlaps in the ranges. Report versions created, keys changed, and any key with a broken timeline.