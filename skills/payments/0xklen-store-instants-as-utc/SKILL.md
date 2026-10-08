---
name: store-instants-as-utc
description: Use when a timestamp is written to a database, log line or API payload — persist the instant in UTC with an explicit offset, never a bare local wall-clock string.
---

# Store instants as UTC

An instant is a point on the world timeline; a wall-clock reading is not. A UTC (or offset-bearing) value lets two hosts, two timezones and two DST regimes agree about what happened and in what order.

## Procedure

1. Declare the column type, not just the value. In Postgres use `TIMESTAMPTZ`; a plain `TIMESTAMP` silently drops the offset:
```
ALTER TABLE events ALTER COLUMN created_at TYPE timestamptz USING created_at AT TIME ZONE 'UTC';
```
2. Serialize as ISO-8601 with an offset. `2026-03-01T14:00:00Z`, never `2026-03-01 14:00:00`:
```
date -u +%Y-%m-%dT%H:%M:%SZ
```
3. In the application layer, produce aware objects and convert only when formatting:
```python
from datetime import datetime, timezone
now = datetime.now(timezone.utc)            # aware, UTC
row = now.isoformat().replace("+00:00", "Z")  # 2026-03-01T14:00:00Z
```
4. Store the original zone name separately if you ever need to redisplay in the user's local time — UTC loses it. Keep `created_at timestamptz` plus `created_tz text` (`'America/New_York'`).
5. Reject writes that carry no offset at the API boundary. A regex gate on ingress:
```
rg -n '\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?!Z|[+-]\d{2}:?\d{2})' payloads/   # finds bare local stamps
```
6. Migrate legacy local strings by pinning the zone they were written in, not by assuming UTC:
```
UPDATE events SET created_at = created_at AT TIME ZONE 'America/New_York' WHERE created_at_was_local;
```
7. Verify round-trip: write an instant, read it back, and confirm the offset survives.

## Pitfalls

- `--` A naive `TIMESTAMP` column read by a driver set to a different `TimeZone` returns a different wall clock for the same row. The bug looks like "the date changed" with no code change.
- `new Date("2026-03-01")` in JavaScript parses date-only as UTC midnight; `new Date("2026-03-01T00:00")` parses as local. Two spellings, two instants.
- Emitting UTC but truncating the `Z` produces a string that a downstream parser reads as local. Keep the offset suffix.
- Sorting a mixed column of `Z` and `+05:00` strings lexically reorders events across zones; sort parsed instants, not text.

## Verification

```
psql -c "SELECT count(*) FROM events WHERE created_at IS NOT NULL AND pg_typeof(created_at)::text <> 'timestamp with time zone';"
```
Returns `0` = every stored timestamp is offset-aware. Report: "events.created_at is timestamptz, 0 naive rows; API rejects offset-less strings."
