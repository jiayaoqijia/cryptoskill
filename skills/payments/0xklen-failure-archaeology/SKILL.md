---
name: failure-archaeology
description: Use when something broke and the cause is not obvious from the last error. Locates the first divergent event, not the loudest one, by bisecting state and inputs.
---

# Failure Archaeology

The last error is rarely the cause; it is the first symptom loud enough to notice. Work backward to the earliest point where reality started disagreeing with expectation.

## Procedure

1. Reproduce first. A failure you cannot trigger on demand is not yet understood. Record the exact command and inputs that reproduce it: `python -m app.run --input case.json`.
2. Read the error text literally for one line — file, line, and message. Do not paraphrase it into a familiar diagnosis; the exact wording usually names the real fault.
3. Find the first divergence, not the last crash. For a code regression, `git bisect start; git bisect bad HEAD; git bisect good v1.2.0` and let it find the introducing commit.
4. For data-dependent failures, shrink the input by binary search: halve the records; if it still fails, recurse into the failing half until you have the minimal reproducing case.
5. Check logs in timestamp order across components, not per component. A message in service A at 10:03:11 usually explains the crash in service B at 10:03:12.
6. Distinguish the trigger from the latent bug: a new input may merely expose an ordering or null-handling defect that existed for months. Fix the latent defect, not only the trigger.
7. Write a timeline file: `[time] [component] [event]` rows, oldest to newest, ending at the observed failure. The row before the first anomaly is your prime suspect.
8. Confirm the cause by a falsification test: revert or patch the suspected cause alone and show the failure disappears; then re-introduce it and show it returns.
9. Check the environment against last-known-good: dependency versions, env vars, timezone (`node -v`, `pip freeze | diff - baseline.txt`).
10. For a regression with no obvious commit, bisect on the input set instead of the code: find the smallest input that flips pass to fail.
11. Preserve the failing state before fixing (copy the artefact to `/tmp/fail-case/`) so the fix can be re-tested against it.

## Pitfalls

- Fixing the final stack frame's error (e.g. a null deref) without asking why the value was null.
- Bisecting code when the divergence is environmental (a dependency version, a clock, a locale).
- Reading one service's log alone and concluding "it just crashed".
- Treating an irreproducible failure as fixed because it did not recur in one run.
- Assuming the cause is the most recent change, when an older latent defect merely surfaced now.
- Concluding "it was a fluke" after one non-reproducing run, then shipping the latent bug.
- Bisecting with a flaky test in the range, so the result points at an innocent commit.

## Verification

    git bisect reset && git log --oneline -1
    # passes when the identified commit, reverted alone, makes the failure disappear

Report to the user: the minimal reproduction, the first divergent event with its timestamp, and the falsification test that confirmed the cause.
