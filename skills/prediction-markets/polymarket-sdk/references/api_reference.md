# Polymarket US API Reference

## Base URLs

- **Public data (no auth):** `https://gateway.polymarket.us`
- **Trading (auth required):** `https://api.polymarket.us`

## Authentication

Ed25519 signature auth. Required headers for `api.polymarket.us`:

| Header | Description |
|--------|-------------|
| `X-PM-Access-Key` | API key ID (UUID) |
| `X-PM-Timestamp` | Unix timestamp in milliseconds |
| `X-PM-Signature` | Base64-encoded Ed25519 signature of `timestamp + method + path` |

The Python SDK handles this automatically when configured with `key_id` and `secret_key`.

## Python SDK Quick Reference

```python
from polymarket_us import PolymarketUS

# Public (no auth needed)
client = PolymarketUS()

# Authenticated
client = PolymarketUS(key_id="...", secret_key="...")
```

### Events
- `client.events.list({"limit": 10, "active": True})` — list events with filters
- `client.events.retrieve(event_id)` — get event by ID
- `client.events.retrieve_by_slug("super-bowl-2025")` — get event by slug

### Markets
- `client.markets.list({"limit": 10})` — list markets with filters
- `client.markets.retrieve(market_id)` — get market by ID
- `client.markets.retrieve_by_slug("btc-100k")` — get market by slug
- `client.markets.book("btc-100k")` — full order book
- `client.markets.bbo("btc-100k")` — best bid/offer (lightweight)
- `client.markets.settlement("market-slug")` — settlement price

### Search
- `client.search.query({"query": "bitcoin", "limit": 10})` — full-text search

### Series & Sports
- `client.series.list()` / `client.series.retrieve(id)`
- `client.sports.list()` / `client.sports.teams()`

### Account (auth required)
- `client.account.balances()` — buying power, asset values, pending

### Portfolio (auth required)
- `client.portfolio.positions()` — all positions (filter with `{"market": "slug"}`)
- `client.portfolio.activities()` — trades, resolutions, deposits/withdrawals

### Orders (auth required)
- `client.orders.list()` — open orders
- `client.orders.retrieve(order_id)` — specific order
- `client.orders.create({...})` — place order
- `client.orders.preview({...})` — preview before placing
- `client.orders.cancel(order_id)` — cancel specific order
- `client.orders.cancel_all()` — cancel all open orders
- `client.orders.modify(order_id, {...})` — modify existing order
- `client.orders.close_position({"marketSlug": "..."})` — close position

## Order Create Parameters

```python
client.orders.create({
    "marketSlug": "btc-100k-2025",
    "intent": "ORDER_INTENT_BUY_LONG",      # BUY_LONG, SELL_LONG, BUY_SHORT, SELL_SHORT
    "type": "ORDER_TYPE_LIMIT",              # LIMIT or MARKET
    "price": {"value": "0.55", "currency": "USD"},  # always YES side price
    "quantity": 100,                          # shares
    "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL", # GTC, GTD, IOC, FOK
})
```

### Order Intents
| Intent | Meaning |
|--------|---------|
| `ORDER_INTENT_BUY_LONG` | Buy YES shares |
| `ORDER_INTENT_SELL_LONG` | Sell YES shares |
| `ORDER_INTENT_BUY_SHORT` | Buy NO shares |
| `ORDER_INTENT_SELL_SHORT` | Sell NO shares |

### Price Rules
- `price.value` ALWAYS refers to the YES (long) side price
- To buy NO at price X, set `price.value = 1.00 - X`
- Valid range: 0.001 to 0.999
- In market slugs: first team = YES, second team = NO

### Order States
`PENDING_NEW → PARTIALLY_FILLED → FILLED` or `→ CANCELED / REJECTED / EXPIRED`

## Market List Filters
- `limit`, `offset`, `orderBy` (volumeNum, liquidityNum, createdAt), `orderDirection`
- `active`, `closed`, `archived` (booleans)
- `liquidityNumMin/Max`, `volumeNumMin/Max`
- `startDateMin/Max`, `endDateMin/Max`
- `tagId`, `relatedTags`, `cyom`, `gameId`, `sportsMarketTypes`

## Event List Filters
- `limit`, `offset`, `orderBy` (volume, liquidity, startTime), `orderDirection`
- `active`, `closed`, `archived`, `featured` (booleans)
- `tagId`, `tagSlug`, `relatedTags`, `seriesId`
- `eventDate` (YYYY-MM-DD), `eventWeek`

## Search Filters
- `query`, `limit`, `page`, `seriesIds`, `marketType`
- `startTimeMin/Max`, `closedTimeMin/Max`, `status` (active/closed/upcoming)

## Error Types
| Exception | Description |
|-----------|-------------|
| `AuthenticationError` | Invalid/missing credentials |
| `BadRequestError` | Invalid parameters |
| `NotFoundError` | Resource not found |
| `RateLimitError` | Rate limited |
| `APITimeoutError` | Timeout |
| `APIConnectionError` | Network error |
