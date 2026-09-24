---
name: deribit-api
description: "Use when tasks require Deribit JSON-RPC market data calls, including ticker, DVOL, book summaries, and permission-aware request shaping for public endpoints."
---

# Deribit API

Use this skill for Deribit JSON-RPC calls.

## When to use

- The task needs futures/options market data from Deribit.
- You need DVOL, perp funding, OI, or book summary metrics.

## Quick start

```bash
python3 scripts/deribit_rpc.py public/ticker \
  --param instrument_name=BTC-PERPETUAL \
  --pretty
```

```bash
python3 scripts/deribit_rpc.py public/get_volatility_index_data \
  --param currency=BTC \
  --param start_timestamp=1764547200000 \
  --param end_timestamp=1767139199000 \
  --param resolution=3600 \
  --pretty
```

## Workflow

1. Call JSON-RPC endpoint `https://www.deribit.com/api/v2`.
2. Use named params only.
3. For DVOL, request hourly candles (`resolution=3600`) and aggregate to daily if needed.
4. For perp snapshot, use `public/ticker`.
5. For aggregate OI/volume, use `public/get_book_summary_by_currency`.
6. Store `error` objects exactly as returned for diagnostics.

## References

- `references/public-methods.md`
