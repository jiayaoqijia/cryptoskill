---
name: compute-contribution-margin-per-unit
description: Use when deciding whether extra volume or a special order is worth taking. Computes contribution margin from price minus variable cost and applies it to short-run decisions and scarce capacity.
---

# Compute contribution margin per unit

Contribution margin is what one more unit adds after its own variable cost. Fixed cost is already sunk for a short-run decision, so the question is never "does this cover everything" but "does this add anything".

## Procedure

1. Separate variable cost (materials, per-unit fulfilment, payment fees, usage) from fixed cost (rent, salaried staff, the platform fee).
2. Compute contribution per unit = price - variable cost. Price $20.00, variable cost $12.00, contribution $8.00.
3. Compute the contribution ratio = contribution / price = 8/20 = 40%.
4. Judge an incremental order on contribution only: a special order at $15.00 against a normal $20.00 still adds $3.00 per unit, so it is profitable if it does not displace normal sales or consume scarce capacity.
5. Add capacity as a second constraint when it binds. Rank by contribution per machine hour, not per unit:

       ```
       python3 -c "from decimal import Decimal as D; print('A', D('8')/D('0.5'), 'B', D('30')/D('2.0'))"
       # A 16/hour vs B 15/hour -> A wins on the scarce resource
       ```

6. Never price below variable cost, even for a strategic order; that is a real cash loss on every unit and the floor in `set-a-minimum-viable-price-floor`.
7. Total contribution for the period = contribution per unit * units; deduct fixed cost once at the end to reach operating profit.
8. Compute contribution in integer minor units; a float variable cost per unit multiplied across thousands of units drifts and can flip the decision near the floor.
9. Re-check the split as volume grows, because some "fixed" costs step up and become semi-variable at a threshold.
10. Report the decision as contribution per unit and per constrained resource, not as a blended margin percentage.

## Pitfalls

- Treating allocated overhead as a variable cost, which makes a valid incremental order look unprofitable.
- Ranking by margin percentage when a scarce resource should rank by contribution per hour.
- Taking an incremental order that displaces full-price sales.
- Pricing below variable cost and calling it strategic; no volume fixes it.
- Blending contribution across products with different cost structure.
- Float variable costs that flip the sign of the decision near the floor.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('20')-D('12'))"
    # 8.00 -> $8.00 contribution per unit at a $20 price and $12 variable cost
    ```

Pass when the variable cost is separated from fixed and both the per-unit and per-resource contribution are shown. Report contribution per unit, per constrained resource, and whether fixed cost remains covered.
