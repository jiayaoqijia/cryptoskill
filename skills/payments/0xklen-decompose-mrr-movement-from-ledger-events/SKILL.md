---
name: decompose-mrr-movement-from-ledger-events
description: Use when MRR moved and no one can say why. Reconstructs new, expansion, contraction and churn from ledger events so the movement reconciles to closing MRR and to net revenue retention.
---

# Decompose MRR movement from ledger events

A single net MRR number hides four different stories. Rebuild MRR from the events that changed it — new, expansion, contraction, churn — and prove they sum to the closing balance.

## Procedure

1. Define MRR: normalised monthly recurring revenue of active subscriptions, in integer minor units, at a fixed as-of date. Exclude one-off and usage overage unless it is contracted recurring.
2. Take a snapshot at the start and end of the period and put every subscription's change in exactly one bucket:
   - **new**: 0 -> positive MRR
   - **expansion**: MRR increased
   - **contraction**: MRR decreased but stayed > 0
   - **churn**: positive -> 0
   - **reactivation**: 0 -> positive from a previously churned account (report separately or fold into new, but state which).
3. Reconcile: `end_mrr = start_mrr + new + reactivation + expansion - contraction - churn`.
4. Worked example (minor units): start 8,000,000; new 900,000; expansion 220,000; contraction 140,000; churn 610,000.
   - end = 8000000 + 900000 + 220000 - 140000 - 610000 = 8,370,000, a net change of +370,000 or +4.6%.
5. Compute net revenue retention: `nrr = (start + expansion - contraction - churn) / start = (8000000+220000-140000-610000)/8000000 = 93.4%`; gross churn alone is 7.6%.
6. Split churn by involuntary (card failure) and voluntary; they route to different teams.
7. Tie the start MRR to last month's closing MRR exactly — an opening that does not equal the prior close means a restatement or a bug.
8. Do it monthly and keep the decomposition table; one month is noise, a trend is signal.

9. Normalise annual plans to monthly (`annual_minor // 12`) and store the normalisation so the figure is reproducible.
10. Report the quick ratio `(new + expansion) / (contraction + churn)`; below 1.0 the book is shrinking even if net MRR rose.
11. Tag each movement event with its subscription id so any bucket can be drilled to the accounts behind it.
12. Recompute the opening MRR from the same ledger events, so the opening equals last month's close by construction.
13. Handle mid-month starts by normalising to a full month so a partial first month does not enter MRR.
14. Separate committed from usage-based MRR and report both, since mixing them makes movement unexplained.

## Pitfalls

- Reporting only net MRR change; +4.6% net hides 7.6% churn the company must out-run every month.
- Counting a downgrade as churn when the account is still paying; contraction is not churn.
- Reactivations folded into "new" flatter the sales team's number.
- Mid-month proration leaking into the MRR snapshot without normalisation makes MRR jitter with the calendar.
- An opening MRR that does not match the prior close leaves the whole decomposition unverifiable.

- Leaving annual plans at their full amount in MRR inflates the number by 12x for those accounts.
- A quick ratio below 1.0 with positive net MRR means a one-off burst is masking underlying decay.
- Untagged movement events cannot be reconciled to accounts and the decomposition becomes unproven.
- A partial first month entering MRR makes the month churn with the calendar.

## Verification

    python3 -c "s=8000000; print(s+900000+220000-140000-610000, round((s+220000-140000-610000)/s*100,1))"
    # 8370000 93.4 -> closing MRR 8,370,000, NRR 93.4%

Report: the four-bucket decomposition table, the reconciliation to closing MRR, the NRR, and the involuntary vs voluntary churn split.
