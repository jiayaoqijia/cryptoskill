# CoinGecko Pro Permissions Checklist

Use this checklist whenever Pro mode is requested.

## Tier validation

1. Call `GET /key` on `pro-api` with `x-cg-pro-api-key`.
2. If response includes code `10011`, this is a Demo key and Pro access is not active.
3. If Cloudflare 403 HTML is returned, retry with explicit `User-Agent` and `Accept: application/json`.

## Common Pro-only target endpoints

- `GET /global/market_cap_chart`
- `GET /key`
- Other endpoints flagged by `10005` on public base

## Fallback policy

- If Pro check fails, route to `coingecko-demo-api` with public-base endpoints.
- Keep one structured capability block in output:
  - `key_tier`: pro or demo
  - `endpoint`: path
  - `status`: available or blocked
  - `error_code`: numeric or null
