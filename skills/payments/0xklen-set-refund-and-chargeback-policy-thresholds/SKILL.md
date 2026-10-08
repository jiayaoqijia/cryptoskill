---
name: set-refund-and-chargeback-policy-thresholds
description: Use when defining when money is given back. Sets refund windows and authority thresholds tied to cost, and treats a chargeback as a processor evidence task with a deadline, not a refund.
---

# Set refund and chargeback policy thresholds

A refund is your choice and your cost; a chargeback is the customer's choice, your fee, and a fight you win or lose on evidence with a hard deadline. The policy must name both, with numbers.

## Procedure

1. Set the refund window in days from the charge date, e.g. 30 days self-serve, 14 for a consumed digital good. Past the window, refunds need a named exception path.
2. Decide refund authority by amount tier: auto-approve under `threshold_minor = 2000` (USD 20), human review 2000-50000, manager above 50000. Keep every amount in integer minor units.
3. Compute the true cost before granting: `cost_minor = amount_minor + gateway_kept_fee_minor`. Processors typically do not return the original transaction fee, so a "full refund" still costs the 2.9% + $0.30.
4. For digital goods on partial use, pro-rate by unelapsed days: `refund_minor = amount_minor * remaining_days // term_days`.
5. Treat a chargeback as a separate workflow: it arrives with a `respond_by` deadline (often 7-14 days). Missing it is an automatic loss.
6. Assemble evidence per chargeback: order record, IP and device, delivery proof, customer communication, and the accepted terms at purchase.
7. Track the chargeback ratio `cb_ratio = chargebacks / transactions` per month. Networks watch this; above roughly 0.9% risks a monitoring program.
8. Reconcile refunds and chargebacks against the settlement report monthly so both hit the ledger as negative revenue, never as an unbooked adjustment.

9. Name the owner: support auto-refunds under the threshold, finance reviews above it, and both write the reason to the ledger.
10. For a cancel-and-refund, pro-rate from the cancellation date, not the request date, when the contract allows forward cancellation only.
11. Trend a monthly refund rate by product; a spike is a quality signal before it is a cost signal.
12. Refund to the original tender; refunding a different card or account is a laundering vector, not a courtesy.
13. Reconcile refunds to the settlement report line, not a separate spreadsheet, so the reversal carries the same currency.
14. Keep a make-good policy for an outage: a credit is cheaper than a cash refund and stays in the billing system.
15. Set a monthly refund-rate alarm; a jump beyond a set band triggers a review before the quarter's recognition closes.

## Pitfalls

- Treating a chargeback as a refund and not responding: you pay the amount plus the chargeback fee and lose by default.
- Forgetting the retained processing fee: refunding a $49 charge made at 2.9% + $0.30 still costs about $1.72 that does not come back.
- A refund window longer than the dispute window invites a double payout if the customer also disputes.
- Auto-refunding above the threshold tier without review is a fraud vector; the tier exists to stop it.
- Tracking refunds in a spreadsheet apart from the ledger hides them from revenue recognition.

- Refunding to a different card or account than the original is a laundering vector; refund the tender.
- A refund rate trended month over month catches a product defect earlier than a growing support backlog.
- Issuing store credit instead of cash without saying so on the policy page invites disputes.
- Make-good credits applied as cash refunds leak margin; keep them as credits unless the customer closes the account.

## Verification

    python3 -c "amt=4900; fee=amt*290//10000+30; print(amt+fee)"
    # 5072 -> the customer gets 4900, you are out 5072 minor

Report: the refund-window days, the authority thresholds, and this month's chargeback ratio read from the processor's dispute report.
