---
name: decide-what-to-automate
description: Use when a recurring manual task keeps interrupting work and you are tempted to script it. Scores frequency, error cost, and lifetime upkeep before any automation is built.
---

# Decide what to automate

An automation is a machine you now own: it needs monitoring, fixing, and a retirement plan. Automate only the tasks whose recurring human cost clearly beats the lifetime cost of the machine that replaces them.

## Procedure

1. Log the manual task for two weeks before deciding. Append one row per occurrence to `notes/toil-log.tsv` with date, minutes spent, and what went wrong. Frequency estimated from memory is almost always wrong; the log settles it.
2. Compute the manual cost per year: `occ_per_month * 12 * minutes / 60` hours, times the loaded hourly rate.
3. Estimate the machine's lifetime cost: build hours + `run_cost_per_month * 12 * years` + an upkeep allowance of about 10-15% of build hours per year for breakage and upgrades.
4. Apply a break-even rule with margin: automate only when the annual manual cost is at least 3x the annualised automation cost. The margin absorbs the first outage and the months you are not looking.
5. Count the error cost separately. A task that is cheap but frequently done wrong (a mistyped account number, a skipped step) is worth automating even when the minutes are low.
6. Refuse to automate judgement. "Decide if this refund is valid" is policy. Automate the lookup and the pre-fill; leave the decision with a person and record who signed off.
7. Skip rare tasks (under roughly monthly cadence) unless each occurrence is very expensive: a job that runs twice a year still needs a runbook, an owner, and an upgrade path.
8. Prefer automating a whole step over shaving seconds off one. Deleting a manual copy-paste beats speeding up a form fill.
9. Write the decision down as a one-line record: task, log-derived frequency, break-even number, verdict, and the date. Review it after the job has run for a quarter.
10. If the answer is yes, decompose the task into a trigger, an idempotent action, and an observable outcome before writing code.
11. If the answer is no, log the rejection too, so the same request is not re-litigated next month from a fresh memory.

## Pitfalls

- Automating a task that happens rarely because it is annoying, not because it is frequent.
- Pricing the build and ignoring the upkeep: the script that rots in six months has negative value.
- Automating a task whose rules change every few weeks, so the job is permanently half-wrong.
- Basing the frequency on the loudest memory instead of the log.
- Building a job with no owner and no runbook; it becomes archaeology within a quarter.
- Automating the judgement step and needing a human to undo it by hand every week.

## Verification

    awk -F'\t' '{c++; m+=$2} END{print c" occurrences, "m" minutes"}' notes/toil-log.tsv
    # cross-check the logged cadence against a calendar or ticket search before signing off

Report the task, the logged cadence, the break-even calculation, and the verdict with its date.
