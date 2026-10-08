---
name: freeze-the-clock-in-tests
description: Use when a test depends on the current time, timezone or a sleep — inject or freeze the clock so the test asserts a fixed instant and never races the wall clock.
---

# Freeze the clock in tests

Tests that read `now()` are time bombs: green today, red on a month boundary or in another timezone. Control time explicitly so the assertion is about logic, not the calendar.

## Procedure

1. Find every nondeterministic time call:
```
rg -n 'datetime\.now|time\.time|new Date\(\)|System\.currentTimeMillis|Instant\.now' src/ tests/
```
2. Prefer injecting a clock at the seam over patching globals:
```python
class Clock(Protocol):
    def now(self) -> datetime: ...

class FixedClock:
    def __init__(self, t): self._t = t
    def now(self): return self._t
```
3. Where injection is too invasive, freeze in tests: Python `@freeze_time("2026-03-01T00:00:00Z")` (freezegun); Node `sinon.useFakeTimers({now: 0, toFake: ['Date']})`; JVM `Clock.fixed(Instant.parse(...), ZoneOffset.UTC)`.
4. Pin the timezone too — a frozen UTC instant still fails under a local-time assumption:
```
TZ=UTC pytest -q tests/test_billing_cycle.py && TZ=Asia/Tokyo pytest -q tests/test_billing_cycle.py
```
5. Test the boundaries, not the middle: month-end (`2026-01-31`), leap day (`2028-02-29`), DST spring-forward (`2026-03-08T02:30` is invalid in US/Eastern), and the year boundary.
6. Replace `sleep` with fake timers or an event wait: freezegun's `tick()`, or `await condition()` with a timeout.
7. Verify determinism: run the same test at three frozen instants and in three timezones; each must pass for its own reason.

## Pitfalls

- `freeze_time` only patches libraries it knows; a C extension or subprocess reading the real clock escapes it. Inject at your own boundary.
- Freezing time can deadlock code that waits on a real `threading.Timer`. Advance the fake clock or use real time deliberately.
- Comparing naive and aware datetimes raises. Standardize on aware UTC and convert only at the edge.
- `monkeypatch.setattr(datetime, "now", ...)` fails on some Python versions because `now` is a C method. Use freezegun.

## Verification

```
TZ=UTC pytest -q tests/test_billing_cycle.py && TZ=Asia/Tokyo pytest -q tests/test_billing_cycle.py
```
Passes = green under both timezones with the frozen instants exercised. Report: "billing cycle test frozen at 2026-01-31, green in UTC and Asia/Tokyo; leap-day and DST cases added."
