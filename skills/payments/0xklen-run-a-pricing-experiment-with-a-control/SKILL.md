---
name: run-a-pricing-experiment-with-a-control
description: Use when testing a price change on live traffic. Designs a between-subjects price test, gates on revenue per visitor rather than conversion, and checks power before reading the result.
---

# Run a pricing experiment with a control

Price tests are easy to run and easy to misread. Measure revenue per visitor, not conversion alone, and keep the arms clean so a lift in transactions that loses money does not look like a win.

## Procedure

1. Assign visitors to a price arm at random, between subjects, and hold the assignment stable for a user across sessions. A user who sees two prices trusts neither.
2. Pick the primary metric: revenue per visitor (RPV). Conversion rate alone is the classic trap; a higher price that converts slightly less can still win on RPV.
3. Compute RPV per arm and the difference:

       ```
       python3 -c "from decimal import Decimal as D; print(D('0.040')*D('20.00'), D('0.034')*D('24.00'))"
       # 0.80 vs 0.816 -> the variant wins on revenue per visitor
       ```

4. Power the test before launch. For a 5% RPV lift at typical variance you need tens of thousands of visitors per arm; a few hundred will not settle it.
5. Pre-register the decision rule: ship, kill or extend, and the minimum lift that clears the noise.
6. Guard against cannibalisation and mix shift. If the arms differ in which products get seen, the RPV difference is a mix, not a price effect.
7. Exclude returning customers from a new-customer test, and never test prices on accounts who already agreed to a fixed rate.
8. Run pricing tests only where it is legal and fair: not on essentials, not on a protected class, and not quietly by geography without a stated reason.
9. Keep prices in integer minor units in both arms; a float price in one arm injects a fractional-cent difference that muddies RPV near the noise floor.
10. Report the result with the arm sizes, the RPV difference and a confidence interval. A point difference with no interval is not a result.

## Pitfalls

- Gating on conversion alone, which makes a revenue-losing price look like a win.
- Testing within subjects, so a user sees both prices.
- Reading an underpowered test as a result.
- Mix shift between arms masquerading as a price effect.
- Testing on existing contracted customers or on protected pricing.
- Float prices in one arm that inject a sub-cent difference.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('0.040')*D('20.00'), D('0.034')*D('24.00'))"
    # 0.80 0.816 -> RPV by arm, the metric that decides
    ```

Pass when the primary metric, power and pre-registered rule are stated before launch. Report RPV per arm, the arm sizes, the difference with an interval, and the pre-registered decision.
