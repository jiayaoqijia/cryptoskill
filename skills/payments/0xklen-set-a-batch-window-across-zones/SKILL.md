---
name: set-a-batch-window-across-zones
description: Use when an overnight batch, ETL window or maintenance window must run across regions — anchor it to one zone and size it against the shortest local night, not each region's 02:00.
---

# Set a batch window across zones

"Run the batch at night" fails when the estate spans regions: night in New York is business hours in Sydney. Anchoring the window correctly is the difference between a quiet maintenance window and an outage during peak traffic.

## Procedure

1. List the regions and their peak-hours in UTC, not local:
```
for z in America/New_York Europe/London Asia/Tokyo; do echo -n "$z "; TZ=$z date -d '09:00' +%z; done
```
2. Convert each region's quiet window to UTC and find the intersection:
```python
from datetime import timezone, datetime
from zoneinfo import ZoneInfo
def quiet_utc(zone, start_hour, end_hour):
    d = datetime(2026, 6, 1, tzinfo=ZoneInfo(zone))
    return (d.replace(hour=start_hour).astimezone(timezone.utc).hour,
            d.replace(hour=end_hour).astimezone(timezone.utc).hour)
print(quiet_utc("America/New_York", 1, 5))  # -> 5..9 UTC
print(quiet_utc("Asia/Tokyo", 1, 5))        # -> 16..20 UTC
```
3. If the intersections do not overlap (they often do not), pick the region with the largest traffic share and run the window to dodge *its* peak; fail secondary regions over to read replicas during the window.
4. Size the window from the shortest local night in the set — the one with the most daylight, i.e. the summer DST region — and subtract a drain buffer.
5. Anchor the cron/timer to a single zone (UTC) and change it only at planned season boundaries:
```
CRON_TZ=UTC
0 3 * * 0 /opt/batch/run.sh --window-minutes 45
```
6. Publish the window in every region's local time in the runbook, computed once with a script, not by hand:
```
for z in UTC America/New_York Europe/London Asia/Tokyo; do echo -n "$z "; TZ=$z date -d '2026-06-07 03:00 UTC' '+%Y-%m-%d %H:%M %Z'; done
```
7. Re-check the window after any tzdata change or the addition of a new region.

## Pitfalls

- Adding a region flips the overlap from "works" to "peak in APAC" — the window must be re-derived, not reused.
- DST makes "03:00 UTC" land at 03:00 or 04:00 local depending on the region's own shift, so a window tuned once drifts an hour twice a year.
- A batch that overruns its window silently competes with morning traffic; cap runtime with a hard kill, not just a nominal window.
- Assuming all of India is `+05:30` and forgetting `Asia/Kolkata` has no DST is safer than assuming the reverse — but Nepal is `+05:45`; use IANA names, never offsets.
- A "maintenance window" published in one zone's local time reads as a different window to every other region's on-call.

## Verification

```
for z in UTC America/New_York Asia/Tokyo; do echo -n "$z "; TZ=$z date -d '2026-06-07 03:00 UTC' '+%H:%M %Z'; done
```
Each line shows the window's real local time; the New York and Tokyo lines must fall outside their 09:00-18:00 traffic peaks. Report: "batch window anchored at 03:00 UTC; local times 23:00 EDT / 12:00 JST — Tokyo covered by replica failover."
