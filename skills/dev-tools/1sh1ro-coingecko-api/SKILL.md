---
name: coingecko-api
description: "Call the CoinGecko API to fetch crypto prices, market data, coin metadata, or charts; use when a task requires querying CoinGecko endpoints, building a quick data pull, or automating CoinGecko API requests (free or Pro)."
---

# CoinGecko API

## Overview

Use this skill to call CoinGecko API endpoints reliably and repeatedly. It provides a small, standard-library script for GET requests, plus lightweight notes on common endpoints and auth.

## Quick Start

Run the bundled script with a relative endpoint path:

```bash
python3 scripts/coingecko_get.py simple/price --param ids=bitcoin --param vs_currencies=usd
```

Use a full URL if you already have one:

```bash
python3 scripts/coingecko_get.py "https://api.coingecko.com/api/v3/coins/bitcoin"
```

## Common Tasks

Get a spot price:

```bash
python3 scripts/coingecko_get.py simple/price \
  --param ids=bitcoin,ethereum \
  --param vs_currencies=usd
```

List all coins:

```bash
python3 scripts/coingecko_get.py coins/list
```

Get coin detail:

```bash
python3 scripts/coingecko_get.py coins/bitcoin
```

Get a market chart:

```bash
python3 scripts/coingecko_get.py coins/bitcoin/market_chart \
  --param vs_currency=usd \
  --param days=30
```

## Auth And Base URL

If your plan requires an API key, pass it explicitly or set env vars:

- `COINGECKO_API_KEY` for the value
- `COINGECKO_API_KEY_HEADER` for the header name

Override the base URL as needed:

- Flag: `--base-url https://...`
- Env: `COINGECKO_BASE_URL`

Example:

```bash
COINGECKO_BASE_URL="https://api.coingecko.com/api/v3" \
COINGECKO_API_KEY="..." \
COINGECKO_API_KEY_HEADER="x-cg-pro-api-key" \
python3 scripts/coingecko_get.py coins/bitcoin
```

## Output And Files

- `--pretty` pretty-prints JSON
- `--raw` bypasses JSON parsing
- `--out path.json` writes to a file

Example:

```bash
python3 scripts/coingecko_get.py coins/markets \
  --param vs_currency=usd \
  --param per_page=5 \
  --pretty \
  --out /tmp/markets.json
```

## Reliability Tips

- Use `--retries` and `--backoff` for 429/5xx responses.
- Increase `--timeout` for large responses.
- Cache results if you poll frequently.

## References

Read `references/coingecko_api.md` for base URL and endpoint patterns. Always verify in official CoinGecko docs if an endpoint or header fails.

