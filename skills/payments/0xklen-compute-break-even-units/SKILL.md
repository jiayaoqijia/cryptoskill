---
name: compute-break-even-units
description: Use when asked how many units or how much sales cover the cost base. Computes break-even from fixed cost and contribution margin, adds a target profit, and reports the margin of safety.
---

# Compute break-even units

Break-even is the volume where contribution exactly pays the fixed base. It converts a cost structure into a sales target and exposes how much cushion the plan actually has.

## Procedure

1. Total the fixed cost for the period: rent, salaried payroll, software, the fixed platform fee. Say $84,000 a month.
2. Get contribution margin per unit: price minus variable cost. $20.00 - $12.00 = $8.00.
3. Break-even units = fixed cost / contribution per unit.

       ```
       python3 -c "from decimal import Decimal as D; print(D('84000')/D('8'))"
       # 10500.0 units
       ```

4. Break-even revenue = break-even units * price = 10,500 * 20 = $210,000, or equivalently fixed / contribution ratio = 84,000/0.40.
5. Add a target profit: units = (fixed + target) / contribution. For $30,000 of profit: (84,000+30,000)/8 = 14,250 units.
6. Compute the margin of safety = (expected units - break-even units) / expected units. At 14,000 expected against 10,500 break-even, safety is 25%.
7. Stress the two inputs together. A 10% price cut raises break-even by the same share as the margin lost and is the most common way a plan misses.
8. Round up, never down, when a plan needs a whole number of units to cover cost: 10,500 covers, 10,499 does not.
9. Keep variable cost per unit in integer minor units so the division has a stated rounding rule; a float contribution reassigns the rounding to the wrong side.
10. Re-state break-even whenever price or fixed cost changes. It is a living target, not an annual figure.

## Pitfalls

- Dividing by gross margin instead of contribution margin.
- Forgetting that a price cut lowers the contribution the fixed base is divided by.
- Rounding break-even units down and leaving the plan a unit short of covering cost.
- Treating a step cost as fixed past the volume where it steps up.
- Using last period's variable cost after an input change.
- Float contribution that reassigns the rounding of the break-even unit.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('84000')/D('8'))"
    # 10500.0 -> 10,500 units cover $84,000 fixed at $8.00 contribution
    ```

Pass when fixed cost, contribution per unit and both break-even figures are shown. Report break-even units, break-even revenue, and the margin of safety at the planned volume.
