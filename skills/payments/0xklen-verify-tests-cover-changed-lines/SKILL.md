---
name: verify-tests-cover-changed-lines
description: Use when a PR adds code that the existing suite may not exercise. Measures patch coverage — the share of newly changed lines hit by tests — before approving.
---

# Verify tests cover the changed lines

Project-wide coverage says nothing about a specific diff. A repo at 90% coverage can merge a new branch that no test ever enters. Review the patch, not the total.

## Procedure

1. Run the suite with coverage on the full tree, then isolate the diff:
       coverage run -m pytest -q && coverage xml -o coverage.xml
       pip install diff-cover
       diff-cover coverage.xml --compare-branch=origin/main --fail-under=80
2. Read the diff-cover report: it lists each changed line left uncovered and the file it is in. Lines that are configuration or generated may be excluded with `--exclude`.
3. Require new branches in control flow to be covered. A new `if err != nil` with no failing-input test is an unverified path.
4. For JavaScript/TypeScript repos, use jest `--coverage` with `--changedSince=origin/main`, or check the CI patch-coverage gate the platform already computes.
5. Distinguish coverage from assertion: a line executed by a test that never inspects its result is covered but unverified. Look at the test body for the new behaviour.
6. When a line is legitimately untestable (a `main()`, a platform call), mark it with the coverage tool's pragma (`# pragma: no cover`) rather than lowering the threshold.
7. Block merge when a non-trivial new branch is uncovered; suggest a specific input the author should add.

## Pitfalls

- A green CI badge produced by the whole-repo number while the new file has zero hits.
- Tests that call the new function but assert nothing, inflating coverage without verification.
- Lowering `--fail-under` to pass CI, which erases the signal for every future PR.
- Chasing 100% and writing brittle tests for trivial getters, which adds maintenance cost for no safety.

## Verification

    diff-cover coverage.xml --compare-branch=origin/main --fail-under=80

A pass means every changed non-excluded line is executed by the suite and the patch coverage is at or above 80%. Report the uncovered changed lines by file, or state that none remain.

## Worked example

A PR adds `def refund(order, amount)` with a guard `if amount > order.total: raise`. diff-cover reports the `raise` line uncovered. The author adds:
    with pytest.raises(ValueError):
        refund(order, order.total + 1)
Re-running `diff-cover coverage.xml --compare-branch=origin/main` now shows 100% patch coverage and the previously red line is gone.
