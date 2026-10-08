---
name: prorate-a-subscription-plan-change
description: Use when a subscriber upgrades, downgrades or changes billing period mid-cycle. Computes the proration credit and charge in exact minor units and names which of the two common conventions applies.
---

# Prorate a subscription plan change

Proration means charging for the days on the new plan and crediting the unused days on the old one. Do the arithmetic in integer minor units and name the convention, because the two conventions disagree by up to a full period.

## Procedure

1. Pick the convention and write it down:
   - **Unused-time credit** (Stripe-style): credit the old plan for days not used, charge the new plan for days remaining.
   - **Foregone-time** (some legacy billers): keep the old period's charge whole and switch at the next renewal. No credit, no charge.
2. Establish the period in whole days: `term_days`, `used_days`, `remaining_days = term_days - used_days`.
3. Prorate with integer division, flooring the credit in the customer's favour:
   `credit_minor = old_amount_minor * remaining_days // term_days`.
   `charge_minor = new_amount_minor * remaining_days // term_days`.
4. Compute the net due: `net_minor = charge_minor - credit_minor`. Positive is an immediate charge; negative is an account credit or a small refund.
5. Worked example, monthly term of 30 days, day 10 used (remaining 20):
   - old plan USD 29.00 = 2900 minor; credit = 2900*20//30 = 1933.
   - new plan USD 99.00 = 9900 minor; charge = 9900*20//30 = 6600.
   - net = 6600 - 1933 = 4667 minor = USD 46.67 due now.
6. On a downgrade the net is usually negative; carry it as an account credit rather than cash, unless the account closes.
7. Keep the period anchor fixed on upgrades: the next renewal stays on the original day so the customer does not get a shortened period.
8. Post the credit and the charge as two ledger lines, not one netted line, so revenue recognition can split them.

9. On an annual-to-monthly switch, convert both sides to a daily rate before prorating so term lengths compare correctly.
10. Round consistently — floor the customer's credit and the charge alike — so support cannot cherry-pick the direction.
11. Store the proration as an immutable event carrying term_days and remaining_days, so a dispute is reconstructible.
12. Handle a mid-cycle downgrade-plus-upgrade in one transaction only if the period anchor is unchanged; otherwise post two events.
13. Recompute proration only from stored dates, never from "today", so the amount does not drift daily.
14. Reconcile the sum of proration events for the period to the invoice total; a mismatch is a missed event.

## Pitfalls

- Using a 30-day denominator for a 28/29/31-day month shifts the result; use the actual `term_days` of that period.
- Float division (`2900*20/30 = 1933.333`) leaks fractions of a cent; integer `//` floors exactly.
- A mid-cycle upgrade that also resets the period anchor silently shortens the paid month.
- Netting credit and charge into one line loses the audit trail and breaks any per-plan revenue report.
- Applying foregone-time on a downgrade while claiming unused-time on an upgrade is inconsistent and looks like double-billing.

- Mixing annual and monthly amounts without a common daily rate inflates one leg and misprices the switch.
- Rounding credit up and charge down in different code paths produces a cent the customer eventually finds.
- Recomputing the proration on every page load from today's date makes the amount drift daily.
- A downgrade-plus-upgrade that resets the anchor can silently hand the customer a longer period.

## Verification

    python3 -c "old=2900;new=9900;term=30;rem=20;print(old*rem//term, new*rem//term, new*rem//term-old*rem//term)"
    # 1933 6600 4667 -> credit 19.33, charge 66.00, net 46.67 due

Report: the convention chosen, term_days, and the net due in minor units for one worked change.
