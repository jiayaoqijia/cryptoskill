---
name: triage-a-flaky-test-to-root-cause
description: Use when a test passes and fails on unchanged code — reproduce the flake at a measured rate, classify the cause, and fix or quarantine it with an owner instead of re-running until green.
---

# Triage a flaky test to root cause

"Re-run and hope" turns a real bug into noise. A flaky test is a signal: reproduce it, name the cause from a fixed taxonomy, then fix it or quarantine it with a ticket — never leave it rerunning silently.

## Procedure

1. Get the flake rate, not a hunch. Run the test 50 times and count failures:
```
pytest tests/test_checkout.py::test_race -q --count=50 2>&1 | tail -3      # pytest-repeat
for i in $(seq 50); do pytest -q tests/test_checkout.py::test_race >/dev/null 2>&1 || echo fail; done | sort | uniq -c
```
2. Classify into one of: **timing** (sleep/async), **order** (leaked state), **isolation** (shared DB/file/port), **time** (`now()`), **random** (unseeded), **network** (real HTTP).
3. Rule out order first — most common and cheapest to prove:
```
pytest tests/ -q -p no:randomly            # fixed order: passes?
pytest tests/ -q --randomly-seed=$RANDOM    # shuffled: fails?
```
Passes fixed + fails shuffled means leaked global/module state.
4. For **timing**, replace the sleep with a condition wait and re-measure: `asyncio.sleep(0.1)` → `await event.wait()`, or `retry_until(lambda: client.ready)`.
5. For **time** freeze the clock (`@freeze_time("2026-01-01")` or an injected `Clock`); for **random** seed it (`random.seed(0)`, `pytest-randomly-noseed`); for **network** record and replay (VCR, `responses`).
6. Re-run 50× after the fix. Required: **0 failures in 50**. One-in-fifty is a 2% rate that breaks main weekly.
7. If you cannot fix it now, quarantine explicitly with `@pytest.mark.flaky(reruns=3)` **and** open a ticket carrying the flake rate and an owner. A quarantine without a ticket is deletion with extra steps.

## Pitfalls

- Reruns mask the same bug in production; `pytest-rerunfailures` must hide nothing that is not ticketed.
- A test that only fails on CI usually differs by CPU count or parallelism — reproduce with `-n auto` locally before blaming infrastructure.
- Deleting the test removes the signal and ships the underlying bug untested. Quarantine, do not delete.
- "It passed on retry" in a PR description is not triage — record the measured rate.

## Verification

```
for i in $(seq 50); do pytest -q tests/test_checkout.py::test_race >/dev/null 2>&1 || echo FAIL; done | sort | uniq -c
```
Passes = the counter line shows `50` and zero `FAIL`. Report: "flake was order dependence from a session-scoped fixture; added a cache reset; 50/50 green."
