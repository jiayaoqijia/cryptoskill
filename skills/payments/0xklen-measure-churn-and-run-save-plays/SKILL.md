---
name: measure-churn-and-run-save-plays
description: Use when churn needs a number and a response. Computes logo and revenue churn from a cohort and routes a cancellation through ranked save offers by expected value.
---

# Measure churn and run save plays

Churn is two numbers, not one: logos lost and revenue lost. And a save play is a priced bet — offer the cheapest retention motion whose expected saved revenue beats its cost.

## Procedure

1. Fix the cohort and window. Monthly logo churn over January is `logos_lost / logos_at_start`; always state the month and the universe.
2. Compute revenue churn separately: `revenue_churn = mrr_lost_minor / mrr_start_minor`, in integer minor units.
3. Distinguish voluntary (they cancel) from involuntary (the card fails); involuntary churn belongs to the retry ladder, not the save desk.
4. For each cancellation compute the value at risk: `var_minor = mrr_minor * expected_remaining_months`. Use a survival estimate (about `1 / monthly_churn_rate` months) rather than the average tenure of everything.
5. Rank save offers by expected value: `ev = accept_prob * var_minor - offer_cost_minor`, and try them in descending EV order.
6. Worked example: a customer at USD 49/mo with an expected remaining life of 12 months gives `var = 4900*12 = 58800` minor. A 50%-off-for-3-months offer costs `4900//2 * 3 = 7350` minor; at 40% accept, `ev = 0.40*58800 - 7350 = 16170` minor. Worth offering.
7. Cap the discount window; a permanent discount converts churn into a permanently lower MRR, which is contraction by another name.
8. Log a reason code on every cancellation and report churn split by reason so next quarter's fix targets the biggest slice.
9. Re-baseline on net revenue retention: save plays cut churn but also cut expansion, so measure NRR, not gross churn, to catch the trade.

10. Compute dollar-weighted churn alongside logo churn; one enterprise loss can dominate both.
11. Track a save rate with its denominator (saves / cancellation attempts) and trend it; a falling rate means the offers are stale.
12. Feed reason codes into the roadmap as a ranked list; the top cancellation reason is the cheapest churn fix.
13. Separate voluntary churn triggered by price from that triggered by product; they need different save offers.
14. Model the save-offer cost against a control group to confirm the save was incremental, not a discount to someone who would have stayed.
15. Re-forecast MRR after a save campaign, since a successful save at a discount lowers next quarter's expansion.

## Pitfalls

- Reporting only logo churn hides the accounts that downgrade, and revenue churn hides the accounts that leave.
- Counting a save as a win when it was a permanent 60% discount: you saved the logo and destroyed the margin.
- Using the average lifetime instead of a survival estimate overstates value at risk for a long-tenured customer already past the hazard peak.
- Mixing involuntary churn into the save-desk denominator inflates the save rate.
- No reason code means you cannot tell a product problem from a price problem, so you discount the wrong thing.

- A save rate without offer cost hides that the saves were bought with margin, not won with product.
- Dollar-weighted churn ignoring a single large account can flip a healthy logo number into a bad revenue quarter.
- Reason codes collected as free text cannot be ranked; force a fixed taxonomy at cancellation.
- Discounting a customer who would have stayed anyway is leakage, not a save; a control group tells the two apart.

## Verification

    python3 -c "var=4900*12; cost=4900//2*3; print(var, cost, 0.40*var-cost)"
    # 58800 7350 16170.0 -> save offer EV is positive, rank it above any costlier save

Report: monthly logo churn, monthly revenue churn, and the top three save offers with their EV in minor units.
