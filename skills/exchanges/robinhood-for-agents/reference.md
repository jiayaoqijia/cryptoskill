# MCP Tools Reference

## Auth

### robinhood_check_session
Check whether there is a *working* Robinhood session. Loads the cached tokens **and probes the API** with them — it does not report healthy merely because tokens exist in the keychain.

**Parameters:** none

**Response:** `{ "status": "logged_in" | "expired" | "unknown" | "not_authenticated", "method": "keychain" | "encrypted_file" | "token", "account_hint": "...1234", "message": "..." }`

| `status` | Meaning | What to do |
|---|---|---|
| `logged_in` | verified working; `account_hint` is the masked account number | proceed |
| `expired` | tokens exist but are dead and automatic refresh could not recover them | run `robinhood_browser_login` |
| `unknown` | the probe failed for a transient/network reason — the session may well be fine | retry; **do not** assume expired, do not re-login |
| `not_authenticated` | no tokens in the store at all | run `robinhood_browser_login` |

`account_hint` is present only on `logged_in`; `message` carries the reason on `expired` / `unknown` / `not_authenticated`. This tool makes a live API call, so it is not free — check once at the start of a session, not before every tool call.

### robinhood_browser_login
Open Chrome for browser-based Robinhood login. Captures OAuth tokens automatically. This is the remedy for `robinhood_check_session` returning `expired` or `not_authenticated` — and the *only* remedy; there is no programmatic re-auth.

**Parameters:** none

**Response:** `{ "status": "logged_in", "account_hint": "...1234" }`

**Timeout note for MCP client authors:** this call waits up to 5 minutes server-side for the user to complete login (including MFA) before the OAuth token exchange resolves. Most MCP SDKs default `callTool`'s request timeout to 60 seconds, which is shorter than that — if you're driving this tool programmatically (not through Claude Code, which already handles this), pass a longer per-call timeout (e.g. the TypeScript SDK's `client.callTool(params, resultSchema, { timeout: 330_000 })`) or the call will abort client-side while the user is still mid-login.

### robinhood_get_account
Get account details, profile, and investment preferences.

**Parameters:**
- `info_type` (enum: "all", "account", "user", "investment", default: "all")

**Response:**
```json
{
  "account": { "account_number": "123", "buying_power": "2000.00" },
  "user": { "username": "user@email.com", "first_name": "John" },
  "investment": { "risk_tolerance": "moderate" }
}
```

### Session errors on any tool
Tokens renew automatically — proactively ~24h before expiry, and again on a 401. When a tool still returns an error containing `session expired and could not be refreshed`, refresh has already been tried and failed: run `robinhood_browser_login`, don't retry the tool. Refresh tokens are single-use and rotate on every renewal, so avoid driving the same session from a second process (a `bun -e` script alongside this server) — one of them will be poisoned.

## Account & Portfolio

### robinhood_get_accounts
Get all brokerage accounts (multi-account support).

**Parameters:** none

**Response:**
```json
{
  "accounts": [{ "account_number": "123", "type": "cash", "cash": "1000.00", "buying_power": "2000.00" }]
}
```

### robinhood_get_portfolio
Get complete portfolio: positions with P&L, equity, buying power, cash.

**Parameters:**
- `account_number` (string, optional) — specific account
- `with_dividends` (boolean, default: false) — include dividend info

**Response:**
```json
{
  "holdings": {
    "AAPL": {
      "price": "150.00", "quantity": "10", "average_buy_price": "120.00",
      "equity": "1500.00", "percent_change": "25.0", "name": "Apple"
    }
  },
  "summary": {
    "equity": "15000.00", "market_value": "14000.00", "cash": "1000.00",
    "buying_power": "2000.00", "crypto_buying_power": "500.00",
    "total_equity": "15000.00", "total_market_value": "14000.00", "options_buying_power": "2000.00",
    "equity_market_value": "14000.00", "option_market_value": "0.00", "futures_market_value": "0.00",
    "event_contracts_market_value": "0.00", "pending_deposits": "0.00", "currency": "USD"
  },
  "unified": { "...": "full bonfire unified snapshot" },
  "live": { "...": "per-asset-class market values + cash" }
}
```
The `summary` now includes bonfire `unified` + `live` parity fields; the full `unified`/`live` objects are also returned.

**Multi-account caveat:** when `account_number` is a non-default account (from `robinhood_get_accounts`), `unified` comes back `null` and the six `unified`-sourced summary fields (`total_equity`, `total_market_value`, `portfolio_equity`, `options_buying_power`, `uninvested_cash`, `withdrawable_cash`) are omitted — bonfire's unified-portfolio endpoint only recognizes the account Robinhood treats as default, and 404s for every other real account_number. `holdings`, the original `equity`/`cash`/`buying_power` fields, and `live` are unaffected and always populated. This is a live Robinhood API quirk, not a bug in this server — don't retry or treat a `null` `unified` as an error.

### robinhood_get_equity_positions
Get raw equity positions (shares, average buy price) without holding enrichment.

**Parameters:**
- `account_number` (string, optional) — omit for all accounts
- `nonzero` (boolean, default: true) — only non-zero quantities

**Response:** `{ "positions": [{ "instrument": "...", "quantity": "10", "average_buy_price": "120.00" }] }`

### robinhood_get_equity_tax_lots
Open tax lots for one equity holding (one symbol per call). A real endpoint passthrough (not computed): `GET /tax_lots/open/{account}/{instrument}/`. Symbol is resolved by exact match. Each lot reports `quantity`, `quantity_available`, `book_cost_basis`, `tax_cost_basis`, `book_proceeds`, `open_date`, `term` (long/short-term), `is_selectable`, `open_lot_id`, `order_id`, and `cost_per_share`. Per-lot account numbers are scrubbed — only the caller-supplied `account_number` is echoed back. Results are complete (`next_cursor` always null: a tax-lots page URL embeds the account number, so no cursor is surfaced).

**Parameters:**
- `account_number` (string, required)
- `symbol` (string, required) — single equity symbol
- `cursor` (string, optional) — accepted for parity, but results are always complete

**Response:** `{ "account_number": "...", "symbol": "AAPL", "tax_lots": [{ "quantity": "10", "quantity_available": "10", "book_cost_basis": "1200.00", "tax_cost_basis": "1200.00", "book_proceeds": "0.00", "open_date": "2025-01-15", "term": "long_term", "is_selectable": true, "open_lot_id": "...", "order_id": "...", "cost_per_share": "120.00" }], "next_cursor": null }`

## Crypto

### robinhood_get_crypto
Get a crypto quote, price history, or positions.

**Parameters:**
- `info_type` (enum: "quote", "historicals", "positions", default: "quote")
- `symbol` (string, required for "quote" and "historicals", e.g. "BTC")
- `interval` (enum: "15second", "5minute", "10minute", "hour", "day", "week", default: "day") — for historicals
- `span` (enum: "hour", "day", "week", "month", "3month", "year", "5year", default: "month") — for historicals

## Research

### robinhood_get_stock_quote
Get quote and fundamentals. Also works for index symbols (SPX, NDX, VIX, RUT, XSP).

**Parameters:**
- `symbols` (string, required) — comma-separated, e.g. "AAPL" or "AAPL,MSFT"

**Response:**
```json
{
  "AAPL": {
    "quote": { "last_trade_price": "150.00", "bid_price": "149.90", "ask_price": "150.10", "previous_close": "148.00", "pe_ratio": "25.5" },
    "fundamentals": { "market_cap": "2500000000000", "pb_ratio": "45.20", "dividend_yield": "0.55", "high_52_weeks": "180.00", "low_52_weeks": "120.00" }
  }
}
```

### robinhood_get_fundamentals
Get company fundamentals (no live quote). Use `robinhood_get_stock_quote` if you also need the current price.

**Parameters:**
- `symbols` (string, required) — comma-separated, e.g. "AAPL" or "AAPL,MSFT"

**Response:** keyed by symbol; each value is the fundamentals object (`float`, `shares_outstanding`, `market_cap`, `pe_ratio`, `pb_ratio`, dividend schedule, `high_52_weeks`/`low_52_weeks`, `sector`, `industry`, `ceo`, `description`).

### robinhood_get_short_interest
Robinhood's **modeled daily** short-interest series — NOT the official biweekly FINRA figure. Each day has a point estimate plus upper/lower confidence bounds. History begins ~mid-2025; the client auto-pages the endpoint's 92-day window limit.

**Parameters:**
- `symbol` (string, required)
- `start_date` (string, optional, YYYY-MM-DD) — narrows the series; omit for full history

**Response:**
```json
{
  "symbol": "AAPL",
  "short_interest": {
    "symbol": "AAPL",
    "instrument_id": "...",
    "daily_data": [
      { "date": "2026-07-13", "shares_short": "141171395.64", "shares_upper_bound": "148709498.66", "shares_lower_bound": "133393566.55", "pc_freefloat": "0.9628" }
    ]
  }
}
```
`pc_freefloat` is a percent (e.g. `0.9628` = 0.9628% of free float).

### robinhood_get_equity_price_book
Level-2 price book (aggregated bid/ask depth) for a stock. Depth is populated during market hours; `asks`/`bids` are empty when the market is closed.

**Parameters:**
- `symbol` (string, required)

**Response:** `{ "price_book": { "instrument_id": "...", "updated_at": "...", "asks": [{ "price": {...}, "quantity": "..." }], "bids": [...] } }`

### robinhood_get_equity_tradability
Tradability flags for one or more symbols.

**Parameters:**
- `symbols` (array of string, required) — e.g. `["AAPL", "MSFT"]`

**Response:** `{ "tradability": [{ "symbol": "AAPL", "tradeable": true, "tradability": "tradable", "fractional_tradability": "...", "short_selling_tradability": "...", "account_type_tradabilities": [...] }] }`

### robinhood_get_earnings_results
Historical and upcoming earnings for one symbol (EPS estimate vs. actual, report date/timing).

**Parameters:**
- `symbol` (string, required)

**Response:** `{ "symbol": "AAPL", "earnings": [{ "year": 2026, "quarter": 2, "eps": { "estimate": "1.50", "actual": "1.55" }, "report": { "date": "...", "timing": "...", "verified": true } }] }`

### robinhood_get_earnings_calendar
Market-wide earnings calendar for a window of days (all reporting companies, not one symbol).

**Parameters:**
- `range_days` (number, default: 7) — positive = upcoming (e.g. 7 = next 7 days), negative = look-back; must be non-zero

**Response:** `{ "range_days": 7, "count": 79, "calendar": [{ "symbol": "...", "year": 2026, "quarter": 2, "eps": {...}, "report": {...} }] }`

### robinhood_get_news
Get news, analyst ratings, and earnings.

**Parameters:**
- `symbol` (string, required)

**Response:**
```json
{
  "news": [{ "title": "...", "source": "...", "published_at": "...", "url": "..." }],
  "ratings": { "summary": { "num_buy_ratings": 20, "num_hold_ratings": 5, "num_sell_ratings": 2 } },
  "earnings": [{ "year": 2025, "quarter": 1, "eps": { "estimate": "1.50", "actual": "1.55" } }]
}
```

### robinhood_get_historicals
Get OHLCV price history.

**Parameters:**
- `symbols` (string, required) — comma-separated
- `interval` (enum: "5minute", "10minute", "hour", "day", "week", default: "day")
- `span` (enum: "day", "week", "month", "3month", "year", "5year", default: "month")
- `bounds` (enum: "regular", "extended", "trading", default: "regular")

### robinhood_search
Search stocks by keyword or browse by market category.

**Parameters:**
- `query` (string, required) — search keyword (ignored if tag provided)
- `tag` (string, optional) — e.g., "technology", "most-popular-under-25"

## Options

### robinhood_get_options
Get options chain with greeks for a stock or index symbol.

**Parameters:**
- `symbol` (string, required) — stock or index ticker
- `expiration_date` (string, optional) — "YYYY-MM-DD"
- `strike_price` (number, optional) — filter by strike
- `option_type` (enum: "call", "put", optional)
- `max_strikes` (number, optional) — limit to N strikes nearest ATM

**Response (equity):**
```json
{
  "chain_info": { "id": "chain-uuid", "symbol": "AAPL", "expiration_dates": ["2025-01-17", "2025-02-21"] },
  "options": [{ "id": "option-uuid", "type": "call", "strike_price": "150.0000", "expiration_date": "2025-01-17" }],
  "market_data": [{ "adjusted_mark_price": "3.50", "delta": "0.5500", "gamma": "0.0300", "theta": "-0.0500", "vega": "0.2000", "implied_volatility": "0.3000", "open_interest": 15000, "volume": 5000 }]
}
```

**Response (index — additional field):**
```json
{ "index_value": { "value": "5700.00", "symbol": "SPX" }, "chain_info": { "symbol": "SPXW" }, "options": [...] }
```

**Notes:**
- `market_data` only included when all three filters (`expiration_date`, `strike_price`, `option_type`) are set.
- `index_value` only for index symbols.
- Chain auto-selected by `expiration_date`. SPXW (daily, PM-settled) is default; SPX monthly (AM-settled) for monthly-only dates.

### robinhood_get_option_positions
Open option positions — per-leg by default, or grouped by strategy (spreads, condors).

**Parameters:**
- `account_number` (string, optional) — omit for all accounts
- `aggregate` (boolean, default: false) — group by strategy instead of individual legs
- `nonzero` (boolean, default: true) — only non-zero quantities

**Response:** `{ "positions": [...], "aggregate": false }`

### robinhood_get_option_orders
Option order history (filled, cancelled, and open multi-leg orders).

**Parameters:**
- `open_only` (boolean, default: false) — only open/unfilled orders

**Response:** `{ "orders": [{ "id": "...", "state": "filled", "legs": [...] }] }`

### robinhood_get_option_historicals
Historical OHLC price series for a specific option contract.

**Parameters:**
- `symbol` (string, required) — underlying ticker
- `expiration_date` (string, required) — "YYYY-MM-DD"
- `strike_price` (number, required)
- `option_type` (enum: "call", "put", required)
- `span` (enum: "day", "week", "month", "3month", "year", "5year", default: "day")
- `interval` (enum: "5minute", "10minute", "hour", "day", "week", default: "hour")

**Response:** `{ "historicals": [{ "symbol": "...", "occ_symbol": "...", "data_points": [{ "begins_at": "...", "open_price": "...", "close_price": "...", "high_price": "...", "low_price": "...", "volume": 0 }] }] }`

## Orders

### robinhood_review_equity_order (read-only simulation)
Pre-trade simulation — places **nothing**. The **required review step** before `robinhood_place_stock_order`: call it, then **show the result to the user** before placing.

**Parameters:**
- `symbol` (string, required), `side` ("buy"/"sell"/"sell_short"), `quantity` (number, fractional except `sell_short`)
- `limit_price` (number, optional), `stop_price` (number, optional)
- `account_number` (string, required)

**Returns:** the order echoed back, live `quote_data` (so the user sees the cost), and `order_checks` — a reproduction of Robinhood's price collar. `order_checks` is `{}` **only** when the collar ran and found no problem; read `evaluated_checks` / `not_evaluated_checks` to know what was and wasn't checked (an empty `order_checks` is **not** a blanket "all clear"). If `order_checks` has an `alert_type` (e.g. `EQUITY_EXTREMELY_MARKETABLE_LIMIT_PRICE`), surface it prominently and re-confirm the price. `market_data_disclosure` is null (not reproducible). TOCTOU: if `quote_timestamp` is stale by the time you place, re-review first.

A clean review does **not** mean the order will be accepted: short eligibility, margin, borrow availability, day-trade suitability, and the server-side priceband are all checked by Robinhood at placement and are not reproduced here. Reviewing a `sell_short` prices it like any other sell.

### robinhood_review_option_order (read-only simulation)
Pre-trade simulation for single/multi-leg option orders — places **nothing**. The **required review step** before `robinhood_place_option_order`.

**Parameters:**
- `symbol` (string, required), `legs` (array of `{ expiration_date, strike, option_type, side, position_effect, ratio_quantity }`)
- `price` (number, required), `quantity` (number), `direction` ("debit"/"credit")
- `account_number` (string, required)

**Returns:** the order echoed back with per-leg `market_data` (mark/bid/ask/greeks) and the `collateral` the order would require. The reproduced check set is intentionally thin for options (see `not_evaluated_checks`). Options carry a ×100 contract multiplier — double-check the net debit/credit and quantity with the user.

### robinhood_place_stock_order
**Always** run `robinhood_review_equity_order` first and **show its result to the user** — this is the review→place gate, not an internal step.

**Parameters:**
- `symbol` (string, required), `side` ("buy"/"sell"/"sell_short"), `quantity` (number, fractional except `sell_short`)
- `limit_price` (number, optional), `stop_price` (number, optional)
- `trail_amount` (number, optional), `trail_type` ("percentage"/"amount", default: "percentage")
- `account_number` (string, required), `time_in_force` ("gtc"/"gfd", **required**)
- `market_hours` ("regular_hours"/"extended_hours"/"all_day_hours", **required** — no default; an order tagged to the wrong session silently queues instead of executing). `all_day_hours` is the 24 Hour Market. Only limit orders execute outside regular hours — a market, stop, or trailing order tagged to another session is rejected. Use `robinhood_get_market_hours` to check which session is live instead of guessing. (Replaces the former `extended_hours` boolean.)

**Short selling:** `sell` only closes an existing long — selling stock you do not own is rejected with `Not enough shares to sell.` Open a short with `side: "sell_short"` (margin-enabled account, whole shares only; a cash account is rejected with `You need to have margin investing enabled to short.`). Outside regular hours set `market_hours` to `extended_hours`, or the order is rejected with `It's after market close. To place this short sell order, change your trading session to extended hours.` Shorts are **not** available in the 24 Hour Market (`all_day_hours` → `Short selling isn't available during the 24 Hour Market.`) and must be `gfd` (`gtc` → `Short sell orders must be good for day only.`). There is no separate cover side — close a short with an ordinary `buy`.

An accepted short returns `state: "locate_completed"` (Robinhood located shares to borrow) — that is success, not an error. Once filled, the position appears in `robinhood_get_equity_positions` as a **negative** quantity; cover by buying the absolute value. Rejections are returned one at a time and the session is validated **before** the account type, so an after-hours attempt on a cash account reports the session error rather than the margin error — fix the reported problem and re-try to surface any that remain.

### robinhood_place_option_order
**Always** run `robinhood_review_option_order` first and **show its result to the user**.

**Parameters:**
- `symbol` (string, required), `legs` (array of `{ expiration_date, strike, option_type, side, position_effect, ratio_quantity }`)
- `price` (number, required), `quantity` (number), `direction` ("debit"/"credit")
- `stop_price` (number, optional), `time_in_force` ("gtc"/"gfd"/"ioc"/"opg", **required**)
- `account_number` (string, required)

### robinhood_place_crypto_order
**Parameters:**
- `symbol` (string, required), `side` ("buy"/"sell")
- `amount_or_quantity` (number), `amount_in` ("quantity"/"price", default: "quantity")
- `order_type` ("market"/"limit", **required**), `limit_price` (number, optional)

### robinhood_get_orders
**Parameters:**
- `order_type` ("stock"/"option"/"crypto", default: "stock")
- `status` ("open"/"all", default: "all")
- `account_number` (string, optional), `limit` (number, default: 50)

### robinhood_cancel_order
**Parameters:**
- `order_id` (string, required), `order_type` ("stock"/"option"/"crypto", default: "stock")

### robinhood_get_order_status
**Parameters:**
- `order_id` (string, required), `order_type` ("stock"/"option"/"crypto", default: "stock")

**Reading `state`** — do not report an order as failed just because it is not `filled`:

| `state` | Meaning |
|---|---|
| `unconfirmed` / `queued` / `confirmed` | Accepted and working |
| `locate_completed` | **Short sale accepted** — Robinhood located shares to borrow. Normal and successful, not an error |
| `partially_filled` | Some shares executed, rest still working |
| `filled` | Fully executed — terminal |
| `cancelled` / `rejected` / `failed` | Terminal; check `reject_reason` |

Only `filled`, `cancelled`, `rejected`, `failed` are terminal. Always quote `cumulative_quantity` — a cancelled order may have partially filled first.

## Markets

### robinhood_get_movers
Get top movers by category.

**Parameters:**
- `category` (enum: "top_movers", "sp500", "top_100", default: "top_movers")
- `direction` (enum: "up", "down") — required when `category: "sp500"`, ignored otherwise

### robinhood_get_market_hours
Market hours for a date: whether it is a trading day, and when the regular and extended sessions open and close.

**Parameters:**
- `date` (string, optional) — `YYYY-MM-DD`. Defaults to today in US market time (ET), not the caller's local date
- `market` (string, optional) — MIC code, default `"XNYS"`

**Response:** `{ "is_open": true, "date": "...", "opens_at": "...", "closes_at": "...", "extended_opens_at": "...", "extended_closes_at": "...", "note": "..." }` (ISO-8601 UTC; session times are null when `is_open` is false)

Call this before placing an order when you are unsure which session is live — `robinhood_place_stock_order` requires an explicit `market_hours`, and inferring it from the local clock is wrong across time zones, weekends, and holidays.

### robinhood_get_indexes
Get all tradable market indexes (SPX, NDX, VIX, RUT, XSP, …).

**Parameters:** none

**Response:** `{ "indexes": [{ "id": "...", "symbol": "SPX", "simple_name": "...", "tradable_chain_ids": [...] }] }`

### robinhood_get_index_quotes
Get current values for one or more index symbols.

**Parameters:**
- `symbols` (array of string, required) — e.g. `["SPX", "VIX"]`

**Response:** `{ "quotes": [{ "symbol": "SPX", "value": "5700.00", "updated_at": "..." }] }`

## Watchlists

Lists are identified by **list_id (UUID)**, obtained from `get_watchlists` / `get_popular_watchlists` — there is no default-list shortcut (a write must never target the wrong list). Add/remove **confirm with the user first** and are idempotent.

### robinhood_get_watchlists
List your own (custom) watchlists — metadata only, including each list's `id`.

**Parameters:** none

**Response:** `{ "count": 3, "watchlists": [{ "id": "<uuid>", "display_name": "...", "owner_type": "custom", "item_count": 5, "allowed_object_types": ["instrument", ...] }] }`

### robinhood_get_watchlist_items
List a watchlist's items, enriched with `symbol`/`name`. Does not return live prices — call `robinhood_get_stock_quote`. For the options watchlist use `robinhood_get_option_watchlist`. Unknown `list_id` → error.

**Parameters:**
- `list_id` (string uuid, required)

**Response:** `{ "list_id": "<uuid>", "count": 2, "items": [{ "object_id": "<uuid>", "object_type": "instrument", "symbol": "AAPL", "name": "Apple" }] }`

### robinhood_get_popular_watchlists
Discover Robinhood-curated lists (e.g. "100 Most Popular"). Paginated results are fully collected.

**Parameters:** none

**Response:** `{ "count": 29, "watchlists": [{ "id": "<uuid>", "display_name": "..." }] }`

### robinhood_get_option_watchlist
Your options watchlist — the list of single-leg option **contracts** it holds (no longer just metadata). Each contract carries `object_id`, a derived `option_id`, `position_type`, `chain_symbol`, `strategy`, `name`, and `single_leg`. Multi-leg strategies are listed with a **null** `option_id` and a pointer to the Robinhood app (they aren't addressable over this path).

**Parameters:** none

**Response:** `{ "count": 2, "contracts": [{ "object_id": "<uuid>", "option_id": "<uuid>", "position_type": "long", "chain_symbol": "AAPL", "strategy": "long_call", "name": "...", "single_leg": true }] }`

### robinhood_create_watchlist
Create a new (empty) watchlist. **Confirm with the user first.** Returns the created list including its new `id` — populate it with `robinhood_add_to_watchlist`.

**Parameters:**
- `display_name` (string, required) — the list's name
- `display_description` (string, optional), `icon_emoji` (string, optional)

**Response:** `{ "operation": "created", "list": { "id": "<uuid>", "display_name": "...", ... }, "note": "..." }`

### robinhood_update_watchlist
Rename / re-describe a watchlist (metadata only — does **not** add/remove items). **Confirm with the user first.** Provide `list_id` + at least one field to change; omitted fields are unchanged.

**Parameters:**
- `list_id` (string uuid, required)
- `display_name` / `display_description` / `icon_emoji` (at least one)

**Response:** `{ "operation": "updated", "list_id": "<uuid>", "list": { ... } }`

### robinhood_follow_watchlist
Follow a Robinhood-**curated** list (from `robinhood_get_popular_watchlists`) so it appears in the user's watchlists. Reversible non-financial write — **confirm with the user first.** Idempotent. Result is declarative (the API echoes the request, not the new state).

**Parameters:**
- `list_id` (string uuid, required) — a curated list id from `robinhood_get_popular_watchlists`

**Response:** `{ "list_id": "<uuid>", "operation": "follow", "followed": true }`

### robinhood_unfollow_watchlist
Unfollow a curated list so it no longer appears in the user's watchlists. Reversible non-financial write — **confirm with the user first.** Idempotent.

**Parameters:**
- `list_id` (string uuid, required)

**Response:** `{ "list_id": "<uuid>", "operation": "unfollow", "followed": false }`

> There is no delete-watchlist tool (the official MCP has none) — removing a curated list is `robinhood_unfollow_watchlist`; a custom list you own can only be emptied via `robinhood_remove_from_watchlist`.

### robinhood_add_to_watchlist
Add items to a watchlist. **Confirm with the user first.** Provide exactly one of `symbols`, `currency_pair_ids`, or `index_ids`. Already-present items are no-ops.

**Parameters:**
- `list_id` (string uuid, required)
- `symbols` (array of string, optional) — stocks/ETFs, e.g. `["AAPL","NVDA"]`
- `currency_pair_ids` (array of string uuid, optional) — crypto pairs
- `index_ids` (array of string uuid, optional) — market indexes (from `get_indexes`)

**Response:** `{ "list_id": "<uuid>", "operation": "add", "ensured_present": [{ "object_type": "instrument", "object_id": "<uuid>", "symbol": "AAPL" }], "note": "..." }`

### robinhood_remove_from_watchlist
Remove items from a watchlist. **Confirm with the user first.** Same mutually-exclusive params as add. Items not on the list are reported as `not_present` (not an error).

**Parameters:**
- `list_id` (string uuid, required)
- `symbols` / `currency_pair_ids` / `index_ids` (exactly one, as above)

**Response:** `{ "list_id": "<uuid>", "operation": "remove", "removed": [{ "symbol": "AAPL", "object_id": "<uuid>" }], "not_present": [{ "symbol": "ZZZZ" }] }`

### robinhood_add_option_to_watchlist
Add option contracts to the options watchlist as single-leg contracts. **Confirm with the user first.** Already-present contracts are no-ops (deduped). **Long only:** `position_type: "long"` is the only supported path — `"short"` returns an error directing to the Robinhood app.

**Parameters:**
- `option_ids` (array of string uuid, required, 1–20) — option instrument ids
- `position_type` (enum: "long" | "short", optional, default "long") — long only over this path

**Response:** `{ "operation": "add_option", "position_type": "long", "results": [{ "option_id": "<uuid>", "status": "ensured_present" }], "summary": { "ensured_present": 1, "already_present": 0, "failed": 0 } }` — one `results` entry per requested id (`status` is `ensured_present` / `already_present` / `failed`; adds are applied one at a time, not atomic).

### robinhood_remove_option_from_watchlist
Remove single-leg option contracts from the options watchlist. **Confirm with the user first.** Contracts not on the list are reported as `not_present` (not an error). **Long only** (same `position_type` constraint as add).

**Parameters:**
- `option_ids` (array of string uuid, required, 1–20)
- `position_type` (enum: "long" | "short", optional, default "long") — long only over this path

**Response:** `{ "operation": "remove_option", "position_type": "long", "removed": [{ "option_id": "<uuid>", "object_id": "<uuid>" }], "not_present": [{ "option_id": "<uuid>" }] }`

## Scanners (screeners)

Read-only. A **scan** is a saved set of filters + columns that screens the market; users create them in Robinhood Legend. Scan *writes* (create/run/update) are not yet exposed.

### robinhood_get_scanner_filter_specs
List the filter vocabulary for building scans — fundamentals, price/volume, options, and technical indicators (RSI/MACD/EMA/…), each with its predicates, unit, and any supported lengths/intervals/plots. Call before constructing filters; don't guess `filter_type` names. Served from a static catalog captured from Robinhood's official scanner service (account-agnostic, rarely changes), not a live per-request read.

**Response:** `{ "count": 56, "filter_specs": [{ "filter_type": "FILTER_TYPE_RSI", "display_name": "RSI", "filter_group": "TECHNICAL", "value_type": "DECIMAL", "unit_type": "PLAIN", "supported_predicates": [">", "<", "BETWEEN", ...], "supported_lengths": [14, ...], "supported_intervals": ["1d", ...] }], "note": "..." }`

Usage: match `filter_type` exactly; when `supported_intervals` is non-empty, pass an interval; use `supported_predicates` symbols exactly.

### robinhood_get_scans
List your saved scanners. Empty when you have none.

**Response:** `{ "count": 1, "scans": [{ "scan_id": "<id>", "title": "...", "column_count": 3, "filter_summary": null, "cortex_managed": null, "sorting": null, "raw": { ...full Beacon object... } }], "note": "..." }`

`scan_id`/`title`/`column_count` are derived faithfully. `filter_summary`, `cortex_managed`, and `sorting` are rendered by Robinhood's own service and are **not reproduced** here (returned `null`) — do **not** read their null as "no filters", "not Cortex-managed", or "unsorted"; the underlying data is under `raw` (e.g. `raw.activeScanConfiguration.filters` / `.sortingColumnId`).

## Realized P&L (computed)

Read-only. Robinhood has **no realized-P&L REST endpoint** for a standard token, so these tools **compute** it: equity by independent **economic FIFO including fees** (matched from your order history — *not* Robinhood's booked/tax-adjusted number), crypto from Robinhood's native `gain_loss`. **Options are not included** (expirations/assignments aren't in the order history). Both tools require `account_number` (from `robinhood_get_accounts`) and fetch full order history, so they can be slow on large accounts. Always relay the result `note` — it carries the honesty caveats.

### robinhood_get_realized_pnl
Bucketed realized gain over a window, plus totals. Params: `account_number` (required); `span` (`day`/`week`/`month`/`3month`/`year`/`all`, default `3month`) **or** `start_date`+`end_date` (YYYY-MM-DD); `asset_classes` (subset of `equity`/`crypto`; `option` accepted but not computed).

**Response:** `{ "account_number": "...", "window": "3month", "display_currency": "USD", "data_points": [{ "start_time": "...", "end_time": "...", "realized_gain": 0, "rate_of_realized_gain": null, "number_of_trades": 0 }], "total_returns": 0, "total_rate_of_return": null, "note": "..." }`

`rate_of_realized_gain` and `total_rate_of_return` are **null** — the rate denominator Robinhood uses isn't reproducible; do not invent a percentage. `data_points` buckets are our own; they tile the window and sum to `total_returns`.

### robinhood_get_pnl_trade_history
Per-trade realized P&L. Params: `account_number` (required); `span` (`week`/`month`/`3month`/`ytd`/`all`, default `week`); `symbol` (optional single-symbol filter).

**Response:** `{ "account_number": "...", "span": "week", "trades": [{ "symbol": "AAPL", "side": "sell", "quantity": 10, "price": 150, "realized_gain": 123.45 }], "next_cursor": null, "note": "..." }`

Results are complete (`next_cursor` always null). For exact reconciliation against Robinhood's own figures, run `bun run pnl:harness` locally (keeps your account number off any transcript).
