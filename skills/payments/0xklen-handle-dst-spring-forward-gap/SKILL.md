---
name: handle-dst-spring-forward-gap
description: Use when code constructs or schedules a local wall-clock time — a spring-forward transition deletes an hour, so some local times do not exist and must be resolved explicitly.
---

# Handle the DST spring-forward gap

On the spring-forward day the clock jumps 02:00 -> 03:00 and every local time in between does not exist. Treating those times as real produces silent off-by-an-hour drift or an exception deep in a scheduler.

## Procedure

1. Confirm the gap for the zone and year before touching code:
```
zdump -v America/New_York | grep 2026
```
Look for the line showing `Mar  8 06:59:59 2026 UT ... isdst=0` followed by `07:00:00 ... isdst=1` — the local 02:00-03:00 hour is missing.
2. Detect nonexistent local times instead of constructing them blindly:
```python
from datetime import datetime
from zoneinfo import ZoneInfo
tz = ZoneInfo("America/New_York")
naive = datetime(2026, 3, 8, 2, 30)
d = naive.replace(tzinfo=tz)
print(d.utcoffset(), d.timestamp())   # offsets betray the gap
```
3. Pick and document a policy for the gap: **shift forward** (02:30 -> 03:30), **shift back** (01:30), or **skip the occurrence**. Most schedulers shift forward; do not leave it to the library default silently.
```python
def resolve_gap(naive, tz):
    d = naive.replace(tzinfo=tz)
    if d.astimezone(tz).replace(tzinfo=None) != naive:  # normalised away
        return (naive + timedelta(hours=1)).replace(tzinfo=tz)
    return d
```
4. Persist the resolved UTC instant, not the requested local string, so the job does not re-resolve differently on retry.
5. In cron/schedulers, prefer an explicit UTC fire time for anything crossing 02:00 local; the gap never exists in UTC.
6. Regression-test the exact date: `2026-03-08` (US), `2026-03-29` (EU/UK), `2026-10-04` (AU).

## Pitfalls

- `datetime(2026,3,8,2,30)` with `zoneinfo` returns an object whose `utcoffset()` is the *pre* offset; formatting it back shows 03:30 local — the round trip silently moved it.
- `pytz.localize(..., is_dst=None)` raises `NonExistentTimeError`; code that passed `is_dst=True` before may now take the wrong branch.
- A daily job "at 06:00 local" that lands inside the gap fires at 07:00 or is missed entirely, and the postmortem blames the queue, not the calendar.
- Hard-coding the gap hour (`02:00-03:00`) breaks for zones that shift at midnight (e.g. some Brazilian/Iranian rules) and for the EU whose transition is at 01:00 UTC.

## Verification

```
TZ=America/New_York python3 -c "import datetime,zoneinfo; d=datetime.datetime(2026,3,8,2,30,tzinfo=zoneinfo.ZoneInfo('America/New_York')); print(d, d.utcoffset())"
```
The printed local time must be the resolved hour (03:30) or the object must have been rejected — never a 02:30 that claims to exist. Report: "spring-forward gap resolved by shift-forward to 03:30 local, stored as 07:30Z; 2026-03-08 case covered by a test."
