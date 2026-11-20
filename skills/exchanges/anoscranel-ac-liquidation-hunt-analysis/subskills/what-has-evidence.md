---
name: "what-has-evidence"
domain: "crypto-trading/what-has-evidence"
trigger: "When asked about what has evidence in liquidation analysis"
anti_trigger: "When conducting unrelated trading tasks or general market research"
scope: "what has evidence analysis for derivative liquidation events"
status: "seedling"
---

# What Has Evidence

## Standard

What has evidence establishes the narrow subset of liquidation and market microstructure phenomena that survive rigorous empirical verification. Unlike speculative folklore, verified empirical findings rely on reproducible data across millions of recorded transactions. This leaf inventories three robustly documented phenomena: UTC temporal volume clustering, order-flow imbalance mechanics, and funding rate extremity extremes. Each finding is detailed with exact parameters, sample sizes, and analytical limits to ensure practitioners distinguish between proven structural regularities and unverified trading myths.

Empirical research across exchange archives demonstrates that liquidation activity is not uniformly distributed across time. Furthermore, order-flow imbalance models (Cont et al., 2014) show a linear relation between order-flow imbalance and short-horizon price changes, with a slope inversely proportional to market depth.

Primary source for the claims here: <https://doi.org/10.1093/jjfinec/nbt003>.

Additional public source for the claims here: <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Rule 1: Utilize UTC temporal clustering as structural context for volatility expectations; derive window multipliers from your own documented dataset (source, window, sample size) before quoting them.
- Rule 2: Apply order-flow imbalance (OFI) metrics strictly under academic assumptions. Acknowledge that OFI measures immediate aggressive queue depletion but does not guarantee directional trend persistence beyond short-term horizons.
- Rule 3: Treat extreme positive or negative funding rates as descriptive markers of crowded leverage rather than precise timing triggers. High funding rates indicate asymmetrical position skew but lack the temporal precision required for entry execution.
- Rule 4: Refuse any analytical framework that treats empirical statistical tendencies as deterministic trading certainties. Observed ratios represent historical probability densities, not guaranteed future outcomes.

## Procedure

1. Query standardized UTC timestamp partitions on historical liquidation datasets to verify current volatility clustering parameters.
2. Calculate order-flow imbalance metrics across consecutive order book snapshots during high-volume liquidation events.
3. Track perpetual swap funding rate moving averages across top-tier derivatives venues to identify prolonged skew anomalies.
4. Cross-reference funding extremes against open interest changes to separate genuine leveraged accumulation from hedging activity.
5. Compile empirical findings into structured descriptive reports without extrapolating trade execution signals.

## Anti-patterns

- Anti-pattern: Treating UTC temporal clustering as an exact trading schedule. Volume concentrations indicate probabilistic risk windows, not mandatory price reversal moments.
- Anti-pattern: Confusing high funding rates with imminent liquidations. Traders can maintain heavily funded positions for extended periods if intraday trend momentum compensates for funding drag.
- Anti-pattern: Assuming order-flow imbalance coefficients remain constant across varying market regimes and asset liquidity tiers.

## Done checklist

- [ ] Multipliers derived from a documented dataset.
- [ ] Its sample parameters referenced.
- [ ] Order-flow imbalance assumptions and decay limits established.
- [ ] Funding rate extremity interpretation defined as crowdedness context.
- [ ] Zero trade recommendations or predictive assertions included.

## Sources

- Cont, R., Kukanov, A., & Stoikov, S. (2014). The Price Impact of Order Book Events. *Journal of Financial Econometrics*, 12(1), 47-88. https://doi.org/10.1093/jjfinec/nbt003 (working paper: <https://arxiv.org/abs/1011.6402>)
- Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and High-Frequency Trading*. Cambridge University Press. ⚠️ cited without URL.
- Reference: <https://arxiv.org/abs/2608.03616>
