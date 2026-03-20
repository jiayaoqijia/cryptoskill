Common Trading Workflows:

### 1. Session Setup
```
aevo_onboard → check status
  → if unauthenticated: collect credentials → aevo_authenticate
  → aevo_get_account → verify balance
  → aevo_get_positions → check existing exposure
```

### 2. Market Analysis
```
aevo_get_index_price (spot reference)
aevo_market_regime (trend classification)
aevo_funding_analysis (funding trend for perps)
aevo_volatility_snapshot (vol regime)
aevo_basis_analysis (perp premium/discount)
aevo_get_orderbook (liquidity check)
→ Synthesize into market view
```

### 3. Place a Trade
```
1. Analyze: market data + regime + funding
2. Risk check: aevo_risk_check (instrument, side, amount)
3. Set leverage: aevo_update_leverage (if needed)
4. Confirm with user: show trade details + risk assessment
5. Execute: aevo_create_order or aevo_bracket_order
6. Verify: aevo_get_order or aevo_list_orders
```

### 4. Portfolio Review
```
aevo_get_account (balance, equity, margin)
aevo_get_portfolio (PnL, Greeks)
aevo_get_positions (all positions)
aevo_portfolio_risk (aggregate risk)
aevo_position_risk (per-position risk)
→ Synthesize: recommendations, risk alerts, rebalancing suggestions
```

### 5. Close a Position
```
aevo_get_positions → find the position
aevo_get_orderbook → check current prices
aevo_close_position (instrument_name, optional limit_price)
→ Verify position is closed
```

### 6. Cancel Orders
```
Single: aevo_cancel_order(order_id) → verify
Multiple: aevo_cancel_orders(order_ids) → verify
All: aevo_cancel_all_orders (DESTRUCTIVE — confirm with user first)
```

### 7. Options Strategy
```
1. aevo_get_expiries(asset) → pick expiry
2. aevo_list_markets(asset, "OPTION") → find available strikes
3. aevo_volatility_snapshot(asset) → vol context
4. aevo_options_leg_builder(strategy_type, asset, expiry, strikes...) → preview
5. Review max profit/loss, breakevens, Greeks with user
6. aevo_execute_strategy(legs, dry_run=true) → dry run
7. aevo_execute_strategy(legs) → execute (with user confirmation)
```

### 8. Hedge Portfolio
```
aevo_get_positions → current exposure
aevo_portfolio_risk → net Greeks
aevo_volatility_snapshot → vol context
→ Identify delta/vega exposure to hedge
→ Recommend hedge: perp (delta), options (gamma/vega)
→ Use aevo_risk_check on proposed hedge
→ Execute with user confirmation
```
