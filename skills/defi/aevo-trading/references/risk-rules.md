Risk Management Rules for AI Trading:

### Pre-Trade Checklist
1. Always call aevo_risk_check before placing any order
2. Verify margin utilization won't exceed 80% post-trade
3. Check liquidation distance is > 10% for leveraged positions
4. Confirm orderbook has sufficient liquidity (check spread and depth via aevo_get_orderbook)

### Position Limits (Recommended Defaults)
- Max position per instrument: $50,000 notional
- Max total exposure: $200,000 notional
- Max leverage: 20x
- Large order threshold: $10,000+ requires explicit user confirmation

### Session Safety
- Track session PnL — halt if loss exceeds $5,000
- Max 10 orders per minute (rate governor)
- 5 consecutive errors → halt all trading (circuit breaker)
- Always confirm with user before placing orders

### Leverage Rules
- Never set leverage higher than user explicitly requests
- Default to lower leverage when user is ambiguous
- Always set leverage BEFORE placing orders (aevo_update_leverage)

### Stop-Loss Policy
- Every leveraged position should have a stop-loss
- Use aevo_bracket_order for entry + SL + TP in one operation
- For existing positions without stops, recommend adding them

### Order Verification
- After placing an order, verify with aevo_list_orders or aevo_get_order
- After cancellation, verify the order is no longer in open orders
- For bracket orders, verify all 3 legs were placed successfully

### Portfolio Monitoring
- Run aevo_portfolio_risk periodically during active sessions
- Alert user if margin utilization > 70%
- Alert user if any position's liquidation distance < 15%
