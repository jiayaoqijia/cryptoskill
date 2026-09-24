# CMC Plan Permission Matrix

Validated with current key on 2026-02-23.

## Plan summary from `/key/info`

- `credit_limit_monthly`: 10000
- `rate_limit_minute`: 30

## Available (HTTP 200 observed)

- `/key/info`
- `/global-metrics/quotes/latest`
- `/cryptocurrency/listings/latest`
- `/cryptocurrency/quotes/latest`
- `/cryptocurrency/map`
- `/cryptocurrency/categories`
- `/tools/price-conversion`
- `/fiat/map`
- `/exchange/map`

## Blocked by plan (`error_code=1006`)

- `/global-metrics/quotes/historical`
- `/cryptocurrency/ohlcv/latest`
- `/cryptocurrency/ohlcv/historical`
- `/cryptocurrency/quotes/historical`
- `/cryptocurrency/market-pairs/latest`
- `/cryptocurrency/price-performance-stats/latest`
- `/exchange/listings/latest`
- `/exchange/quotes/latest`
- `/exchange/market-pairs/latest`
- `/content/latest`

## Fallback guidance

- If global historical is blocked, use:
  - CMC global latest snapshot for current structure
  - CoinGecko per-coin history for trend proxies
  - Deribit for derivatives volatility and perp metrics
