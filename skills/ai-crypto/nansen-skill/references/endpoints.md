# Nansen API — Endpoint Catalog

Base: `https://api.nansen.ai`
Auth: header `apiKey: <key>` (camelCase)
All **POST** with JSON body containing `chains`, optional `filters`, `pagination`, `order_by`.

Full OpenAPI schemas: see `docs/nansen/llms-full.txt` in the skills repo.

## Solana support quick matrix

| Category | Solana? |
|----------|---------|
| Smart Money (netflow, dex-trades, holdings, historical-holdings, dcas) | ✅ Full |
| TGM flows, transfers, holders, pnl | ✅ Full |
| Profiler (current-balances, historical-balances, pnl) | ✅ Full |
| Profiler single-tx lookup | ❌ EVM only |
| Labels endpoints | ❌ EVM only |
| Hyperliquid perps | N/A (chain is `hyperliquid`) |

## Smart Money — 5 credits each

| Endpoint | Path | Description |
|----------|------|-------------|
| Netflow | `/api/v1/smart-money/netflow` | Net capital flow per token (DEX + CEX) |
| DEX Trades | `/api/v1/smart-money/dex-trades` | Individual trades |
| Holdings | `/api/v1/smart-money/holdings` | Aggregated current balances |
| Historical Holdings | `/api/v1/smart-money/historical-holdings` | Balance snapshots over time |
| Perp Trades | `/api/v1/smart-money/perp-trades` | Hyperliquid perps |
| DCAs | `/api/v1/smart-money/dcas` | Jupiter DCA orders (Solana) |

Sort fields (netflow example): `net_flow_1h_usd`, `net_flow_24h_usd`, `net_flow_7d_usd`, `net_flow_30d_usd`, `market_cap_usd`, `token_age_days`, `trader_count`.

Common filters:
- `include_smart_money_labels` / `exclude_smart_money_labels` — array of label enums
- `token_address` — single or array
- `include_stablecoins`, `include_native_tokens` — default false
- `token_sector` — array of sector strings
- `market_cap_usd`, `token_age_days`, `trader_count` — `{min, max}` ranges
- `value_usd` — `{min, max}` USD bound

## Profiler — mostly 1 credit

| Endpoint | Path | Credits | Solana |
|----------|------|---------|--------|
| Current Balances | `/api/v1/profiler/address/current-balances` | 1 | ✅ |
| Historical Balances | `/api/v1/profiler/address/historical-balances` | 1 | ✅ |
| Transactions | `/api/v1/profiler/address/transactions` | 1 | ✅ |
| Transaction with Token Lookup | `/api/v1/profiler/address/transactions-with-token-transfer` | 1 | ❌ EVM only |
| Counterparties | `/api/v1/profiler/address/counterparties` | **5** | ✅ |
| Related Wallets | `/api/v1/profiler/address/related-wallets` | 1 | ✅ |
| PnL Summary | `/api/v1/profiler/address/pnl-summary` | 1 | ✅ |
| PnL Detail | `/api/v1/profiler/address/pnl` | 1 | ✅ |
| Labels (common) | `/api/v1/profiler/address/labels` | **100** | ❌ EVM only |
| Labels (premium) | `/api/v1/profiler/address/premium-labels` | **500** | ❌ EVM only |
| Perp Positions | `/api/v1/profiler/perp-positions` | 1 | N/A |
| Perp Trades | `/api/v1/profiler/perp-trades` | 1 | N/A |
| Perp Leaderboard | `/api/v1/profiler/perp-leaderboard` | **5** | N/A |

## Token God Mode (TGM) — 1–150 credits

| Endpoint | Path | Credits | Solana |
|----------|------|---------|--------|
| Token Information | `/api/v1/tgm/token-information` | 1 | ✅ |
| Token OHLCV | `/api/v1/tgm/token-ohlcv` | 1 | ✅ |
| Token Screener | `/api/v1/tgm/token-screener` | 1 | ✅ |
| Flow Intelligence | `/api/v1/tgm/flow-intel` | 1 | ✅ |
| Flows | `/api/v1/tgm/flows` | 1 | ✅ |
| Transfers | `/api/v1/tgm/transfers` | 1 | ✅ |
| DEX Trades | `/api/v1/tgm/dex-trades` | 1 | ✅ |
| Who Bought/Sold | `/api/v1/tgm/who-bought-sold` | 1 | ✅ |
| Jupiter DCAs | `/api/v1/tgm/dcas` | 1 | ✅ |
| Indicators (Nansen Score) | `/api/v1/tgm/indicators` | **5** | ✅ |
| Holders | `/api/v1/tgm/holders` | **5 / 150** | ✅ |
| PnL Leaderboard | `/api/v1/tgm/pnl-leaderboard` | **5 / 150** | ✅ |
| Perp Screener | `/api/v1/tgm/perp-screener` | 1 | N/A |
| Perp Positions | `/api/v1/tgm/perp-positions` | **5 / 150** | N/A |
| Perp PnL Leaderboard | `/api/v1/tgm/perp-pnl-leaderboard` | **5 / 150** | N/A |
| Perp Trades | `/api/v1/tgm/perp-trades` | **5 / 150** | N/A |

**5 / 150 rule:** default cost is 5. Setting `premium_labels: true` in request body → 150 credits. Don't set unless user explicitly wants premium labels.

## Portfolio — 1 credit

| Endpoint | Path | Credits |
|----------|------|---------|
| DeFi Holdings | `/api/v1/portfolio/defi-holdings` | 1 |

## Prediction Markets — mostly 1 credit

11 endpoints. Key ones:
- `/api/v1/prediction-market/market-screener` (1)
- `/api/v1/prediction-market/event-screener` (1)
- `/api/v1/prediction-market/ohlcv` (1)
- `/api/v1/prediction-market/pnl-by-address` (1)
- `/api/v1/prediction-market/top-holders` (**5**)
- `/api/v1/prediction-market/pnl-by-market` (**5**)
- `/api/v1/prediction-market/position-detail` (**5**)

## Hyperliquid (perpetuals only)

| Endpoint | Path |
|----------|------|
| Address Leaderboard | `/api/v1/hyperliquid/leaderboard` |
| Address Perp Positions | `/api/v1/profiler/perp-positions` (pass `chains: ["hyperliquid"]`) |
| Address Perp Trades | `/api/v1/profiler/perp-trades` |

## Agent (AI-powered research)

| Endpoint | Path | Credits |
|----------|------|---------|
| Fast Research | `/api/v1/agent/fast` | **200** |
| Expert Research | `/api/v1/agent/expert` | **750** |

Both extremely expensive. `/agent/expert` = ~half of Pro starter credits in one call. **Always confirm with user before calling agent endpoints.**

## Pagination (universal)

```json
"pagination": {
  "page": 1,
  "per_page": 1000  // max
}
```

Response `pagination.is_last_page` indicates end of set.

**Always set `per_page: 1000` for batches** — default is 10.

## Sort order (universal)

```json
"order_by": [
  {"field": "net_flow_7d_usd", "direction": "DESC"},
  {"field": "market_cap_usd", "direction": "DESC"}
]
```

Multi-field sort supported. Fields are enum per endpoint — if you get 422, check allowed sort fields in `llms-full.txt`.
