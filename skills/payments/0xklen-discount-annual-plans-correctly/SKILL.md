---
name: discount-annual-plans-correctly
description: Use when setting an annual price against a monthly plan. Computes the true discount from months-free, the effective monthly rate and the cash timing, without overstating the saving.
---

# Discount annual plans correctly

"Two months free" is not a 20% discount and "pay annually" is not the same cash as "pay monthly". Get the effective rate and the discount in minor units right, or the plan quietly sells below its floor.

## Procedure

1. Start from the monthly price and the promised benefit. Monthly $30.00, annual price $300.00 means you give up $60.00 of the $360.00 full-year value.
2. Compute the true discount: `1 - annual/(monthly*12)` = `1 - 300/360` = 16.67%, which is exactly 2/12.

       ```
       python3 -c "from decimal import Decimal as D; print(1 - D('300')/(D('30')*12))"
       # 0.1667 -> two months free is 16.7% off, not 20%
       ```

3. Compute the effective monthly rate for comparison: annual / 12 = $25.00, the number to show if you advertise a monthly-equivalent.
4. Never call 16.7% "20% off"; the mismatch is the fastest route to a bait-pricing complaint.
5. Value the cash timing. $300 upfront versus $30 monthly means the annual cash is collected at month 0, so the benefit to you is the time value plus lower churn, often worth more than the nominal discount.
6. Check the discount against margin. A 16.7% discount on a 40% margin needs `0.1667/(0.40-0.1667)` = 71% more annual units to hold profit.
7. Set the annual price as an integer minor unit (`annual_price_minor=30000`) and derive the monthly-equivalent by integer division with a stated rounding rule.
8. Offer a monthly plan only if the monthly premium covers the extra billing cost and the churn; otherwise annual-only is cleaner.
9. Handle annual renewal declines carefully: one decline is a full year of revenue, so retries and dunning matter more than on monthly.
10. Re-check the discount when the monthly price changes; an annual price left fixed deepens the discount over time.

## Pitfalls

- Advertising "two months free" as 20% off when it is 16.7%.
- Forgetting that the discount deepens the break-even volume requirement.
- Comparing annual cash to monthly MRR without valuing the timing.
- Fixing the annual price while the monthly price rises, silently deepening the discount.
- Ignoring that an annual renewal decline is a full year of revenue at risk.
- Float annual prices that do not divide exactly into the monthly-equivalent.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(1 - D('300')/(D('30')*12))"
    # 0.1667 -> the true discount behind "two months free"
    ```

Pass when the true discount and the effective monthly rate are both stated. Report the true discount, the effective monthly rate, and the extra annual units the discount requires.
