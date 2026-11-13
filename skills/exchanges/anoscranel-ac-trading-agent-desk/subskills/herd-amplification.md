---
name: herd-amplification
domain: crypto-trading/herd-amplification
trigger: how agents amplify market herds, all-or-nothing participation dynamics, market maker liquidity fragility, reading volume with agent participation
anti_trigger: assuming markets self-correct instantly, treating volume as genuine liquidity, optimistic liquidity assumptions
scope: Agent-driven herd amplification, all-or-nothing participation, and market maker fragility
status: seedling
---

## Standard
Agent-driven trading systems introduce severe structural feedback loops into financial markets through herd amplification and all-or-nothing participation dynamics. Because profit-seeking autonomous agents utilize similar objective functions, data sources, and threshold triggers, they tend to synchronize their actions during volatility events. This synchronization accelerates price momentum, deepens liquidity vacuums, and amplifies market herds far beyond traditional human baseline participation.

Conversely, professional market makers providing spread-earning liquidity must widen quotes or withdraw entirely during these herd surges to manage inventory risk, rendering visible book liquidity highly fragile (https://doi.org/10.1111/jofi.13210). Consequently, high trading volume during agent-dominated episodes does not reflect genuine depth; rather, it indicates transient, high-turnover activity masking severe structural thinness. Trading desks must account for maker fragility and avoid interpreting volume spikes as stable liquidity reserves (https://arxiv.org/abs/2308.09876).

## Decision rules
- Rule 1: Never treat high trading volume during volatile periods as stable execution liquidity; assume book depth is highly fragile.
- Rule 2: Account for the tendency of automated agents to synchronize actions, creating exaggerated price impulses and sudden liquidity evaporations.
- Rule 3: Enforce strict execution slippage limits and time-weighted participation caps to prevent algorithms from chasing herd momentum.
- Rule 4: Model market maker withdrawal risk explicitly in position liquidation and order-slicing algorithms.
- Rule 5: Prohibit execution strategies from relying on continuous resting liquidity during periods of extreme sentiment divergence.

## Procedure
1. Review execution algorithms to ensure order sizing scales inversely with observed order book thinness and volatility.
2. Implement execution pacing controls (e.g., TWAP/VWAP with participation rate caps) to avoid exacerbating herd momentum or consuming fragile maker quotes.
3. Monitor real-time bid-ask spread expansion and depth depletion ratios across monitored venues as indicators of maker withdrawal.
4. Stress-test historical execution models against simulated liquidity evaporation scenarios where resting book depth drops by 80% instantaneously.
5. Record and analyze fill quality degradation during high-intensity news events to quantify agent-driven herd impact on desk fills.

## Anti-patterns
- Anti-pattern 1: Slicing large orders aggressively into surging volume without accounting for maker withdrawal.
- Anti-pattern 2: Assuming resting limit orders on central limit order books represent committed, sticky liquidity during crashes.
- Anti-pattern 3: Deploying unthrottled momentum-following agents that contribute directly to feedback-driven herd acceleration.
- Anti-pattern 4: Measuring market depth solely by aggregate 24-hour volume figures.

## Done checklist
- [ ] Execution algorithms incorporate dynamic participation rate caps and slippage bounds.
- [ ] Liquidity stress tests account for instantaneous maker withdrawal and spread widening.
- [ ] Volume metrics are filtered for transient agent churn rather than structural depth.
- [ ] Order-slicing logic prevents aggressive consumption of fragile book liquidity (https://doi.org/10.1111/jofi.13210).
- [ ] Risk documentation details the mechanics of agent herd amplification (https://arxiv.org/abs/2308.09876).

## Sources
- Market Maker Inventory Risk and Liquidity Fragility in Electronic Markets: https://doi.org/10.1111/jofi.13210
- Feedback Loops and Herd Dynamics in Algorithmic Trading Ecosystems: https://arxiv.org/abs/2308.09876
