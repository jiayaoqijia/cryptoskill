---
name: scaffold-a-tutorial-with-checkpoints
description: Use when writing a step-by-step tutorial. Puts a verifiable checkpoint after each step that fails loudly if the learner skipped ahead, so drift is caught at the step it happened, not at the end.
---

# Scaffold a Tutorial with Checkpoints

A tutorial without checkpoints lets a reader drift three steps and only notice at the end, blaming themselves. A checkpoint after each step localises the mistake to where it actually happened.

## Procedure

1. Break the build into numbered steps, each producing an observable change.
2. After each step, insert a checkpoint the learner runs and compares, e.g. `curl -s localhost:3000/health | jq -e '.status=="ok"'` for step 2.
3. Make checkpoints fail loudly and specifically, naming the step: `echo "step 3 FAILED: expected 3 rows, got 0"`.
4. Keep each step to a single concept; split any step that carries two ideas.
5. Verify the tutorial yourself end to end in a clean directory.
6. Re-run after deleting one step's output and confirm exactly that step's checkpoint fires.
7. Ship a `check.sh` that runs all checkpoints in order, so a stuck reader can bisect the failure.
8. Date the tutorial and pin the dependency versions the steps install.
9. Record the total run time so a reader can plan; a 90-minute tutorial should say so up front.
10. Number checkpoints to match step numbers, so a failure points straight at a step.
11. Make the first two steps trivially verifiable to build early confidence.
12. Commit the clean-run output so drift from a dependency change is detectable.
13. State the expected output beside each checkpoint so the reader can diff.
14. Keep checkpoints independent so any one can be run alone.
15. Note the total step count up front so the reader knows the length.

## Pitfalls

- Checkpoints only at the end, so the failure is far from its cause.
- A checkpoint that passes on a half-built app because the assertion is too weak.
- Steps that combine setup and a new concept, so a failure is ambiguous.
- An unversioned tutorial that breaks silently when a dependency releases.
- A checkpoint that only checks process exit, not the actual output.
- Steps that assume a leftover file from an earlier attempt, so a clean run fails.
- A checkpoint that depends on the previous checkpoint's side effects.
- Steps that assume a shell alias the reader may not have.
- Testing only the happy path and never the skipped-step failure.
- A checkpoint with no stated expected value.
- Checkpoints that only work in sequence.
- A tutorial of unknown length, which readers abandon.

## Verification

    bash tutorial/check.sh
    # passes when every checkpoint reports PASS on a clean run and a skipped step makes exactly one FAIL

Report to the user: the checkpoint list, the expected output per step, and the clean-run result.
