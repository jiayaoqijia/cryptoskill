---
name: cmc-api
description: "Use when tasks require CoinMarketCap Pro API calls, endpoint capability checks, and permission-aware fallback design based on current plan limits."
---

# CoinMarketCap API

Use this skill for CMC API integration and plan-aware endpoint selection.

## When to use

- The task needs CMC market/global/exchange metadata.
- You need to map which CMC endpoints are allowed by the current key.

## Quick start

```bash
export CMC_API_KEY="..."
python3 scripts/cmc_get.py /key/info --pretty
```

```bash
python3 scripts/cmc_get.py /global-metrics/quotes/latest --pretty
```

## Workflow

1. Read current plan and limits from `/key/info` first.
2. Build endpoint set from `references/plan-permissions.md`.
3. Call supported endpoints only for production workflows.
4. Treat `error_code=1006` as hard capability block.
5. Emit blocked endpoint summary in report metadata.

## Notes

- Base URL is fixed: `https://pro-api.coinmarketcap.com/v1`.
- Auth header: `X-CMC_PRO_API_KEY`.

## References

- `references/plan-permissions.md`
