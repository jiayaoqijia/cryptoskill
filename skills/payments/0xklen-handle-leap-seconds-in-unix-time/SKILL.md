---
name: handle-leap-seconds-in-unix-time
description: Use when mixing POSIX time with UTC or converting epoch seconds on a UTC-day boundary — POSIX time ignores leap seconds, so day arithmetic and UTC conversions can differ.
---

# Handle leap seconds in Unix time

POSIX time treats every day as exactly 86400 seconds, so it diverges from UTC by the 27 leap seconds inserted since 1972. Most application code can ignore this; code that converts epoch seconds to a UTC calendar date, or counts a day as 86400s on a UTC boundary, cannot.

## Procedure

1. Know the current offset: TAI minus UTC is 37 seconds as of the last leap second (27 inserted). Confirm from the system:
```
grep -i leap /usr/share/zoneinfo/leap-seconds.list 2>/dev/null | tail -3
zdump -v -c 2016,2018 UTC | tail -4
```
2. Decide the domain explicitly: **wall-clock calendar** (use UTC/zoneinfo, leap seconds included as `:60`) or **elapsed SI seconds** (use POSIX epoch or TAI). Do not mix.
3. For civil timestamps — billing dates, log stamps, `created_at` — use POSIX/UTC time and accept the 27s discontinuity; it is invisible at human scale.
4. For elapsed measurements and physics, use a monotonic or TAI source, where each second is a real second:
```python
import time
t0 = time.monotonic_ns()   # SI seconds, no leap handling needed
```
5. Never compute a UTC calendar date by `epoch // 86400`; go through a real converter that knows the rule:
```python
from datetime import datetime, timezone
datetime.fromtimestamp(1700000000, tz=timezone.utc).date()
```
6. Parse `23:59:60` if a producer emits it instead of clamping; most parsers reject it, so log and normalise to `23:59:59.999...`:
```
python3 -c "print(__import__('datetime').datetime.fromisoformat('2026-12-31T23:59:60Z'))"  # expect ValueError
```
7. For high-precision cross-system comparisons, use TAI or GPS time and convert at the edges, keeping the leap table version with the data.

## Pitfalls

- Some libraries accept `23:59:60` by clamping to `23:59:59` and some reject it; a stream with a leap second splits handling by parser.
- `datetime.fromtimestamp(ts, tz=utc)` and `utcfromtimestamp(ts)` differ — the latter is naive and deprecated; use the aware form.
- Day-boundary reports built on `ts // 86400` drift by whole seconds for every leap second after the epoch, though only at the second granularity.
- GPS time has no leap seconds, so GPS and UTC differ by a growing integer; converting between them needs the leap table.
- Assuming a "Unix day" is exactly 86400s is correct POSIX but wrong if compared against a UTC-derived count; state which one you mean.

## Verification

```
python3 -c "import datetime as d; print(d.datetime.fromtimestamp(1700000000, tz=d.timezone.utc))"
```
A converter-backed date equals the UTC calendar date; a `// 86400` shortcut on the same number differs only where a leap second has accumulated. Report: "civil timestamps use POSIX/UTC; elapsed uses monotonic SI seconds; `23:59:60` inputs are normalised and counted."
