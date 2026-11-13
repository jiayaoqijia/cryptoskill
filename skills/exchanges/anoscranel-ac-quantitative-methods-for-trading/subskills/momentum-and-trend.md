---
name: momentum-and-trend
domain: crypto-trading/momentum-and-trend
trigger: "Measuring trend or momentum for a systematic rule."
anti_trigger: "Not for predicting direction, and not for backtest validation."
scope: "What trend measures, horizon choice, and why momentum crashes happen."
status: seedling
---

# Momentum and trend

## Standard

A momentum rule buys what has risen and sells what has fallen over a stated lookback, and a trend rule holds a position aligned with a smoothed price direction. Both are measurements of the same object: persistence in returns over a horizon. The horizon is the decision, and it is not free — short horizons pick up microstructure noise and turnover costs, long horizons hold positions through the reversals that define the method's worst moments.

The known failure mode is structural, not random. Momentum strategies earn steady returns and then lose in sharp clusters when markets reverse across correlated holdings at once — a crash profile rather than a smooth drawdown. This is not a defect of measurement but a consequence of the rule itself: exiting a falling market is always late, and the lateness is the cost paid for the persistence the rule captures.

Primary sources: <https://quant.stackexchange.com/> and <https://www.nber.org/>.

## Decision rules

- Record the rule's exact form: lookback, smoothing, weighting (equal, exponentially weighted).
- Record the horizon rationale and the turnover it implies.
- Record the cost per round trip and the horizon's break-even persistence.
- Record the crash profile: worst historical cluster of the rule, not just its average.
- Record the exit latency: how many periods of reversal before the rule flips.
- State the falsifier: how much persistence loss makes the rule uneconomic.

## Procedure

1. Specify the rule's form and parameters exactly.
2. Measure turnover and cost per period.
3. Compute the break-even persistence after costs.
4. Assemble the rule's worst historical clusters and their depth.
5. Measure exit latency in periods.
6. Write the falsifier and the review trigger into the record.

## Anti-patterns

- Tuning the lookback until the backtest smiles.
- Reporting average returns without the crash clusters.
- Ignoring turnover cost at short horizons.
- Treating a momentum crash as an unlucky period rather than the expected tail.
- Fitting the exit latency to a sample that never contained a reversal.

## Done checklist

- [ ] Rule form and parameters recorded.
- [ ] Turnover and cost computed.
- [ ] Break-even persistence stated.
- [ ] Crash clusters assembled.
- [ ] Exit latency measured.
- [ ] Falsifier and trigger written.

The horizon decision also interacts with the instrument's own dynamics: a horizon tuned on an index averages over regimes, while one tuned on a single asset fits that asset's recent character. Record which class of underlying the parameters were estimated on, because a rule carried from an index to a single name inherits evidence it does not have.

## Sources

- Momentum research evidence base: <https://www.nber.org/>
- Quantitative discussion of trend rules: <https://quant.stackexchange.com/>
- Investor education on risk: <https://www.investor.gov/introduction-investing>
