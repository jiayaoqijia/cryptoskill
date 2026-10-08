---
name: convert-trial-to-paid-with-paywall-timing
description: Use when a free trial is not converting to paid. Sets trial length and paywall trigger from activation data and measures trial-to-paid on the correct denominator of trials started.
---

# Convert a trial to paid with paywall timing

A trial is a lead with a deadline. The length and the moment you ask for the card decide conversion more than any email — and the rate is only trustworthy if the denominator is trials started, not trials that finished.

## Procedure

1. Define the funnel rungs precisely: trial_start -> activated (first real use) -> trial_engaged -> trial_end -> paid. Each rung is an event with a timestamp.
2. Choose trial length from time-to-value: find the median days-to-activation, then set the trial at 1.5-2x it. A 3-day trial for a product with 10-day time-to-value mostly measures impatience.
3. Choose card-upfront vs no-card:
   - Card upfront: lower start volume, higher end conversion; the card is the paywall.
   - No-card: higher start, lower end; you must earn the card at the end.
4. Place the paywall at the value moment, not day zero: after the first successful output, not on login.
5. Measure trial-to-paid on a fixed cohort with the started-trials denominator:
   `ttp = paid_trials / started_trials`, over all trials that have had time to reach the deadline.
6. Segment by acquisition source: paid-search trials often convert worse than organic because intent is weaker.
7. Guard against self-selection when changing length: A/B the length; do not compare this month's 14-day trial to last month's 7-day.
8. Convert to revenue: `trial_derived_mrr = paid_trials * arpa_minor`, in integer minor units.

9. Decide when the card is charged — trial start (auth only) or conversion — and state it, to avoid a surprise first charge.
10. Treat trial-extension requests as a product event, not a support favour, so extensions are countable and measurable.
11. Set a kill criterion: if paid trials per 1,000 starts do not beat the free-tier funnel, remove the trial.
12. Measure time-to-value after the paywall change, not just conversion; a paywall that converts but never activates churns immediately.
13. Cap the number of reminder emails to trial users; a sequence that reads as nagging lifts cancellations.
14. Hold the paywall experiment for a full cohort maturity window before reading the result.

## Pitfalls

- Dividing by ended trials hides trials that simply stopped being used; that abandoned count is the number you most want to see.
- Calling a trial "converted" on signup with no payment measures intent, not revenue.
- A 30-day trial with a 7-day decision horizon delays cash without lifting conversion.
- Card-upfront trials inflate conversion by scaring churners away at signup, so the cohort mix shifts under you.
- Comparing cohorts that have not all reached trial end yet; restrict to cohorts whose last member has hit the deadline.

- An auth hold at trial start that the customer did not expect is a chargeback source even though nothing was charged.
- Unbounded manual extensions make the cohort's deadline fuzzy and the conversion rate meaningless.
- Keeping a losing trial variant because "it drove signups" ignores the paid-trials denominator.
- Reading a paywall test before the cohort matures rewards the variant with the shortest decision lag, not the best.

## Verification

    python3 -c "started=1200; paid=228; print(round(paid/started*100,1))"
    # 19.0 -> trial-to-paid, with the started-trials denominator stated alongside

Report: trial length, card-upfront flag, paywall trigger, and trial-to-paid with the started-trials denominator spelled out.
