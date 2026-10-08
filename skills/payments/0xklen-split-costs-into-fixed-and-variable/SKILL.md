---
name: split-costs-into-fixed-and-variable
description: Use when a cost base must be classified before contribution or break-even work. Classifies each line and separates mixed costs with the high-low method, validated on a third point.
---

# Split costs into fixed and variable

Contribution and break-even both depend on a split most ledgers do not carry. Classify every line by whether it moves with volume, and split the mixed ones instead of guessing.

## Procedure

1. Go line by line. Fixed if unchanged over the relevant volume range (rent, salaried staff, insurance); variable if it scales with units (materials, per-order fees, usage); mixed if it has both (a bill with a base fee and a per-unit rate).
2. Choose the relevant range and state it. A cost is fixed only over a band; rent at 4,000-7,000 units may step up past 7,000.
3. Split a mixed cost with the high-low method using two observed periods. Cost $68,000 at 12,000 units and $52,000 at 8,000 units:

       ```
       python3 -c "from decimal import Decimal as D
       vc=(D('68000')-D('52000'))/(D('12000')-D('8000')); fixed=D('52000')-vc*D('8000')
       print(vc, fixed)"
       # 4.0 20000 -> $4.00 per unit variable, $20,000 fixed
       ```

4. Validate the split on a third period. High-low is sensitive to which two points you pick, so a midpoint that matches confirms it.
5. Watch for step costs: support headcount jumps at a ticket threshold and behaves as fixed within each band.
6. Reclassify for the decision horizon. Over a month most labour is fixed; over a year it is often variable because you can hire or release.
7. Resist the allocation reflex. Overhead allocated per unit is not a variable cost; it does not change when you make one more unit.
8. Keep variable rates as integer minor units per unit and fixed totals as integer minor units; a float high-low slope moves the fixed remainder and mis-sets break-even.
9. Store the classification with the account so contribution reports do not re-argue the same lines every quarter.
10. Re-run the split yearly or after any step change in the cost base, and version the assumption.

## Pitfalls

- Calling every ledger line fixed because it does not change month to month; the decision horizon decides.
- Using high-low without checking a third point.
- Ignoring the relevant range, so a step cost is treated as fixed past the step.
- Allocating overhead per unit and then treating it as variable.
- Classifying once and never revisiting after a step change.
- Float slopes that mis-set the fixed remainder.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; vc=(D('68000')-D('52000'))/(D('12000')-D('8000')); print(vc, D('52000')-vc*D('8000'))"
    # 4.0 20000 -> $4.00/unit variable and $20,000 fixed at the 8k-12k range
    ```

Pass when the split is validated on a period outside the two used. Report the variable rate, the fixed remainder, the relevant range, and the third-point check.
