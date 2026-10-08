---
name: calculate-affiliate-and-referral-payouts
description: Use when affiliates or referrers must be paid. Computes commission on net-of-refund revenue with integer minor units and reserves against later refunds and clawbacks.
---

# Calculate affiliate and referral payouts

Commission on gross that later refunds is commission you overpaid. Compute on net-of-refund revenue, hold a clawback reserve, and keep the payout maths in integer minor units.

## Procedure

1. Define the commission base: net revenue actually collected, after refunds, chargebacks and tax, in integer minor units. Gross-of-all is the common trap.
2. Set the rate as basis points so it stays integer: 20% = 2000 bp. `commission_minor = base_minor * rate_bp // 10000`.
3. Handle tiers deliberately: e.g. 2000 bp on the first 100,000 minor per affiliate per month, 1000 bp above. Compute each band separately and sum.
4. Worked example, base 250000 minor at 2000 bp up to 100000 then 1000 bp:
   `100000*2000//10000 + 150000*1000//10000 = 20000 + 15000 = 35000` minor = USD 350.00.
5. Apply a clawback window: hold commission on sales that could still refund. `reserve = commission_minor * refund_rate_estimate`; pay the rest.
6. On a refund inside the window, reverse the matching commission out of the reserve, so a clawback never comes out of a future legitimate payout.
7. Recurring commissions: pay on each renewal's net revenue, but stop on churn. Model expected payout as `commission_per_period * expected_periods`, not lifetime.
8. Cap and fraud-check: flag an affiliate whose conversion rate is a statistical outlier and whose customers share a fingerprint; self-referral is the most common abuse.
9. Report total commission as a customer-acquisition cost line, net of clawbacks, so unit economics include it.

10. Pay on a fixed cadence with a minimum threshold so the payment run cost does not exceed a small affiliate's commission.
11. Store last-click attribution evidence so a disputed commission is resolved with data, not a support argument.
12. Reconcile affiliate payouts to the acquisition-cost line in the ledger so CAC includes them.
13. Claw back on churn inside the warranty window, not just on refund, when the commission is modelled on retention.
14. Detect click fraud (duplicate fingerprints, abnormal click-to-signup) before paying, not after.
15. Publish the commission terms and the clawback window so the maths is auditable by the affiliate.

## Pitfalls

- Paying commission on gross and later eating the refund understates CAC by the refund rate.
- Lifetime-commission promises on a churning product cost more than any single payout shows.
- Float percentages on many small commissions drift; integer bp arithmetic keeps the totals exact.
- No clawback reserve means a refund month turns the programme cash-negative.
- Self-referral and coupon-stacking inflate payouts; cap and flag before paying.

- Paying micro-commissions weekly costs more in transfer fees than the commission itself; batch to a threshold.
- Without stored attribution evidence, a commission dispute becomes a goodwill payment.
- Leaving affiliate payouts out of CAC understates acquisition cost and flatters unit economics.
- Not clawing back on early churn overpays for customers who leave within the warranty window.

## Verification

    python3 -c "b=250000; c=100000*2000//10000+150000*1000//10000; print(c, b-c)"
    # 35000 -> commission $350.00 on $2,500.00 net; a 5% reserve leaves 33250 payable

Report: per-affiliate net base, commission by band, clawback reserve, and the net payable for the period.
