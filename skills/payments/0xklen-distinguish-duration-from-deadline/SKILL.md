---
name: distinguish-duration-from-deadline
description: Use when a spec says "within 30 minutes" or "by end of day" — separate a measured elapsed duration from a fixed wall-clock deadline so the two are never conflated.
---

# Distinguish duration from deadline

"Retry within 30 minutes" and "finish by 17:00" are different guarantees. A duration is an elapsed interval measured from an event; a deadline is a fixed instant that may already have passed. Mixing them produces jobs that run past their cut-off or measure time with a clock that jumps.

## Procedure

1. Classify each time bound in the task: elapsed (`timeout=30s`, `retry_window`) or absolute (`due_at`, `expires_at`, `SLA breach at`).
2. Measure elapsed time with a monotonic clock, never wall time:
```python
import time
start = time.monotonic()
...
if time.monotonic() - start > 30: raise TimeoutError
```
3. Carry a deadline as an absolute UTC instant through the call chain and recompute remaining budget at each hop:
```python
deadline = start_wall + timedelta(seconds=90)
remaining = (deadline - datetime.now(timezone.utc)).total_seconds()
if remaining <= 0: abort("budget exhausted")
```
4. Do not recompute a duration at each retry — that turns a 90s budget into 90s per attempt. Pass the original deadline down and let it shrink.
5. When an NTP step or DST change can occur mid-run, prefer monotonic for the interval and wall time only to *report* the deadline in the user's zone.
6. If the deadline is expressed in business hours ("by 17:00 next working day"), resolve it to an instant using the user's zone and a holiday calendar, then hand only the instant to the worker.
7. State the guarantee explicitly in logs: `attempt=3 elapsed=41.2s remaining=48.8s`.

## Pitfalls

- `time.time()` is wall time and can jump backwards on NTP correction or DST; a 30s timeout computed from it can be huge or negative.
- Sleeping `interval` between 5 retries under a 90s deadline overshoots: 5×20s + work > 90s. Budget the total, not the interval.
- `asyncio.wait_for` and HTTP `timeout=` measure elapsed, but a connection pool queue wait may not count — the user sees a much later finish than the timeout promises.
- A cron job "every 30 minutes" plus a run that takes 25 minutes drifts into overlap; elapsed work and fixed-schedule are separate concerns.
- Reporting a deadline as a duration ("in ~2 hours") is wrong across a DST shift; give the absolute local time.
- A per-attempt timeout larger than the remaining deadline guarantees an overrun; always clamp each attempt to what the deadline still allows.

## Verification

```
python3 -c "import time; s=time.monotonic(); [time.sleep(0.01) for _ in range(200)]; print('elapsed', round(time.monotonic()-s,3))"
```
Elapsed time computed from `monotonic()` unaffected by a wall-clock step = correct basis. Report: "retry budget is a 90s absolute deadline passed down; elapsed measured with `monotonic`; observed overshoot 0s."
