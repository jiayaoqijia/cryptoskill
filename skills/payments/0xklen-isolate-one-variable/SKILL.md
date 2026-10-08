---
name: isolate-one-variable
description: Use when debugging a change or comparing approaches and two things could explain the result. Changes exactly one input per trial and reverts it before the next, so the observed effect is attributable.
---

# Isolate One Variable

If two things changed and the result moved, you learned nothing about either. Vary one input, hold everything else fixed, record the delta, and revert before the next trial.

## Procedure

1. State the hypothesis as a single variable: "the failure is caused by the cache being enabled", not "something about the config".
2. Establish a control: a run with the variable at its known-good value and everything else untouched. Record its observable output.
3. Change exactly one thing and re-run. Record the same observable. Do not bundle a second tweak "while you're here" — that is the trap this skill exists to avoid.
4. Compare deltas against the control. A change that does not move the observable is not the cause; revert it and pick the next variable.
5. Revert the variable before the next trial so trials do not accumulate. Use `git stash` or `git checkout -- <file>` between runs.
6. Log each trial as one row: `trial_id, variable, control_value, test_value, observable_control, observable_test`.
7. When the cause is confirmed, re-introduce it once to show the effect returns (a falsification test), then apply the real fix.
8. If no single variable explains it, suspect an interaction: test the two candidates together and separately to detect a joint effect.
9. Log each trial's environment (commit sha, config hash, input hash) so trials are provably comparable.
10. Run the control at least twice to establish the observable's natural variance before attributing any delta.
11. If reverting the variable does not restore the control observable, something else changed — find it before continuing.

## Pitfalls

- Upgrading the library and changing the config in one commit, then not knowing which fixed it.
- Running trials without reverting, so results reflect the pile of prior changes, not the variable.
- Changing the observable between trials (logging more in one run), making deltas incomparable.
- Inferring causation from a single trial with no control run.
- Adjusting two config knobs "that are obviously related" and calling it one variable.
- Comparing a trial under load with a control on an idle machine, mistaking latency for causation.
- Reverting in the editor but not restarting the service, so the old process keeps the changed config live.

## Verification

    cat notes/trials.tsv | cut -f2 | sort | uniq -d
    # passes when no variable appears with two different test values in the same trial row

Report to the user: the hypothesis, the control vs test observables, and the falsification run that confirmed the single cause.
