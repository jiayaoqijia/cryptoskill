---
name: report-status-not-activity
description: Use when writing an update or progress note. Report the state of the deliverable — done, not done, blocked — not the list of things you touched.
---

# Report status, not activity

A list of things you did can grow while the deliverable stalls. The reader wants the state of the world, not a log of your effort.

## Procedure

1. Fix the done-criteria before writing: an item is `done` only when its acceptance check passes, e.g. `pytest -q tests/test_api.py` green.

2. For each item emit exactly one of three states: `done` (with the verifying command), `in progress` (with a fraction and the next checkpoint), or `blocked` (with the blocker).

3. Never list effort as progress: "spent 2h on the parser" is activity; "parser handles nested arrays, `make test` passes" is status.

4. Give one completion fraction for the deliverable itself: `7/12 endpoints implemented`.

5. Attach the changed files with `git diff --stat`, not a prose tour of the day.

6. End with the next concrete checkpoint and its ETA, so the reader knows when to look again.

7. If the deliverable has no acceptance check yet, write one first; a status with no check behind it is an opinion.

## Pitfalls

- Activity lists look busy while the deliverable does not move, giving false comfort.
- A percentage with no denominator ("80% done") cannot be checked.
- Calling a task done because the clock ran out is a lie of omission.
- "Mostly working" hides which parts are not; name the failing parts.
- Mixing plan, activity, and status in one list forces the reader to extract state themselves.

## Verification

    git diff --stat && pytest -q   # changed files and a pass/fail line underpin the status

Report each item as done, in progress, or blocked with the command behind it; never as effort.
