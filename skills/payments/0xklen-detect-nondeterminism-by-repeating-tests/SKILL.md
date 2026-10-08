---
name: detect-nondeterminism-by-repeating-tests
description: Use when a suite is green once but you suspect hidden nondeterminism — repeat runs under varied seed, order, parallelism and timezone, and require zero variance before trusting it.
---

# Detect nondeterminism by repeating tests

One green run says nothing about a test that depends on time, order or randomness. Run the suite many times with varied inputs and treat any variance as a bug in the test or the code.

## Procedure

1. Repeat under identical conditions first — pure flakiness shows here:
```
pytest -q --count=10 -n auto          # pytest-repeat
```
2. Vary the seed to expose random-dependent failures:
```
for s in $(seq 1 20); do pytest -q --randomly-seed=$s >/dev/null 2>&1 || echo "seed $s failed"; done
```
pytest-randomly shuffles order and reseeds `random` per test.
3. Vary parallelism — races and shared state often appear only with workers:
```
pytest -q -n 1 && pytest -q -n 8 && pytest -q -p no:xdist
```
4. Vary the clock — run under a shifted timezone to catch date-boundary assumptions:
```
TZ=Pacific/Kiritimati pytest -q tests/
```
5. Fix per cause: seed racy timing with waits, reset session fixtures between tests, freeze `now()`, make assertions order-insensitive by sorting sets before comparison.
6. Re-run the failing configuration until **20 consecutive clean runs**, not one.
7. Add the deterministic variant to CI as the default (fixed seed) and keep one shuffled job in a nightly matrix so new flakiness surfaces without blocking PRs.

## Pitfalls

- `-p no:randomly` disables the shuffler and can hide the order dependence you meant to catch. Keep a shuffled job.
- A fixed `TZ=UTC` run never catches timezone/date-arithmetic bugs. Vary it deliberately.
- Running with `-p no:xdist` changes global-state behavior; test both in-process and multi-worker.
- A test that only fails under load is still a bug. Do not dismiss it as "CI being slow."

## Verification

```
for i in $(seq 20); do pytest -q --randomly-seed=$i -n auto >/dev/null 2>&1 || echo "FAIL seed $i"; done; echo done
```
Passes = the loop prints only `done`, no `FAIL`. Report: "20 shuffled parallel runs clean; fixed an order-dependent session fixture; nightly shuffled job added."
