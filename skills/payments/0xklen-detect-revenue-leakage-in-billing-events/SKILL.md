---
name: detect-revenue-leakage-in-billing-events
description: Use when revenue should be higher than it is. Audits billing events for missed invoices, uncaptured usage, stale discounts still applied, and downgrades that never took effect.
---

# Detect revenue leakage in billing events

Leakage is revenue you earned but never billed or never collected. It hides in missing events, stale discounts and failed downgrades, and it is found by comparing what should have happened to what did.

## Procedure

1. Enumerate the leak classes and their detectors:
   - **missed invoice**: an active subscription with no invoice in a period where one is due.
   - **uncaptured usage**: metered units recorded after the billing cutoff and never rolled into an invoice.
   - **stale discount**: a coupon or trial with an `expires_at` in the past still reducing the charge.
   - **failed downgrade**: a downgrade requested but the charge still at the old amount.
   - **unbilled overage**: usage above the tier with no overage line.
2. Query each class as a delta between expected and actual in integer minor units.
3. Worked example, stale discount: 84 subscriptions still discounted 2500 minor each after expiry:
   `leak = 84 * 2500 = 210000` minor = USD 2,100.00 per month, compounding every month it stays broken.
4. Compute total leakage as the sum of the found deltas, then annualise `monthly_leak * 12` to size the fix.
5. Rank by size and by fix cost; a one-line coupon-expiry check beats a manual sweep.
6. For missed invoices, inspect the subscription state machine: a paused/reactivated transition that skipped invoice generation is the usual cause.
7. Add a reconciliation guard: at month-end assert `count(invoiced_subs) == count(active_subs)` and alert on the gap.
8. Fix forward and recover: back-bill where the contract allows; where it does not, book the write-off so the leakage is visible rather than silent.
9. Report leakage by class and the annualised total before and after the fix.

10. Check dunning suppression: a failed payment suppressed to avoid over-emailing can silence billing entirely for an account.
11. Alert when a subscription's charge drops month over month with no matching downgrade event; that is a silent discount or an error.
12. Reconcile metered usage against the plan entitlement to catch usage never captured.
13. Recompute expected invoice totals from contract terms and diff against issued invoices each month.
14. Log the fix and the recovered dollars so leakage reduction is measured, not asserted.
15. Re-run the detector after the fix and confirm the class is empty.

## Pitfalls

- A stale discount is invisible in net MRR because it just makes each charge smaller; only an expected-vs-actual delta finds it.
- Usage recorded after the billing cutoff is dropped silently; a late-watermark check catches it.
- Paused subscriptions that fail to reactivate keep billing at zero; the state machine must emit an invoice on resume.
- Back-billing without a contract clause damages trust and can be legally unenforceable.
- Fixing the cash leak but not the reporting one leaves leakage invisible next quarter.

- Over-aggressive communication suppression quietly stops invoices for a whole segment.
- A month-over-month charge drop with no downgrade event is leakage by another name.
- Verifying a fix by anecdote rather than re-running the detector leaves the class still open.
- Metered usage never reconciled to entitlement hides lost billable units indefinitely.

## Verification

    python3 -c "print(84*2500, 84*2500*12)"
    # 210000 2520000 -> a $2,100.00/mo leak, $25,200.00 annualised

Report: leakage by class in minor units, the annualised total, the reconciliation guard added, and the before/after month-end assertion result.
