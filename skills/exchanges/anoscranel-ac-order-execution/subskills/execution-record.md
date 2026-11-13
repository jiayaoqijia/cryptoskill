---
name: execution-record
domain: crypto-trading/execution-record
trigger: execution record, fill audit, arrival price, slippage measurement, transaction cost analysis
anti_trigger: trade journal, pre-trade memo, risk budget, strategy thesis
scope: Detailed execution logging, TCA metrics, and fill benchmark attribution
status: seedling
---

## Standard

An institutional execution record provides the empirical foundation for Transaction Cost Analysis (TCA) and performance attribution. Unlike subjective trade journals that record narrative rationales, the execution record captures objective, timestamped market data points for every parent order and child fill. Key required fields include decision timestamp, arrival midpoint price, routing venue, order type and modifiers, exact fill timestamps, executed quantities, fill prices, commission fees, and realized slippage versus benchmark prices. Rigorous execution recordkeeping isolates alpha generation from execution leakage, allowing operators to quantify exactly how much return is lost to spread crossing, poor routing, and market impact across centralized and decentralized venues.

Primary sources for the claims here: <https://www.cfainstitute.org/en/research/foundation/2020/transaction-cost-analysis> and <https://www.fiatchains.com/crypto-tca-standards/>.

## Decision rules

- Log the exact arrival timestamp and prevailing mid-market price programmatically at the moment an order decision is finalized.
- Capture every individual fill report with microsecond-level precision rather than relying solely on aggregated average execution prices.
- Record all fee components separately, categorizing maker rebates and taker fees distinctly to evaluate venue cost efficiency.
- Benchmark execution quality against arrival midpoint, VWAP, and implementation shortfall standards.
- Audit execution records periodically to detect systematic execution anomalies, venue latency issues, or recurring slippage bias.

## Procedure

1. Initialize order tracking object upon signal generation, recording strategy ID, intent, and target size.
2. Capture arrival reference data via API websocket feeds at dispatch time: best bid, best ask, and mid price.
3. Collect all exchange execution fill messages in an immutable audit log, recording order ID, trade ID, timestamp, price, and quantity.
4. Compute TCA metrics post-trade: implementation shortfall, basis points of slippage, total fees paid, and net execution cost.
5. Store the structured execution record in the permanent vault database for quantitative TCA reporting and strategy review.

## Anti-patterns

- Recording only rounded entry and exit prices while ignoring intra-trade fill dispersion and partial execution details.
- Confusing strategy alpha generation with execution outperformance caused by favorable market drift.
- Failing to track exchange fees and maker/taker tier structures in the execution ledger.

## Done checklist

- [ ] Arrival midpoint and timestamp captured programmatically at order dispatch.
- [ ] Immutable log of all fill reports and execution quantities maintained.
- [ ] TCA metrics (slippage, implementation shortfall, fees) computed per order.
- [ ] Execution record archived in permanent vault storage.


Additionally, storing transaction cost analysis datasets in structured timeseries databases enables automated reporting and rapid identification of latency degradation across distinct API gateway routes.
## Sources

- Transaction Cost Analysis in Digital Asset Markets: Best Practices and Metrics: https://www.cfainstitute.org/en/research/foundation/2020/transaction-cost-analysis
- Execution Data Standards for Institutional Crypto Trading: https://www.fiatchains.com/crypto-tca-standards/
