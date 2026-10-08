---
name: review-the-rollback-path
description: Use when approving a change that writes data, alters schema, or changes a public contract. Requires a tested way to undo it before merge, not after an incident.
---

# Review the rollback path

If the only way out of a bad deploy is "fix forward fast", that is not a rollback plan. Review how the change is undone before it is merged, not while it is failing.

## Procedure

1. Ask what the deploy changes that outlives the process: rows written in a new format, files created, messages published, a schema altered. Those are the parts a code revert does not undo.
2. Confirm the deploy can be reverted by re-deploying the previous build — no forward-only migration in the same release, or the migration is written so the old code still reads the data.
3. Prefer a flag for behaviour changes: ship the code dark behind `feature.new_checkout=false`, then flip it. A flag rollback is seconds; a redeploy is minutes.
4. Check the new code path is exercised in staging with the flag both on and off, so "turn it off" is a tested state, not a guess.
5. For data changes, require the write be additive and idempotent so replaying the old code over the new data does not corrupt it.
6. Verify the previous artifact is still deployable: the image tag exists, the config it needs is still present. A rollback target that has been garbage-collected is not a rollback.
7. Write the rollback one-liner into the PR description: the exact command or flag flip an on-call engineer runs at 03:00.

## Pitfalls

- A rename migration in the same deploy, so reverting the code leaves it reading a column that no longer exists.
- A flag with no kill switch default; the operator has to know the flag name under pressure.
- Deleting data on the new path, which no revert restores.
- Assuming "git revert" suffices while the change already published events to consumers.

## Verification

    # Confirm the previous release is still pinnable and starts:
    docker pull registry.example.com/app:$(git describe --tags --abbrev=0 HEAD^) 2>/dev/null && echo rollback-target-ok
    # And that the flag exists and defaults off:
    grep -rn "feature\." config/flags.* | head

Report the revert command, the state the change leaves behind, and whether a flag gates it. A change that writes durable data with no tested undo is blocking.

## Worked example

A deploy writes `orders.status_history` rows in a new JSON shape and ships the reader in the same release. Reverting the code removes the reader but the rows remain, so the next deploy must tolerate the mixed shape. The fix ships the flag `orders.history_v2` default off, deploys the tolerant reader, then flips the flag. Rollback becomes `flag set orders.history_v2 off` — seconds, not minutes.
