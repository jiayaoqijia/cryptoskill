---
name: verify-a-fix-under-original-conditions
description: Use when a fix passes the local test but has not run where the bug lived. Re-runs in the original environment, version, and data path before declaring the bug closed.
---

# Verify a Fix Under Original Conditions

A green unit test on your laptop is not evidence the bug is gone in production. The failure had an environment; the fix must be proven in that same environment or the claim is unearned.

## Procedure

1. List the original conditions explicitly: app version, data snapshot, concurrency, hardware, region, and the exact input that failed.
2. Confirm the fix is present in that environment, not just locally: check the deployed sha or package version actually running where you test.
3. Re-run the *original* reproduction (from `reproduce-a-bug-before-fixing`), unchanged, in the original environment. Do not substitute a newer, easier repro.
4. Compare the observable before and after with the same measurement: the query count, the exit code, the response body.
5. Test the boundary conditions that surrounded the bug: empty input, the largest input seen, and the concurrent path — fixes often hold for the case and break the neighbours.
6. For a production fix, watch the relevant metric or error rate for at least one full traffic cycle before closing, not just the next minute.
7. Attempt to falsify: try to make the old bug happen again by reverting only the fix in a scratch environment (see `reset-to-a-known-good-baseline`); it must fail there.
8. Report both outcomes — the fixed environment passing and the reverted environment failing — as the proof.

## Pitfalls

- Testing on the canary's next deploy while the report came from a different region or shard still on the old build.
- Declaring victory from logs that simply do not log the failing path any more, rather than from the measurement.
- Closing on a single successful request when the original bug was intermittent; run enough repetitions to clear the rate.
- Verifying in a staging stack whose dependencies differ (different DB size, no cache), so the path is not the same.
- Forgetting that a fix needs a data backfill; the code is right but existing bad rows remain.
- Marking the ticket closed while the original repro command is still red somewhere.

## Verification

    kubectl -n prod get pods -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u
    # the image running must contain the fixed sha before you test

    ./repro/run.sh; echo "prod exit=$?"
    # passes when the original repro now exits 0 here, and (after revert) non-zero in scratch

Report to the user: the environment and version verified, the before/after measurement, and the scratch revert that reproduced the failure.
