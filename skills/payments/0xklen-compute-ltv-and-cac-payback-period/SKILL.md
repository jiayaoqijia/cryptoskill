---
name: compute-ltv-and-cac-payback-period
description: Use when judging whether customer acquisition pays. Computes LTV from gross profit and churn, the CAC payback period, and the LTV:CAC ratio that gates spending, for the newest cohort rather than a blend.
---

# Compute LTV and CAC payback period

LTV and payback answer different questions: how much a customer is worth, and how long until they have paid back their cost. Both must be right before you scale spend.

## Procedure

1. Use gross profit per customer, not revenue. A $100 MRR customer at 80% gross margin contributes $80 a month.
2. Estimate average customer lifetime. For a monthly churn rate c, lifetime is 1/c. At 2% monthly churn the expected lifetime is 50 months.
3. Compute LTV = gross profit per month * lifetime.

       ```
       python3 -c "from decimal import Decimal as D; print(D('80')/(D('0.02')))"
       # 4000 -> $4,000 LTV at $80 gross profit and 2% monthly churn
       ```

4. Compute payback = CAC / monthly gross profit. A $600 CAC against $80/month is 7.5 months.
5. Set the gate: LTV:CAC >= 3 and payback <= 12 months is a common floor; tighten payback when cash is tight, since payback, not LTV, is what the bank balance feels.
6. Treat churn as the dominant variable. Halving churn to 1% doubles lifetime and LTV, while halving CAC only gets you halfway to the same ratio.
7. Use contracted revenue for committed contracts and realised retention for the rest; do not count an unseen renewal as lifetime.
8. Compute the ratio for a cohort, not the whole base. Old cheap-acquired cohorts flatter the blend; the newest cohort's payback is the live number.
9. Keep cash-flow inputs in integer minor units so payback is computed from exact cents; a float CAC drifts payback across a month boundary.
10. Recompute whenever churn or CAC moves 20%, because the ratio is a product and both terms move together.

## Pitfalls

- Using revenue instead of gross profit, inflating LTV by the cost of delivery.
- Assuming a lifetime the retention data does not support.
- Quoting a blended LTV:CAC that old cohorts prop up.
- Watching only LTV and ignoring payback, which is the actual cash constraint.
- Treating churn as a constant when it falls with cohort age, which is survivorship bias.
- Float CAC that moves payback across a month boundary.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('80')/D('0.02'), D('600')/D('80'))"
    # 4000 7.5 -> $4,000 LTV, 7.5-month payback
    ```

Pass when LTV, payback and the ratio are reported for a named cohort. Report LTV, payback in months, and the LTV:CAC ratio for the newest cohort, not the blend.
