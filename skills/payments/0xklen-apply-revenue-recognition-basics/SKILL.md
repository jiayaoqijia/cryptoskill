---
name: apply-revenue-recognition-basics
description: Use when cash received is not the same as revenue earned. Recognises subscription and prepaid revenue over the service period instead of at the payment date, in integer minor units.
---

# Apply revenue recognition basics

A prepaid annual plan is cash in January and revenue spread over twelve months. Booking the whole payment as January revenue lies to every downstream number, so recognise it over the period it was earned.

## Procedure

1. Separate the events: **cash** (collected), **deferred revenue** (a liability you owe as service), and **recognised revenue** (earned). A payment creates the first two, not the third.
2. On an annual prepay of USD 1,200.00 = 120000 minor on 2026-01-01, record day one: cash +120000, deferred revenue +120000, recognised revenue 0.
3. Recognise on a schedule. Straight-line monthly over 12 months: `monthly_minor = 120000 // 12 = 10000`.
4. Book a month-end entry: deferred revenue -10000, recognised revenue +10000. After three months recognised = 30000, deferred = 90000.
5. Follow delivery, not the calendar, when the obligation is not uniform: recognition follows performance. A one-off onboarding fee is recognised when delivered, not over the term.
6. On a mid-term cancellation, recognise the earned portion and refund the unearned deferred balance `refund_minor = deferred_remaining`. Never refund money already recognised.
7. Track the deferred balance as the unearned portion of all open contracts; it must reconcile to the schedule, not to the bank balance.
8. Keep tax separate: sales tax collected is a liability, never enters the recognition schedule.

9. Handle a mid-term plan change by splitting the period: recognise the old plan to the change date and the new plan after.
10. Keep a deferred-revenue roll-forward by contract that sums to the balance-sheet deferred total each month.
11. Recognise usage-based revenue when the usage is delivered, not when the invoice issues; the dates differ.
12. For a bundled offering, allocate the transaction price across performance obligations and recognise each on its own schedule.
13. Treat a non-refundable setup or onboarding fee as recognised on delivery, not spread over the term.
14. Reconcile cash to recognition: cash minus the deferred delta over the period should equal recognised revenue plus tax remitted.
15. Disclose the recognition policy alongside the schedule so a reader can reproduce the monthly figure.

## Pitfalls

- Recognising a whole annual payment in the month it lands inflates one month and depresses the next eleven.
- Treating deferred revenue as profit: it is a liability until delivered, and spending it early is spending money you owe.
- Refunding out of recognised revenue shorts a period already booked; refund the unearned deferred balance.
- Mixing collected sales tax into revenue overstates both revenue and profit.
- A cancellation that writes off the whole contract ignores the months already delivered.

- A mid-term plan change recognised entirely on the new plan overstates one period and understates the old.
- A roll-forward that does not tie to the balance sheet means some contract is recognised twice or not at all.
- Recognising usage at invoice date with a lag shifts revenue between months and breaks comparability.
- Spreading a non-refundable setup fee over the term understates the month it was earned and distorts early cohorts.

## Verification

    python3 -c "total=120000; per=total//12; print(per, per*3, total-per*3)"
    # 10000 30000 90000 -> monthly recognised 10000, deferred after 3 months 90000

Report: for the month, recognised revenue, closing deferred balance, and proof that deferred opens + additions - recognitions = closing.
