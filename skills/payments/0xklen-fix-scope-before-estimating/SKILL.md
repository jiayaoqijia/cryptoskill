---
name: fix-scope-before-estimating
description: Use when an estimate keeps moving because the thing being estimated keeps growing. Writes an explicit done-definition and exclusions first, so the estimate is attached to a fixed object.
---

# Fix scope before estimating

An estimate on a moving definition is worthless: any number can be met by adding or removing work after the fact. Freeze what "done" means and what is out of scope, then estimate — and treat any change to that boundary as a change to the estimate.

## Procedure

1. Write the done-definition in testable terms: "a user can reset their password via email link, on desktop, and the old password stops working." Not "improve auth."
2. List explicit exclusions: "no SMS reset, no admin-forced reset, no rate-limit UI." Exclusions are as load-bearing as inclusions.
3. Estimate only against the frozen definition in `notes/scope.md`. If a step is needed but excluded, note that the exclusions assume it is not needed.
4. Version the scope. When scope changes, bump it and re-estimate; never let a silent addition ride inside the old number:

       notes/scope.md
       scope v1 (2026-02-01): as above — estimate 6-9 days
       scope v2 (2026-02-05): +SMS reset (asked by support) — estimate 9-14 days

5. Attach the estimate's confidence to the scope version, so a "5-day" answer is never reused for a larger v2.
6. If asked for a number before scope is fixed, give a range and say it is conditional on scope: any change moves it.
7. Keep the exclusions visible in the same file reviewers read, not buried in a thread.

## Pitfalls

- Estimating a feature name rather than a behaviour, so the object the number refers to is undefined.
- Accepting a small mid-flight addition as "obviously in scope," which is how a 6-day estimate becomes 14 with nobody deciding.
- Listing inclusions but no exclusions, so everything is arguably in scope.
- Re-using a v1 estimate after a v2 scope change because the ticket number stayed the same.
- Writing done-definition so loosely ("works well") that it cannot be tested and therefore cannot be frozen.

## Verification

    grep -n 'scope v' notes/scope.md
    # passes when each scope version has a date, its additions/removals, and its own estimate

Report the frozen done-definition, the exclusions, the scope version the estimate belongs to, and the estimate.
