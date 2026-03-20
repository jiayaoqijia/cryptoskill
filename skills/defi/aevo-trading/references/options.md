Options Strategy Reference:

### Supported Strategies

#### Straddle (Long)
- **Outlook**: Expecting big move, direction unknown
- **Legs**: Buy 1 ATM Call + Buy 1 ATM Put (same strike, same expiry)
- **Max Loss**: Total premium paid
- **Max Profit**: Unlimited (upside) / Strike - premium (downside)
- **Breakeven**: Strike ± total premium
- **Use when**: Expecting volatility spike (earnings, macro events)

#### Strangle (Long)
- **Outlook**: Expecting big move, cheaper than straddle
- **Legs**: Buy 1 OTM Call + Buy 1 OTM Put (different strikes)
- **Max Loss**: Total premium paid
- **Max Profit**: Unlimited
- **Breakeven**: Call strike + premium / Put strike - premium
- **Use when**: Want convexity with less upfront cost

#### Bull Call Spread
- **Outlook**: Moderately bullish
- **Legs**: Buy 1 Call (lower strike) + Sell 1 Call (upper strike)
- **Max Loss**: Net premium paid
- **Max Profit**: Strike difference - net premium
- **Breakeven**: Lower strike + net premium
- **Use when**: Bullish but want to cap cost

#### Bear Put Spread
- **Outlook**: Moderately bearish
- **Legs**: Buy 1 Put (upper strike) + Sell 1 Put (lower strike)
- **Max Loss**: Net premium paid
- **Max Profit**: Strike difference - net premium
- **Breakeven**: Upper strike - net premium
- **Use when**: Bearish but want to cap cost

#### Iron Condor
- **Outlook**: Range-bound, low volatility expected
- **Legs**: Buy OTM Put (far) + Sell OTM Put + Sell OTM Call + Buy OTM Call (far)
- **Max Loss**: Width of wider spread - net credit
- **Max Profit**: Net credit received
- **Breakeven**: Short put - credit / Short call + credit
- **Use when**: Expecting price to stay in range, selling volatility

#### Butterfly
- **Outlook**: Price stays near a specific level
- **Legs**: Buy 1 Call (lower) + Sell 2 Calls (middle) + Buy 1 Call (upper)
- **Max Loss**: Net premium paid
- **Max Profit**: Middle strike - lower strike - net premium
- **Breakeven**: Lower + premium / Upper - premium
- **Use when**: High conviction on a price target

### Using the Tools
1. **Plan**: `aevo_options_leg_builder` — builds strategy with live premiums (read-only)
2. **Preview**: `aevo_execute_strategy` with `dry_run=true` — validates without executing
3. **Execute**: `aevo_execute_strategy` with `dry_run=false` — places real orders
4. **Close**: Use `aevo_close_position` for each leg, or `aevo_cancel_all_orders` for unfilled legs

### Greeks Quick Reference
- **Delta**: Sensitivity to underlying price. Calls: 0 to 1, Puts: -1 to 0
- **Gamma**: Rate of delta change. Highest ATM near expiry
- **Theta**: Time decay. Options lose value daily (negative for buyers)
- **Vega**: Sensitivity to implied volatility. Highest ATM, longer expiry
