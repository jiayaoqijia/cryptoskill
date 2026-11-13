---
name: correlation-regimes
domain: crypto-trading/correlation-regimes
trigger: "correlation regime, tail dependence, common shock, calm market correlation"
anti_trigger: "capital allocation, rebalancing rules, portfolio review"
scope: Measuring regime-dependent correlation and managing tail dependence in common shocks.
status: seedling
---

# Correlation Regimes

## Standard

Crypto asset correlations are highly regime-dependent and increase dramatically during market stress events, liquidity contractions, and cascading liquidations. Measuring asset correlation exclusively during calm market periods severely underestimates portfolio vulnerability because tail dependence causes seemingly uncorrelated digital assets to move in tandem during systemic shocks. Portfolio construction must account for regime shifts, ensuring that diversification assumptions do not rely on historical data gathered solely during low-volatility environments. When common shocks occur across global venues, liquidation dynamics amplify cross-asset co-movement, neutralizing traditional portfolio variance reduction techniques. Understanding these structural shifts is essential for maintaining robust risk boundaries across all active trading operations.

Primary sources for the claims here: <https://www.bis.org/publ/qtrpdf/r_qt2212s.htm> and <https://www.nber.org/papers/w31000>.

## Decision rules

- Historical correlation coefficients calculated during calm market regimes must be adjusted upward significantly for stress-testing and risk modeling across all portfolio components.
- Strategies holding seemingly uncorrelated crypto assets must be treated as fully correlated when market-wide liquidity shocks, margin cascades, or systemic exchange failures occur.
- Portfolio diversification models must incorporate tail dependence metrics, extreme value theory, and stress-scenario correlation matrices rather than standard Pearson coefficients alone.
- Exposure concentration in assets exhibiting high beta to market-wide liquidity must be tightly capped regardless of apparent historical decorrelation during stable periods.

## Procedure

1. Extract comprehensive historical return series for all portfolio assets across both calm and high-stress market periods, including major historical liquidation cascades.
2. Calculate regime-specific correlation matrices, isolating data from known systemic events and high-volatility market contractions.
3. Apply stress correlation weights and tail dependence parameters to portfolio risk simulations to identify hidden structural vulnerabilities.
4. Adjust position sizing, asset selection, and strategy weights to maintain acceptable risk parameters under high-correlation stress scenarios.
5. Continuously monitor real-time market liquidity indicators, order book depth, and volatility indexes for early signals of an emerging correlation regime shift.

## Anti-patterns

- Relying exclusively on trailing 30-day or 90-day correlation figures computed during calm, stable market phases without stress adjustments.
- Assuming cross-asset diversification holds true during sharp market-wide drawdowns, funding squeezes, or exchange insolvency events.
- Ignoring volume contraction and open interest unwinding as leading indicators of correlation breakdown and systemic stress.

## Done checklist

- [ ] Portfolio risk models utilize stress-adjusted correlation matrices and tail dependence metrics.
- [ ] Tail dependence and common shock scenarios are explicitly tested across all active strategies.
- [ ] Asset weights reflect potential correlation spikes during liquidity crunches and margin cascades.

## Sources

- National Bureau of Economic Research (NBER): https://www.nber.org/papers/w31000
- Bank for International Settlements (BIS): https://www.bis.org/publ/qtrpdf/r_qt2212s.htm
- Federal Reserve Bank of New York: https://www.newyorkfed.org/
- European Central Bank (ECB): https://www.ecb.europa.eu/
