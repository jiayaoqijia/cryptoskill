---
name: match-underpaid-and-overpaid-invoices
description: Use when crypto payments arrive for the wrong amount, split, or batched. Defines tolerance, matching rules, and how to settle the residual without double-crediting.
---

# Match underpaid and overpaid invoices

Crypto payments rarely equal the invoice: exchange fees shave them, rounding adds a unit, one tx pays three invoices. Match on a deliberate tolerance and settle residuals explicitly instead of letting the ledger drift.

## Procedure

1. Set a matching tolerance as a fraction of the invoice (e.g. 0.5%), not an absolute amount, so it scales:
   `python3 -c "print(round(abs(paid-due)/due,5) <= 0.005)"`.
2. Match by the payment reference first: a unique amount or a memo/tag. If neither, match by (from address, time window).
3. Underpaid within tolerance: credit the invoice in full and absorb the shortfall as a fee.
4. Underpaid beyond tolerance: credit the partial amount, leave the invoice open, and invoice the residual — do not mark it paid.
5. Overpaid: credit the invoice and record the surplus as a customer credit; refund only on request to avoid a taxable disposal and gas cost.
6. Batched payment covering N invoices: allocate by invoice order until the amount is exhausted; the last invoice may be partial.
7. Never credit two invoices from one tx unless the amounts sum to the tx value within tolerance.

## Pitfalls

- Matching on amount alone when two customers owe the same amount; always use the reference or sender.
- A 0.5% tolerance is 10 cents on a $20 invoice but $2,500 on $500k of free slippage for the payer; cap tolerance in absolute terms too.
- Crediting a partial payment as full and discovering the shortfall only at reconciliation.
- Refunding tiny surpluses on-chain when gas exceeds the surplus.
- Customer credits accumulate on the balance sheet and must be reconciled, and in some jurisdictions escheated if forgotten.
- A partial match left open can be paid again, resulting in a double payment that looks like an overpayment later.
- Matching by sender breaks when a customer pays from a new or exchange address.
- A memo the customer puts in the wrong slot (amount, comment) silently defeats reference matching.
- Rounding the credited amount to the nearest cent creates drift that compounds against the on-chain sum.

## Verification

    python3 -c "print(round(abs(paid-due)/due,5) <= 0.005)"   # tolerated?
    # settled ledger: sum(matched) + open_residual + customer_credit == sum(received)

Report each payment's match status, the residual, and the total credited versus total received.
