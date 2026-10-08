---
name: silent-failure-detection
description: Use when a command may exit 0 without doing its job, or when a tool reports success but the effect is unverified. Asserts the intended effect on the artefact, not merely the exit status.
---

# Silent Failure Detection

Exit code 0 means the program finished, not that it worked. Assert the effect you wanted on the real artefact; a green checkmark on an empty result is the classic silent failure.

## Procedure

1. Turn on strict shell behaviour for any step that must not silently miss: `set -euo pipefail` at the top of scripts.
2. Assert the artefact, not the status. After a write, check it exists and is non-empty: `test -s out.json || { echo "empty output"; exit 1; }`.
3. After an upsert or count-changing operation, compare before/after counts and fail if unchanged when it should have changed: `[ "$after" -gt "$before" ] || exit 1`.
4. Never treat "no output" as success. An empty `grep` means either no match or a bad pattern; print the count explicitly and branch on it: `n=$(grep -c "ERROR" app.log || true); [ "$n" -gt 0 ] && ...`.
5. Check stderr even when the exit code is 0. Many tools print the real error to stderr and still exit 0: capture and inspect it (`2>err.txt; test ! -s err.txt || cat err.txt`).
6. For HTTP work, assert the body/parse, not just the status: a 200 that returns an error page or `{"error": ...}` is a failure. Validate a field exists: `jq -e '.results | length > 0' resp.json`.
7. For find/glob/loop steps, assert the input set was non-empty before iterating; a loop over zero items "succeeds" while doing nothing.
8. For pipelines, know that `set -o pipefail` catches a failing earlier stage whose success masked a crash.
9. Record the assertion's evidence (the count, the byte size, the parsed field) in the workspace so the check is auditable.
10. For each critical step, name the one number that proves it worked (row count, byte size, parsed field) and assert it.
11. Assert the input set was non-empty before a loop or map, so zero items is a failure rather than a success.
12. Hash the artefact when a transform should change it: `shasum -a 256 before.bin after.bin` must differ.

## Pitfalls

- Reporting "tests passed" when the runner collected 0 tests.
- `find src -name '*.ts' | xargs tsc` passing because the glob matched nothing.
- A fetch that returns a login/error HTML page with HTTP 200, parsed as if it were data.
- Ignoring stderr because the exit code was 0, missing a warning that foreshadows data loss.
- A migration that "ran" but affected 0 rows because the WHERE clause matched nothing.
- A test runner reporting success while collecting zero tests, because the glob matched nothing.
- Grepping for a success string that also appears in an error message, so failures read as passes.

## Verification

    test -s out.json && jq -e '.results|length>0' out.json >/dev/null && echo OK
    # passes only when the artefact exists, is non-empty, and contains real results

Report to the user: for each critical step, the effect assertion run and its observed value (count, size, parsed field), not just the exit code.
