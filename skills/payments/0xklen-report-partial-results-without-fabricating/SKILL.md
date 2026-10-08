---
name: report-partial-results-without-fabricating
description: Use when a task cannot be fully completed. Deliver the finished part with evidence, name each unfinished part, and never fill the gap with invented output.
---

# Report partial results without fabricating

Half a result reported honestly is useful; a whole one invented is sabotage. This skill makes the boundary between done and not-done unambiguous, and forbids synthesising the missing pieces.

## Procedure

1. Enumerate the sub-tasks and mark each `complete`, `partial`, or `untouched`.

2. For every `complete`, give the command that demonstrates it and paste its output.

3. For every `partial`, state exactly which portion works and which does not, with the error text for the failing part.

4. For every `untouched`, say why: no time, blocked dependency, or out of scope.

5. Do NOT synthesise missing output. If a step could not run, the report says it did not run and shows the failure. Fabricated logs, data rows, or API responses are never acceptable, under any deadline.

6. List what a successor needs to finish: commands to run, files to read, decisions still pending.

7. Reconcile the counts at the end: the number of marked sub-tasks must equal the number you enumerated.

## Pitfalls

- "Mostly done" with no sub-task list hides exactly which parts are missing.
- Filling an empty data file with plausible rows turns a known gap into an invisible lie.
- Presenting an untested path as working fails the moment the user relies on it.
- Omitting a failed step from the summary is fabrication by silence, and equally disqualifying.
- A partial that is 90% done still carries its 10% of risk; name that 10% explicitly.

## Verification

    grep -cE "^(complete|partial|untouched)" RESULT.md   # must equal the sub-task count

Report the partition and the failing error verbatim; leave the gap open and labelled, never filled.
