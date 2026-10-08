---
name: isolate-test-order-dependence
description: Use when tests pass alone but fail together — bisect the ordering to name the leaking test and prove isolation with shuffled and reversed runs.
---

# Isolate test order dependence

A test that passes alone but fails in the suite is leaking or consuming shared state. Bisect the order to name the offender, then fix the fixture or global it touches.

## Procedure

1. Confirm order dependence — run the target alone, then within the whole suite:
```
pytest -q tests/test_a.py::test_x          # alone: green?
pytest -q tests/                            # suite: red?
```
2. Shuffle to make it reproducible and frequent:
```
pytest -q --randomly-seed=0   ;   pytest -q --randomly-seed=1
```
Find a seed where it fails and keep it as the reproducer.
3. Get the ordered list of test ids and binary-search the leaking prefix:
```
pytest --collect-only -q
pytest -q tests/  -k "test_1 or test_2 or ... or test_k"
```
Shrink `k` until the failing test passes; the last test added to the failing prefix is the leaker.
4. Confirm with a reversed run: `pytest -q -p no:cacheprovider tests/test_z.py tests/test_a.py`.
5. Name the shared state: module-level `cache = {}`, a session-scoped fixture, an unrolled DB transaction, a monkeypatched module attribute, or a fixed-name temp file. Grep the suspect for `global`, `@pytest.fixture(scope=`, and `monkeypatch.setattr`.
6. Fix toward isolation: function-scoped fixtures, `tmp_path` for files, `monkeypatch` (auto-undo) instead of manual setattr, and a DB rollback per test:
```python
@pytest.fixture
def db(session):
    t = session.begin()
    yield session
    t.rollback()
```
7. Prove it: 20 shuffled runs and the reversed run both green.

## Pitfalls

- `pytest -x` stops early and hides which test leaked. Run the full suite to see the failure in context.
- A passing single-test run proves nothing about leakage. Always compare against the suite.
- `scope="session"` fixtures are the usual culprit. Prefer the narrowest scope that still works.
- Adding teardown only to the victim leaves the leaker poisoning other tests later. Fix the leaker.

## Verification

```
for i in $(seq 20); do pytest -q --randomly-seed=$i >/dev/null 2>&1 || echo "FAIL $i"; done; pytest -q --reverse && echo ISOLATED
```
Passes = no `FAIL` lines and `ISOLATED` prints. Report: "leaker was a module-global cache in test_pricing; moved to a function fixture; 20 shuffled + reversed runs green."
