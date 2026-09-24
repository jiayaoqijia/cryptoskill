---
name: cex-api-orchestrator
description: "Use when tasks must coordinate CEX report data across CoinGecko, CMC, Deribit, Coinglass, Glassnode, Nansen, Santiment, and Alternative.me with capability checks and fallback routing."
---

# CEX API Orchestrator

Use this as the top-level planning skill for report generation.

## Goal

Route each metric to the best available API source without failing the full report when one endpoint is blocked.

## Skill routing order

1. CoinGecko tier check
2. CMC plan check
3. Deribit public data pull
4. Paid-source key check (Coinglass / Glassnode / Nansen / Santiment)
5. Free-source check (Alternative.me)
6. Metric-level source selection and fallback

## Capability checks

1. CoinGecko:
   - Pro test on `pro-api` with `/key`
   - If error code `10011`, switch to Demo route
2. CMC:
   - Read `/key/info`
   - Build allowed endpoint set
3. Deribit:
   - Probe one known method (`public/ticker`) and continue if reachable
4. Coinglass:
   - Check `COINGLASS_API_KEY` exists
   - Probe one endpoint and classify plan capability by returned error
5. Glassnode:
   - Check `GLASSNODE_API_KEY` exists
   - Probe one metric path and classify tier by returned error
6. Nansen:
   - Check `NANSEN_API_KEY` + `NANSEN_BASE_URL`
   - Probe one endpoint and classify capability
7. Santiment:
   - Check `SANTIMENT_API_KEY`
   - Run GraphQL probe and classify capability
8. Alternative.me:
   - Probe `/fng/` as no-key sentiment fallback

## Daily report minimum payload

- Market snapshot:
  - CMC `global-metrics/quotes/latest`
  - CoinGecko `global`
  - CoinGecko `coins/markets` top-N table
- Derivatives:
  - Deribit `public/ticker` for BTC/ETH perp
  - Deribit `public/get_volatility_index_data`
  - Coinglass OI/funding/liquidation (when key available)
- On-chain funds:
  - Glassnode exchange/supply metrics (when key available)
  - Nansen smart-money/flow metrics (when key available)
- Sentiment:
  - Alternative.me `fng` (free fallback)
  - Santiment social/sentiment metrics (when key available)
- Narratives:
  - CoinGecko `coins/categories`
  - CoinGecko `search/trending`

## Fallback policy

- Do not fail full report on a single blocked endpoint.
- Add one structured `data_gaps` item per blocked call.
- Prefer alternate endpoint in same provider before switching provider.

## References

- `references/call-matrix.md`
- `references/source-access-matrix.md`
