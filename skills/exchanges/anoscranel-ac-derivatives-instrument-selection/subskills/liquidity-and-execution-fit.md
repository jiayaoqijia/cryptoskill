---
name: liquidity-and-execution-fit
domain: crypto-trading/liquidity-and-execution-fit
trigger: "where is liquidity for this instrument; depth to turnover test; execution friction elimination"
anti_trigger: "how to calculate funding rate; historical backtest performance"
scope: Order book depth, turnover ratios, depth-to-turnover test, and execution friction elimination.
status: seedling
---

## Standard

Theoretical payoff profiles and attractive funding rates are irrelevant if an instrument suffers from prohibitive execution friction. Liquidity in digital asset markets is highly fragmented across spot, perpetuals, dated futures, and options. An instrument may boast high reported trading volume while exhibiting paper-thin order book depth within the top few basis points, resulting in massive slippage for institutional sizing.

A documented venue case demonstrates that among numerous listed perpetual contracts, only a small fraction maintain active liquidity, with quoted depth frequently misaligned with reported turnover. The depth-to-turnover test evaluates whether an order book can absorb position entry and exit without severe market impact. If execution slippage exceeds expected strategy alpha, the instrument must be eliminated from consideration regardless of its theoretical merits.

Primary sources for the claims here: <https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html> and <https://www.bis.org/publ/qtrpdf/r_qt2203e.htm](https://www.bis.org/publ/qtrpdf/r_qt2203e.htm>.

## Decision rules

1. Perform the depth-to-turnover test before selecting any derivative instrument: verify that order book bids and asks within 0.5% cover intended size.
2. Eliminate instruments where quoted turnover is heavily concentrated in wash trading while organic order book depth is negligible.
3. Prioritize spot or perpetual contracts on Tier-1 venues for large-notional execution to minimize market impact costs.
4. Avoid illiquid dated futures or exotic options contracts where widening bid-ask spreads create insurmountable hurdle rates.
5. Apply the one-line test: if execution slippage exceeds expected edge, the instrument is unviable regardless of payoff attractiveness.

## Procedure

1. Inspect order book depth across top five price levels on bid and ask sides for the candidate instrument.
2. Calculate the estimated market impact and round-trip transaction cost for the target position size.
3. Compare reported trading volume against actual visible order book liquidity to detect artificial turnover.
4. Screen alternative instruments or venues if execution friction threatens strategy profitability.
5. Record liquidity verification results and maximum allowable position sizing in the execution plan.

## Anti-patterns

- Relying on headline 24-hour volume statistics without inspecting order book depth and spread width.
- Executing large-notional orders in fragmented altcoin perpetual markets without slicing execution over time.
- Ignoring options market illiquidity, leading to uncloseable positions and wide bid-ask spread penalties.
- Assuming all listed instruments on a centralized or decentralized exchange share equal liquidity guarantees.

## Done checklist

- [ ] Order book depth inspected across top five levels.
- [ ] Market impact and slippage calculated for intended size.
- [ ] Reported volume cross-checked against visible order book liquidity.
- [ ] Alternative venues screened for superior execution fit.
- [ ] Liquidity verification recorded in execution plan.

## Sources

- BIS Market Liquidity and Execution Structure Reports: [https://www.bis.org/publ/qtrpdf/r_qt2203e.htm](https://www.bis.org/publ/qtrpdf/r_qt2203e.htm)
- Derivatives Risk Management and Margin Methodologies: [https://www.cmegroup.com/education/courses/introduction-to-options.html](https://www.cmegroup.com/education/courses/introduction-to-options.html)
- Tail-risk calibration and hedging friction in crypto option surfaces: [https://arxiv.org/abs/2611.00958](https://arxiv.org/abs/2611.00958)
