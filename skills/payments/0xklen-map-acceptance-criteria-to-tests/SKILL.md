---
name: map-acceptance-criteria-to-tests
description: Use when a build is "done" but no one can say which tests prove it. Builds a traceability matrix linking every acceptance criterion to a test, and every test to a criterion.
---

# Map acceptance criteria to tests

"Done" is a claim; the matrix is the proof. This skill links each acceptance criterion to the test that exercises it, and surfaces both untested criteria and orphan tests.

## Procedure

1. List every criterion `AC-01..AC-nn` from `AC.md` as a row in `trace.md`.
2. For each row name the test that verifies it, with its full path and test name: `tests/test_checkout.py::test_retry_does_not_double_charge`.
3. Fill the `layer` column (`unit`, `integration`, `e2e`, `manual`) and confirm high-risk criteria have a test below `e2e`; an `e2e`-only safety net is slow and flaky.
4. Find untested criteria: rows with no test path. Each is an unproven requirement, not a pass.
5. Find orphan tests: tests that map to no criterion. Decide whether they guard an implicit requirement (add the criterion) or are dead weight (delete them).
6. For manual rows write the exact steps and the expected observation so anyone can repeat them.
7. Re-run the mapped tests and paste the summary counts beside each row.
8. Freeze the matrix with the release; a criterion with no test at ship time should block or be explicitly waived with a name.
9. Include the migration or backfill path as a row if it changes user data, and map it to its own test.
10. Check that the mapped tests fail when the feature is disabled, or they are not guarding it.

11. Store the matrix where it is regenerated on each release, not hand-maintained in a wiki.

## Pitfalls

- Mapping many criteria to one broad `e2e` test, so one failure hides which requirement broke.
- Counting test line coverage instead of criterion coverage; 90% line coverage can still leave a criterion unproven.
- Letting the matrix drift from the tests as they are renamed; regenerate it in CI.
- Marking a criterion `manual` to avoid writing the test it actually needs.
- Asserting the happy path only and skipping the negative criterion you wrote.
- Trusting a green suite without checking that each mapped test actually exercises its criterion.
- Mapping a criterion to a test that asserts something adjacent, like rendering without behaviour.

- Leaving a criterion mapped to a skipped or quarantined test and counting it as covered.

## Verification

    grep -c 'AC-' trace.md; grep -cE 'tests/.*::' trace.md

Passes when every `AC-` row has a test path or a manual step and the counts match. Report untested criteria and orphan tests.
