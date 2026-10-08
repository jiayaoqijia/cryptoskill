---
name: measure-land-and-expand-net-revenue-retention
description: Use when a business claims land-and-expand economics. Builds NRR and GRR from a revenue bridge and checks that expansion is real growth, not reclassification of price rises.
---

# Measure land-and-expand net revenue retention

Land-and-expand is a claim about existing accounts growing. Net revenue retention is the number that tests it, so long as you build it from a revenue bridge and not from a headline.

## Procedure

1. Build the bridge for one cohort over one period: starting MRR, expansion, contraction, churn, and ending MRR.
2. Compute NRR = (start + expansion - contraction - churn) / start, from the same cohort so new logos do not pollute it.
3. Worked: start $100,000, expansion $18,000, contraction $4,000, churn $9,000, ending $105,000. NRR = 105,000/100,000 = 105%.

       ```
       python3 -c "from decimal import Decimal as D; print(D('105000')/D('100000'), D('87000')/D('100000'))"
       # 1.05 0.87
       ```

4. Compute GRR the same way without expansion: (100,000 - 4,000 - 9,000)/100,000 = 87%. GRR is the leak; NRR is the pump. Report both.
5. Check the expansion source. Seat growth, usage overage and upgrades are real expansion; a price rise is re-pricing, not expansion.
6. Look at the land-to-expand path per cohort: median time from $5k ACV to $15k ACV, and the share that ever expand at all. Use the median; one whale distorts a mean.
7. Segment by landing size. Small lands that expand fast are the thesis; large lands that never move weaken it.
8. Keep the bridge in integer minor units so the four components sum exactly to the ending MRR; a float bridge will not tie to the ledger.
9. Reconcile the bridge to finance's MRR movement report every period; a retention figure that does not tie out is worse than none.
10. Flag negative-NRR cohorts early. Under 100% means expansion no longer covers churn and the model is running backwards.

## Pitfalls

- Computing NRR including new logos, which turns retention into a growth number.
- Calling a price rise "expansion" and inflating NRR.
- Reporting NRR without GRR, hiding the churn underneath.
- Using a mean expansion figure that one whale distorts.
- Mixing cohorts across acquisition dates, so the comparison is not like for like.
- A float bridge that will not sum to the ending MRR.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('105000')/D('100000'), D('87000')/D('100000'))"
    # 1.05 0.87 -> NRR 105%, GRR 87% for the same cohort
    ```

Pass when the bridge components sum to the ending MRR. Report NRR, GRR, the expansion source, and confirmation the bridge ties to the ledger.
