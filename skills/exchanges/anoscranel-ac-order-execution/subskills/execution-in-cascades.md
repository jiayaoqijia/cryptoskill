---
name: execution-in-cascades
domain: crypto-trading/execution-in-cascades
trigger: cascade execution, liquidation tape, halted books, sparse book depth
anti_trigger: strategy backtest, historical data collection, volatility metrics
scope: Order execution tactics and tape interpretation during forced liquidation cascades
status: seedling
---

## Standard

A liquidation cascade represents a systemic liquidity vacuum where forced margin liquidations trigger sequential stop-losses and cascading market sells across leveraged venues. During these episodes, limit orders are pulled or overrun, order books exhibit extreme thinning, and price prints gap across multiple price ticks. Academic findings and exchange forensics indicate that cascade dynamics are subcritical (branching ratio $\hat{\lambda}$ between 0.1 and 0.2), meaning cascades propagate through interconnected margin dependencies rather than infinite self-sustaining feedback loops. Consequently, market orders become catastrophic execution choices, as they sweep depleted book depth at severe adverse prices. Working limit orders or utilizing passive passive liquidity accumulation requires distinguishing between genuine price discovery and transient cascade wicks.

Primary sources for the claims here: <https://www.sciencedirect.com/science/article/pii/S037843712100412X> and <https://www.arxiv.org/abs/2003.02672>.

## Decision rules

- Never submit unconstrained market orders during an active liquidation cascade; crossing a thinned order book guarantees maximum negative slippage.
- Avoid placing resting bids directly inside visible liquidity clusters during a cascade, as these clusters are frequently swept or canceled instantly.
- Use passive working orders behind established volatility bands or wait for order book depth to reconstitute before executing large scale rebalancing.
- Monitor real-time order book skew and trade flow toxicity metrics to detect when liquidation intensity reaches exhaustion points.
- Route execution through venues maintaining deep insurance funds and robust cross-margined risk engines during cascade events.

## Procedure

1. Detect cascade initiation: observe sudden spikes in liquidation volume, rapid open interest contraction, and accelerated funding rate shifts.
2. Freeze aggressive crossing: halt all unhedged market-order entry routines and cancel vulnerable resting limit orders near the current mark price.
3. Assess book depth: measure available resting liquidity across top-of-book levels and evaluate order book slope asymmetry.
4. Execute defensive positioning: if exiting, utilize sliced passive limit orders or allow automatic margin backstops to handle forced liquidations rather than manual panic crossing.
5. Post-cascade audit: record fill dispersion, maximum adverse excursion, and post-cascade price reversion characteristics.

## Anti-patterns

- Chasing cascading price momentum with aggressive market sell orders into an empty order book.
- Assuming visible limit order depth at adjacent price levels will persist during a high-speed liquidation sweep.
- Relying on static stop-loss triggers that execute as market orders during systemic volatility spikes.

## Done checklist

- [ ] Market order submissions suspended during active cascade indicators.
- [ ] Order book depth asymmetry and spread widening measured prior to re-entry.
- [ ] Passive limit execution rules applied for defensive positioning.
- [ ] Cascade execution metrics recorded in the trading log.

## Sources

- Flash Crash Mechanics and Liquidity Vacuums in Crypto Derivatives: https://www.arxiv.org/abs/2003.02672
- Empirical Analysis of Liquidation Cascades on Decentralized and Centralized Exchanges: https://www.sciencedirect.com/science/article/pii/S037843712100412X
