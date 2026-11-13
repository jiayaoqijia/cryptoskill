---
name: basis-trade
domain: crypto-trading/basis-trade
trigger: "Implement cash-and-carry basis trades between spot and perpetual or calendar futures."
anti_trigger: "Execute basis trades without accounting for margin liquidation risk on the short leg."
scope: "Constructs cash-and-carry spot-perp and calendar basis trades, carry arithmetic, and risk factors."
status: seedling
---

## Standard
The basis trade represents a market-neutral arbitrage strategy exploiting price discrepancies between spot and derivative markets. The classic cash-and-carry structure involves purchasing an asset in the spot market while simultaneously establishing an equivalent short position in perpetual futures or dated calendar futures when the derivative trades at a positive premium. The profit margin, termed the basis, locks in the annualized return derived from perpetual funding payments or the futures premium upon contract expiration.

Execution complexity arises from the asymmetrical risk profile of the two legs. The spot leg requires full capital allocation unless margin is utilized, while the derivative leg operates on margin subject to mark-to-market fluctuations. If spot prices rise sharply, the short perpetual leg incurs unrealized losses requiring continuous collateral top-ups to prevent liquidation, even though the net economic position remains neutral. Additional risks include fluctuating funding rates that compress carry returns, borrowing costs for spot leverage, and execution slippage during market entry and exit.

Primary sources for the claims in this step: <https://www.cmegroup.com/education/courses/introduction-to-futures/basis-trading.html> and <https://academy.binance.com/en/articles/what-is-cash-and-carry-arbitrage>.

## Decision rules
- Calculate net annualized basis yield after subtracting spot borrow fees, transaction commissions, and expected funding variance.
- Maintain adequate collateral buffers on the short perpetual leg to withstand severe upward price shocks without liquidation.
- Monitor funding rate trajectories continuously to ensure positive carry persists above hurdle rate thresholds.
- Execute both spot and derivative legs simultaneously using algorithmic routing to minimize leg-risk slippage.
- Exit or rebalance the basis structure when the premium compresses below transaction cost thresholds.

## Procedure
1. Measure the current basis spread between spot price and perpetual or calendar futures price.
2. Compute estimated annualized carry incorporating transaction fees, funding expectations, and borrow costs.
3. Allocate capital across spot acquisition and short derivative positioning according to risk budget constraints.
4. Execute simultaneous market or pegged limit orders for both legs.
5. Establish automated collateral monitoring rules to manage margin health on the short derivative leg.

## Anti-patterns
- Assuming basis trades are risk-free without accounting for margin call risk on the short derivative leg.
- Failing to factor in trading fees and funding exchange friction when projecting net arbitrage yield.
- Neglecting to monitor sudden funding rate flips that turn positive carry into a sustained negative drag.
- Overleveraging the short futures leg, exposing the position to cascading liquidation risks during market squeezes.

## Done checklist
- [ ] Basis spread and annualized yield calculated with cost deductions.
- [ ] Simultaneous execution plan established for spot and derivative legs.
- [ ] Collateral buffer configured to withstand upward price shocks.
- [ ] Funding rate monitoring and rebalancing triggers defined.
- [ ] Transaction fees and borrow costs factored into net return.

## Sources
- CME Group Introduction to Basis Trading and Cash and Carry: https://www.cmegroup.com/education/courses/introduction-to-futures/basis-trading.html
- Binance Academy Cash and Carry Arbitrage Strategy: https://academy.binance.com/en/articles/what-is-cash-and-carry-arbitrage
