---
name: measure-elapsed-time-with-a-monotonic-clock
description: Use when timing durations, timeouts or latency — read a monotonic clock that never steps backwards, not wall time, so DST and NTP cannot corrupt the measurement.
---

# Measure elapsed time with a monotonic clock

The wall clock is a moving target: NTP can step it backwards, DST relabels it, and a VM suspend jumps it. Any duration — a timeout, a latency histogram, a stopwatch — must come from a monotonic source that only ever advances.

## Procedure

1. Pick the monotonic API for the language, not `now()`:
```
Python   time.monotonic_ns() / perf_counter()
Golang   time.Since(start)  (uses monotonic component)
Java     System.nanoTime()
Node     process.hrtime.bigint()
C        clock_gettime(CLOCK_MONOTONIC_RAW, &ts)
```
2. Time the interval with monotonic, report the instant with wall time:
```python
import time
from datetime import datetime, timezone
start_mono = time.monotonic()
start_wall = datetime.now(timezone.utc)
do_work()
elapsed  = time.monotonic() - start_mono
finished = datetime.now(timezone.utc)
print(f"elapsed={elapsed:.3f}s started={start_wall.isoformat()} finished={finished.isoformat()}")
```
3. Use the monotonic delta for timeouts and SLO math; use the wall instants for logs and correlation.
4. On Linux, confirm which clock you are reading — `CLOCK_REALTIME` is wall, `CLOCK_MONOTONIC` excludes suspend time, `CLOCK_BOOTTIME` includes it:
```
cat /proc/uptime            # monotonic-ish seconds since boot
```
5. In Go, keep the monotonic reading rather than stripping it: `t.Round(0)` or a JSON/serialise round trip drops it, after which `Sub` silently uses wall time.
6. In a histogram, bucket by the monotonic delta; using wall time makes a step appear as a negative or huge bucket.
7. Test the property: monkeypatch the wall clock backwards and assert the measured duration stays positive.

## Pitfalls

- `time.time()` differences go negative when NTP steps the clock back; a timeout computed as `now - start > limit` then never fires.
- `CLOCK_MONOTONIC` excludes suspend, so a laptop or VM that slept shows a shorter interval than reality; use `CLOCK_BOOTTIME` when suspend must count.
- Serialising a Go `time.Time` through JSON strips the monotonic component; the same value measures differently after a round trip.
- `process.hrtime()` in Node is monotonic but not epoch-based; adding it to `Date.now()` mixes two clocks.
- A monotonic clock has an arbitrary epoch — never log it as a timestamp, only as a delta.

## Verification

```
python3 -c "import time; a=time.monotonic(); b=time.monotonic(); print('mono delta ok', b>=a)"
```
Monotonic readings never decrease, and a negative-step test on the wall clock leaves the monotonic measurement positive. Report: "durations measured with `monotonic_ns`; wall clock used only for log instants; timeout test steps wall clock back and still fires."
