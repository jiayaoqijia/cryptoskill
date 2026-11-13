---
name: execution-failure-modes
domain: crypto-trading/execution-failure-modes
trigger: execution failure, rejected order, venue halt, partial fill, stale quote, STP
anti_trigger: strategy backtest, historical analysis, risk budgeting, portfolio rebalancing
scope: Handling execution failures, order rejections, exchange halts, and self-trade prevention
status: seedling
---

## Standard

Execution failures occur when order routing or matching engine mechanics diverge from expected parameters due to venue outages, API rejections, partial fills, stale quotes, or self-trade prevention (STP) triggers. During high-volatility events, exchanges frequently throttle API requests, reject orders due to risk limits, or trigger circuit breakers that freeze matching. Operators must maintain a robust fallback ladder to handle execution failures without panicking or exposing unhedged delta risk. Crucially, when an order execution fails or hangs, operators must never blindly resubmit identical market orders without checking open position state, as duplicate fills can instantly double unintentional risk exposure across trading accounts.

Primary sources for the claims here: <https://www.coindesk.com/markets/2021/05/19/crypto-exchange-outages-risk-management/> and <https://www.usenix.org/conference/nsdi20/presentation/andersen>.

## Decision rules

- Never blindly resubmit unconfirmed or failed orders without first querying the exchange account state to verify whether the initial order filled or rested.
- Implement automated self-trade prevention (STP) configurations (e.g., cancel-newest, cancel-oldest) to prevent crossing internal resting liquidity.
- Establish a strict fallback ladder for venue API disconnects: switch routing to secondary liquidity venues or execute emergency risk reduction via pre-approved secondary channels.
- Handle partial fills gracefully by updating remaining child order quantities rather than issuing aggressive market sweeps to cover the delta.
- Abort automated execution routines immediately upon detecting stale quote feeds, anomalous price gapping, or exchange websocket heartbeat failures.

## Procedure

1. Detect execution failure event: capture API error codes, rejection payloads, websocket disconnects, or timeout exceptions.
2. Query active position state and open orders via REST endpoints to reconcile local ledger with exchange reality.
3. Classify failure mode: API rate limit, insufficient margin, venue halt, self-trade prevention trigger, or network timeout.
4. Execute fallback protocol: pause automated routing, cancel unexecuted dangling orders, or reroute through secondary backup venues if necessary.
5. Log failure incident in the execution audit ledger with complete error payloads and recovery timestamps.

## Anti-patterns

- Blindly spamming order resubmissions after an API timeout without verifying prior order fill status, leading to catastrophic overfills.
- Ignoring self-trade prevention warnings and allowing proprietary accounts to cross against each other, incurring unnecessary fees and volume distortion.
- Continuing trade execution despite detecting stale quote feeds or broken websocket heartbeats.

## Done checklist

- [ ] Exchange state queried and reconciled immediately upon any order rejection or timeout.
- [ ] Self-trade prevention parameters configured on all routing accounts.
- [ ] Fallback ladder activated and logged during venue disconnect events.
- [ ] Execution failure recorded in the permanent audit ledger.

## Sources

- API Error Handling and Execution Resilience in High-Frequency Trading: https://www.usenix.org/conference/nsdi20/presentation/andersen
- Exchange Outage Protocols and Risk Management for Crypto Derivatives: https://www.coindesk.com/markets/2021/05/19/crypto-exchange-outages-risk-management/
