---
name: risk-adjusted-ratios
domain: investing/risk-adjusted-ratios
trigger: "Computing and interpreting a Sharpe or information ratio."
anti_trigger: "Not for predicting returns, and not for strategy selection."
scope: "Sharpe, information ratio, and the assumptions each carries."
status: seedling
---

# Risk-adjusted ratios

## Standard

The Sharpe ratio divides excess return by the volatility of returns; the information ratio divides excess return over a benchmark by the volatility of that excess, called tracking error. Both convert a return into a return per unit of risk, and both rest on assumptions that are usually left unstated: that volatility is the right measure of risk, that returns are roughly symmetric, and that the sample period is long enough to estimate the denominator.

The information ratio is the more useful of the two when a benchmark exists, because tracking error measures the risk actually being taken relative to the policy rather than total volatility, which includes the market's own swings. Neither ratio says anything about the direction of a tail, and a strategy that loses heavily in a crisis can post an attractive ratio computed over a calm sample.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the numerator: which return, which benchmark, which risk-free rate.
- Record the denominator: total volatility or tracking error, and the frequency used.
- Record the sample period and whether it includes a stress episode.
- Record the annualisation method and apply it consistently.
- Record the ratio alongside the drawdown, which the ratio does not capture.
- Where the sample is short, record the confidence interval or state that it is wide.

## Procedure

1. Define the return and the benchmark.
2. Compute excess return and the appropriate denominator.
3. Annualise consistently.
4. Record the sample and its coverage of stress.
5. Pair the ratio with the drawdown.
6. Write the summary with assumptions named.

## Anti-patterns

- Comparing ratios computed over different periods.
- Using a risk-free rate inconsistent with the return's currency.
- Quoting an information ratio without the benchmark.
- Ignoring the tail the ratio does not measure.
- Presenting a two-year ratio as evidence of skill.

## Done checklist

- [ ] Numerator components recorded.
- [ ] Denominator and frequency recorded.
- [ ] Sample period and stress coverage recorded.
- [ ] Annualisation consistent.
- [ ] Drawdown paired with the ratio.
- [ ] Confidence statement made.

A further caution is that the ratio is not comparable across frequencies unless the annualisation is done consistently, and a Sharpe computed from monthly returns then annualised by the square-root convention is a different number from one computed on daily data and annualised the same way, because the underlying return distribution is not identical at the two frequencies.


## Sources

- Investment performance standards: <https://www.cfainstitute.org/>
- Investor education on risk-adjusted returns: <https://www.investor.gov/introduction-investing>
- Risk-free rate data: <https://fred.stlouisfed.org/>
