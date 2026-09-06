# Nansen Filters, Chains, Labels

## Chain enum (full list)

### Supported chain values (37 total)

**EVM (24):**
`ethereum`, `arbitrum`, `avalanche`, `base`, `bitlayer`, `bnb`, `celo`, `chiliz`, `gravity`, `hyperevm`, `iotaevm`, `linea`, `mantle`, `monad`, `optimism`, `plasma`, `polygon`, `ronin`, `scroll`, `sei`, `sonic`, `unichain`, `viction`, `zksync`

**Non-EVM (12):**
`algorand`, `aptos`, `bitcoin`, `hyperliquid`, `near`, `solana`, `stacks`, `starknet`, `stellar`, `sui`, `ton`, `tron`

### Using "all"

Some endpoints accept `chains: ["all"]` → expands to all chains supported by that endpoint.

## Smart Money labels (for `include_smart_money_labels` / `exclude_smart_money_labels`)

| Label | Meaning |
|-------|---------|
| `Fund` | Institutional investment funds |
| `Smart Trader` | Historically profitable traders |
| `30D Smart Trader` | Top performers in 30-day window |
| `90D Smart Trader` | Top performers in 90-day window |
| `180D Smart Trader` | Top performers in 180-day window |
| `Smart HL Perps Trader` | Profitable Hyperliquid perp traders |

**Usage:**
```json
"filters": {
  "include_smart_money_labels": ["Fund", "Smart Trader"]
}
```

Multiple labels = OR filter (match any). Use `exclude_*` to remove noise categories.

## Filter types

### Numeric range filter
Used for prices, volumes, ratios, counts:
```json
"market_cap_usd": {"min": 10000000, "max": 1000000000},
"value_usd": {"min": 100},
"token_age_days": {"max": 30},
"trader_count": {"min": 5}
```
Both `min` and `max` optional. Inclusive bounds.

### Boolean filter
```json
"include_stablecoins": false,
"include_native_tokens": true
```
Default usually `false`.

### Address filter
```json
"token_address": "0xabc...",                              // single
"token_address": ["0xabc...", "0xdef..."],                // array
```

### Sector filter
```json
"token_sector": ["DeFi", "Gaming", "Meme"]
```
Token sectors are human-readable category strings. Refer to `tgm/token-information` for the sector a token belongs to.

## Filter support varies by endpoint

Each endpoint has its own filter schema. If you get 422, the filter isn't supported on that endpoint. Common unsupported combos:

- `token_age_days` on Profiler endpoints (they're about wallets, not tokens)
- `smart_money_labels` on non-Smart Money endpoints
- `trader_count` outside Smart Money

Check the specific endpoint's request schema in `docs/nansen/llms-full.txt` (search for the endpoint path).

## Multi-field sort

```json
"order_by": [
  {"field": "market_cap_usd", "direction": "DESC"},
  {"field": "net_flow_7d_usd", "direction": "ASC"}
]
```

First field is primary sort; subsequent fields break ties.

**Sort fields are enum per endpoint.** Wrong value → 422. Common fields per category:

### Smart Money netflow
`chain`, `token_address`, `token_symbol`, `net_flow_1h_usd`, `net_flow_24h_usd`, `net_flow_7d_usd`, `net_flow_30d_usd`, `token_sectors`, `trader_count`, `token_age_days`, `market_cap_usd`

### Smart Money holdings
`value_usd`, `balance_24h_percent_change`, `balance_7d_percent_change`, `trader_count`, `token_age_days`, `market_cap_usd`

### Profiler PnL
`realized_pnl_usd`, `unrealized_pnl_usd`, `total_pnl_usd`, `win_rate`, `trade_count`

### TGM token-screener
`market_cap_usd`, `volume_24h_usd`, `holder_count`, `price_change_24h`, `nansen_score`

If stuck, run the endpoint once without `order_by` and inspect the returned fields — those are generally the sortable ones.
