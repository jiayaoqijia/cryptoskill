---
name: enforce-a-tool-call-budget-ceiling
description: Use when an agent run has a cost, token, or call-count limit. Track spend against the ceiling per step and stop before the limit is crossed, not after.
---

# Enforce a tool-call budget ceiling

An unbudgeted agent run ends when it happens to finish, which is never a number you can quote. Set the ceiling first, meter every call, and stop at the line rather than discovering it in the bill.

## Procedure

1. State the ceiling before step one, in the units you are billed in: `max_calls=40 max_tokens=200000 max_usd=1.50`.
2. Track a running total from the first call; never estimate the total at the end from a feeling.
3. Set a soft alarm at 70% and a hard stop at 100%. At the alarm, decide: finish, simplify, or abort early.
4. Charge each step its real cost — a fan-out of ten children costs ten calls, not one.
5. Reserve a floor for the final step: never spend the last 10% before the task's own verification can run.
6. When the hard stop trips, emit a partial result with the work completed and the reason for stopping, not a silent failure.
7. Log per step: `step=7 calls=3 cum_calls=18 pct=45` so the trajectory, not just the endpoint, is visible.
8. If a step's cost is unknown, bound it first with a cheap probe (a `--dry-run`, a `head`, a count) before committing budget.
9. Carry the running total across a resumed run by reading it from the checkpoint, not restarting the meter at zero.
10. Meter wall-clock separately from tokens; a run can be under budget on tokens and still over on time.

## Pitfalls

- Counting only the top-level calls and ignoring nested fan-out, so the ledger is wrong by an order of magnitude.
- Setting the ceiling after the run and reporting whatever it spent as "the budget".
- Hard-stopping with no partial output, wasting everything spent to reach the limit.
- Spending the reserve on exploration, leaving nothing for the verification the task required.
- Treating the soft alarm as a warning to ignore until the hard stop ends the run abruptly.
- Budgeting tokens but not wall-clock, then timing out mid-run with the token limit untouched.

## Verification

```bash
python3 tools/budget.py notes/action.log --ceiling 40
# prints cumulative calls per step; fails if any step pushes cum_calls past 40
```

Report the ceiling, the spent total at exit, and whether the final verification step still ran.
