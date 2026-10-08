---
name: test-an-automation-against-a-fixture-run
description: Use when an automation is changed and you need evidence it still does the right thing. Exercises the job against a fixed input and asserts on its output counts.
---

# Test an automation against a fixture run

An automation is code, and code changes break in silence until the next scheduled run. Give each job a fixture input with a known-correct output, and run the test in CI so a change cannot ship untested.

## Procedure

1. Capture a small, representative fixture of the job's real input: a trimmed table dump, a few log lines, a handful of API responses, checked into the repo under `fixtures/<job>/`.
2. Define the expected outcome as assertions on counts and key fields, not on the whole blob:
       assert out["rows_written"] == 42
       assert out["skipped"] == 3          # the three known-bad rows
       assert all(r["status"] == "settled" for r in out["rows"])
3. Run the job against the fixture with output redirected to a temp store, so the test cannot touch production. Use the same `--dry-run` or `--output` seams the job already has.
4. Include the edge cases the fixture must cover: empty input, all-duplicate input, one malformed record, a timezone boundary, and a partial failure.
5. Assert the idempotency property inside the test: run the job twice on the fixture and require the second run to change nothing (diff is empty).
6. Assert on side effects, not just the return value: no email sent, exactly one row in `job_runs`, the watermark advanced by the expected amount.
7. Freeze time (`faketime` or an injected clock) so a job with "as of now" logic is deterministic and does not fail at midnight.
8. Wire the test into CI and fail the build on a non-zero exit; a job with no test cannot be changed safely.
9. Snapshot the emitted outcome log line and compare its shape to the documented schema.
10. When the job's output is intended to change, update the fixture expectation in the same PR, with a note on why.

## Pitfalls

- Testing against a live source, so results drift and the test flakes.
- Asserting on the whole output blob, so every legitimate change fails the test.
- A fixture that only covers the happy path, missing duplicates and empties.
- Forgetting the double-run assertion, so the idempotency guard is untested.
- A "test" that calls the job's internal function rather than running it end to end.
- Time-dependent jobs with no frozen clock, failing intermittently at boundaries.

## Verification

    ./test/run-job.sh nightly-reconcile --fixture fixtures/nightly-reconcile; echo "exit=$?"
    # pass: exit 0, assertions on rows_written/skipped hold, second run diffs empty

Report the fixture, the assertions (counts and fields), the edge cases covered, and the double-run idempotency result.
