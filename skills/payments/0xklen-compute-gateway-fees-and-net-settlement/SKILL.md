---
name: compute-gateway-fees-and-net-settlement
description: Use when pricing must survive processor fees. Computes net settlement per transaction from percentage-plus-fixed fees with integer basis points and finds the break-even ticket.
---

# Compute gateway fees and net settlement

2.9% + $0.30 is not 2.9%. On a $5 charge the fixed fee dominates and net is $4.56 — 91% of gross. Every unit-economic model must compute net, in integer minor units.

## Procedure

1. Get the real rate from a settlement statement, not a website. Rates vary by card type, region and interchange; keep at least a blended rate and a worst-case rate.
2. Express the percentage as basis points to keep integer maths: 2.9% = 290 bp. The fixed fee is `fixed_minor = 30`.
3. Compute the fee on a charge: `fee_minor = amount_minor * fee_bp // 10000 + fixed_minor`. Floor the multiplication so you never over-charge the fee.
4. Compute net: `net_minor = amount_minor - fee_minor`.
5. Worked example, blended 290 bp + 30:
   - $5.00 = 500 minor: fee = 500*290//10000 + 30 = 14 + 30 = 44; net = 456.
   - $100.00 = 10000 minor: fee = 290 + 30 = 320; net = 9680.
   - effective rate on $5 = 44/500 = 8.8%; on $100 = 3.2%.
6. Find the break-even ticket where the fixed fee is 1% of gross: `fixed_minor / 0.01 = 3000` minor = $30. Below $30 the fixed fee exceeds 1%.
7. For international or Amex cards, re-run with their bp and a cross-border markup so the model is not optimistic.
8. Net settlements, not gross revenue, feed contribution margin. State which rate a model used.
9. Model refunds: the original fee is usually retained, so a refund costs the fee again unless a fee-return policy applies.

10. Recompute unit economics per SKU; a low-ticket SKU can be net-negative and should be surfaced, not hidden in a blend.
11. Track the blended effective rate monthly; a creeping rate is a silent margin leak even at flat volume.
12. Include chargeback fees and refund-fee retention when estimating the true take rate.
13. Model a fee change: a 20 bp raise on 10,000,000 minor of monthly volume is 20,000 minor of margin.
14. Compare processors on net settlement for your actual ticket mix, not on headline rate.
15. Store the rate schedule with a start date so historical reconciliations use the rate that applied then.

## Pitfalls

- Quoting gross revenue as if it were collected; the processor takes its cut before the deposit.
- Using the advertised 2.9% when the statement shows 3.4% before interchange plus markup.
- Float division of the fee drifts across millions of rows; integer bp arithmetic does not.
- Ignoring chargeback fees and refund-fee retention understates the true take rate.
- Applying one blended rate to a subscription and a one-off hides that small tickets are unprofitable.

- A low-ticket SKU can be net-negative after the fixed fee and still show "revenue" on the dashboard.
- Never re-auditing the rate after a plan change means the model prices with a stale fee.
- Comparing processors on headline rate ignores the fixed fee that dominates small tickets.
- Applying today's rate to last quarter's reconciliation silently restates history.

## Verification

    python3 -c "for a in (500,2000,10000): print(a, a*290//10000+30, a-(a*290//10000+30))"
    # 500 44 456 / 2000 88 1912 / 10000 320 9680 -> net rises slower than gross on small tickets

Report: the rate used (bp + fixed), net settlement on the smallest and largest ticket, and the effective rate at each.
