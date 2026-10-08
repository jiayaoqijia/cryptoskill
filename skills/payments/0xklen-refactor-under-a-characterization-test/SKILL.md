---
name: refactor-under-a-characterization-test
description: Use when changing code you cannot fully test yet — capture current behavior with a characterization test before refactoring so behavior preservation is provable, not assumed.
---

# Refactoring under a characterization test

Freeze the observable behavior of the code you are about to change, then refactor to a green suite. A refactor that leaves the characterization test unchanged and passing is evidence of preservation; one that edits the snapshot is not.

## Procedure

1. Pick the smallest unit that exposes the seam you want to move — a module (`src/billing/legacy.py`), a function, or one public method. Target 100-400 lines; larger units make the assertion too coarse to catch a dropped branch.
2. Capture real inputs, not invented ones. Pull 20-50 representative records from the current data source:
```
sqlite3 prod_copy.db "SELECT id, amount_cents, currency FROM invoices ORDER BY id LIMIT 50" > fixtures/invoices.tsv
```
3. Write a characterization test that records *current* output verbatim, including parts that look wrong. Use snapshot/approval files so nothing is normalized silently:
```
pytest --snapshot-update tests/test_legacy_billing.py::test_totals
git add tests/__snapshots__/test_totals.ambr
```
4. Assert on the golden file, not hand-written expected values, and confirm the test passes before any refactor:
```python
def test_recompute_run_totals(snapshot):
    out = legacy.recompute_run_totals(load_fixture("invoices.tsv"))
    snapshot.assert_match(json.dumps(out, sort_keys=True), "run_totals.json")
```
5. Commit the characterization test alone. `git log --oneline -1 -- tests/` must show a commit touching no production file — that is the baseline the refactor may not move.
6. Refactor in small steps running only this test: `pytest tests/test_legacy_billing.py -q`. A snapshot diff means either behavior changed (fix the code) or the fixture was luck (fix the fixture and redo step 5).
7. After green, delete the old path and confirm coverage of the deleted file dropped to 0: `coverage report --include='src/billing/legacy.py'` shows `0` statements.

## Pitfalls

- Updating the snapshot to make the test pass defeats the exercise. Diff the `.ambr` file and justify every changed byte.
- Snapshot files serialize unstable fields (timestamps, dict order, floats). Normalize with `json.dumps(..., sort_keys=True)` and fixed precision, or you are testing the serializer, not the logic.
- Capturing one example gives a characterization test that also passes on an empty result. Include at least one non-empty, one empty, and one error-path fixture.
- Refactoring test and code in the same commit hides which change caused a diff.

## Verification

```
pytest tests/test_legacy_billing.py -q && git diff --stat HEAD -- tests/__snapshots__ | tail -1
```
Passes = all tests green and the snapshot directory is unchanged from the baseline commit. Report: "characterization suite green, 0 snapshot changes, legacy.py now 0 covered statements."
