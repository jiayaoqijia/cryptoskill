---
name: convert-recurring-events-across-zones
description: Use when a recurring meeting, job or calendar event recurs on a local clock — keep the local wall time fixed and the zone as a TZID, not a fixed UTC offset.
---

# Convert recurring events across zones

"Every Monday 09:00" means 09:00 *local*, which is a different instant after every DST change. Storing the first occurrence as UTC and adding seven days drifts the meeting by an hour twice a year. Keep the rule in local time with its zone and materialise each occurrence.

## Procedure

1. Represent the recurrence with the zone attached, RRULE-style, never a bare UTC timestamp:
```
DTSTART;TZID=America/New_York:20260302T090000
RRULE:FREQ=WEEKLY;BYDAY=MO
```
2. Expand occurrences in the event's own zone, not in UTC:
```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
tz = ZoneInfo("America/New_York")
first = datetime(2026, 3, 2, 9, 0, tzinfo=tz)
for w in range(4):
    occ = first + timedelta(weeks=w)          # naive-add stays 09:00 local
    print(w, occ.isoformat(), occ.astimezone(ZoneInfo("UTC")))
```
3. Watch that adding a week keeps the *wall time* 09:00 with the offset changing in March — that is the correct behaviour for "09:00 local". Adding 7 UTC days instead would print 08:00 local.
4. If the recurrence should hold a *fixed instant* (a broadcast at market open in UTC), store the zone as UTC and say so; the two policies must not be mixed silently.
5. Materialise a bounded horizon to a table and let the scheduler pick up an instant per occurrence, so retries never re-expand the rule differently:
```sql
INSERT INTO occurrences(event_id, starts_at) VALUES ($1, $2) ON CONFLICT DO NOTHING;
```
6. When a viewer in another zone asks "what time is that for me?": convert each materialised instant, do not re-apply the rule in their zone.
7. Handle the DST edge: a 02:30 local weekly recurrence hits the spring-forward gap once a year (see `handle-dst-spring-forward-gap`) — decide skip vs shift.

## Pitfalls

- `first_utc + 7*86400` looks right in summer and is an hour off after the transition; the interval is not a fixed number of seconds across DST.
- Expansion in the viewer's zone moves the organiser's 09:00 to a different wall time — always expand in the *event's* zone.
- Caches keyed on the UTC instant miss when the recurrence materialises to a new instant after a rule change; key on the local occurrence too.
- Missing `TZID` makes a parser assume UTC and the meeting shows at 04:00 local for a New York organiser.
- Count-based rules (`COUNT=10`) plus cancellations need an exception model (EXDATE); renumbering after a cancelled occurrence changes which dates exist.

## Verification

```
python3 -c "from datetime import datetime,timedelta; from zoneinfo import ZoneInfo; tz=ZoneInfo('America/New_York'); f=datetime(2026,3,2,9,tzinfo=tz); [print((f+timedelta(weeks=w)).strftime('%Y-%m-%d %H:%M %Z'), (f+timedelta(weeks=w)).astimezone(ZoneInfo('UTC')).strftime('%H:%MZ')) for w in range(4)]"
```
The local column stays 09:00 while the UTC column shifts from 14:00Z to 13:00Z after the March transition = the wall time is held. Report: "weekly recurrence stored as TZID + RRULE, expanded in America/New_York; local 09:00 held across the DST change."
