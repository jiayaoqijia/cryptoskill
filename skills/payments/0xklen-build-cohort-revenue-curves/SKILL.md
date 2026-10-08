---
name: build-cohort-revenue-curves
description: Use when aggregate revenue hides whether new cohorts are getting worse. Builds cohort revenue by month of age, computes cumulative revenue and payback, and compares cohorts at equal age.
---

# Build cohort revenue curves

Total revenue rises while the underlying cohorts decline — a classic survival illusion. Plot each signup cohort's revenue by month of age so the curves are comparable and the trend is visible.

## Procedure

1. Assign every customer to a signup cohort by month. Cohort is the month of acquisition, never the month of first payment after a gap.
2. Build revenue by cohort and age in months: `age = months_between(cohort_month, revenue_month)`.
3. Sum to integer minor units per cohort-age cell, then cumulative per cohort: `cum_rev[cohort][age] = sum(revenue[cohort, 0..age])`.
4. Normalise by cohort size for comparability: `arpu_cum = cum_rev_minor // cohort_size`. Divide by cohort size, never by surviving customers — that hides churn.
5. Worked example, a Jan cohort of 1,000 at ARPU 40/mo with 5%/mo churn: monthly revenue runs 40,000 -> 38,000 -> 36,100 -> ..., so the cumulative curve bends below the linear 6*40,000 as it loses people.
6. Compute LTV as the curve's asymptote or a capped finite-horizon sum; a finite horizon is more honest than dividing by a noisy churn rate.
7. Compute payback: the age at which `cum_rev >= cac_minor`. If payback is 20 months and funding is 18, the cohort never pays back in time.
8. Compare cohorts at equal age: cohort 2025-01 and cohort 2025-06 both at age 6. A falling cumulative curve means acquisition or product quality is slipping.
9. Report the curve matrix and the cohort-over-cohort delta at matched age.

10. Segment cohorts by channel as well as month; a channel-mix shift reads as a product decline when it is acquisition quality.
11. Keep cohort revenue net of refunds and chargebacks, so recent cohorts do not look strong until refunds land.
12. Compare cohorts on cumulative revenue per customer, not absolute revenue, to remove size effects.
13. Plot a retention-adjusted revenue curve alongside the raw one to separate price from volume effects.
14. Flag a cohort whose curve crosses below the prior cohort's at the same age; that is the alarm.
15. Store the curve as a table so a later analysis does not have to recompute from raw events.

## Pitfalls

- Comparing a 3-month-old cohort's revenue to a 12-month-old cohort's; compare at equal age.
- Dividing cumulative revenue by surviving customers, which makes retention look like growth.
- Using total revenue by month, which mixes old cohort decay with new cohort additions and can rise while every cohort falls.
- Ignoring seasonality: a Q4 cohort looks strong at age 3 if you measure it in January.
- Booking refunds later than the measurement date leaves recent cohort months overstated until they settle.

- A cohort curve that mixes channels shows a product decline that is really a worse acquisition mix.
- Gross cohort revenue overstates recent months and then drops when refunds settle.
- Absolute cohort revenue makes a big cohort look successful while its per-customer curve falls.
- Recomputing curves ad hoc each quarter means no stable comparison across reports.

## Verification

    python3 -c "print([round(40000*0.95**a) for a in range(7)])"
    # [40000, 38000, 36100, 34295, 32580, 30951, 29403] -> cumulative curve flattens under 5%/mo churn

Report: the cohort-by-age revenue matrix, cumulative ARPU at matched ages, and the payback month against the funding horizon.
