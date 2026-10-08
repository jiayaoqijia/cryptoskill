---
name: compute-gross-margin-and-markup
description: Use when someone quotes a margin or a markup for a product or a service. Separates the two denominators, prices backwards from a target margin the correct way, and computes the ratio from exact minor units.
---

# Compute gross margin and markup

Margin and markup are different denominators and people use the words interchangeably. Mixing them is how a "40% margin" plan ends up selling at 29%. Pin the definition, then price backwards from the target.

## Procedure

1. Define margin on revenue: `margin = (price - cost) / price`. Define markup on cost: `markup = (price - cost) / cost`.
2. Worked pair — cost $40.00, price $100.00: margin 0.60 (60%), markup 1.50 (150%). Same deal, two numbers.
3. To hit a target margin, divide the cost; never multiply. `price = cost / (1 - target_margin)`. For a 40% margin on a $30.00 cost: `30/0.6 = 50.00`, not `30*1.4 = 42.00`.
4. The multiply path is the markup formula: `price = cost * (1 + markup)`. The two diverge as the target grows, and at 60% margin the multiply path is nowhere near.
5. The keystone convention (double the cost) is exactly a 50% margin, no more: `(2c - c)/2c = 0.5`.
6. Convert a supplier's markup before comparing it to your margin target: `margin = markup/(1+markup)`. A 50% markup is a 33.3% margin.
7. State which denominator every report uses, once, at the top: "all margins are on revenue."
8. Keep gross margin (after cost of goods) distinct from contribution margin, which strips variable cost only — see `compute-contribution-margin-per-unit`.
9. Compute the ratio from exact integers, then round the percentage once:

       ```
       python3 -c "from decimal import Decimal as D; c=D('3000'); p=D('5000'); print((p-c)/p)"
       # 0.4  -> 40.0% margin on an exact minor-unit basis
       ```

10. Re-derive the price whenever cost moves. A margin held as a percentage of a stale price is not held at all.

## Pitfalls

- Multiplying cost by (1 + margin) to hit a margin target; that is the markup formula, so the price comes out too low and the realised margin misses.
- Dropping a supplier markup straight into a margin comparison without converting it.
- Reporting margin on cost ("we make 50% on cost") and labelling it margin.
- Using contribution margin and gross margin interchangeably when a decision turns on the fixed-cost line.
- Computing the ratio from a rounded price, which moves a true 39.8% to a displayed 40%.
- Storing cost or price as a float, so `30.00` sits as `29.999999` and the ratio wobbles.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('3000')/(1-D('0.40')))"
    # 5000 minor units = $50.00, the price that yields a 40% margin on a $30.00 cost
    ```

Pass when the report names its denominator and the backward price matches the formula. Report which denominator was used, the margin and markup pair, and the backward price for the target margin.
