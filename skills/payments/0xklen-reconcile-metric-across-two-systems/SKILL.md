---
name: reconcile-metric-across-two-systems
description: Use when two tools report different numbers for the same metric. Traces the gap through filters, joins, timezone, and grain before trusting either figure.
---

# Reconcile a Metric Across Two Systems

The warehouse says 12,400 signups, the product tool says 13,100. Neither is lying; they are counting different things. Reconcile by isolating one source of difference at a time.

## Procedure

1. Freeze the comparison: same date range, same timezone (state it), same filter, same population. Most gaps die here.
2. Compare totals first, then by day, then by segment — the shape of the gap tells you where it enters.
3. Attack the differences in order: (a) event definition, (b) row grain and de-duplication, (c) the JOIN, (d) null handling, (e) late-arriving data.
4. Check de-duplication: one system may count events, the other distinct users. Compare `count(*)` against `count(DISTINCT user_id)`.
5. Check join cardinality — a join to a dimension with duplicate keys fans rows out and inflates one side:
   ```sql
   SELECT (SELECT count(*) FROM a) AS a_rows,
          (SELECT count(*) FROM a JOIN dim USING (k)) AS joined_rows;  -- must be equal
   ```
6. Check timezone: a daily boundary in UTC versus America/New_York shifts several percent of a day's events.
7. Reconcile to the raw event source, the tiebreaker, and document which system is canonical.

## Pitfalls

- Comparing a calendar week to a trailing 7 days manufactures a recurring unexplained gap.
- A slowly-changing dimension joined naively multiplies rows; the bug looks like one system over-counting.
- One tool excludes bots and internal traffic, the other does not; the difference is a filter, not an error.
- Late-arriving events mean the warehouse number keeps rising for the comparison day after the tool has settled.
- Deciding the "right" number without tracing to raw events just picks a favourite.
- A test-event filter (`is_test = false`) present in one system and absent in the other is a definition gap, not a bug.
- Comparing two systems for a day still being written guarantees a gap; always compare a settled day.

## Verification

    psql "$DSN" -c "SELECT count(*) AS events, count(DISTINCT user_id) AS users FROM signups WHERE day = '2026-09-15';"
    # the residual gap after each fix should equal exactly one traced cause

Report: "12,400 vs 13,100 (5.6%) traced to grain: the warehouse counted events, the tool counted users with a session; aligned to distinct users, both report 12,400 within 0.1%."
