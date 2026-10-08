---
name: compute-funnel-conversion-from-impression-to-payment
description: Use when a full acquisition funnel must be measured impression to payment. Computes stage-by-stage conversion and end-to-end rate, then locates the stage that loses the most absolute volume.
---

# Compute funnel conversion from impression to payment

One end-to-end conversion rate hides which stage failed. Compute every stage-to-stage rate and find where the funnel loses the most absolute people, because a leaky stage early matters more than a bad rate late.

## Procedure

1. Fix the stages and define each as an event, not a page view: impression -> click -> landing -> signup -> activated -> trial -> payment. Every stage must be countable in one pass.
2. Build counts per stage for the same cohort and window. Never mix a marketing-sourced impression count with a product-sourced signup count from a different period.
3. Compute stage conversion: `rate_i = count_{i+1} / count_i`.
4. Compute end-to-end: `e2e = count_last / count_first`, and verify it equals the product of the stage rates to catch a counting break.
5. Worked example:
   - impressions 2,000,000 -> clicks 40,000 (2.0%) -> landing 38,000 (95%) -> signup 4,560 (12%) -> activated 2,280 (50%) -> paid 570 (25%).
   - e2e = 570 / 2,000,000 = 0.0285%.
6. Find the biggest absolute leak: the stage that loses the most *people*, not the lowest rate. Here signup->activated loses 2,280 people; that is usually the lever.
7. Value each improvement by its downstream multiplier: `value = delta_people * downstream_rate * arpu_minor`.
8. Segment by source and device; a funnel can look healthy blended and be broken on mobile.
9. Report the table plus the one stage to fix first, with the modelled revenue lift.

10. Track stage lateness: a signup that activates 20 days later belongs to a later cohort and distorts the recent window.
11. Reconcile the ad platform's click count to your server-side landing count; a 10%+ gap is tracking loss.
12. Weight improvements by downstream conversion so you fix where a lift propagates furthest.
13. Watch the tail: a stage can look healthy at the median and lose a large segment entirely.
14. Rebuild the funnel monthly and store it, so a change in one stage is attributable rather than inferred.
15. Separate paid and organic funnels; blending them hides that organic carries a different drop-off profile.

## Pitfalls

- Quoting only the end-to-end rate, which makes a 2% click-through look like the whole problem when the leak is later.
- Mixing cohorts: ad-platform impressions and ledger payments rarely cover the same window.
- Counting a "signup" as email-submitted when the account is never activated inflates the next stage.
- Optimising the lowest-rate stage instead of the highest-volume-loss stage spends effort where it moves least revenue.
- The product of stage rates not equalling e2e reveals a tracking break you would otherwise miss.

- Delayed activation assigns recent cohorts a falsely low rate; wait for maturity or model the lag.
- Trusting the ad platform's click count when the server logs 15% fewer starts the funnel from a wrong denominator.
- Optimising a median stage while a whole segment exits there loses eligible revenue the average hides.
- A funnel rebuilt ad hoc each month cannot attribute a change to a stage.

## Verification

    python3 -c "c=[2000000,40000,38000,4560,2280,570]; print([round(c[i+1]/c[i]*100,2) for i in range(len(c)-1)], round(c[-1]/c[0]*100,4))"
    # [2.0, 95.0, 12.0, 50.0, 25.0] 0.0285 -> stage rates multiply to the end-to-end rate

Report: the stage table, the largest absolute leak, and the modelled revenue lift from a named improvement.
