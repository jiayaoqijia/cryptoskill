---
name: carry-economics
domain: crypto-trading/carry-economics
trigger: "Evaluate annualized carry yields, funding variance, capital capacity, and cost structures."
anti_trigger: "Rely on headline APY figures without calculating the full operational and execution cost stack."
scope: "Analyzes annualized carry yields, funding variance, capacity constraints, and total cost stacks."
status: seedling
---

## Standard
Evaluating carry strategies requires looking past headline annual percentage yields (APY) to examine the complete economic cost stack. Nominal carry is calculated by annualizing prevailing funding rates, but realized carry fluctuates significantly due to cyclical funding rate variance, interest rate adjustments, and periodic market regimes where funding turns negative. The true return equation incorporates trading commissions for entry and exit, slippage across fragmented order books, spot borrowing interest, and the opportunity cost of locked collateral posted as margin buffers.

Capacity constraints limit the scale at which basis and carry strategies can operate without degrading execution prices. Large capital deployments cause adverse price impact when establishing spot legs and thinning order books when executing short perpetual legs. Furthermore, capital efficiency calculations must account for the collateral required to maintain short positions during high volatility, as excess capital must sit idle as a safety buffer rather than earning active yield. Risk-adjusted return metrics must penalize carry strategies for periods of high funding variance and drawdown exposure.

Primary sources for the claims in this step: <https://www.researchaffiliates.com/publications/journals/829-the-carry-trade-risks-and-rewards> and <https://www.sciencedirect.com/science/article/abs/pii/S0304405X2200153X>.

## Decision rules
- Discount headline funding APY by at least thirty percent to account for historical funding variance and fee drag.
- Incorporate full execution slippage and round-trip trading commissions into projected carry return models.
- Set maximum capital allocation limits based on order book depth to prevent adverse execution impact.
- Account for collateral buffer requirements when computing return on allocated capital versus return on total capital.
- Review and update carry return forecasts weekly to reflect shifting macro interest rates and crypto market regimes.

## Procedure
1. Extract historical funding rate time series for the asset across multiple venues over a ninety-day window.
2. Compute the mean, median, standard deviation, and variance of realized funding rates.
3. Subtract trading commissions, estimated slippage, and borrow costs from the mean annualized funding yield.
4. Calculate net capital efficiency by factoring in required margin buffers and idle collateral reserves.
5. Generate a net risk-adjusted carry report incorporating capacity limits and variance penalties.

## Anti-patterns
- Multiplying the current hourly funding rate by 8,760 hours to project forward annual yield without variance adjustment.
- Ignoring collateral buffer costs when calculating return on total deployed capital.
- Scaling carry strategies beyond venue liquidity limits, resulting in severe execution slippage.
- Assuming stable funding rates across volatile market cycles and structural regime shifts.

## Done checklist
- [ ] Historical funding variance and standard deviation computed.
- [ ] Trading commissions, slippage, and borrow costs subtracted from nominal yield.
- [ ] Capital efficiency and margin buffer requirements factored into return metrics.
- [ ] Capacity limits assessed against order book liquidity.
- [ ] Risk-adjusted net carry report generated.

## Sources
- Research Affiliates Analysis of Carry Trades and Risk Premiums: https://www.researchaffiliates.com/publications/journals/829-the-carry-trade-risks-and-rewards
- Journal of Financial Economics Study on Crypto Derivative Carry and Funding Dynamics: https://www.sciencedirect.com/science/article/abs/pii/S0304405X2200153X
