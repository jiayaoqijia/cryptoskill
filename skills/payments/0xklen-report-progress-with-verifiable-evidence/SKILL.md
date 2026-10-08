---
name: report-progress-with-verifiable-evidence
description: Use when giving a status update on multi-step work. Pair every "done" with the command that proves it and the raw output line a reader can reproduce.
---

# Report progress with verifiable evidence

"Done" is a claim; a passing command is proof. This skill forbids any status line the reader cannot re-run for themselves and check in seconds.

## Procedure

1. Before writing the report, list what you believe is complete.

2. For each item, identify a command that would FAIL if the work were undone — a health check, a grep for the new symbol, a test selector: `curl -s -o /dev/null -w "%{http_code}" localhost:8080/health` must print `200`.

3. Run each command now, in this session. Paste the literal output, trimmed to the decisive line.

4. Classify each item strictly: `done` (command passed), `in progress` (partial output exists), `blocked` (command failed, with its error text). Never promote `in progress` to `done` on expectation.

5. For blocked items, state the exact blocking error first, then what you tried, in that order.

6. Add one sentence of next action with a rough time estimate.

7. Save the report to `STATUS.md` so the next reader sees the same evidence you did, with commands inline.

8. If a claim cannot be backed by a re-runnable command, either find one or downgrade the claim's wording to match what you actually verified.

## Pitfalls

- "Should work" and "looks good" are not statuses; the command either passed or it did not.
- A suite you did not run is not green; a 0 exit from a previous session proves nothing about the current tree.
- Reporting tasks instead of outcomes hides whether the system actually works for the user.
- Pasting partial output without the failing line reads as success — include the failure verbatim.
- A passing unit test is not a passing integration path; name which layer the evidence covers.

## Verification

    curl -s -o /dev/null -w "%{http_code}\n" localhost:8080/health   # expect 200

Report only values a reader can reproduce; when you cannot re-run a check, say so plainly.
