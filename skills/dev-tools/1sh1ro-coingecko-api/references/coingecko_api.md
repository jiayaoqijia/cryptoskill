# CoinGecko API Notes (Reference)

Keep this file small and factual. Always verify against official CoinGecko docs if an endpoint or header fails.

## Base URLs

- Public API default (common): `https://api.coingecko.com/api/v3`
- Pro API often uses a different base URL. If you have a Pro subscription, verify the correct base URL in the official docs and pass it via `--base-url` or `COINGECKO_BASE_URL`.

## Authentication

- Some plans require an API key in a header. The exact header name can vary by plan.
- Use `--api-key` and set `--api-key-header`, or set env vars:
  - `COINGECKO_API_KEY`
  - `COINGECKO_API_KEY_HEADER`

## Common Endpoint Patterns (Verify Before Use)

These are common patterns that have existed historically. Treat them as examples, not guarantees.

- `simple/price` with `ids` and `vs_currencies`
- `coins/list`
- `coins/{id}`
- `coins/markets` with `vs_currency`, `order`, `per_page`, `page`
- `coins/{id}/market_chart` with `vs_currency` and `days`

## Rate Limits & Reliability

- Handle HTTP 429 and 5xx with retries and backoff.
- Add reasonable timeouts.
- Cache results when polling repeatedly.

