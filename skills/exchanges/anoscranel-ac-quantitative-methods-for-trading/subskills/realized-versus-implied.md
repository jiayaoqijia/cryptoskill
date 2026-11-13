---
name: realized-versus-implied
domain: crypto-trading/realized-versus-implied
trigger: "Comparing realized and implied volatility for a decision."
anti_trigger: "Not for predicting volatility, and not for options execution."
scope: "Two volatilities, two estimators, and the premium between them."
status: seedling
---

# Realized versus implied

## Standard

Realized volatility is computed from returns that have happened; implied volatility is extracted from option prices as the market's forward guess. The two use different estimators, different windows, and different conventions, so comparing them requires care on all three. The difference between them — implied usually above realized — is the volatility risk premium: the amount option buyers pay for the certainty.

The estimator choices matter as much as the comparison. Realized volatility from closing prices differs from a range-based estimator that uses highs and lows, and both differ from estimators designed for jump-heavy data. The implied figure is the market's under its own quoting convention and expiry. A spread between an aggressively estimated realized and a conservative implied is an artifact of estimation, not a premium.

Primary sources: <https://www.cboe.com/> and <https://quant.stackexchange.com/>.

## Decision rules

- Record both figures with their estimators, windows, and conventions.
- Compare like for like: same period, same annualisation, same return basis.
- Record the premium and its own history over a stated window.
- Record the estimator's sensitivity: what jumps and gaps do to the realized figure.
- Treat the realized figure as noisy for short windows and state the window.
- Note that the premium's sign and size both vary by regime.

## Procedure

1. Compute realized volatility with a stated estimator and window.
2. Record the implied figure with expiry and source.
3. Annualise both consistently.
4. Compute the premium and place it in its own percentile range.
5. Test sensitivity by varying the estimator.
6. Record the comparison with dates and conventions.

## Anti-patterns

- Comparing a close-to-close realized with a range-based figure as if equivalent.
- Reading the premium as guaranteed carry.
- Using a short-window realized as if it were precise.
- Ignoring jumps in the realized window.
- Stating the comparison without estimator, window, and annualisation.

## Done checklist

- [ ] Estimators and windows recorded.
- [ ] Conventions aligned.
- [ ] Premium computed and ranged.
- [ ] Sensitivity to estimator varied.
- [ ] Short-window noise stated.
- [ ] Comparison dated and sourced.

The two figures also answer different questions: implied is a market price for future uncertainty and reacts to demand for protection, while realized is a measurement of what occurred. Mixing them into a single spread without noting this treats a price as if it were a sample statistic.

## Sources

- Implied volatility data and methodology: <https://www.cboe.com/>
- Volatility estimation discussion: <https://quant.stackexchange.com/>
- Market volatility series: <https://fred.stlouisfed.org/>
