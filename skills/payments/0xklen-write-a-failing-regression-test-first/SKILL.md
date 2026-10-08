---
name: write-a-failing-regression-test-first
description: Use when fixing a reported bug — reproduce it as a test that fails on the unfixed code first, then fix until that exact test passes, so the fix is proven and stays fixed.
---

# Write a failing regression test first

A fix without a reproducing test is a guess that can silently return. Reproduce the bug as a test that goes red on the current commit, fix until that test alone turns green, and keep the test forever.

## Procedure

1. Reduce the report to the smallest trigger: exact input, exact call, observed vs expected output. If you cannot, ask for a repro before writing any code.
2. Write the test and run it against the **unfixed** tree. It must fail for the reported reason:
```
pytest -q tests/test_discounts.py::test_percent_off_99_cents; echo "exit=$?"   # expect exit=1
```
3. Read the failure. An import or setup error is a broken test, not a repro — fix the test until it fails on the assertion.
4. Commit the failing test alone: `git commit -am "test: reproduce #482 zero-cent discount"`. The history now shows red-before-green.
5. Implement the minimal fix. Resist touching anything else — unrelated changes make the commit unreviewable and the cause ambiguous.
6. Run the single test, then the whole suite:
```
pytest -q tests/test_discounts.py::test_percent_off_99_cents && pytest -q
```
7. If it still fails you fixed a different bug. Re-read actual vs expected and iterate on the code, not the test's expectation.
8. Reference the issue in the test docstring so the why survives: `"""Regression for #482: 99-cent item rounded discount to 100."""`.

## Pitfalls

- Writing the test after the fix means you never saw it fail. A test that never failed cannot prove it catches the bug.
- Loosening the assertion to match buggy output bakes the bug in. The expected value comes from the spec, not the current behavior.
- One giant test asserting everything hides the true cause on a later regression. One bug, one focused test.
- Skipping the full-suite run after the fix lets it break a neighboring case.

## Verification

```
git stash -- src/ && pytest -q tests/test_discounts.py::test_percent_off_99_cents; echo "red=$?"; git stash pop && pytest -q tests/test_discounts.py::test_percent_off_99_cents && echo GREEN
```
Passes = `red=1` without the fix and `GREEN` with it. Report: "repro red on unfixed tree (exit 1), fixed in one commit, suite green, test references #482."
