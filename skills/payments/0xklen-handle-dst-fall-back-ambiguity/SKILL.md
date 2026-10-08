---
name: handle-dst-fall-back-ambiguity
description: Use when a local time can occur twice — on fall-back the same wall clock happens twice, so an unpinned time is ambiguous and must specify which occurrence.
---

# Handle the DST fall-back ambiguity

When the clock falls back, 01:30 local happens twice: once at the earlier offset (EDT, -04:00) and again at the later one (EST, -05:00). A naive `01:30` maps to two distinct instants; picking the wrong one moves the job an hour.

## Procedure

1. Prove the ambiguity for the zone:
```
zdump -v America/New_York | grep 2026
```
Two lines for `Nov  1` with `isdst=1` then `isdst=0` at the same local hour = duplicated time.
2. Make the occurrence explicit with `fold`:
```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
tz = ZoneInfo("America/New_York")
first  = datetime(2026, 11, 1, 1, 30, fold=0, tzinfo=tz)  # EDT  -04:00 -> 05:30Z
second = datetime(2026, 11, 1, 1, 30, fold=1, tzinfo=tz)  # EST  -05:00 -> 06:30Z
assert first.timestamp() != second.timestamp()
```
3. Choose a policy and write it down: **first occurrence** (earlier UTC instant) is the usual default for "run at 01:30"; for deadlines, use the **last** occurrence so nothing can slip through with an extra hour.
4. Store the resolved absolute instant (`2026-11-01T05:30:00Z`) — not the ambiguous local string — so retries and replicas agree.
5. For "at most once" semantics, dedupe on the absolute instant, not the local time; a local-keyed dedupe fires twice.
6. Test both folds explicitly; a single assertion on the timestamp value catches a library default change.

## Pitfalls

- `pytz.localize(naive, is_dst=False)` silently picks the standard-time occurrence; code that reads `is_dst` as a boolean flag ("is it DST now?") gets the opposite of what it means.
- `.timestamp()` on a Python datetime without `fold` set defaults to `fold=0`; two code paths can disagree without any error.
- An hourly job keyed on local hour text runs twice in the repeated hour; counters and quotas overcount.
- Session cookies or cache entries expiring "at 01:30 local" may live an extra hour or none, depending on which occurrence the writer picked.
- Sorting a batch of naive local strings across the transition orders the two 01:30s arbitrarily.
- A calendar invite created before the rule was pinned may render 01:30 once and shift on the next client refresh; export the resolved instant to make it stable.

## Verification

```
TZ=America/New_York python3 -c "from datetime import datetime; from zoneinfo import ZoneInfo; tz=ZoneInfo('America/New_York'); a=datetime(2026,11,1,1,30,fold=0,tzinfo=tz); b=datetime(2026,11,1,1,30,fold=1,tzinfo=tz); print(a.timestamp(), b.timestamp())"
```
Two different Unix timestamps 3600s apart = the ambiguity is modelled, not collapsed. Report: "fall-back 2026-11-01 01:30 resolves to 05:30Z (fold=0) by policy; dedupe keys on the absolute instant."
