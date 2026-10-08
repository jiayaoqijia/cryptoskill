---
name: match-deposits-to-invoices-at-fixed-cutoff
description: Use when bank deposits must be matched to issued invoices. Fixes a cut-off, matches each deposit to invoices by reference and amount, and lists the unmatched on both sides.
---

# Match deposits to invoices at a fixed cut-off

Bank money and invoice records disagree at the edges: a wire lands a day late, an ACH batch covers three invoices, a partial payment leaves a balance. Cut off the period, match to the minor unit, and list what is left on each side.

## Procedure

1. Fix the cut-off date and time; deposits and invoices after it belong to the next period and must not be pulled into this one.
2. Normalise both sides to integer minor units in a single currency; convert foreign invoices at the rate recorded on the invoice, not today's rate.
3. Match in three passes: **exact** (amount plus reference or memo), **exact amount, fuzzy reference** (same payer, same amount), then **many-to-one** (one deposit covering several invoices — sum candidate invoices and compare).
4. For each deposit, the matched invoice total must equal the deposit to the minor unit. A leftover means a fee deducted in transit, a partial payment, or a real mismatch.
5. Record unmatched deposits (money in with no invoice — unidentified) and unmatched invoices (issued, unpaid, or paid on a channel not yet imported).
6. Explain every residual: bank fee, FX spread, early-payment discount, or a short-pay the customer wrote off.
7. Output the three lists with counts and totals; only `matched` plus a fully-explained residual closes the period.
8. Re-run at the next cut-off; a residual that persists across two runs is a real break.
9. Load both sides into the same integer type; a CSV deposit in dollars and an invoice in cents is a scale mismatch before it is a match problem.
10. Record the matching-rule version, so a re-run after a rule change does not silently reclassify prior matches.
11. For a partial payment, split the invoice into paid and open amounts rather than dropping the difference.
12. Schedule the run after the bank's cut-off time, not before the day's last posting.

## Pitfalls

- Matching on amount alone mis-associates two customers who paid the same round number; use the reference and the payer.
- Comparing raw minor units across currencies (a EUR invoice against a USD deposit) without the invoice's FX rate is meaningless.
- Ignoring transit fees: a $1,000 invoice paid by a $999.50 deposit is not a mismatch if the $0.50 is a wire fee — record it as such.
- Treating a customer credit or an overpayment as a match hides a real shortfall elsewhere.
- Batch ACH deposits covering several invoices fail one-to-one matching; the many-to-one pass is mandatory.
- Summing with floats drifts over thousands of rows; use integer minor units.
- An overpayment leaves a credit balance the customer will apply later; track it as a liability, not as an unexplained residual.

## Verification

    python3 -c "inv=[10000,20000]; dep=30000; print(sum(inv)-dep)"   # 0 when matched
    # matched_total + unexplained_residual == deposits_total

Report the cut-off, matched/unmatched counts and totals, and each residual with its cause.
