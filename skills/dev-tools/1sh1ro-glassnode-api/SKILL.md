---
name: glassnode-api
description: "Use when tasks require Glassnode on-chain metrics API integration with key-based auth, metric-path routing, and paid-plan capability checks."
---

# Glassnode API

Use this skill for Glassnode metric pulls.

## When to use

- The task needs on-chain metrics (exchange flows, supply, entity metrics).
- You want deterministic calls to `/v1/metrics/*` endpoints.
- You need to handle plan-restricted metrics cleanly.

## Quick start

```bash
export GLASSNODE_API_KEY="..."
python3 scripts/glassnode_get.py /v1/metrics/market/price_usd_close \
  --param a=BTC \
  --param i=24h \
  --pretty
```

## Workflow

1. Set `GLASSNODE_API_KEY`.
2. Call metric endpoint path directly.
3. Use `a` (asset), `i` (interval), `s/u` (range) as query params where required.
4. On plan/permission errors, keep endpoint path and error payload in `data_gaps`.

## References

- `references/permissions.md`
