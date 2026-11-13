---
name: perp-versus-dated
domain: crypto-trading/perp-versus-dated
trigger: "perp or dated future; funding risk vs roll risk; basis convergence in futures"
anti_trigger: "how to calculate funding rate; liquidation price calculation"
scope: Funding risk versus expiry/roll risk, basis convergence, and instrument selection trade-offs.
status: seedling
---

## Standard

The choice between perpetual futures and dated futures centers on how holding costs and convergence mechanics are structured over time. Perpetual futures maintain price tethering to the spot index through periodic funding payments exchanged between long and short positions. When funding rates remain persistently positive or negative, perpetual holders experience continuous cash flow drag that can silently outweigh directional price gains during extended holding periods.

Dated futures, by contrast, feature a fixed expiration date where the contract price converges inexorably to the spot index at maturity. They eliminate periodic funding payments, replacing them with an upfront or floating basis (contango or backwardation). However, dated futures introduce roll risk: maintaining exposure across contract expiries requires active position rollover, exposing the trader to basis slippage and transaction friction. Selecting between them requires evaluating whether funding volatility or roll timing presents a greater threat to strategy profitability.

Primary sources for the claims here: <https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html> and <https://www.cftc.gov/LearnAndProtect/EducationCenter/index.htm](https://www.cftc.gov/LearnAndProtect/EducationCenter/index.htm>.

## Decision rules

1. Select perpetual futures when holding duration is short-to-medium term and continuous funding payments align with prevailing market sentiment.
2. Select dated futures when hedging macro exposure over a fixed window where funding rate spikes would introduce unacceptable cash flow unpredictability.
3. Evaluate the term structure of the basis: avoid entering dated contracts in deep contango if holding duration is too short to capture convergence alpha.
4. Execute roll procedures well in advance of contract maturity to avoid liquidity fragmentation and slippage spikes on expiry day.
5. Apply the one-line test: perpetuals trade funding predictability for cash flow drag; dated futures trade roll friction for funding stability.

## Procedure

1. Analyze historical funding rate persistence and magnitude for the target asset over the anticipated holding window.
2. Examine the dated futures term structure across available quarterly and bi-monthly maturities to quantify annualized basis.
3. Compare the cumulative estimated funding expense of perpetuals against the roll friction and basis cost of dated contracts.
4. Select the instrument that minimizes total carry cost over the expected duration.
5. Document the carry mechanism and scheduled roll dates in the risk management ledger.

## Anti-patterns

- Holding perpetual futures through multi-month range-bound markets where cumulative funding payments exceed directional gains.
- Ignoring basis convergence dynamics when trading dated futures in high-volatility regimes.
- Waiting until expiry day to roll dated futures positions, resulting in severe execution slippage.
- Assuming dated futures eliminate all carry costs simply because funding payments are absent.

## Done checklist

- [ ] Cumulative funding cost estimated for perpetual horizon.
- [ ] Term structure and annualized basis calculated for dated futures.
- [ ] Carry cost comparison completed between perpetual and dated options.
- [ ] Roll schedule established for dated futures positions.
- [ ] Carry mechanism documented in risk ledger.

## Sources

- CFTC Futures and Derivatives Market Structure Guidance: [https://www.cftc.gov/LearnAndProtect/EducationCenter/index.htm](https://www.cftc.gov/LearnAndProtect/EducationCenter/index.htm)
- Derivatives Risk Management and Margin Methodologies: [https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html)
- Tail-risk calibration and hedging friction in crypto option surfaces: [https://arxiv.org/abs/2611.00958](https://arxiv.org/abs/2611.00958)
