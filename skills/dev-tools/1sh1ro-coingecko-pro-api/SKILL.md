---
name: coingecko-pro-api
description: "Use when tasks require CoinGecko Pro endpoints and permission-aware workflows on pro-api.coingecko.com, including key-tier validation and fallback behavior."
---

# CoinGecko Pro API

Use this skill only when a Pro key is expected.

## When to use

- The task needs Pro-only CoinGecko endpoints.
- The user explicitly requests Pro API behavior or Pro permission checks.

## Quick start

```bash
export COINGECKO_API_KEY="..."
python3 scripts/coingecko_pro_get.py key --pretty
```

```bash
python3 scripts/coingecko_pro_get.py global/market_cap_chart \
  --param vs_currency=usd \
  --param days=90 \
  --pretty
```

## Workflow

1. Always target base URL `https://pro-api.coingecko.com/api/v3`.
2. Send key in header `x-cg-pro-api-key`.
3. Validate tier first with `/key`.
4. If API returns code `10011`, key is Demo and must switch to `coingecko-demo-api` skill.
5. If endpoint returns `10005`, mark endpoint unavailable for current plan.
6. Keep per-endpoint permission notes in report output.

## References

- Read `references/pro-permissions.md` before building new Pro data pulls.
