---
name: use-zoneinfo-not-naive-datetime
description: Use when creating or converting datetimes in application code — construct zone-aware objects with an IANA zone, never a naive datetime plus a bare offset.
---

# Use zoneinfo, not a naive datetime

A naive datetime is a wall-clock reading with no location. Attaching a raw offset (`-05:00`) says what the clock was but not what rule produced it, so it cannot answer "what is the local time next week?" Use an IANA zone object end to end.

## Procedure

1. Use `zoneinfo.ZoneInfo` (Python 3.9+) which reads the system tzdata and honours DST rules:
```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
now = datetime.now(timezone.utc)                 # aware, UTC
tokyo = now.astimezone(ZoneInfo("Asia/Tokyo"))   # aware, Tokyo rules
```
2. Attach zones at the boundary where a human gives you a local time, and never earlier:
```python
meeting = datetime(2026, 3, 1, 9, 0, tzinfo=ZoneInfo("Europe/London"))
```
3. Convert, do not re-attach. `dt.replace(tzinfo=tz)` relabels a wall clock; `dt.astimezone(tz)` converts an instant:
```python
wrong = now.replace(tzinfo=ZoneInfo("Asia/Tokyo"))   # same digits, wrong instant
right = now.astimezone(ZoneInfo("Asia/Tokyo"))       # correct instant
```
4. Store the zone *name* a user chose, not the offset, so future conversions survive DST:
```python
user_prefs = {"timezone": "America/New_York"}  # never "-05:00"
```
5. Ban naive construction in review: grep for `datetime.now()` and `datetime(...)` without `tzinfo`:
```
rg -n 'datetime\.now\(\)|datetime\.utcnow|date\.today\(\)' src/
```
`utcnow()` returns a naive object — use `datetime.now(timezone.utc)`.
6. If you must use a third-party library, prefer `zoneinfo`; for legacy `pytz`, use `pytz.timezone(z).localize(naive)`, never `tzinfo=` at construction.
7. Serialise with `.isoformat()` (keeps offset) and parse back with an aware parser.

## Pitfalls

- `datetime.now()` on a host set to `UTC` looks correct in tests and returns local time in production; use `datetime.now(timezone.utc)`.
- Comparing aware and naive datetimes raises `TypeError`; two libraries each producing their own kind is a common integration failure.
- `dateutil.tz.gettz` and `zoneinfo` can disagree if the vendored tzdata is stale; pick one source of zone truth.
- `pandas` timestamps are tz-aware but `Series.dt.tz_localize` vs `tz_convert` are easy to swap — `localize` on an already-aware series raises.
- A fixed offset `+05:30` cannot express that India never shifts; a zone can. Offsets are for display of a known instant, zones for computation.

## Verification

```
python3 -c "from datetime import datetime, timezone; from zoneinfo import ZoneInfo; n=datetime.now(timezone.utc); print(n.astimezone(ZoneInfo('Asia/Tokyo')).utcoffset())"
```
Prints `9:00:00` = Tokyo rules applied to a UTC instant. Report: "all datetimes are zone-aware; grep for naive constructors returns 0 hits outside tests."
