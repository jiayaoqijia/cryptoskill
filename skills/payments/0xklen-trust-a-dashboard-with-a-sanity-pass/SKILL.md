---
name: trust-a-dashboard-with-a-sanity-pass
description: Use when reading or shipping a dashboard number. Runs a fixed sanity pass — freshness, totals, nulls, defaults — before the figure drives a decision.
---

# Trust a Dashboard with a Sanity Pass

A dashboard that is wrong looks exactly like one that is right. Run the same cheap checks every time before quoting a number to someone who will act on it.

## Procedure

1. Check freshness: compare the last good timestamp to now and to the expected schedule. A stale tile is the most common silent failure.
2. Reconcile a headline total against the source table for a fixed day, with matched filters:
   ```sql
   SELECT (SELECT count(*) FROM events WHERE day = '2026-09-15')        AS src,
          (SELECT value FROM dashboard_daily WHERE day = '2026-09-15')  AS dash;
   ```
3. Check the default filter. A dashboard opening on "last 7 days" is frequently read as "this quarter" — confirm what the viewer sees.
4. Look for null and incomplete rates: a step with 3% nulls is measuring a different population.
5. Eyeball the series for flatlines (pipeline stopped) and for steps (definition changed). A perfectly flat line is a broken feed, not stability.
6. Compare week-over-week and year-over-year on the same tile; a number that moved for calendar reasons should not be read as a break.
7. Note the definition and version behind each quoted figure so the next reader can reproduce it.

## Pitfalls

- The dashboard's boundary timezone differs from the warehouse; midnight UTC and midnight local disagree on every day's total.
- A tile filtered to exclude internal traffic while the source does not will never reconcile.
- Row-level security can silently scope a dashboard to the viewer's region, making it look wrong to everyone else.
- Percentages recomputed from rounded displayed values drift from the underlying rate.
- "It loaded" is not "it is fresh" — caching serves yesterday's number with today's timestamp.
- A dashboard that reconciles today may not reconcile last quarter if the pipeline was rebuilt; spot-check an old date.
- Defaults differ per viewer role (an admin sees internal traffic); compare two numbers only under the same role.

## Verification

    psql "$DSN" -c "SELECT max(day) AS latest_day, count(*) AS rows FROM dashboard_daily;"
    # latest_day must match the schedule; reconcile the headline against events for that day

Report: "Dashboard fresh to 2026-09-15; headline reconciled to source within 0.2%; two tiles showed flatlines (stalled pipeline) and were excluded from the review deck."
