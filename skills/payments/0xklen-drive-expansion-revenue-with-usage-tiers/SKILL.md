---
name: drive-expansion-revenue-with-usage-tiers
description: Use when growth must come from existing accounts. Models usage-based expansion, prices the next tier, and separates real expansion from a disguised price rise on the same seats.
---

# Drive expansion revenue with usage tiers

Expansion is more MRR from an account that already pays. It is more seats, more usage, or a higher tier — and the last is only expansion if the price per unit actually fell with volume.

## Procedure

1. Classify the expansion source: seats (more users), consumption (more units), or tier (same units, different plan). Book each to a separate movement code.
2. For a usage ladder, price with declining marginal rates so the effective rate falls as volume rises (rates in minor units per unit):
   - Tier 1: 0-1,000 units at 10.
   - Tier 2: 1,001-10,000 at 6.
   - Tier 3: 10,001+ at 3.
3. Compute a bill tier by tier in integer minor units:
   `bill_minor = 1000*10 + 9000*6 + (units - 10000)*3` for units above 10,000.
4. Worked example, 12,500 units: `1000*10 + 9000*6 + 2500*3 = 10000 + 54000 + 7500 = 71500` minor = USD 715.00.
5. Compute the effective rate: `71500 / 12500 = 5.72` minor/unit — decreasing, which proves the ladder is a volume discount, not a disguised price rise.
6. Trigger expansion at a threshold, not a surprise: alert the account owner when usage crosses 80% of the current tier so the upsell is a conversation, not an overage shock.
7. Forecast expansion from the usage curve: `projected_units * marginal_rate` for accounts above 70% of a tier.
8. Report net revenue retention: `(start + expansion - contraction - churn) / start`. Expansion is only good news if NRR is above 100%.

9. Price a seat true-up at the same unit rate as the base plan, not a one-off rate, or the account feels penalised.
10. Alert on negative expansion — downgrades and seat removals — as its own motion with its own save play.
11. Cap the usage meter and notify before the next tier so an uncapped bill cannot surprise the customer.
12. Segment expansion by plan to see whether the ladder drives upgrades or just bills existing usage.
13. Measure expansion per cohort; if expansion only comes from old accounts, new accounts are not sticking.
14. Book usage expansion in the month the units were consumed, not the month the invoice lands.

## Pitfalls

- A ladder where the effective rate rises at a boundary is a cliff, and customers tunnel under it.
- Calling a list-price increase "expansion" inflates NRR without new usage; separate price from volume.
- Overage bills that arrive without warning drive churn; the 80% alert exists to prevent it.
- Aggregating tiers with float rates accumulates cent errors across thousands of accounts; use integer minor units per unit.
- Booking seat expansion without checking the seat is actually active counts empty licences as growth.

- A true-up at a different rate than the base plan is a hidden price rise the customer finds in reconciliation.
- Ignoring contraction because it is not churn lets a slow downgrade attrition go unmeasured.
- An uncapped overage that surprises the customer converts expansion into a refund and a churn.
- Counting expansion from price rises as volume growth inflates NRR without new usage.

## Verification

    python3 -c "u=12500; bill=1000*10+9000*6+max(0,u-10000)*3; print(bill, bill*100//u)"
    # 71500 572 -> $715.00 at an effective 5.72 minor/unit, below the 10-unit tier-1 rate

Report: expansion MRR by source code (seats/consumption/tier), the effective rate at the new volume, and NRR.
