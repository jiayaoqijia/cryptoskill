---
name: reconcile-gateway-payout-to-orders
description: Use when a payment processor's settlement or payout must be proven against your orders. Matches gross charges minus fees, refunds and chargebacks to the bank deposit, penny for penny.
---

# Reconcile a gateway payout to orders

The processor deposits one net figure; your system knows only gross orders. A payout reconciles when `charges - fees - refunds - chargebacks + adjustments = deposit`, every term in the gateway's currency and minor unit.

## Procedure

1. Fix the settlement window from the payout record (`period_start`, `period_end`, currency) and the deposit amount in integer minor units.
2. Pull the gateway's balance-transaction report for that window: one row per charge, refund, fee, chargeback and adjustment, each with its amount and fee in minor units.
3. Classify each row: `charge` (+gross), `fee` (-fee), `refund` (-gross, and the original processing fee is usually not returned), `chargeback` (-gross minus the chargeback penalty fee), `adjustment` (±).
4. Sum each class in integer minor units — never floats, and never across currencies without an FX snapshot (see `snapshot-fx-rates-at-posting-time`).
5. Compute `net = charges - fees - refunds - chargebacks + adjustments` and compare to the deposit. The difference must be 0.
6. Match individual charges to your own orders by the gateway charge id; flag gateway rows with no order (unexpected revenue, test charges) and orders with no gateway row (never captured).
7. Explain any residue: pending-not-yet-paid items, a currency-conversion spread, and reserve/hold balances the gateway withholds from the payout.
8. Record the comparison as a dated reconciliation with both the computed net and the deposit.
9. Reconcile each payout the day the bank confirms it, not the day the gateway initiated it — bank timing differs.
10. Keep the gateway report file itself (and a hash of it) as the evidence behind the reconciliation.
11. Store the gateway's `balance_transaction_id` on your ledger entry so a re-run is idempotent.
12. Investigate any residue larger than a few minor units before closing; small residues are fees, large ones are bugs.

## Pitfalls

- Fees are charged per transaction and are genuinely `amount * rate` rounded; summing a "monthly fee estimate" instead of the per-row fees never matches.
- Refunds do not restore the original processing fee unless the gateway says they do; assuming they do shows a phantom shortfall.
- Chargebacks carry a separate penalty fee (often $15–$25) that is easy to omit.
- Gateway reports are per payout, not per calendar month; a charge that settles next period lands in the wrong window.
- Multi-currency accounts net each currency separately; summing raw minor units across currencies is meaningless.
- A currency adjustment row in the report is not a fee; misclassifying it double-counts and breaks the net.

## Verification

    python3 -c "charges=1000000; fees=29000; refunds=50000; cb=15000+2500; print(charges-fees-refunds-cb)"   # must equal the deposit in minor units
    # compare against the payout record's net amount

Pass when the computed net equals the deposit exactly. Report the window, the deposit, and the class subtotals with the zero difference.
