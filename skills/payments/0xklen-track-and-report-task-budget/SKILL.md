---
name: track-and-report-task-budget
description: Use when a task has a time, call, or token limit. Measure consumption as you go, reserve room to report, and stop before the ceiling instead of after it.
---

# Track and report a task budget

Budgets fail silently: the work looks fine right up to the moment it is not. This skill keeps consumption visible and reserves enough room to wrap up and hand off cleanly.

## Procedure

1. Fix the ceiling before starting and write it to `budget.txt`: `limit=600s calls=40 tokens=200k`.

2. Record the start time: `date +%s > .start`. Append a line per tool call as you make it, or keep a counter in the file.

3. At each tenth of the budget, compute remaining against work left. If less work is done proportionally than budget consumed, stop and re-plan rather than push through.

4. Reserve the last 15% for wrap-up: writing the summary, running verification, and cleaning up temp files.

5. If you reach the ceiling with work incomplete, stop cleanly: report the partial state with commands, hand off the remaining steps, and do not bluff a finish.

6. Persist interim results to disk continuously (JSON or CSV in the workspace), so a timeout costs seconds, not the task.

7. Watch for silent sinks: a retry loop can eat the whole budget. Cap retries at three, then switch approach or report.

8. Read large inputs with paging — `read_file` with `offset`/`limit` — so a single read cannot blow the token budget.

## Pitfalls

- Renegotiating the ceiling to finish is scope creep wearing a clock.
- A background command with no `timeout` may run past your window; set an explicit timeout.
- Not budgeting the verification step leaves "done" unproven, which is worse than slow.
- Counting wall-clock only misses call exhaustion, and vice versa; track the binding limit.
- Polling a long job in a tight loop burns calls for no information; check at increasing intervals.

## Verification

    echo "elapsed=$(( $(date +%s) - $(cat .start) ))s"; cat budget.txt

Report consumed versus limit and the exact reason for stopping; never present an over-budget run as success.
