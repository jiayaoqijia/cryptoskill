---
name: measure-the-value-of-an-automation
description: Use when you need to justify keeping, fixing, or cutting an automation. Tracks hours saved against build, run, and maintenance cost in a running ledger.
---

# Measure the value of an automation

An automation earns its place only if what it saves exceeds what it costs to run and maintain. Keep the numbers, because "it seems useful" is how dead jobs survive.

## Procedure

1. Record the build cost once: engineer-hours to write, review, and ship, from the ticket or the commit range.
2. Track the running cost continuously: compute minutes, storage, paid API calls, and (for cloud) the billable tags on the job's resources. Tag them so the cost is attributable.
3. Track the upkeep cost: hours per month spent fixing, upgrading, and answering its alerts. Pull this from the tickets that reference the job's name or runbook.
4. Record the benefit in the same units as the manual baseline: hours of human work no longer spent, from the original toil log extrapolated, plus avoided-error cost.
5. Compute value monthly: `benefit_hours - (run_cost + upkeep_hours + amortised_build)` in hours, so everything is comparable.
6. Keep a ledger file so the trend is visible, not just the current value:
       # automation-ledger.tsv
       month	benefit_h	run_h	upkeep_h	build_amort_h
7. Watch the trend: an automation whose upkeep is climbing and benefit is flat is decaying toward negative and should be fixed or retired.
8. Re-baseline when the world changes: if the manual task would now be trivial (a vendor added a feature), the original benefit is gone.
9. Count the cost of its failure too: a job that pages at 2am and takes an hour has an upkeep entry for every such incident.
10. Review the ledger quarterly with the owner and decide keep, fix, or retire explicitly, recorded with a date.

## Pitfalls

- Counting the build once and never the upkeep, which is usually the larger number.
- Measuring benefit from an optimistic estimate instead of the logged manual frequency.
- Ignoring incident cost — a job that pages twice a month is not free.
- Untagged resources, so run cost is buried in a shared bill and unknowable.
- Comparing hours to money without converting, then declaring a win.
- Never revisiting the baseline after the underlying task changed.

## Verification

    column -t automation-ledger.tsv
    # pass: every live automation has a row for this month and a nonzero upkeep figure

Report the benefit hours, the run and upkeep hours, the amortised build, and the keep/fix/retire decision with its date.
