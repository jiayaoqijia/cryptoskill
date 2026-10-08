---
name: store-user-timezone-and-render-locally
description: Use when a product shows times to a user — store the IANA zone name the user chose and render every timestamp in it, never store a fixed offset.
---

# Store the user timezone and render locally

Users think in their own local time and expect the product to do the same. Store the IANA zone name once, render every timestamp through it, and the display stays correct across DST without per-row math.

## Procedure

1. Capture the zone name, not the offset, and not the browser's abbreviation (`EST` is ambiguous across the world):
```js
Intl.DateTimeFormat().resolvedOptions().timeZone   // "America/New_York"
```
2. Persist it as a column with a default of UTC and validate against the tz database:
```
python3 -c "import zoneinfo,sys; zoneinfo.ZoneInfo(sys.argv[1])" America/New_York
```
3. Let the user override it explicitly; do not re-detect on every login, or a travelling user's logs jump zones.
4. Store every instant in UTC and convert only at the render edge:
```python
from zoneinfo import ZoneInfo
def render(dt_utc, zone):
    return dt_utc.astimezone(ZoneInfo(zone)).strftime("%Y-%m-%d %H:%M %Z")
```
5. Render with the zone label so the user is never guessing: `2026-03-01 09:00 EST`, not `2026-03-01 09:00`.
6. For date-only displays (due dates, birthdays), keep the value as a *civil date*, not an instant — an instant rendered in a western zone can slip a day for users east of UTC.
7. Re-render on zone change and cache with the zone in the key, so a user in two zones does not see another's formatting:
```
cache_key = f"render:{user_id}:{zone}:{instant_epoch}"
```
8. Backfill: for existing rows with no zone, default to UTC and flag them for the user to confirm at next login.

## Pitfalls

- Storing `-05:00` freezes the user in winter time; six months later their 09:00 shows as 08:00 because the offset never shifted.
- `toLocaleString()` without an explicit zone uses the server's or runtime's zone in SSR, so the same page renders differently on the server and the client — a hydration mismatch.
- Emails generated server-side with no zone land at odd hours for the recipient; resolve the recipient's zone before formatting.
- A user who moves regions may want history in their old zone; storing only the current zone loses that. Consider a per-event zone for anything legally timestamped.
- Date-only fields converted through UTC can move a day; keep them as `DATE` and never run them through a zone.

## Verification

```
psql -c "SELECT count(*) FROM users WHERE timezone IS NULL OR timezone !~ '^[A-Za-z]+/[A-Za-z_]+$';"
```
Returns `0` = every user has a valid IANA zone name. Report: "users.timezone stores IANA names; render path converts UTC to the user's zone with a `%Z` label; server and client output match."
