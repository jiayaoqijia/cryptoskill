---
name: reconcile-processor-payout-to-booked-revenue
description: Use when the processor payout lands and must tie back to the books. Reconciles gross charges, fees, refunds and chargebacks from the payout report to booked revenue to the cent.
---

# Reconcile processor payout to booked revenue

The bank deposit is net; your books are gross. The gap is fees, refunds, chargebacks and timing — every cent must be explained or the revenue figure is unproven.

## Procedure

1. Pull the processor payout report for the period and the bank credit. The credit equals `gross - fees - refunds - chargebacks - reserves`.
2. Pull your own booked revenue for the same period: the sum of successful charges in integer minor units.
3. Write the identity to prove:
   `payout_minor = gross_minor - processor_fee_minor - refund_minor - chargeback_minor - chargeback_fee_minor - reserve_held_minor + reserve_released_minor`.
4. Compare gross charges processor-side to books-side. Differences are usually timing (a charge authorised late on the last day) or a void/refund not yet booked: `timing_gap = books_gross - processor_gross`.
5. Worked example, minor units: gross 1,000,000; fee 30,100; refunds 12,000; chargebacks 5,000; cb fee 1,500; reserve held 0.
   - expected payout = 1000000 - 30100 - 12000 - 5000 - 1500 = 951400 minor = USD 9,514.00.
6. Tie to the bank: if the credit is 951400 it reconciles exactly; if not, find the missing line before booking.
7. Classify every residual: known-timing (carry forward), error (fix the ledger), or unknown (investigate). Never leave an unexplained residual as a rounding plug.
8. Roll reserves: a rolling reserve is your money held by the processor; track it as an asset, not an expense, and reconcile releases.
9. Run the reconciliation monthly and store the tie-out so an auditor can re-derive it.

10. Store the payout report line ids beside the ledger entries so the tie-out is reproducible without re-downloading.
11. Reconcile the processor's stated fee to the fee you compute from the rate; a divergence means the rate changed mid-month.
12. Split net settlement by currency; a multi-currency payout mixes FX and fees and hides both.
13. Handle refunds that settle in a later period as an explicit carry-forward, not as a plug in the current one.
14. Reconcile the reserve balance to the processor's reserve statement monthly, since it is an asset on your books.
15. Keep the tie-out signed and dated by the reconciler so the audit trail has an owner.

## Pitfalls

- Booking the net payout as revenue understates revenue and hides the fee expense.
- A "rounding" plug of a few cents is usually an unbooked chargeback fee, not rounding.
- Ignoring timing gaps and forcing the periods to match creates false breaks next month.
- Treating a reserve as a cost writes off money you will get back.
- Reconciling by the summary total while refunds sit in a different report misses the refund row entirely.

- Re-downloading a new payout report each month with different ids loses the audit link to last month's ledger.
- Trusting a computed fee over the processor's stated fee hides a rate change until the margin looks wrong.
- Blending currencies in one payout total hides FX loss and double-counts fees.
- A refund settling next period booked as a current plug creates a false break next month.

## Verification

    python3 -c "g=1000000;fee=30100;r=12000;cb=5000;cbf=1500;print(g-fee-r-cb-cbf)"
    # 951400 -> must equal the bank credit; any difference is an unclassified line

Report: the payout tie-out bottom line against the bank credit, and the count of unexplained residual lines (target: zero).
