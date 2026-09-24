---
name: coinglass-api
description: "Use when tasks need Coinglass derivatives data (OI, funding, liquidations) with API-key auth, including paid-tier permission checks and fallback behavior."
---

# Coinglass API

Use this skill for Coinglass Open API calls.

## When to use

- The task needs OI, funding, liquidation, long/short, exchange derivatives metrics.
- The endpoint is from Coinglass Open API.
- You need to detect paid-plan restrictions early.

## Quick start

```bash
export COINGLASS_API_KEY="..."
python3 scripts/coinglass_get.py futures/funding-rate/history \
  --param symbol=BTC \
  --param interval=1h \
  --pretty
```

## Workflow

1. Send `CG-API-KEY` header from `COINGLASS_API_KEY`.
2. Use base URL from `COINGLASS_BASE_URL` or default in script.
3. On non-200, capture raw error JSON and mark as capability block.
4. Keep one capability note in report per blocked endpoint.

## References

- `references/permissions.md` for paid-access notes and expected auth behavior.
