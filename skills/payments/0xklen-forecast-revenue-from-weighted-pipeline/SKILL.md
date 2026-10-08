---
name: forecast-revenue-from-weighted-pipeline
description: Use when a revenue forecast must come from the pipeline. Scores each open deal by stage and age probability, sums to a commodity forecast, and presents a range calibrated against actuals.
---

# Forecast revenue from weighted pipeline

A pipeline forecast is only as good as the probabilities you put on it. Weight each deal by its stage and its age, present a range, and backtest the weights so the forecast is calibrated rather than optimistic.

## Procedure

1. Enumerate open deals with `amount_minor` (contracted value, not the aspirational figure), stage, expected close date, and the date the deal entered its current stage.
2. Assign a probability per stage from historical close rates, not from rep optimism. Pull actuals: of deals that reached "proposal", what share closed?
3. Age-adjust: a deal stuck in a stage past its median dwell time is decaying. `p_adj = p_stage * decay_factor`, with decay rising with time-in-stage.
4. Compute the commodity forecast with probability in basis points and divide once at the end:
   `forecast_minor = sum(deal.amount_minor * p_bp) // 10000`.
5. Worked example:
   - deal A 200,000 minor @ 6000 bp = 120,000
   - deal B 500,000 minor @ 3000 bp = 150,000
   - deal C 300,000 minor @ 1000 bp = 30,000
   - forecast = 300,000 minor = USD 3,000.00.
6. Present a range, not a point: compute the pessimistic case (late-stage, high-probability deals only) and the optimistic case (adds early-stage deals), and report both plus the mid.
7. Keep the committed base separate: revenue already contracted and in the ledger is near-certain and must not be double-counted in the weighted sum.
8. Backtest monthly: compare last month's forecast to actual, compute the ratio, and adjust the stage probabilities. A persistent over-forecast means the weights are too high.
9. Report the forecast with the exogenous inputs stated — churn, expansion and the current MRR baseline.

10. Model the distribution, not just the mean: bootstrap past deal outcomes to get a P10/P50/P90, since a weighted sum hides the tail.
11. Carry in-quarter slippage explicitly: a deal that slips out of the quarter should be removed, not re-dated and left counted.
12. Segment the forecast by segment or region so a single large-deal dependency is visible.
13. Track forecast accuracy per rep to calibrate their individual probabilities over time.
14. Re-derive probabilities quarterly from trailing close rates, not from last year's.
15. Publish the forecast with its assumptions so a later variance analysis can attribute the miss.

## Pitfalls

- Using rep-supplied probabilities, which cluster near 90% and make every pipeline look certain.
- Ignoring deal age; a deal in "negotiation" for six months is not a 70% deal.
- Forecasting gross new business without netting forecast churn, overstating the revenue line.
- A single-point forecast that hides the range; stakeholders anchor on the point and blame the model for the spread.
- Double-counting committed revenue that is already in MRR when it also sits in the pipeline.

- Slippage silently re-dated keeps a dead deal in the forecast and inflates the optimistic end.
- A mean weighted forecast without a distribution understates the chance of a bad quarter.
- Stale probabilities from last year misprice a pipeline whose win rates have moved.
- A single large-deal dependency hidden in an aggregate makes the forecast brittle.

## Verification

    python3 -c "d=[(200000,6000),(500000,3000),(300000,1000)]; print(sum(a*p for a,p in d)//10000)"
    # 300000 -> weighted forecast $3,000.00; backtest last month's ratio to calibrate the weights

Report: the weighted forecast, the pessimistic-optimistic range, the prior-month forecast-to-actual ratio, and the stage probabilities used.
