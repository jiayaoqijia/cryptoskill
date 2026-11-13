---
name: hedge-and-basis-risk
domain: crypto-trading/hedge-and-basis-risk
trigger: Use when managing hedged positions, cash-and-carry basis trades, and inter-leg liquidation asymmetry.
anti_trigger: Not for single-direction speculative leverage selection, isolated margin setup, or cascade post-mortems.
scope: Hedge-leg liquidation, funding flips, the asymmetry between legs, and what a hedged book does in a cascade.
status: seedling
---

## Standard
Hedged books and cash-and-carry basis trades combine spot and perpetual legs or cross-venue futures to capture yield or neutralize directional risk. However, hedged structures introduce severe operational complexities during market stress, notably inter-leg liquidation asymmetry, funding rate flips, and execution slippage during liquidations. In a violent market cascade, the short perpetual leg may experience extreme positive funding payments while the spot or long leg suffers collateral haircutting or withdrawal freezes on custodial platforms. If the margin on the leveraged leg is not proactively managed independently of the hedge leg, a sudden basis expansion can trigger the liquidation of the winning or losing leg before structural convergence occurs. Funding flips from positive to deeply negative can drain margin balances rapidly, turning a carry trade into an unhedged directional loss maker.

Primary sources for the claims here: <https://www.binance.com/en/support/faq/basis-trading-introduction-4199d79998494f1c9c488349257bb5cb> and <https://www.deribit.com/pages/docs/futures>.

## Decision rules
1. Maintain separate, over-collateralized margin buffers for perpetual short legs in basis trades, ensuring capital reserves can absorb at least a 40% basis expansion against the position.
2. Monitor funding rate velocity across all hedged legs daily; unwind basis positions immediately when annualized funding yields drop below risk-free benchmark rates plus operational friction.
3. Prohibit cross-venue hedging where margin balances cannot be instantly reallocated between venues during network congestion or API latency spikes.
4. Assume non-linear price divergence during systemic liquidation cascades; never rely on historical correlation coefficients remaining stable during market stress.

## Procedure
1. Calculate the maximum expected basis expansion using historical extreme events (e.g., historical spot-perp basis spikes).
2. Allocate excess cash margin to the perpetual leg to ensure the liquidation price sits beyond the historical maximum basis divergence.
3. Establish automated alerts for funding rate inflections and margin ratio thresholds across all hedging venues.
4. Implement emergency unravelling protocols that execute simultaneous spot and perpetual market orders if basis divergence exceeds pre-set risk limits.
5. Rebalance collateral daily between spot and futures accounts to maintain balanced leverage ratios.

## Anti-patterns
- Assuming a hedged cash-and-carry trade is risk-free and leaving perpetual margin unmonitored during high volatility events.
- Failing to account for funding rate sign flips that drain margin instead of generating yield.
- Using low-liquidity altcoin spot-perp pairs where widening bid-ask spreads during cascades prevent clean position unwinding.
- Relying on automated cross-margin transfers between separate centralized exchanges that suffer withdrawal suspensions during crashes.

## Done checklist
- [ ] Maximum historical basis expansion calculated for target asset pair.
- [ ] Perpetual leg over-collateralized to withstand extreme basis spikes.
- [ ] Funding rate velocity monitored and automated alerts configured.
- [ ] Inter-leg execution slippage modeled under stressed liquidity conditions.
- [ ] Emergency simultaneous unwind protocol defined and tested.

## Sources
- Deribit Basis Trading and Futures Mechanics: https://www.deribit.com/pages/docs/futures
- Binance Futures Cash and Carry Basis Strategy Guide: https://www.binance.com/en/support/faq/basis-trading-introduction-4199d79998494f1c9c488349257bb5cb
