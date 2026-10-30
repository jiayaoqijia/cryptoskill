# 08 — Market Regime, Scenarios and Reverse Stress

## Purpose

Place the portfolio in a regime and test it against named shocks. A base-case forecast is not a risk analysis.

## Inputs

- Portfolio weights and cluster map.
- Historical returns and benchmark returns.
- Stablecoin, bridge, and liquidity exposures.
- Mandate loss floor and scenario limits.

## Method

1. Identify the current regime and the transmission channel.
2. Define historical, hypothetical, and reverse scenarios.
3. Apply shocks to positions and clusters.
4. Report loss, contribution, and first breached limit.
5. Separate market loss from liquidity and counterparty loss.
6. State assumptions and label modeled outputs.

## Regime inputs

| Dimension | What to observe | Portfolio transmission |
|---|---|---|
| Liquidity | Stablecoin supply, exchange balances, funding | Risk appetite and exit depth |
| Rates | Real yields, policy expectations | Discount rate and carry |
| BTC dominance | Rotation between BTC and alts | Beta and correlation |
| Volatility | Realized/implied volatility, funding/OI | Drawdown and liquidation risk |
| Regulation | Licensing, enforcement, tax changes | Access, eligibility, venue risk |
| Adoption | ETF/fund flows, enterprise usage | Demand and credibility |

Sentiment (Fear & Greed, social) is context, not evidence. State the named channel: cash flow, discount rate, funding, demand, or cost.

## Scenario design

Use three layers:

1. **Historical:** replay a known stress period; state the dates and data source.
2. **Hypothetical:** define shocks and co-movements; state why they are plausible.
3. **Reverse stress:** find the combination that breaches the mandate’s loss floor.

Minimum scenario set:

| Scenario | Shocks | What it tests |
|---|---|---|
| Risk-off | BTC −30%, ETH −40%, alts −50% to −70% | Beta and correlation |
| Stablecoin depeg | 5% and 20% depeg; redemption gate | “Cash” and liquidity |
| Bridge/chain halt | 7-day pause; wrapped asset discount | Exit and custody |
| Correlation → 1 | All risky assets move together | Diversification failure |
| Liquidity haircut | 25% of normal volume | Forced-sale loss |
| Reverse stress | Solve for loss-floor breach | Mandate viability |

## Stress output

| Scenario | Portfolio loss | % | Worst position | First breached limit | Recovery assumption |
|---|---:|---:|---|---|---|
| Risk-off | $X | X% | Top position | Top-1 limit | None |
| Depeg | $X | X% | Stablecoin | Liquidity limit | Redemption gate |

## Reverse stress method

1. Define the loss floor from the IPS-lite.
2. Choose the material risk factors.
3. Search a grid of plausible shocks (or solve analytically for simple linear exposures).
4. Report the first combination that breaches the floor.
5. Do not present the result as a probability unless a model supports it.

## Scenario rules

- Do not use a single “worst case.”
- State whether correlations are assumed stable or stressed.
- Separate market loss from liquidity loss and counterparty loss.
- Include fees, slippage, and taxes where material.
- Label modeled outputs `MODELED`; do not mix them with observed losses.

## Failure modes

- Forecasting a target price and calling it a scenario.
- Using only a −30% BTC shock for a portfolio of small-cap alts.
- Assuming stablecoins are immune to depeg.
- Ignoring the exit path in the loss estimate.
- Presenting reverse stress as a probability.

## Sources

- CFA Institute, *Measuring and Managing Market Risk* (2026): historical, hypothetical, and reverse stress.
- FSB, *The Financial Stability Risks of Decentralised Finance* (2023).
- arXiv 2507.08915 (2025): heavy tails, contagion, stablecoin hedging.
