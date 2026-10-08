---
name: model-marketplace-take-rate-and-net
description: Use when a marketplace must be priced or evaluated. Models take rate on gross merchandise value, nets out payment and fraud pass-through, and finds the take rate that covers cost to serve.
---

# Model marketplace take rate and net

Take rate is your cut of gross merchandise value (GMV). The headline rate is not the margin — payment fees, tax, fraud loss and support sit between a 15% take and what you keep.

## Procedure

1. Define GMV precisely: order value before or after discounts, before or after tax and shipping. Pick one and state it.
2. Compute gross take: `gross_take_minor = gmv_minor * take_bp // 10000`. 15% = 1500 bp.
3. Subtract pass-through costs to get net take:
   - payment processing: `gmv * proc_bp // 10000 + fixed_per_order * orders`
   - tax: flows through, not yours
   - fraud/chargeback loss: `gmv * fraud_bp // 10000`
   - support and refund cost.
4. Worked example on 1,000 orders averaging 5,000 minor (GMV 5,000,000):
   - gross take @1500 bp = 750000.
   - processing @290 bp + 30/order = 145000 + 30000 = 175000.
   - fraud @40 bp = 20000; support 2% of GMV = 100000.
   - net take = 750000 - 175000 - 20000 - 100000 = 455000 minor, a 9.1% net take, not 15%.
5. Compute the break-even take: the rate at which net take equals cost to serve (hosting, ops, acquisition). `break_even_bp = cost_minor * 10000 // gmv_minor`.
6. Model two-sided sensitivity: raising take pushes supply off the platform, and a take rise that cuts GMV can lower absolute net take.
7. Keep seller payouts in integer minor units and reconcile them to the payment processor payout; a marketplace is two payout flows, not one.
8. Report net take per GMV and contribution margin after variable cost; never quote gross take alone.

9. Model refund and dispute cost as a take-rate drag: a 2% refund rate at a 9% net take cuts net margin by about a fifth.
10. Segment net take by category; heavy items, low tickets and high-fraud categories carry a different true take.
11. Watch seller concentration: a single seller above 30% of GMV is a take-rate risk, not an asset.
12. Include platform-paid promotions and subsidies in the model as a negative line, not an afterthought.
13. Recompute net take per order size; the fixed processing fee makes small orders structurally thinner.
14. Model the escrow float: holding seller funds between sale and payout earns float but is restricted cash, not revenue.

## Pitfalls

- Quoting a 15% take as margin when payment and fraud eat a third of it.
- Fixed per-order costs (the 30-cent fee) give small orders a much lower net take; blending hides it.
- Letting tax and shipping into GMV inflates the take numerator and the denominator differently.
- A take-rate increase that curtails supply can reduce total net take even though the rate rose.
- Float arithmetic across millions of GMV rows accumulates error; stay in integer minor units.

- Blending net take across categories hides that one category is loss-making after payment and fraud.
- Applying a refund rate to gross take rather than net take overstates how much margin a refund removes.
- Seller concentration above a third of GMV means one seller's exit moves the whole forecast.
- Counting escrow float as revenue overstates the take and ignores the liability to sellers.

## Verification

    python3 -c "gmv=5000000; gt=gmv*1500//10000; proc=gmv*290//10000+30*1000; print(gt, gt-proc-gmv*40//10000-gmv*2//100)"
    # 750000 455000 -> net take $4,550.00, a 9.1% net take on $50,000 GMV

Report: gross take, each pass-through cost, net take and its rate, and the break-even take rate.
