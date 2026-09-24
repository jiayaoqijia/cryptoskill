# CoinGecko Demo Endpoint Permissions

Validated with Demo key on 2026-02-23.

## Base URL

- Use: `https://api.coingecko.com/api/v3`
- Do not use with Demo key: `https://pro-api.coingecko.com/api/v3`

## Available (HTTP 200 observed)

- `GET /ping`
- `GET /global`
- `GET /coins/categories`
- `GET /coins/markets`
- `GET /coins/list`
- `GET /coins/{id}`
- `GET /coins/{id}/market_chart`
- `GET /coins/{id}/ohlc`
- `GET /coins/{id}/market_chart/range` (only within last 365 days)
- `GET /search/trending`
- `GET /derivatives`
- `GET /derivatives/exchanges`
- `GET /exchanges`
- `GET /exchange_rates`
- `GET /simple/price`
- `GET /nfts/list`

## Restricted / Pro-only

- `GET /global/market_cap_chart` -> 401 with code 10005
- `GET /key` -> Pro-only

## Known limits

- Range history over 365 days returns error code 10012.
- Treat 401/403 as capability errors, not transient network errors.

## Fallback guidance

- If `global/market_cap_chart` is blocked, use:
  - `coins/markets` snapshot for top-N market structure
  - `coins/{id}/market_chart` for representative trend series
