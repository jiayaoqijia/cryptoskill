---
name: specify-the-denominator-of-a-rate
description: Use when a percentage, churn, or conversion figure is quoted. Forces the numerator and denominator to be named and checked against the claim.
---

# Specify the Denominator of a Rate

A rate is a fraction, and the bottom of the fraction decides whether it means anything. "20% churn" is fine if the denominator is last month's cohort and alarming if it is every user who ever signed up.

## Procedure

1. Write the rate as `numerator / denominator` in words before quoting a number, and attach a time window to each side.
2. Fix the population to the at-risk set. Churn's denominator is users active at period start, not all users ever created; a rate over the dead moves for irrelevant reasons.
3. Check the numerator is not downstream of the denominator's filter. "Conversion of converted users" and "retention of users who returned" are double-counting bugs, not metrics.
4. Match grain: a city-level numerator over a country-level denominator is not a rate. Aggregate both to the same key before dividing.
5. Emit numerator, denominator, and rate together in every query so the reader sees the base:
   ```sql
   SELECT count(DISTINCT user_id) FILTER (WHERE churned) AS churned,
          count(DISTINCT user_id)                      AS at_risk,
          round(count(DISTINCT user_id) FILTER (WHERE churned)::numeric
                / nullif(count(DISTINCT user_id),0), 4) AS churn_rate
   FROM monthly_at_risk WHERE month = '2026-08-01';
   ```
6. Flag small bases. Suppress or annotate any rate whose denominator is under 30 — the interval is wider than the point.
7. When comparing two rates, compare their denominators too; unequal bases often explain an apparent winner.

## Pitfalls

- Mixing people and sessions: "bounce rate" over sessions and "churn" over users are different universes.
- A trailing-30d denominator against a calendar-month numerator double-counts boundary users.
- Survivorship shrinks the base quietly — users who never returned cannot churn.
- Percentages that sum past 100% are a sign the row denominators differ.
- A rate computed after dropping nulls has a denominator the reader never sees.

## Verification

    grep -rn 'rate' metrics/*.sql | grep -v 'denominator\|at_risk\|/ '   # no bare rate without its base

Report: "Churn 4.1% = 412 churned / 10,046 active at month start (UTC, calendar month). The old tile used all-time signups as the base, which is why it read 0.9%."
