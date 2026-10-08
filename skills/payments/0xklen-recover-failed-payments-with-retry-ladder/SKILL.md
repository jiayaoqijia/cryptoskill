---
name: recover-failed-payments-with-retry-ladder
description: Use when involuntary churn from declined cards is bleeding revenue. Times card retries against paycheck and balance cycles and measures the recovered dollars rather than retrying blindly.
---

# Recover failed payments with a retry ladder

A card decline is usually a timing accident, not a lost customer. Retry on a schedule aligned to paydays, back off the decline, and measure recovered dollars — not attempts.

## Procedure

1. Classify the decline before retrying: `insufficient_funds` and `try_again_later` are soft (retry); `stolen_card`, `lost_card`, `pickup_card` are hard (never retry); `expired_card` retries only after a card-update ping.
2. For soft declines schedule 3-4 retries near salary dates, e.g. day +3, +5, +7 from failure, each at a fixed local hour. Salary cycles mean the 1st and the 15th recover best.
3. Run a card-updater (Visa VAU / Mastercard ABU) before every retry so a reissued card is recovered without customer effort.
4. Compute recovered dollars from the ledger, not the retry log:
   `recovered_minor = sum(amount_minor for charge in attempts where attempt_n > 0 and status == 'succeeded')`.
5. Compute the recovery rate as recovered over failed — `rate = recovered_minor / failed_minor` — and track it per decline reason.
6. Worked example: a month failed 400,000 minor involuntarily; retries recovered 108,000 minor; rate = 27%. A month later, adding the pre-final-retry email lifts recovery to 39% with no extra retries.
7. Give up after the ladder: on final failure, move the account to the dunning/suspension path. Do not retry forever.
8. Cap retries per card BIN per day across the whole book so one bad processor day does not draw a network warning.
9. Report recovered dollars and rate; a lower attempt count with a higher rate is a win, not a regression.

10. Retry the outstanding balance, not the original charge, so a partial recovery is not re-collected in full.
11. Suppress retries during an active support thread so a retry does not land seconds after the "we'll retry" notice.
12. Log every attempt with the decline code and a processor request id so a dispute is answered from evidence.
13. Feed recovered dollars back into MRR the month they land and keep a separate involuntary-churn line so the save rate stays honest.
14. A/B the retry timing (payday versus fixed hour) and keep the variant with the higher recovered dollars, not the higher attempt count.
15. Recompute the recovery rate net of second-order losses: a recovered payment that later chargebacks is not recovered.

## Pitfalls

- Retrying hard declines (`stolen_card`) is network abuse and flags the merchant ID; classify first.
- Timing retries at a fixed daily hour ignores payday cycles and leaves recovery on the table.
- Measuring "retries sent" instead of "dollars recovered" rewards volume over outcome.
- No card-updater means reissued cards are never recovered even though the customer is willing to pay.
- Retrying the same card dozens of times in a month produces duplicate authorisation holds and support tickets.

- Retrying the gross charge after a partial payment double-collects; always retry the residual.
- A retry that fires while a support email is open reads as aggressive and triggers a chargeback.
- Recovered dollars booked as new revenue overstate new business and hide involuntary churn.
- Counting a recovered charge that later chargebacks as a save inflates the rate against reality.

## Verification

    python3 -c "failed=400000; recovered=108000; print(round(recovered/failed*100,1), '%')"
    # 27.0 % recovery -> compare against the prior month and per decline reason

Report: recovered dollars, recovery rate, and the split by decline reason, with the number of attempts used.
