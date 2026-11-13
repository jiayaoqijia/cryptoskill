---
name: garch-style-volatility
domain: crypto-trading/garch-style-volatility
trigger: "Using a conditional volatility model to forecast or size."
anti_trigger: "Not for promising a forecast, and not for backtest validation."
scope: "Clustering, persistence, and what the model assumes about tails."
status: seedling
---

# GARCH-style volatility

## Standard

Volatility clusters: quiet days follow quiet days, wild days follow wild days. A GARCH-style model captures this by making today's variance a function of yesterday's variance and yesterday's squared return, which produces a persistent, mean-reverting variance forecast. The model is a statement about second moments with parameters estimated from data, and its usefulness is entirely conditional on that clustering persisting.

The honest limits are in the tails and the parameters. The standard model's innovations are assumed normal, which understates the frequency of large moves; variants exist for that but carry their own estimation fragility. The parameters are fitted, and a fitted persistence near the boundary of stability produces forecasts that decay too slowly and hold a high variance estimate long after a shock has faded. The model is a measurement scaffold, not a guarantee.

Primary sources: <https://quant.stackexchange.com/> and <https://fred.stlouisfed.org/>.

## Decision rules

- Record the model class, its innovation assumption, and the parameter estimates.
- Record the data window used for estimation and the state of that window.
- Compute the persistence (the sum of the key parameters) and state what it implies.
- Test the residuals of the fit for remaining clustering, which indicates misspecification.
- State the tail assumption explicitly and where it understates.
- Use the forecast with its confidence band, never alone, for sizing.

## Procedure

1. Fix the model class and innovation assumption.
2. Estimate the parameters over a stated window.
3. Compute and interpret persistence.
4. Test residuals for leftover clustering.
5. State the tail assumption and its known understatement.
6. Produce the forecast with a band, and date it.

## Anti-patterns

- Presenting a point forecast of volatility without a band.
- Estimating on a calm window and trusting the model through a crisis.
- Treating normal innovations as a description of real tails.
- Recomputing parameters until the forecast says something convenient.
- Using the volatility forecast as if it were a return forecast.

## Done checklist

- [ ] Model class and innovations recorded.
- [ ] Estimation window recorded.
- [ ] Persistence computed and interpreted.
- [ ] Residual test recorded.
- [ ] Tail assumption stated.
- [ ] Forecast dated with a band.

A final caution is that fitted parameters are themselves estimates with standard errors: a persistence computed near the stability boundary may be two parameter errors from a model that forecasts sensibly and one from one that does not. The parameter uncertainty belongs in the forecast band, not in a footnote.

## Sources

- Volatility model discussion: <https://quant.stackexchange.com/>
- Return and volatility data: <https://fred.stlouisfed.org/>
- Estimation background: <https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity>
