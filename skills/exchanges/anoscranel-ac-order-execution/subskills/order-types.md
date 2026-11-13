---
name: order-types
domain: crypto-trading/order-types
trigger: order type, market, limit, stop-market, stop-limit, post-only, IOC, FOK, reduce-only
anti_trigger: perp venue diligence, venue risk, margin mode, liquidation price
scope: Order types and execution primitives in perpetual futures and spot markets
status: seedling
---

## Standard

Order types are the elementary instructions sent to an exchange matching engine. Choosing the correct order primitive determines whether an execution incurs maker rebates or taker fees, whether fills are guaranteed or bounded by price, and whether position state is accidentally inverted during high-volatility events. In electronic order books, market orders cross the spread immediately, paying taker fees and absorbing available book depth up to the requested size. Limit orders rest on the book, providing liquidity and earning maker rebates but risking non-execution if price moves away. Advanced modifiers—such as Post-Only, Immediate-or-Cancel (IOC), Fill-or-Kill (FOK), and Reduce-Only—control routing behavior and safeguard against unintentional position flipping or maker fee penalties on aggressive entries.

Primary sources for the claims here: <https://bybit-exchange.github.io/docs/derivatives/v5/order/create-order> and <https://binance-docs.github.io/apidocs/futures/en/#trade-s-endpoints>.

## Decision rules

- Use limit orders for routine entries and exits when execution certainty is secondary to price improvement and fee minimization.
- Use market orders strictly when immediate execution is required to avoid adverse selection in fast-moving markets, accepting known slippage and taker fees.
- Use Post-Only modifiers on all resting limit orders to guarantee maker status; if the limit price crosses the opposing book, the order cancels automatically rather than executing as a taker.
- Use Reduce-Only modifiers on every exit, stop, or take-profit order to ensure the order can only decrease or close an existing open position, preventing accidental position reversal if fills mismatch.
- Use Immediate-or-Cancel (IOC) or Fill-or-Kill (FOK) when sweeping specific book depth without resting unexecuted remainder sizes on the order book.

## Procedure

1. Evaluate the urgency of the trade: determine if price bounds (limit) or time-to-fill bounds (market/IOC) take priority under current market conditions.
2. Select the base primitive: Limit for resting liquidity, Market for immediate crossing.
3. Apply exchange modifiers: attach Post-Only for maker entries; attach Reduce-Only for position exits and risk stops.
4. Submit the order payload to the matching engine API endpoint.
5. Verify execution feedback via WebSocket or REST response: confirm fill price, fee tier (maker vs taker), and resulting net position size.

## Anti-patterns

- Submitting raw limit orders without Post-Only during high volatility, resulting in unintentional aggressive crossing and higher taker fees.
- Using standard limit or stop orders for exits without Reduce-Only flags, which can flip a short position into an accidental long position if fills cross unexpectedly.
- Relying on market orders during thin liquidity intervals, causing extreme slippage against sparse book depth.
- Treating Stop-Market orders as guaranteed price execution bounds rather than conditional market triggers.

## Done checklist

- [ ] Base order primitive (limit/market) matches urgency and fee constraints.
- [ ] Post-Only flag verified for resting liquidity orders.
- [ ] Reduce-Only flag verified for all exit and stop orders.
- [ ] Exchange execution confirmation received and logged.

## Sources

- Binance Futures API Documentation, Order Types and Modifiers: https://binance-docs.github.io/apidocs/futures/en/#trade-s-endpoints
- Bybit API Documentation, Order Execution and Reduce-Only Behavior: https://bybit-exchange.github.io/docs/derivatives/v5/order/create-order
