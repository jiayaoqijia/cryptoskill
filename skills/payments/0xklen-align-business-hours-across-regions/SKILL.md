---
name: align-business-hours-across-regions
description: Use when scheduling a call, SLA or support rota across regions — compute the local working-hours overlap in UTC and size staffing to the real intersection, not each region's 09:00.
---

# Align business hours across regions

"Business hours" is a per-region local concept. A meeting for three continents, or an SLA that promises a response "within business hours", fails unless you convert every region's window to UTC and reason about the intersection — holidays included.

## Procedure

1. Build the offset/transition table for each region instead of assuming a fixed hour:
```
for z in America/Los_Angeles America/New_York Europe/London Asia/Kolkata Asia/Tokyo Australia/Sydney; do
  echo -n "$z  "; TZ=$z date -d '09:00' '+%H:%M %Z (%z)'; done
```
2. Compute each region's working window in UTC for a specific date (offsets differ by season):
```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
def window_utc(zone, start=9, end=17, day=(2026, 6, 1)):
    z = ZoneInfo(zone)
    s = datetime(*day, start, tzinfo=z).astimezone(timezone.utc)
    e = datetime(*day, end,   tzinfo=z).astimezone(timezone.utc)
    return s.hour, e.hour
for r in ["America/Los_Angeles","Europe/London","Asia/Tokyo"]:
    print(r, window_utc(r))
```
3. Take the intersection of the windows as the real overlap; if empty, the meeting is out of hours for someone — say who and how much.
4. Convert the *chosen* UTC slot back to each region's local time for the invite, with the zone label so nobody re-derives it.
5. For SLA "business hours", define it per region: count working hours in that region's zone, excluding weekends and a per-region holiday calendar. Do not count wall-clock hours and call them business hours.
6. Handle holidays: load each region's public holidays for the year and subtract them from the SLA clock; a US holiday does not pause an EU-based SLA unless the contract says so.
7. Document the overlap and re-check it after each DST transition, since the intersection shifts by an hour when only one side changes.

## Pitfalls

- Comparing only offsets misses DST: London and New York are 5h apart in winter and 4h in summer, so a fixed "5 hours" gap is wrong half the year.
- A "follow-the-sun" rota needs a handover during overlap; a gap between regions' end and start leaves hours unstaffed.
- India (`+05:30`) and Nepal (`+05:45`) shift the window by half or quarter hours; floor to the hour and you lose real coverage.
- Counting business hours as 8 wall-clock hours per weekday overstates coverage by the length of any outage inside the window.
- Meeting invites sent as a UTC time without local rendering confuse attendees in summer-time regions; always show the local equivalent.

## Verification

```
for z in America/Los_Angeles Europe/London Asia/Tokyo; do echo -n "$z "; TZ=$z date -d '2026-06-01 14:00 UTC' '+%H:%M %Z'; done
```
The printed local times show who is in hours and who is not; the chosen slot sits inside the computed overlap. Report: "three-region overlap at 14:00-16:00 UTC; SLA business hours counted per region with holiday calendars."
