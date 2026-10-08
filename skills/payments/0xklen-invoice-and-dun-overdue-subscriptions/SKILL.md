---
name: invoice-and-dun-overdue-subscriptions
description: Use when a subscription invoice goes past its due date. Runs a staged dunning ladder keyed to days-past-due so retries, emails and suspension fire on schedule instead of by ad-hoc chasing.
---

# Invoice and dun overdue subscriptions

Dunning is a schedule, not a mood. Compute every action from the invoice's due date and days-past-due (DPD); never decide "who to chase" by hand, because a hand-picked list is inconsistent and unauditable.

## Procedure

1. Store the invoice `due_date` and the amount in integer minor units, e.g. `amount_minor = 4900` for USD 49.00. Never store 49.00 in a binary float.
2. Compute DPD in whole days between `due_date` and today in the customer's billing timezone:
   `dpd = (as_of_date - due_date).days`.
3. Define one ladder and apply it identically to every account. A workable default:
   - DPD 0: invoice issued, email "payment due".
   - DPD 1: first retry against the saved payment method.
   - DPD 3: retry #2, email "payment failed, card on file".
   - DPD 7: retry #3, email "final notice, access ends in 7 days".
   - DPD 14: suspend access, keep the invoice open.
   - DPD 30: mark uncollectible, hand to recovery.
4. Run the ladder as a daily job over a state table, not a running list. Each row carries `current_dpd`; the job looks up the rung's action and records it once (idempotency key = `invoice_id + rung`).
5. Stop the whole ladder the moment `paid_minor >= amount_minor`, including a partial payment that covers the balance.
6. Route a partial payment (`residual = amount_minor - paid_minor > 0`) to its own branch: chase the residual, do not run the full suspension ladder.
7. On success set `paid_at` and halt. On permanent failure codes (stolen, closed account) skip retries and jump to the DPD 7 notice.
8. Log every send and attempt so a dispute ("I was never told") is answered from data, not memory.

9. Keep `pause` distinct from `suspend`: a customer on a payment plan has access but a frozen ladder, so they are not suspended by accident.
10. Time the send-hour in the customer's timezone but store every timestamp in UTC; the local hour is a display concern.
11. Emit a metric per rung (sends, opens, conversions) so the DPD 7 email's effect on recovery is measured, not assumed.
12. Keep the account recoverable after uncollectible: paying the balance later reactivates it without a new signup.
13. Cap the ladder at a defined maximum DPD; beyond it, route to collections or write-off rather than looping forever.
14. Test the ladder with a synthetic invoice that never pays and one that pays at DPD 2, asserting no further rungs fire.

## Pitfalls

- Querying "unpaid invoices older than X" each day double-sends when the job reruns; the rung-keyed idempotency key prevents it.
- Suspending at DPD 14 without the DPD 7 final notice trades a save for a churn; the warning rung must fire or the ladder is incomplete.
- Comparing `due_date` to a UTC `now()` shifts DPD by a day for customers west of UTC; use their billing timezone.
- Retrying a hard-decline card nightly invites card-network flags on the MID; classify decline codes and stop on permanent ones.
- Float dollars in the condition (`paid < 49.00`) miss the cent that matters; compare `paid_minor < amount_minor`.

- A pause state that shares the suspend code path freezes access and the restart re-fires the whole ladder at once; give pause its own branch.
- Sending from a shared "billing@" that lands in spam means the DPD 7 warning never arrives and the suspension reads as a surprise.
- Deleting the invoice after write-off destroys the audit trail; mark it uncollectible, do not delete.
- A ladder with no maximum DPD loops a written-off invoice forever and inflates the open-AR number.

## Verification

    python3 -c "from datetime import date; print((date(2026,3,15)-date(2026,3,1)).days)"
    # 14 -> the suspension rung; confirm exactly one suspension event logged per invoice_id

Report: for a sample of suspended invoices, the DPD at suspension and the count of distinct ladder events per invoice, e.g. "all 20 suspended at DPD 14, six rungs each, no reruns."
