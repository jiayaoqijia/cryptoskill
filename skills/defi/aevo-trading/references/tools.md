# AEVO MCP Tools Reference

Complete reference for all 45 AEVO MCP tools. Tools are grouped by category with authentication requirements, parameters, and usage examples.

**Parameter defaults:** `""` means empty string (optional/omitted), numeric defaults shown as values, boolean defaults shown as `true`/`false`.

---

## Market Data (14 tools)

All market data tools are **public** -- no authentication required.

### aevo_list_assets

List all supported assets on the exchange.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

```
aevo_list_assets()
# Returns: ["ETH", "BTC", "SOL", ...]
```

---

### aevo_list_markets

List available markets, optionally filtered by asset or instrument type.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | `""` | No | Filter by asset (e.g. `"ETH"`) |
| instrument_type | string | `""` | No | Filter by type (e.g. `"PERPETUAL"`, `"OPTION"`, `"FUTURE"`) |

```
aevo_list_markets(asset="ETH", instrument_type="PERPETUAL")
```

---

### aevo_get_orderbook

Retrieve the top 10 bids and asks for an instrument.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument name (e.g. `"ETH-PERP"`) |

```
aevo_get_orderbook(instrument_name="ETH-PERP")
# Returns: { bids: [[price, size], ...], asks: [[price, size], ...] }
```

---

### aevo_get_instrument

Full instrument metadata including tick size, min order size, and contract specs.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument name or numeric ID |

```
aevo_get_instrument(instrument_name="ETH-PERP")
aevo_get_instrument(instrument_name="12345")
```

---

### aevo_get_funding_rate

Current funding rate for a perpetual contract.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Perpetual instrument name (e.g. `"ETH-PERP"`) |

```
aevo_get_funding_rate(instrument_name="ETH-PERP")
# Returns: current hourly funding rate
```

---

### aevo_get_funding_history

Historical funding rates for a perpetual contract.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Perpetual instrument name |
| start_time | string | `""` | No | Start timestamp (unix seconds) |
| end_time | string | `""` | No | End timestamp (unix seconds) |
| limit | string | `"50"` | No | Number of records to return |
| offset | string | `""` | No | Pagination offset |

```
aevo_get_funding_history(instrument_name="ETH-PERP", limit="100")
```

---

### aevo_get_trade_history

Recent public trades for an instrument.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument name |

```
aevo_get_trade_history(instrument_name="ETH-PERP")
# Returns: list of recent trades with price, size, side, timestamp
```

---

### aevo_get_statistics

Exchange-wide statistics (volume, open interest, etc.).

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

```
aevo_get_statistics()
```

---

### aevo_get_index_price

Spot reference (index) price for an asset.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | | **Yes** | Asset symbol (e.g. `"ETH"`) |

```
aevo_get_index_price(asset="ETH")
# Returns: current spot index price
```

---

### aevo_get_index_history

Historical index (spot reference) prices for an asset.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | | **Yes** | Asset symbol |
| resolution | string | `""` | No | Candle resolution (e.g. `"1h"`, `"1d"`) |
| start_time | string | `""` | No | Start timestamp (unix seconds) |
| end_time | string | `""` | No | End timestamp (unix seconds) |
| limit | string | `"50"` | No | Number of records |

```
aevo_get_index_history(asset="BTC", resolution="1h", limit="24")
```

---

### aevo_get_mark_history

Historical mark prices for an instrument.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument name |
| resolution | string | `""` | No | Candle resolution |
| start_time | string | `""` | No | Start timestamp (unix seconds) |
| end_time | string | `""` | No | End timestamp (unix seconds) |
| limit | string | `"50"` | No | Number of records |

```
aevo_get_mark_history(instrument_name="ETH-PERP", resolution="1d", limit="30")
```

---

### aevo_get_settlement_history

Settlement history for options/futures.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | `""` | No | Filter by asset |
| start_time | string | `""` | No | Start timestamp (unix seconds) |
| end_time | string | `""` | No | End timestamp (unix seconds) |
| limit | string | `"50"` | No | Number of records |

```
aevo_get_settlement_history(asset="ETH", limit="10")
```

---

### aevo_get_expiries

Available expiry dates for options and futures on an asset.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | | **Yes** | Asset symbol (e.g. `"ETH"`) |

```
aevo_get_expiries(asset="ETH")
# Returns: list of available expiry timestamps
```

---

### aevo_get_server_time

Current exchange server time.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

```
aevo_get_server_time()
# Returns: server timestamp in unix seconds
```

---

## Account & Auth (10 tools)

### aevo_onboard

Start or resume an onboarding session. Returns current status and recommended next steps.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

**Auth required:** No

```
aevo_onboard()
# Returns: { status: "...", next_steps: [...] }
```

---

### aevo_get_status

Runtime and identity context -- shows current session state, environment, and whether credentials are loaded.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

**Auth required:** No

```
aevo_get_status()
```

---

### aevo_authenticate

Store session credentials for subsequent authenticated calls. Does not make an API call itself.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| api_key | string | `""` | No | API key |
| api_secret | string | `""` | No | API secret |
| wallet_address | string | `""` | No | Ethereum wallet address |
| wallet_private_key | string | `""` | No | Wallet private key (for signing) |
| signing_key_private_key | string | `""` | No | Signing key private key |

**Auth required:** No (this tool *stores* credentials)

```
aevo_authenticate(
    api_key="ak-...",
    api_secret="as-...",
    signing_key_private_key="0x..."
)
```

---

### aevo_clear_auth

Clear all stored session credentials.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

**Auth required:** No

```
aevo_clear_auth()
```

---

### aevo_get_account

Account summary including balance, equity, available margin, and margin usage.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_get_account()
```

---

### aevo_get_portfolio

Portfolio summary with PnL, Greeks, and position aggregates.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_get_portfolio()
# Returns: { pnl, greeks: { delta, gamma, theta, vega }, ... }
```

---

### aevo_get_positions

List all open positions.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_get_positions()
# Returns: list of open positions with instrument, size, entry price, PnL
```

---

### aevo_update_leverage

Update leverage for a specific instrument.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument name (e.g. `"ETH-PERP"`) |
| leverage | integer | | **Yes** | New leverage value |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_update_leverage(instrument_name="ETH-PERP", leverage=5)
```

---

### aevo_get_trade_fills

Account trade fill history with filtering.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| start_time | string | `""` | No | Start timestamp (unix seconds) |
| end_time | string | `""` | No | End timestamp (unix seconds) |
| limit | string | `"50"` | No | Number of records |
| offset | string | `""` | No | Pagination offset |
| trade_types | string | `""` | No | Filter by trade type |
| instrument_name | string | `""` | No | Filter by instrument |
| instrument_type | string | `""` | No | Filter by instrument type |
| asset | string | `""` | No | Filter by asset |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_get_trade_fills(instrument_name="ETH-PERP", limit="20")
```

---

### aevo_get_order_history

Account order history with the same filtering options as trade fills.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| start_time | string | `""` | No | Start timestamp (unix seconds) |
| end_time | string | `""` | No | End timestamp (unix seconds) |
| limit | string | `"50"` | No | Number of records |
| offset | string | `""` | No | Pagination offset |
| trade_types | string | `""` | No | Filter by trade type |
| instrument_name | string | `""` | No | Filter by instrument |
| instrument_type | string | `""` | No | Filter by instrument type |
| asset | string | `""` | No | Filter by asset |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_get_order_history(asset="ETH", limit="50")
```

---

## Order Management (7 tools)

All order management tools require **authentication**.

### aevo_list_orders

List all currently open orders.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

```
aevo_list_orders()
```

---

### aevo_get_order

Retrieve a single order by its ID.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| order_id | string | | **Yes** | Order ID to look up |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

```
aevo_get_order(order_id="0xabc123...")
```

---

### aevo_build_order

Build and sign an order **without submitting** it. Useful for preview, dry-run, or multi-step workflows.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument to trade |
| is_buy | boolean | | **Yes** | `true` for buy, `false` for sell |
| amount | string | | **Yes** | Order size |
| limit_price | string | | **Yes** | Limit price |
| salt | string | `""` | No | Custom salt for order uniqueness |
| order_timestamp | integer | `0` | No | Custom timestamp |
| post_only | boolean | `false` | No | Post-only (maker) order |
| reduce_only | boolean | `false` | No | Reduce-only order |
| time_in_force | string | `"GTC"` | No | `"GTC"`, `"IOC"`, `"FOK"` |
| mmp | boolean | `false` | No | Market maker protection |
| stop | string | `""` | No | Stop type |
| trigger | string | `""` | No | Trigger price for stop orders |
| close_position | boolean | `false` | No | Close entire position |
| partial_position | boolean | `false` | No | Allow partial fill of position close |

```
aevo_build_order(
    instrument_name="ETH-PERP",
    is_buy=true,
    amount="0.1",
    limit_price="3000"
)
# Returns: signed order payload (not submitted)
```

---

### aevo_create_order

Build, sign, and **submit** an order to the exchange. **CAUTION: This places a real order.**

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument to trade |
| is_buy | boolean | | **Yes** | `true` for buy, `false` for sell |
| amount | string | | **Yes** | Order size |
| limit_price | string | | **Yes** | Limit price |
| salt | string | `""` | No | Custom salt |
| order_timestamp | integer | `0` | No | Custom timestamp |
| post_only | boolean | `false` | No | Post-only (maker) order |
| reduce_only | boolean | `false` | No | Reduce-only order |
| time_in_force | string | `"GTC"` | No | `"GTC"`, `"IOC"`, `"FOK"` |
| mmp | boolean | `false` | No | Market maker protection |
| stop | string | `""` | No | Stop type |
| trigger | string | `""` | No | Trigger price |
| close_position | boolean | `false` | No | Close entire position |
| partial_position | boolean | `false` | No | Allow partial fill |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

```
aevo_create_order(
    instrument_name="ETH-PERP",
    is_buy=true,
    amount="0.1",
    limit_price="3000",
    post_only=true
)
# WARNING: Places a real order on the exchange
```

---

### aevo_cancel_order

Cancel a single open order by its ID.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| order_id | string | | **Yes** | Order ID to cancel |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

```
aevo_cancel_order(order_id="0xabc123...")
```

---

### aevo_cancel_orders

Cancel multiple orders by their IDs.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| order_ids | list[string] | | **Yes** | List of order IDs to cancel |
| instrument_type | string | `""` | No | Filter by instrument type |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

```
aevo_cancel_orders(order_ids=["0xabc...", "0xdef..."])
```

---

### aevo_cancel_all_orders

Cancel **ALL** open orders. Optionally filter by asset or instrument type. **DESTRUCTIVE: cancels everything matching the filter (or all orders if no filter).**

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | `""` | No | Cancel only orders for this asset |
| instrument_type | string | `""` | No | Cancel only orders of this type |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

```
aevo_cancel_all_orders()                          # Cancel everything
aevo_cancel_all_orders(asset="ETH")               # Cancel all ETH orders
aevo_cancel_all_orders(instrument_type="OPTION")  # Cancel all option orders
```

---

## Analysis (4 tools)

All analysis tools are **read-only** and require **no authentication**. They aggregate market data into actionable insights.

### aevo_funding_analysis

Funding rate trend analysis for a perpetual contract.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Perpetual instrument name (e.g. `"ETH-PERP"`) |

**Returns:** Current rate, 7-day average, annualized percentage, percentile ranking, trend direction, persistence metric.

```
aevo_funding_analysis(instrument_name="ETH-PERP")
# Returns: {
#   current_rate, avg_7d, annualized_pct,
#   percentile, trend, persistence
# }
```

---

### aevo_volatility_snapshot

Realized volatility and implied volatility snapshot for an asset.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | | **Yes** | Asset symbol (e.g. `"ETH"`) |

**Returns:** 7-day and 30-day realized volatility, ATM implied volatility, regime classification.

```
aevo_volatility_snapshot(asset="ETH")
# Returns: {
#   realized_vol_7d, realized_vol_30d,
#   atm_iv, regime
# }
```

---

### aevo_market_regime

Market regime classification based on price action analysis.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | | **Yes** | Asset symbol (e.g. `"BTC"`) |

**Returns:** Regime (`trending_up`, `trending_down`, `ranging`, `volatile`), confidence score, support level, resistance level.

```
aevo_market_regime(asset="BTC")
# Returns: {
#   regime: "trending_up", confidence: 0.82,
#   support: 62000, resistance: 68000
# }
```

---

### aevo_basis_analysis

Perpetual-to-spot basis analysis showing premium or discount.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| asset | string | | **Yes** | Asset symbol (e.g. `"ETH"`) |

**Returns:** Premium/discount in basis points, annualized percentage, 7-day statistics, percentile ranking.

```
aevo_basis_analysis(asset="ETH")
# Returns: {
#   basis_bps, annualized_pct,
#   stats_7d: { min, max, avg },
#   percentile
# }
```

---

## Risk (3 tools)

All risk tools require **authentication**.

### aevo_portfolio_risk

Aggregate portfolio risk metrics.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Returns:** Net Greeks (delta, gamma, theta, vega), margin utilization percentage, liquidation distance, position concentration breakdown.

```
aevo_portfolio_risk()
# Returns: {
#   net_delta, net_gamma, net_theta, net_vega,
#   margin_pct, liquidation_distance, concentration
# }
```

---

### aevo_position_risk

Per-position risk detail. If no instrument specified, returns risk for all positions.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | `""` | No | Filter to a specific instrument |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Returns:** PnL, equity percentage, liquidation distance, funding cost, time decay (theta).

```
aevo_position_risk(instrument_name="ETH-PERP")
# Returns: {
#   pnl, equity_pct, liquidation_distance,
#   funding_cost, time_decay
# }
```

---

### aevo_risk_check

Pre-trade risk validation. Simulates the impact of a hypothetical trade **without placing an order**.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument to simulate |
| side | string | | **Yes** | `"buy"` or `"sell"` |
| amount | string | | **Yes** | Trade size |
| limit_price | string | `""` | No | Price to simulate at (uses mark if omitted) |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Returns:** Post-trade margin usage, delta change, estimated slippage, pass/fail verdict.

```
aevo_risk_check(
    instrument_name="ETH-PERP",
    side="buy",
    amount="1.0",
    limit_price="3000"
)
# Returns: {
#   post_trade_margin_pct, delta_change,
#   slippage_bps, verdict: "pass"
# }
```

---

## Strategy (4 tools)

### aevo_bracket_order

Place an entry order with attached stop-loss and take-profit orders. **CAUTION: Places real orders.**

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument to trade |
| is_buy | boolean | | **Yes** | `true` for long entry, `false` for short entry |
| amount | string | | **Yes** | Order size |
| entry_price | string | | **Yes** | Entry limit price |
| stop_loss_price | string | | **Yes** | Stop-loss trigger price |
| take_profit_price | string | | **Yes** | Take-profit trigger price |
| time_in_force | string | `"GTC"` | No | Time in force for all legs |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_bracket_order(
    instrument_name="ETH-PERP",
    is_buy=true,
    amount="0.5",
    entry_price="3000",
    stop_loss_price="2900",
    take_profit_price="3200"
)
# WARNING: Places 3 real orders (entry + SL + TP)
```

---

### aevo_close_position

Close an existing position via a reduce-only order. **CAUTION: Places a real order.**

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| instrument_name | string | | **Yes** | Instrument with open position |
| limit_price | string | `""` | No | Limit price (uses market if omitted) |
| time_in_force | string | `"GTC"` | No | Time in force |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes

```
aevo_close_position(instrument_name="ETH-PERP")
# WARNING: Closes your entire ETH-PERP position
```

---

### aevo_options_leg_builder

Build an options strategy plan with live premiums. **Read-only -- does NOT execute any trades.**

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| strategy_type | string | | **Yes** | One of: `straddle`, `strangle`, `bull_call_spread`, `bear_put_spread`, `iron_condor`, `butterfly` |
| asset | string | | **Yes** | Underlying asset (e.g. `"ETH"`) |
| expiry | string | | **Yes** | Expiry date |
| strike | string | `""` | No | Strike price (for straddle) |
| lower_strike | string | `""` | No | Lower strike (for strangle) |
| upper_strike | string | `""` | No | Upper strike (for strangle) |
| put_strike | string | `""` | No | Put strike |
| call_strike | string | `""` | No | Call strike |
| put_buy_strike | string | `""` | No | Put buy strike (for iron condor) |
| put_sell_strike | string | `""` | No | Put sell strike (for iron condor) |
| call_sell_strike | string | `""` | No | Call sell strike (for iron condor) |
| call_buy_strike | string | `""` | No | Call buy strike (for iron condor) |
| amount | string | `"1"` | No | Number of contracts per leg |

**Auth required:** No

```
aevo_options_leg_builder(
    strategy_type="straddle",
    asset="ETH",
    expiry="2026-03-28",
    strike="3000"
)
# Returns: leg breakdown with live premiums, net debit/credit, max profit/loss
```

---

### aevo_execute_strategy

Execute a multi-leg options or futures strategy. **CAUTION: Places real orders unless `dry_run=true`.**

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| legs | list[dict] | | **Yes** | List of leg definitions (instrument, side, amount, price) |
| dry_run | boolean | `false` | No | If `true`, simulate only -- no orders placed |
| time_in_force | string | `"GTC"` | No | Time in force for all legs |
| api_key | string | `""` | No | Override stored API key |
| api_secret | string | `""` | No | Override stored API secret |

**Auth required:** Yes (unless `dry_run=true`)

```
# Dry run (safe)
aevo_execute_strategy(
    legs=[
        {"instrument_name": "ETH-20260328-3000-C", "is_buy": true, "amount": "1", "limit_price": "150"},
        {"instrument_name": "ETH-20260328-3000-P", "is_buy": true, "amount": "1", "limit_price": "140"}
    ],
    dry_run=true
)

# Live execution (REAL ORDERS)
aevo_execute_strategy(
    legs=[
        {"instrument_name": "ETH-20260328-3000-C", "is_buy": true, "amount": "1", "limit_price": "150"},
        {"instrument_name": "ETH-20260328-3000-P", "is_buy": true, "amount": "1", "limit_price": "140"}
    ]
)
```

---

## System (2 tools)

Both system tools are **public** -- no authentication required.

### aevo_ping

Simple health check / liveness probe.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

```
aevo_ping()
# Returns: "pong" or equivalent
```

---

### aevo_healthcheck

Verify connectivity to the AEVO API and confirm the service is operational.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| *(none)* | | | | |

```
aevo_healthcheck()
# Returns: connectivity status and latency
```

---

## Registration (1 tool)

### aevo_register_account

Register a signing key with the exchange and obtain API credentials. Requires wallet and signing key private keys to be set via `aevo_authenticate` first.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| key_expiry | string | `""` | No | Signing key expiry timestamp |
| no_api_key | boolean | `false` | No | If `true`, skip API key generation |
| referral_code | string | `""` | No | Referral code |
| wallet_address | string | `""` | No | Override wallet address |
| store_credentials | boolean | `true` | No | Auto-store returned credentials in session |

**Auth required:** Requires wallet + signing key private keys (set via `aevo_authenticate`)

```
# First, set wallet credentials
aevo_authenticate(
    wallet_address="0x...",
    wallet_private_key="0x...",
    signing_key_private_key="0x..."
)

# Then register
aevo_register_account(referral_code="MYREF")
# Returns: API key, API secret (auto-stored if store_credentials=true)
```

---

## Quick Reference: Tool Count by Category

| Category | Count | Auth Required |
|----------|-------|---------------|
| Market Data | 14 | No |
| Account & Auth | 10 | Mixed (5 yes, 5 no) |
| Order Management | 7 | Yes |
| Analysis | 4 | No |
| Risk | 3 | Yes |
| Strategy | 4 | Mixed (3 yes, 1 no) |
| System | 2 | No |
| Registration | 1 | Wallet keys required |
| **Total** | **45** | |

> **Note:** The 45 total includes 4 Analysis tools and 4 Strategy tools that are composite/analytical wrappers built on top of the base exchange API.
