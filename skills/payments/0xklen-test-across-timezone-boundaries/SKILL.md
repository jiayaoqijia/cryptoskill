---
name: test-across-timezone-boundaries
description: Use when a test suite runs in one timezone — run it in several, including a DST-transition day, so a local-time assumption fails in CI not production.
---

# Test across timezone boundaries

CI usually runs in UTC, which hides every local-time bug. A green suite in `TZ=UTC` and a red one in `TZ=America/New_York` is the signature of an unmodelled local-time dependency.

## Procedure

1. Find code that reads the ambient zone rather than an injected one:
```
rg -n 'TZ|localtime|mktime|strftime|gettimezone|Calendar\.getInstance' src/ | head -40
```
2. Run the suite under a matrix of zones. A one-liner sweep catches the common cases:
```
for z in UTC America/New_York Europe/London Asia/Tokyo Australia/Sydney Asia/Kolkata; do
  echo "== $z"; TZ=$z pytest -q || break
done
```
3. Pin a transition day inside the test, not just the zone — the DST bug only fires on the changeover:
```python
import os, datetime
from zoneinfo import ZoneInfo
def test_rollover_on_dst_day(monkeypatch):
    monkeypatch.setenv("TZ", "America/New_York")
    day = datetime.datetime(2026, 3, 8, 3, 0, tzinfo=ZoneInfo("America/New_York"))
    assert billing_period_end(day).isoformat().endswith("Z")
```
4. Include a half-hour offset (India `+05:30`) and a quarter-hour one (Nepal `+05:45`) to catch offset truncation.
5. Test the season boundary both ways: run the DST cases for `2026-03-08` and `2026-11-01` (US) and `2026-03-29`/`2026-10-25` (EU).
6. Add the matrix to CI as a job, not a manual step:
```yaml
strategy:
  matrix:
    tz: [UTC, America/New_York, Asia/Kolkata]
env:
  TZ: ${{ matrix.tz }}
```
7. If a case genuinely must fail under some zone, mark it and link the ticket — do not let the sweep `break` silently.

## Pitfalls

- `export TZ` in the parent shell does not override a `TZ` baked into the container or the test's own fixtures; assert the effective zone in a first test.
- Node reads `process.env.TZ` at first `Date` use; setting it mid-test may not take effect unless you restart the worker.
- Testing only the summer date misses the winter offset and vice versa; both offsets must be exercised.
- Databases may evaluate `now()` in the server zone regardless of the client `TZ`; test the query, not just the application.
- A passing sweep in-process can hide a subprocess that inherits a different zone; cover subprocess paths too.

## Verification

```
for z in UTC America/New_York Asia/Kolkata; do TZ=$z pytest -q tests/test_billing.py -k timezone || echo "FAIL $z"; done
```
Every zone passes, and a deliberately naive `datetime.now()` case fails in `America/New_York` = the matrix has teeth. Report: "suite green in 6 zones; DST-day cases 2026-03-08 / 2026-11-01 covered; CI matrix job added."
