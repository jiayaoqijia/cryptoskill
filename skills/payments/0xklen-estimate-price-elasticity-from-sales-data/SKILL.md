---
name: estimate-price-elasticity-from-sales-data
description: Use when a price has changed and you must judge whether revenue went up or down. Computes arc elasticity from two observed points and states the revenue direction with both raw totals.
---

# Estimate price elasticity from sales data

Raising a price usually lowers units, and the only question that matters is whether the extra dollars per unit beat the lost volume. Elasticity answers that from two observed points, without a new experiment.

## Procedure

1. Collect clean paired periods: units and average realised price, same segment, before and after the change. Strip promotions and one-off orders.
2. Compute the arc elasticity in midpoint form, not the naive point form:

       ```
       python3 -c "from decimal import Decimal as D
       p1,u1=D('10.00'),D('1000'); p2,u2=D('12.00'),D('850')
       print((u2-u1)/((u1+u2)/2) / ((p2-p1)/((p1+p2)/2)))"
       # -0.739
       ```

3. Read the sign and magnitude: |e| < 1 is inelastic, so raising the price raised revenue here.
4. Confirm with the raw revenue, not the elasticity alone: 10.00 * 1000 = $10,000 against 12.00 * 850 = $10,200, up $200.
5. Use the elasticity to target, not to predict. For linear demand, revenue peaks near |e| = 1, where a 1% rise costs almost 1% of units.
6. Check the confound before trusting the ratio: a season, a channel shift, or a marketing change during the window breaks the comparison.
7. With two points you have a slope, not a curve; label it as an estimate and re-measure after the next change.
8. Segment the elasticity. A move that is inelastic for loyal buyers is usually elastic for new ones.
9. Keep prices as integer minor units and units as integers so the ratio is exact; a float price average flips the sign near |e| = 1.
10. Publish the number with its window and segments attached, or it will be reused as if it were a constant.

## Pitfalls

- Point elasticity on a large price change overstates the response; use the arc form above.
- Comparing periods that differ by season or a marketing push.
- Treating elasticity as a constant when it is local to the price you measured.
- Reading a revenue rise as a win without checking whether units fell off a cliff.
- Averaging price across mixed SKUs, which hides the move you are measuring.
- Float price averages that flip the sign of the ratio near unit elasticity.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print((D('850')-1000)/(D('925')) / ((D('12')-10)/(D('11'))))"
    # approx -0.739 -> inelastic in this window
    ```

Pass when the elasticity, the window, the segment and both raw revenue totals appear together. Report the elasticity, its population, and the revenue direction.
