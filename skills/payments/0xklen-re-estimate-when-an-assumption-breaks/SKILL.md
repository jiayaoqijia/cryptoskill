---
name: re-estimate-when-an-assumption-breaks
description: Use when a plan was built on assumptions that have since changed. Recomputes the estimate from the new facts and reports the delta, instead of quietly defending the old number.
---

# Re-estimate when an assumption breaks

An estimate is only valid under its assumptions. When one breaks, the honest move is to recompute and say what changed — not to absorb the change silently and deliver a surprise later.

## Procedure

1. Keep the assumptions next to the estimate, each with a date and a status:

       notes/plan.md
       - assumption: single sign-on already exists (2026-02-01, CHECKED true)
       - assumption: staging deploys under 5 min (2026-02-01, now 22 min — BROKEN)

2. When an assumption flips to BROKEN, list what depended on it. Usually several tasks inherit the change.
3. Re-run the affected parts of the estimate with the new value, updating `notes/plan.md`. Do not re-estimate the whole plan from scratch — that discards the parts that are still valid and invites re-litigating settled work.
4. Compute the delta explicitly:

       python3 -c "old=11.5; new=16.0; print('delta', round(new-old,1), 'x', round(new/old,2))"
       delta 4.5 x 1.39

5. Report the new range, the delta, and the assumption that caused it — the cause is the actionable part.
6. If the delta breaks a deadline, escalate with options: cut scope, add people, move the date. Do not silently pick one.
7. Update the estimate's date so consumers can see it is fresh.

## Pitfalls

- Absorbing the change into overtime and hoping it does not recur, then reporting the slip at the end.
- Re-estimating everything, which creates noise and lets people question parts nobody changed.
- Removing the old assumption from the file, so the cause of the delta disappears from the record.
- Reporting only the new number without the delta, so stakeholders cannot see how much worse it got.
- Treating every broken assumption as equally severe; rank by the delta each produces.

## Verification

    grep -n 'BROKEN' notes/plan.md
    # passes when each BROKEN assumption names the tasks that depended on it and the resulting delta

Report the old estimate, the new estimate, the delta, and the specific assumption whose change caused it.
