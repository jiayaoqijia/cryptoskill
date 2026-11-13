---
name: ac-liquidation-risk-management
description: "Professional liquidation risk management for perpetual futures trading: calculation of liquidation geometry, margin modes, leverage bands, hedge and basis risk, cascade exposure, margin monitoring, and post-liquidation recovery. Use when asking 'liquidation price', 'margin mode', 'how much leverage', 'cross or isolated', 'avoid getting liquidated', 'ADL'. Not for risk budgets or trade journals (ac-crypto-trading-discipline), venue selection (ac-perp-venue-diligence), or liquidation hunt analysis (ac-liquidation-hunt-analysis)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# ac-liquidation-risk-management

## Overview
Perpetual futures trading exposes positions to forced liquidation when equity falls below maintenance margin requirements. This skill governs the mechanics of liquidation geometry, margin allocation, leverage constraints, basis and hedge risks, cascade exposures, real-time margin monitoring, and post-liquidation protocols. It provides rigorous mathematical and operational procedures to ensure positions remain isolated from catastrophic liquidation events.

Primary sources for the claims here: <https://www.binance.com/en/support/faq/leverage-margin-types-and-isolated-margin-borrowing-rules-360033162192> and <https://www.bybit.com/en/help-center/article/Linear-Contract-Liquidation-Price>.

## When to use
Use when calculating liquidation distances, choosing between isolated and cross margin, determining leverage from invalidation thresholds rather than conviction, managing hedged leg risks during market cascades, auditing account margin health, or recovering operational stability after a liquidation event.

## When NOT to use
Not for maintaining the discretionary trade journal or sizing risk budgets (use ac-crypto-trading-discipline), evaluating perpetual venue collateral safety or backstop resilience (use ac-perp-venue-diligence), or analyzing historical stop hunts and cascade mechanics (use ac-liquidation-hunt-analysis).

## Index
| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| [](subskills/liquidation-geometry.md) | crypto-trading/liquidation-geometry | MMR, leverage→liquidation-distance arithmetic with worked numbers, mark vs last price, maintenance-margin bands. |
| [](subskills/margin-modes.md) | crypto-trading/margin-modes | Isolated vs cross vs portfolio margin; what cross-collateral really puts at risk. |
| [](subskills/leverage-bands.md) | crypto-trading/leverage-bands | Choose leverage from the invalidation distance, never from conviction; the 10–25× vs 100× geometry; why a 0.5% liquidation distance sits inside the tool noise. |
| [](subskills/hedge-and-basis-risk.md) | crypto-trading/hedge-and-basis-risk | Hedge-leg liquidation, funding flips, the asymmetry between legs, and what a hedged book does in a cascade. |
| [](subskills/cascade-exposure.md) | crypto-trading/cascade-exposure | ADL, insurance fund depletion, partial liquidations, order-book gaps; how to hold a position such that a wick cannot take it out. |
| [](subskills/margin-monitoring.md) | crypto-trading/margin-monitoring | The pre-trade and daily checks: liquidation distance vs realised volatility, funding drain, OI shifts, the tripwires that force a size cut. |
| [](subskills/post-liquidation-recovery.md) | crypto-trading/post-liquidation-recovery | What a liquidation did mechanically, the record it must produce, restart rules, and the prohibition on averaging down into a liquidation. |

## Status and honest limits
Status: seedling. Designed for professional desk risk management. Relies on published exchange margin specifications and empirical cascade observations. Does not predict market direction, funding rate inflections, or flash crash wicks. All margins assume standard flat maintenance margin regimes.

## Sources
- Binance Futures Trading Rules and Margin Mechanics: https://www.binance.com/en/support/faq/leverage-margin-types-and-isolated-margin-borrowing-rules-360033162192
- Bybit Perpetual Contracts Specifications and Liquidation Price Calculation: https://www.bybit.com/en/help-center/article/Linear-Contract-Liquidation-Price
