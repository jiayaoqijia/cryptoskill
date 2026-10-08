---
name: avoid-bare-date-comparisons
description: Use when filtering or joining by a calendar date — compare half-open instant ranges, not DATE() of a timestamp, or you drop or double-count rows at the boundary and across zones.
---

# Avoid bare date comparisons

`WHERE DATE(created_at) = '2026-03-01'` reads as "March 1st" but means "the server's local March 1st", is not index-usable, and silently excludes the last instant of the day. Compare instants with a half-open range instead.

## Procedure

1. Replace date-equality with a half-open interval `[start, end)` in the value's own zone:
```sql
-- wrong: zone-dependent and unindexable
SELECT count(*) FROM events WHERE DATE(created_at) = '2026-03-01';

-- right: half-open UTC range, index usable
SELECT count(*) FROM events
WHERE created_at >= '2026-03-01T00:00:00Z'
  AND created_at <  '2026-03-02T00:00:00Z';
```
2. If the day boundary is a *local* day, compute the local boundaries then convert to the storage zone:
```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
tz = ZoneInfo("America/New_York")
start = datetime(2026, 3, 1, tzinfo=tz).astimezone(timezone.utc)
end   = (datetime(2026, 3, 1, tzinfo=tz) + timedelta(days=1)).astimezone(timezone.utc)
```
3. Never add `86400` seconds to a local start to get the end — a DST day is 23 or 25 hours. Advance the calendar date, then convert.
4. For date-only columns (a real `DATE`), do not convert through a zone at all; compare dates as dates and keep them out of instant joins.
5. Joining a `DATE` to a `TIMESTAMPTZ` should be done by expanding to a range on the instant side, never by casting the instant to date:
```sql
ON e.created_at >= d.day AND e.created_at < d.day + INTERVAL '1 day'
```
6. Check the plan: a `DATE()` on the column defeats the index, a range uses it.
```
EXPLAIN (ANALYZE, BUFFERS) SELECT ... WHERE created_at >= $1 AND created_at < $2;
```
7. For reporting, materialise a `business_date` in the agreed zone as a stored column, so dashboards do not re-derive it differently.

## Pitfalls

- `BETWEEN '2026-03-01' AND '2026-03-02'` includes `2026-03-02 00:00:00`, double-counting one instant at the boundary; half-open ranges do not.
- `DATE(created_at)` in Postgres applies the session `TimeZone`; the same query returns a different count for a client in another zone.
- A DST day is not 24 hours: a local-day report built by adding a day of seconds is off by an hour twice a year.
- Casting a UTC instant to a date for a user east of UTC can push an event into the previous or next day.
- Sort keys built from a string date omit the time and reorder same-day events.

## Verification

```
psql -c "SELECT count(*) FROM events WHERE created_at >= '2026-03-01T00:00:00Z' AND created_at < '2026-03-02T00:00:00Z';"
psql -c "SELECT count(*) FROM events WHERE DATE(created_at AT TIME ZONE 'UTC') = '2026-03-01';"
```
Equal counts = the range reproduces the intended day; `EXPLAIN` shows an index scan. Report: "day filters are half-open UTC ranges; `DATE()` removed from hot queries; counts match, plan is index-only."
