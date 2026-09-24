---
name: coingecko-demo-api
description: "Use when tasks need CoinGecko data with a Demo/Public key on api.coingecko.com, including endpoint limits, 365-day history constraints, and repeatable pull commands."
---

# CoinGecko Demo API

Use this skill for CoinGecko Demo/Public access.

## When to use

- The task needs CoinGecko market, category, trend, or derivatives data.
- The available key is a Demo key (`x-cg-demo-api-key`).
- You need clear handling for Pro-only endpoint failures.

## Quick start

```bash
export COINGECKO_API_KEY="..."
python3 scripts/coingecko_demo_get.py global --pretty
```

```bash
python3 scripts/coingecko_demo_get.py coins/markets \
  --param vs_currency=usd \
  --param order=market_cap_desc \
  --param per_page=20 \
  --param page=1 \
  --pretty
```

## Workflow

1. Always call base URL `https://api.coingecko.com/api/v3`.
2. Send key in header `x-cg-demo-api-key` when key exists.
3. Prefer endpoints listed in `references/demo-endpoints.md` as available.
4. For historical range API, enforce last 365 days.
5. If endpoint returns `error_code=10005`, mark it as Pro-only and use fallback.
6. Keep raw API errors in report metadata for auditability.

## Report-safe endpoint set

- `global`
- `coins/categories`
- `coins/markets`
- `coins/{id}/market_chart`
- `coins/{id}/ohlc`
- `search/trending`
- `derivatives`
- `derivatives/exchanges`
- `exchanges`
- `simple/price`

## References

- Read `references/demo-endpoints.md` for tested endpoint permissions and fallback rules.
