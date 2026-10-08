---
name: write-a-failing-test-before-the-fix
description: Use when a bug's cause is identified and the fix is about to be written. Encodes the reproduction as a test that fails now and must pass after, so the bug cannot silently return.
---

# Write a Failing Test Before the Fix

The reproduction is a script; the regression guard is a test. Convert the bug into a committed, fast test that fails on the current code, then let the fix turn it green.

## Procedure

1. Pick the lowest test level that still exercises the bug: unit if the cause is isolated, integration if it crosses a boundary, end-to-end only if nothing smaller reproduces it.
2. Name the test after the behaviour, not the ticket: `test_cart_totals_when_sid_cookie_absent`, so the failure message explains itself years later.
3. Write the assertion first from the expected behaviour; run it and confirm it **fails for the right reason**. Read the failure text — a `KeyError` when you expected a wrong total means the test is wrong.
4. Keep the test hermetic: no network, no shared mutable fixture, no sleep. Inject the clock, the client, or the seed.
5. Record the pre-fix failure output in the commit message: `fails: AssertionError: 0 != 3.50`.
6. Implement the fix with the test as the target; run only that test in a loop: `pytest path::test_name -x`.
7. Run the whole suite to catch regressions the fix introduced elsewhere.
8. Commit test and fix together, with the reproduction command in the message; a test committed only after the fix has never been seen red.
9. If the test cannot be made to fail first, you do not understand the bug yet — return to `reproduce-a-bug-before-fixing`.

## Pitfalls

- Writing the test after the fix, so it passes trivially and proves nothing.
- Asserting on the whole output blob, so any unrelated change breaks it and the intent is lost.
- A test that fails for an environment reason (missing fixture) rather than the bug; the colour is green by accident.
- Mocking so much that the test only exercises the mock and never the buggy path.
- Copy-pasting the repro's timing or randomness straight into the test, producing a flaky regression guard.
- Marking it `skip` or `xfail` "for now" and shipping the fix without a live guard.

## Verification

    git stash -- src/            # remove the fix, keep the test
    pytest tests/test_cart.py::test_cart_totals_when_sid_cookie_absent -x; echo "pre-fix exit=$?"
    # passes when it FAILS here (exit non-zero) for the documented reason
    git stash pop && pytest tests/test_cart.py::test_cart_totals_when_sid_cookie_absent
    # and PASSES (exit 0) with the fix applied

Report to the user: the test name, its pre-fix failure message, and confirmation it passes with the fix.
