# TypeScript Client API

Methods from `robinhood-for-agents` for programmatic access without MCP.

## Quick Start

```typescript
import { RobinhoodClient, getClient, TokenExpiredError } from "robinhood-for-agents";

const rh = getClient(); // singleton
await rh.restoreSession();  // loads tokens + wires refresh — does NOT validate them
```

`restoreSession()` reads the token store and registers both refresh paths (a pre-request hook that renews ~24h before expiry, plus a 401 handler). It proves nothing about whether the tokens still work — the first real call is where a dead session surfaces, as a `TokenExpiredError`. To verify up front, probe:

```typescript
await rh.restoreSession();
await rh.getAccountProfile();  // throws TokenExpiredError if the session is dead
```

All methods are `async`. Multi-account is first-class: account-scoped methods accept `accountNumber`.

## Errors & Session Expiry

```
RobinhoodError
├── AuthenticationError
│   └── TokenExpiredError     // 401 that survived automatic refresh
├── NotLoggedInError
└── APIError                  // every other non-2xx
    ├── RateLimitError        // 429
    └── NotFoundError         // 404
```

Catch `AuthenticationError` (or `TokenExpiredError` specifically) for auth failures — **not** `APIError`. A 401 is no longer surfaced as a bare `APIError: HTTP 401`: `TokenExpiredError` is thrown only after automatic refresh has already run and failed, so it means "re-authenticate", never "retry".

```typescript
import { getClient, AuthenticationError, TokenExpiredError, APIError } from "robinhood-for-agents";

try {
  await rh.getAccountProfile();
} catch (e) {
  if (e instanceof TokenExpiredError) {
    // refresh already tried and failed — only a browser login fixes this
    // (`bunx robinhood-for-agents onboard`, or the robinhood_browser_login MCP tool)
  } else if (e instanceof AuthenticationError) {
    // no tokens in the store at all — same remedy
  } else if (e instanceof APIError) {
    // a real API error (404/429/5xx) — the session is fine
  } else {
    // network/transient — the session may well be fine; retry before re-authenticating
  }
}
```

**How refresh works.** `restoreSession()` registers two paths: a pre-request hook that renews ~24h before the access token expires (using `TokenData.expires_at`, derived from the JWT `exp` claim), and an `onUnauthorized` handler that renews on a 401. Concurrent 401s share a single refresh attempt, and attempts are rate-limited to one per 5s.

**Single-use rotation — the concurrency rule.** Robinhood rotates refresh tokens: each renewal returns a new refresh token, instantly kills the old one, and revokes the previous access token. Two clients on one session (an MCP server plus a `bun -e` script, or two Claude Code sessions) will poison each other. When a refresh is rejected the client re-reads the token store and adopts a token another process may have persisted, so it usually self-heals — but there is **no cross-process lock**. Drive a session from one process at a time.

**Idle sessions still lapse.** Proactive renewal only runs while the client is making requests. Leave a session idle longer than the refresh-token lifetime and the chain lapses — a new browser login is required. Access-token TTL varies (~6-8.5 days observed); never hard-code a number.

**No-refresh mode.** A client constructed with a direct `accessToken` registers neither refresh path — the first 401 raises `TokenExpiredError` immediately.

## MCP Tool → Client Method Mapping

| MCP Tool | Client Method |
|----------|--------------|
| `robinhood_check_session` | `restoreSession()` + a probe call (`getAccountProfile()`) — `restoreSession()` alone does not validate the tokens |
| `robinhood_get_account` | `getAccountProfile(accountNumber?)` |
| `robinhood_get_accounts` | `getAccounts(opts?)` |
| `robinhood_get_portfolio` | `buildHoldings(opts?)` |
| `robinhood_get_crypto` (positions) | `getCryptoPositions()` |
| `robinhood_get_crypto` (quote) | `getCryptoQuote(symbol)` |
| `robinhood_get_crypto` (historicals) | `getCryptoHistoricals(symbol, opts?)` |
| `robinhood_get_equity_positions` | `getPositions(opts?)` |
| `robinhood_get_stock_quote` | `getQuotes(symbols)` + `getFundamentals(symbols)` |
| `robinhood_get_fundamentals` | `getFundamentals(symbols)` |
| `robinhood_get_equity_price_book` | `getPriceBook(symbol)` |
| `robinhood_get_equity_tradability` | `getTradability(symbols)` |
| `robinhood_get_earnings_results` | `getEarnings(symbol)` |
| `robinhood_get_earnings_calendar` | `getEarningsCalendar(rangeDays?)` |
| `robinhood_get_short_interest` | `getShortInterest(symbol, opts?)` |
| `robinhood_get_news` | `getNews(symbol)` + `getRatings(symbol)` + `getEarnings(symbol)` |
| `robinhood_get_historicals` | `getStockHistoricals(symbols, opts?)` |
| `robinhood_search` | `findInstruments(query)` |
| `robinhood_get_options` (chain) | `getChains(symbol, opts?)` |
| `robinhood_get_options` (instruments) | `findTradableOptions(symbol, opts?)` |
| `robinhood_get_options` (greeks) | `getOptionMarketData(symbol, expDate, strike, type)` |
| `robinhood_get_options` (index value) | `getIndexValue(symbol)` |
| `robinhood_get_option_positions` | `getOptionPositions(opts?)` / `getOptionAggregatePositions(opts?)` |
| `robinhood_get_option_orders` | `getAllOptionOrders(opts?)` / `getOpenOptionOrders(opts?)` |
| `robinhood_get_option_historicals` | `getOptionHistoricals(symbol, expDate, strike, type, opts?)` |
| `robinhood_get_movers` | `getTopMovers()` / `getTopMoversSp500(direction)` / `getTop100()` |
| `robinhood_get_market_hours` | `getMarketHours(opts?)` |
| `robinhood_get_indexes` | `getIndexInstruments()` |
| `robinhood_get_index_quotes` | `getIndexQuotes(symbols)` |
| `robinhood_review_equity_order` | `reviewEquityOrder(opts)` |
| `robinhood_review_option_order` | `reviewOptionOrder(opts)` |
| `robinhood_place_stock_order` | `orderStock(symbol, side, quantity, opts?)` |
| `robinhood_place_option_order` | `orderOption(symbol, legs, price, quantity, direction, opts?)` |
| `robinhood_place_crypto_order` | `orderCrypto(symbol, side, amount, opts?)` |
| `robinhood_get_orders` (stock) | `getAllStockOrders()` / `getOpenStockOrders()` |
| `robinhood_get_orders` (option) | `getAllOptionOrders()` / `getOpenOptionOrders()` |
| `robinhood_get_orders` (crypto) | `getAllCryptoOrders()` / `getOpenCryptoOrders()` |
| `robinhood_cancel_order` | `cancelStockOrder(id)` / `cancelOptionOrder(id)` / `cancelCryptoOrder(id)` |
| `robinhood_get_order_status` | `getStockOrder(id)` / `getOptionOrder(id)` / `getCryptoOrder(id)` |
| `robinhood_get_watchlists` | `getWatchlists()` |
| `robinhood_get_watchlist_items` | `getWatchlistItems(listId)` |
| `robinhood_get_popular_watchlists` | `getPopularWatchlists()` |
| `robinhood_get_option_watchlist` | `getOptionWatchlistContracts()` |
| `robinhood_add_to_watchlist` | `resolveInstrumentBySymbol(sym)` + `updateWatchlistItems(listId, "create", refs)` |
| `robinhood_remove_from_watchlist` | `getWatchlistItems(listId)` + `updateWatchlistItems(listId, "delete", refs)` |
| `robinhood_create_watchlist` | `createWatchlist(name, opts?)` |
| `robinhood_update_watchlist` | `updateWatchlist(listId, updates)` |
| `robinhood_follow_watchlist` | `followWatchlist(listId)` |
| `robinhood_unfollow_watchlist` | `unfollowWatchlist(listId)` |
| `robinhood_add_option_to_watchlist` | `getOptionInstrumentById(optionId)` + `quickAddOption(optionId, "long")` |
| `robinhood_remove_option_from_watchlist` | `getOptionWatchlistContracts()` + `updateWatchlistItems(listId, "delete", refs)` |
| `robinhood_get_scans` | `getScans()` |
| `robinhood_get_scanner_filter_specs` | `getScannerFilterSpecs()` |
| `robinhood_get_realized_pnl` / `robinhood_get_pnl_trade_history` | `getRealizedPnl(opts?)` |
| `robinhood_get_equity_tax_lots` | `getEquityTaxLots(symbol, { accountNumber })` |

## Portfolio Methods

### `buildHoldings(opts?): Promise<Record<string, Holding>>`
```typescript
const holdings = await rh.buildHoldings({ withDividends: true });
// => { "AAPL": { price, quantity, average_buy_price, equity, percent_change, name, ... } }
```
Options: `{ accountNumber?: string; withDividends?: boolean }`

### `getAccountProfile(accountNumber?): Promise<Account>`
```typescript
const account = await rh.getAccountProfile();
// => { account_number, buying_power, ... } — omit accountNumber to default to the first account
```

### `getAccounts(opts?): Promise<Account[]>`
```typescript
const accounts = await rh.getAccounts();
```

### `getPortfolioProfile(accountNumber?): Promise<Portfolio>`
```typescript
const portfolio = await rh.getPortfolioProfile();
// => { equity, market_value, ... }
```

### `getUnifiedPortfolio(accountNumber?): Promise<UnifiedPortfolio | null>`
Total equity + full buying-power breakdown (bonfire) — the data behind `robinhood_get_portfolio`'s `unified` field. **Returns `null` for any non-default account** — bonfire's `/accounts/{id}/unified/` endpoint 404s for every account_number except the one Robinhood treats as default, even though it's a real, valid account and the sibling `getPortfolioLive`/`getPortfolioProfile`/`getPositions` calls accept it fine. The 404 is caught and mapped to `null` rather than thrown (an invalid/unknown account_number also 404s here and gets the same `null`, since bonfire returns 404 either way — this method can't distinguish the two cases), so scoping to a non-default account doesn't break the call — the six `unified`-sourced summary fields (`total_equity`, `total_market_value`, `portfolio_equity`, `options_buying_power`, `uninvested_cash`, `withdrawable_cash`) are just `undefined` in that case; everything else (`holdings`, `cash`, `buying_power`, `live`) is unaffected. (Omitting `accountNumber` entirely still throws if the caller has no accounts at all — only the per-request 404 is swallowed, not account resolution.)

### `getPortfolioLive(accountNumber?): Promise<PortfolioLive>`
Live per-asset-class market values + cash (bonfire) — the data behind `robinhood_get_portfolio`'s `live` field.

### `getPositions(opts?): Promise<Position[]>`
```typescript
const positions = await rh.getPositions({ nonzero: true });
// => raw equity positions (shares, average_buy_price) — no P&L/name enrichment (use buildHoldings for that)
```
Options: `{ accountNumber?: string; nonzero?: boolean }`

### `getCryptoPositions(): Promise<CryptoPosition[]>`
### `getCryptoQuote(symbol): Promise<CryptoQuote>`
```typescript
const btc = await rh.getCryptoQuote("BTC");
// => { mark_price, ask_price, bid_price, symbol, ... }
```

## Research Methods

### `getQuotes(symbols): Promise<Quote[]>`
Accepts single symbol or array. Returns `last_trade_price`, `bid_price`, `ask_price`, `bid_size`, `ask_size`, `previous_close`, `pe_ratio`, `state` (trading status).

### `getFundamentals(symbols): Promise<Fundamental[]>`
Returns `market_cap`, `pe_ratio`, `pb_ratio`, `float`, `dividend_yield`, `high_52_weeks`, `low_52_weeks`, `description`, `ceo`, `sector`, plus a full dividend schedule (`dividend_per_share`, `ex_dividend_date`, `payable_date`, `distribution_frequency`).

### `getPriceBook(symbol): Promise<PriceBook>`
Level-2 price book (aggregated bid/ask depth). `asks`/`bids` are empty when the market is closed.

### `getTradability(symbols): Promise<Array<{ symbol, tradeable?, ... }>>`
```typescript
const flags = await rh.getTradability(["AAPL", "MSFT"]);
// => [{ symbol, tradeable, tradability, fractional_tradability, short_selling_tradability, account_type_tradabilities, ... }]
```

### `getStockHistoricals(symbols, opts?): Promise<StockHistorical[]>`
```typescript
const hist = await rh.getStockHistoricals("AAPL", { interval: "day", span: "year", bounds: "regular" });
// => [{ symbol, historicals: [{ begins_at, open_price, close_price, high_price, low_price, volume }] }]
```

### `getShortInterest(symbol, opts?): Promise<ShortInterest | null>`
Robinhood's **modeled daily** short-interest series (not the official biweekly FINRA figure). Returns `{ symbol, instrument_id, daily_data: [{ date, shares_short, shares_upper_bound, shares_lower_bound, pc_freefloat, pc_freefloat_upper_bound, pc_freefloat_lower_bound }] }`. `pc_freefloat` is a percent (e.g. `0.9628` = 0.9628%). `opts.startDate` / `opts.endDate` (YYYY-MM-DD) bound the range; omit `startDate` for full history. The endpoint caps each request at 92 days — the method auto-pages ≤90-day windows and merges them (RH's history begins ~mid-2025). Returns `null` if the symbol has no instrument or no data.

### `getNews(symbol): Promise<News[]>`
### `getRatings(symbol): Promise<Rating>`
### `getEarnings(symbol): Promise<Earnings[]>`
EPS is nested under `eps` (`eps.estimate`, `eps.actual`) — not flat top-level fields (assuming flat returns `undefined`). Also includes `report` (date/timing) and `call` (datetime, replay_url).

### `getEarningsCalendar(rangeDays?): Promise<Earnings[]>`
Market-wide earnings calendar (all reporting companies, not one symbol). `rangeDays` (default `7`) selects the window: positive = upcoming, negative = look-back; must be non-zero.
```typescript
const calendar = await rh.getEarningsCalendar(7);  // next 7 days
```

### `findInstruments(query): Promise<Instrument[]>`

## Options Methods

### `getChains(symbol, opts?): Promise<OptionChain>`
Works for equities and indexes (SPX, NDX, VIX, RUT, XSP). For indexes with multiple chains, pass `expirationDate` to select. Defaults to SPXW.
```typescript
const chain = await rh.getChains("AAPL");
// => { id, expiration_dates: [...], ... }
```

### `findTradableOptions(symbol, opts?): Promise<OptionInstrument[]>`
```typescript
const calls = await rh.findTradableOptions("AAPL", {
  expirationDate: "2026-04-17", strikePrice: 200, optionType: "call"
});
```

### `getOptionMarketData(symbol, expirationDate, strikePrice, optionType): Promise<OptionMarketData[]>`
```typescript
const data = await rh.getOptionMarketData("AAPL", "2026-04-17", 200, "call");
// => [{ adjusted_mark_price, delta, gamma, theta, vega, implied_volatility, open_interest, volume, ... }]
```

### `getIndexValue(symbol): Promise<IndexValue | null>`
```typescript
const spx = await rh.getIndexValue("SPX");
// => { value: "5700.00", symbol: "SPX" } or null for non-index
```

### `getOptionPositions(opts?): Promise<OptionPosition[]>`
```typescript
const legs = await rh.getOptionPositions({ nonzero: true }); // open positions, per-leg
```
Options: `{ accountNumber?: string; nonzero?: boolean }`

### `getOptionAggregatePositions(opts?): Promise<OptionAggregatePosition[]>`
```typescript
const strategies = await rh.getOptionAggregatePositions({ nonzero: true }); // same positions grouped by strategy (spreads, condors, ...)
```
Same options as `getOptionPositions`.

### `getOptionHistoricals(symbol, expirationDate, strikePrice, optionType, opts?): Promise<OptionHistorical[]>`
```typescript
const hist = await rh.getOptionHistoricals("AAPL", "2026-04-17", 200, "call", { span: "day", interval: "hour" });
```
Historical OHLC series for one contract. Options: `{ span?: string; interval?: string; bounds?: string }`

## Order Methods

**Safety**: Always confirm with the user before calling any order method. **Review first**: run `reviewEquityOrder` / `reviewOptionOrder` and show the result to the user before the matching `orderStock` / `orderOption`.

### `reviewEquityOrder(opts): Promise<EquityOrderReview>` — pre-trade simulation (places nothing)
```typescript
const review = await rh.reviewEquityOrder({
  symbol: "AAPL", side: "buy", quantity: 10, limitPrice: 150.0, accountNumber: "ACCT",
});
// review.order_checks: {} when the collar ran clean, else { alert_type, details }
// review.evaluated_checks / not_evaluated_checks: which criteria ran (an empty
//   order_checks is meaningful only when evaluated_checks is non-empty)
// review.quote / quote_timestamp: live quote for cost + TOCTOU staleness check
```
Options: `{ symbol, side, quantity, limitPrice?, stopPrice?, accountNumber? }`. Read-only: composed from the app's own preflight GETs; the price collar is reproduced from the account's live thresholds. Robinhood's server-side priceband/suitability/killswitch checks are **not** reproduced (named in `not_evaluated_checks`).

### `reviewOptionOrder(opts): Promise<OptionOrderReview>` — pre-trade option simulation
```typescript
const review = await rh.reviewOptionOrder({
  symbol: "AAPL",
  legs: [{ expirationDate: "2026-04-17", strike: 200, optionType: "call", side: "buy", positionEffect: "open" }],
  price: 3.50, quantity: 1, direction: "debit", accountNumber: "ACCT",
});
// review.legs[].market_data (mark/bid/ask/greeks) + review.collateral (account ids scrubbed)
```
The option check set is intentionally thin (see `not_evaluated_checks`) — options have no simple last-trade collar.

### `orderStock(symbol, side, quantity, opts)`
```typescript
await rh.orderStock("AAPL", "buy", 10, { timeInForce: "gfd", marketHours: "regular_hours" });              // market
await rh.orderStock("AAPL", "buy", 10, { limitPrice: 150.0, timeInForce: "gfd", marketHours: "regular_hours" }); // limit
await rh.orderStock("AAPL", "sell", 10, { stopPrice: 145.0, limitPrice: 144.0, timeInForce: "gfd", marketHours: "regular_hours" }); // stop-limit
await rh.orderStock("AAPL", "sell", 10, { trailAmount: 5, trailType: "percentage", timeInForce: "gfd", marketHours: "regular_hours" }); // trailing stop
await rh.orderStock("AAPL", "sell_short", 10, { limitPrice: 150.0, timeInForce: "gfd", marketHours: "regular_hours" }); // open a short
await rh.orderStock("AAPL", "buy", 10, { limitPrice: 150.0, timeInForce: "gfd", marketHours: "regular_hours" }); // cover a short
await rh.orderStock("AAPL", "buy", 10, { limitPrice: 150.0, timeInForce: "gfd", marketHours: "all_day_hours" }); // 24 Hour Market
```
Options: `{ limitPrice, stopPrice, trailAmount, trailType, accountNumber, timeInForce (required), marketHours, extendedHours }`

**Side** — `"buy" | "sell" | "sell_short"`:

| Intent | Side |
|---|---|
| Open / add to a long | `buy` |
| Close a long | `sell` |
| Open a short | `sell_short` |
| Cover a short | `buy` |

`sell` only closes a long — selling stock the account does not hold fails with `Not enough shares to sell.` There is no separate cover side; a plain `buy` against an open short is recognised as closing it.

`sell_short` carries extra constraints, all enforced client-side so you get the reason before an order is attempted:

| Constraint | Rejected by | Message you will see |
|---|---|---|
| Whole shares | client, before sending | `Short sales must be whole shares — fractional short selling is not supported` |
| `timeInForce: "gfd"` | client, before sending | `Short sales must be good-for-day — timeInForce "gtc" is not accepted` |
| Not in the 24 Hour Market | client, before sending | `Short selling is not available during the 24 Hour Market (all_day_hours)` |
| Margin-enabled account | Robinhood | `You need to have margin investing enabled to short.` |
| Session named outside regular hours | Robinhood | `It's after market close. To place this short sell order, change your trading session to extended hours.` |
| Symbol shortable / borrow available | Robinhood | varies — check `short_selling_tradability` first |

The first three throw locally, so no order is ever attempted; the rest come back as an `APIError` from Robinhood. Match on the message in this table, not on Robinhood's wording, for the client-side ones.

An accepted short returns `state: "locate_completed"` (Robinhood located shares to borrow) — success, not an error. A filled short shows in `getPositions()` as a **negative** quantity; cover by buying the absolute value. Robinhood returns one rejection at a time and checks the session **before** the account type, so an after-hours attempt on a cash account reports the session error rather than the margin error.

**Session** — `marketHours` is `"regular_hours" | "extended_hours" | "all_day_hours"` (the last is Robinhood's 24 Hour Market). It supersedes the legacy `extendedHours` boolean (`extended_hours` on the wire is just `market_hours !== "regular_hours"`); passing both with contradictory values throws. Only limit orders execute outside regular hours — a market, stop, or trailing order tagged to another session is rejected client-side. A short sell placed outside regular hours is rejected unless the session is named.

**Pass `marketHours` explicitly.** It is optional here only for backwards compatibility: omitted, the order goes out as regular hours, which after the close means it queues for the next open instead of executing. The MCP tool makes `market_hours` **required** for exactly that reason. Use `getMarketHours()` to find out which session is live rather than inferring it from the local clock.

### `getMarketHours(opts?)`
```typescript
const hours = await rh.getMarketHours();                          // today, US equities (XNYS)
const nye = await rh.getMarketHours({ date: "2026-12-31" });      // a specific date
// => { is_open, date, opens_at, closes_at, extended_opens_at, extended_closes_at }
```
`is_open` is false on weekends and holidays, with null session times. The date defaults to today **in market time (ET)**, not the caller's local date. Times are ISO-8601 UTC.

### `orderOption(symbol, legs, price, quantity, direction, opts?)`
```typescript
// Single call
await rh.orderOption("AAPL", [
  { expirationDate: "2026-04-17", strike: 200, optionType: "call", side: "buy", positionEffect: "open" }
], 3.50, 1, "debit");

// Bull call spread
await rh.orderOption("AAPL", [
  { expirationDate: "2026-04-17", strike: 200, optionType: "call", side: "buy", positionEffect: "open" },
  { expirationDate: "2026-04-17", strike: 210, optionType: "call", side: "sell", positionEffect: "open" },
], 2.50, 1, "debit");
```

### `orderCrypto(symbol, side, quantityOrPrice, opts?)`
```typescript
await rh.orderCrypto("BTC", "buy", 0.5);                           // buy 0.5 BTC
await rh.orderCrypto("BTC", "buy", 100, { amountIn: "price" });    // buy $100 of BTC
await rh.orderCrypto("BTC", "buy", 0.5, { limitPrice: 60000 });    // limit buy
```
Options: `{ amountIn?: "quantity" | "price"; orderType?: "market" | "limit"; limitPrice?: number }` — setting `limitPrice` implies a limit order.

### Order Queries
```typescript
const allOrders = await rh.getAllStockOrders();
const openOrders = await rh.getOpenStockOrders();
const order = await rh.getStockOrder("order-uuid");
```

### Cancel Orders
```typescript
await rh.cancelStockOrder("order-uuid");
await rh.cancelOptionOrder("order-uuid");
await rh.cancelCryptoOrder("order-uuid");
```

## Markets Methods

### `getTopMovers(): Promise<Instrument[]>`
```typescript
const movers = await rh.getTopMovers(); // Robinhood's featured top-movers list
```

### `getTopMoversSp500(direction): Promise<Instrument[]>`
```typescript
const gainers = await rh.getTopMoversSp500("up"); // "up" | "down" — S&P 500 movers
```

### `getIndexInstruments(): Promise<IndexInstrument[]>`
All tradable index instruments (SPX, NDX, VIX, RUT, …).

### `getIndexQuotes(symbols): Promise<IndexValue[]>`
```typescript
const values = await rh.getIndexQuotes(["SPX", "VIX"]); // current values; unknown symbols are skipped
```
See also `getIndexValue(symbol)` above (Options Methods) for a single-symbol lookup.

## Watchlist Methods

**Safety**: watchlist writes mutate the user's account — confirm the exact list + symbols before calling. Lists are addressed by `list_id` (UUID) only; there is no default-list resolution.

### Reads
```typescript
const lists = await rh.getWatchlists();                 // your own lists (metadata + ids)
const curated = await rh.getPopularWatchlists();         // Robinhood-curated lists
const items = await rh.getWatchlistItems(lists[0].id);   // items enriched with symbol/name
const optContracts = await rh.getOptionWatchlistContracts(); // single-leg option contracts on the options watchlist
const optList = await rh.getOptionWatchlist();           // options watchlist metadata (Watchlist | null) — for contracts use getOptionWatchlistContracts()
```

### Writes — `updateWatchlistItems(listId, operation, items)`
A single-list, single-operation primitive; it builds the underlying bulk wire-map internally, so multi-list / mixed create+delete writes are not expressible.
```typescript
// Add AAPL: resolve the exact instrument first (never findInstruments()[0]).
const inst = await rh.resolveInstrumentBySymbol("AAPL");
await rh.updateWatchlistItems(listId, "create", [
  { object_type: "instrument", object_id: inst.id },
]);

// Remove: match against the list's actual members so you delete the listed
// object_id (dodging stale-instrument ids), then delete only what's present.
const present = await rh.getWatchlistItems(listId);
const hit = present.find((p) => p.symbol?.toUpperCase() === "AAPL");
if (hit?.object_id) {
  await rh.updateWatchlistItems(listId, "delete", [
    { object_type: "instrument", object_id: hit.object_id },
  ]);
}
```
`object_type` is `"instrument"` (stocks/ETFs), `"index"`, or `"currency_pair"` for adds; reads may also surface `"option_strategy"` (options-watchlist entries), `"futures"`, and `"tokenized_stock"`. For indexes/crypto the `object_id` is the UUID directly (from `getIndexInstruments()` / `getCurrencyPairs()`).

### List metadata writes — create / update / delete
```typescript
const list = await rh.createWatchlist("Tech Longs", { displayDescription: "high-conviction" });
// list.id → populate with updateWatchlistItems(list.id, "create", …)

await rh.updateWatchlist(list.id, { displayName: "Tech Longs (2026)" }); // rename; items untouched

await rh.deleteWatchlist(list.id); // client-only — no MCP tool (no official delete_watchlist)
```
`createWatchlist` / `updateWatchlist` are the `robinhood_create_watchlist` / `robinhood_update_watchlist` tools.

### Follow / unfollow a curated list — `followWatchlist(listId)` / `unfollowWatchlist(listId)`
Make a Robinhood-**curated** list (id from `getPopularWatchlists()`) appear in / disappear from the user's watchlists. **Confirm with the user first.** Both return `void`; the API echoes the request, not the new state, so treat success declaratively (`followed: true` / `followed: false`).
```typescript
const curated = await rh.getPopularWatchlists();
await rh.followWatchlist(curated[0].id);    // now shows in the user's watchlists
await rh.unfollowWatchlist(curated[0].id);  // removed again
```

### Options watchlist writes — `getOptionInstrumentById(optionId)` + `quickAddOption(optionId, "long")`
Add a single-leg option contract to the options watchlist. **Confirm with the user first.** **Long only** — `quickAddOption` mints one single-leg **long** contract; short-leg entries return an error directing to the Robinhood app, and multi-leg strategies aren't modifiable here. Validate a raw `option_id` first with `getOptionInstrumentById` (throws on an unknown id). Already-present contracts are no-ops (deduped).
```typescript
const inst = await rh.getOptionInstrumentById(optionId); // validate the id (throws if unknown)
await rh.quickAddOption(inst.id, "long");                 // add as a single-leg long contract
```

## Scanner Methods

Read-only. Scan *writes* (create/run/update) are not yet exposed.

```typescript
// Filter vocabulary for building scans — an embedded static catalog captured
// from Robinhood's official scanner service (account-agnostic, no network).
const specs = await rh.getScannerFilterSpecs(); // ScannerFilterSpec[]
const rsi = specs.find((s) => s.filter_type === "FILTER_TYPE_RSI");
// rsi.supported_predicates, rsi.supported_lengths, rsi.supported_intervals, ...

// Your saved scanners (raw Beacon objects, camelCase wire fields).
const scans = await rh.getScans(); // Scan[]  — [] when you have none
for (const s of scans) {
  s.scanId;                              // id
  s.title;                               // name
  s.activeScanConfiguration?.filters;    // the scan's filter config
  s.activeScanConfiguration?.sortingColumnId;
}
```

The client returns **raw** scan objects. The MCP tool (`robinhood_get_scans`) additionally derives the official-DTO fields `scan_id`/`title`/`column_count` and nulls the three it can't reproduce (`filter_summary`/`cortex_managed`/`sorting`) — when working through the client directly, read those off `activeScanConfiguration` yourself.

## Realized P&L Methods

Read-only, **computed** — Robinhood has no realized-P&L REST endpoint for a standard token. `getRealizedPnl` returns the full computed dataset (all realized trades, not windowed); apply your own span/bucketing, or use the two MCP tools which window and bucket for you.

```typescript
// Equity: independent economic FIFO incl. fees (NOT Robinhood's booked/tax number).
// Crypto: native gain_loss. Options: excluded. Fetches full order history (can be slow).
const pnl = await rh.getRealizedPnl(); // { trades, overrunSymbols, totalRealizedGain }
// Restrict asset classes / target an account:
const eq = await rh.getRealizedPnl({ assetClasses: ["equity"], accountNumber });

for (const t of pnl.trades) {
  t.symbol; t.side; t.quantity; t.price;
  t.realizedGain;          // proceeds − matched cost − fees (equity) | native gain_loss (crypto)
  t.closedAt; t.openedAt;  // openedAt is null for crypto
  t.assetClass;            // "equity" | "crypto"
}
pnl.totalRealizedGain;     // Σ realizedGain
pnl.overrunSymbols;        // sells that exceeded recorded buys → basis incomplete (transfer/reward/split)
```

Pure helpers live in `src/compute/realized-pnl.ts` (`computeFifoRealized`, `bucketRealized`). For reconciliation against Robinhood's own numbers, `bun run pnl:harness` runs locally so your account number never enters a transcript.

## Tax Lots

Read-only, and unlike realized P&L this is a **real endpoint passthrough** (`GET /tax_lots/open/{account}/{instrument}/`), not a computed figure. One equity symbol per call; the symbol is resolved by exact match.

### `getEquityTaxLots(symbol, { accountNumber }): Promise<TaxLot[]>`
```typescript
const lots = await rh.getEquityTaxLots("AAPL", { accountNumber });
for (const lot of lots) {
  lot.quantity; lot.quantity_available;
  lot.book_cost_basis; lot.tax_cost_basis; lot.book_proceeds;
  lot.open_date; lot.term;          // "long_term" | "short_term"
  lot.cost_per_share;
  lot.is_selectable; lot.open_lot_id; lot.order_id;
}
```
Results are complete (there is no cursor — a tax-lots page URL embeds the account number, so none is surfaced). Per-lot account numbers are scrubbed. The exported `TaxLot` / `TaxLotSchema` types describe each lot.
