# API Reference

**Base URL:** `https://wallet-data.kryptogo.app`

**Authentication:** All endpoints require Bearer token authentication unless noted otherwise.

```
Authorization: Bearer sk_live_<48 hex chars>
```

**Common constants:**
- Wrapped SOL mint: `So11111111111111111111111111111112`
- 1 SOL = 1,000,000,000 lamports (1e9)
- All balance values are normalized by token decimals (6 decimal places as strings)

---

## Account & Rate Limits

### GET /agent/account

Check your current subscription tier and API usage. **This call does not count toward your daily quota.**

```
GET /agent/account
Authorization: Bearer <API_KEY>
```

**Response:**

```json
{
  "tier": "free",
  "daily_limit": 100,
  "daily_calls_used": 12,
  "daily_calls_remaining": 38
}
```

| Tier | Daily Limit |
|------|-------------|
| Free | 100 |
| Pro | 1,000 |
| Alpha | 5,000 |

### Rate Limits by Tier

| Tier  | Daily API Calls | Trading Fee | Signal Dashboard | KOL Finder |
|-------|-----------------|-------------|------------------|------------|
| Free  | 100 calls/day   | 1%          | No               | No         |
| Pro   | 1,000 calls/day | 0.5%        | Yes              | Yes        |
| Alpha | 5,000 calls/day | 0%          | Yes              | Yes        |

---

## Multi-Chain Support

Analysis endpoints support multiple chains via the `chain_id` parameter. **Trading (swap/submit) is currently Solana-only.**

| Chain | chain_id | Address Format | Trading Support |
|-------|----------|----------------|-----------------|
| Solana | `501` (default) | Base58 | Yes |
| BSC | `56` | Hex (0x-prefixed) | Analysis only |
| Base | `8453` | Hex (0x-prefixed) | Analysis only |
| Monad | `143` | Hex (0x-prefixed) | Analysis only |

---

## Analysis APIs

### GET /token-overview

Token metadata and market data.

```
GET /token-overview?address=<token_address>&chain_id=501
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "name": "FARTCOIN",
  "symbol": "FART",
  "logo_url": "https://...",
  "decimals": 9,
  "price": "0.001234",
  "market_cap": "1234567.89",
  "price_change_24h": "-5.23",
  "volume_24h": "567890.12",
  "holders_count": "12345",
  "liquidity": "234567.89",
  "total_supply": "1000000000",
  "circulating_supply": "950000000",
  "risk_level": 1,
  "creation_time": 1700000000
}
```

All fields are nullable. Numeric fields are strings.

---

### GET /analyze/:token_mint

Full cluster analysis for a token.

```
GET /analyze/<token_mint>?chain_id=501
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "clusters": [
    {
      "wallets": [
        {
          "address": "Abc123...",
          "token_balance": "500000.000000",
          "sol_balance": "10.000"
        }
      ],
      "total_balance": "1500000.000000",
      "sol_balance": "30.000"
    }
  ],
  "wintermute_balances": [
    { "address": "...", "token_balance": "...", "sol_balance": "..." }
  ],
  "other_top_holders": [
    { "address": "...", "token_balance": "...", "sol_balance": "..." }
  ],
  "address_metadata": {
    "Abc123...": { "label": "kol_name", "twitter_username": "kol_handle" }
  }
}
```

- `clusters`: Ordered by `total_balance` descending. Each cluster groups related wallets.
- `wintermute_balances`: Market maker (Wintermute) addresses, separated for clarity.
- `other_top_holders`: Top 200 non-cluster addresses (subject to survivorship bias).
- `address_metadata`: Known labels and social accounts for addresses.
- For EVM chains: uses `native_balance` instead of `sol_balance`, no `wintermute_balances`.

**Alternative:** `POST /analyze-token` with body `{"token_mint": "...", "chain_id": 501}` — same response, Solana only.

---

### GET /analyze-cluster-change/:token_mint

Cluster holding ratio and change trends across multiple time periods.

```
GET /analyze-cluster-change/<token_mint>?chain_id=501&include_top_holders=true
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "cluster_ratio": 0.35,
  "changes": {
    "15m": 0.001,
    "1h": 0.005,
    "4h": 0.012,
    "1d": 0.03,
    "7d": 0.08
  },
  "chart_data": {
    "1h": [
      { "timestamp": 1700000000, "balance": 0.33 },
      { "timestamp": 1700000120, "balance": 0.34 }
    ]
  },
  "top_holder_ratio": 0.25,
  "top_holder_changes": { "15m": 0.0, "1h": 0.001, "4h": -0.002, "1d": 0.01, "7d": 0.02 },
  "top_holder_chart_data": { "1h": [...], "4h": [...], ... }
}
```

- `cluster_ratio`: Current insider holding as fraction of total supply (0.35 = 35%)
- `changes`: Ratio change per period (positive = accumulating, negative = distributing)
- `chart_data`: Time series per period for trend visualization
- `top_holder_*`: Same metrics for non-cluster top holders (only when `include_top_holders=true`)

**Chart data granularity per period:**

| Period | Interval | Data Points |
|--------|----------|-------------|
| 15m | 1 min | ~15 |
| 1h | 2 min | ~30 |
| 4h | 5 min | ~48 |
| 1d | 30 min | ~48 |
| 7d | 4 hours | ~42 |

---

### POST /balance-history

Time-series balance data for specific wallets on a token.

```
POST /balance-history
{
  "token": "<token_address>",
  "wallets": ["<wallet_1>", "<wallet_2>"],
  "after": 1700000000,
  "bar": "1H",
  "limit": 100,
  "chain_id": 501
}
```

**Auth:** Bearer API key required. Bar/time restrictions by tier (Free: 1H/4H/1D, 7d lookback; Pro: +5m/15m, 90d; Alpha: +1m, unlimited).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `token` | string | Yes | Token address |
| `wallets` | []string | Yes | Min 1 wallet |
| `after` | int64 | Yes | Unix timestamp start |
| `bar` | string | Yes | `1m`, `5m`, `15m`, `1H`, `4H`, `1D` |
| `limit` | int | Yes | 1-1000 |

**Response:** Array of `{"timestamp": int, "balance": "string"}` points.

---

### POST /wallet-labels

Behavior labels for multiple wallets (smart money, whale, blue-chip, high-frequency).

```
POST /wallet-labels
{
  "token_mint": "<token_address>",
  "wallets": ["<wallet_1>", "<wallet_2>"]
}
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "token_mint": "...",
  "data": {
    "<wallet_address>": [
      {
        "label_type": "smart_money",
        "token_mint": null,
        "token_symbol": null,
        "usd_value": 150000.50
      }
    ]
  }
}
```

Label types: `smart_money`, `high_frequency`, `whale`, `blue_chip_profit`. Only wallets with labels are included; unlabeled wallets are omitted.

---

### POST /token-wallet-labels

Token-specific labels: developer, sniper, bundle, new_wallet.

```
POST /token-wallet-labels
{ "token_mint": "<token_address>" }
```

**Auth:** Bearer API key required.

**Response:** Same structure as `/wallet-labels` but with label types: `developer`, `sniper`, `bundle`, `new_wallet`.

---

### GET /balance-increase/:token_mint

Range accumulation filter -- who bought the most in a time range.

```
GET /balance-increase/<token_mint>?from=<unix_ts>&to=<unix_ts>&chain_id=501
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "addresses": [
    {
      "address": "...",
      "balance_at_from": "100.000000",
      "balance_at_to": "500.000000",
      "current_balance": "480.000000",
      "balance_change_in_period": "400.000000",
      "balance_change_after_period": "-20.000000",
      "sol_balance": "1.500"
    }
  ],
  "address_metadata": { ... },
  "from_time": "2024-01-01T00:00:00Z",
  "to_time": "2024-01-02T00:00:00Z"
}
```

Max 500 results. Useful for verifying pre-pump accumulation: set range to 2-3 days before spike and check if top accumulators are known clusters.

---

### GET /top-holders-snapshot/:token_mint

Point-in-time top holder snapshot for before/after comparison.

```
GET /top-holders-snapshot/<token_mint>?timestamp=<unix_ts>&chain_id=501
```

**Auth:** Bearer API key required. Returns up to 1000 holders.

**Response:**
```json
{
  "top_holders": [
    { "address": "...", "balance": "123456.789000" }
  ],
  "address_metadata": { ... },
  "snapshot_time": "2024-01-01T00:00:00Z"
}
```

---

### GET /historical-top-holders/:token_mint

Addresses that held the most at ANY point in history.

```
GET /historical-top-holders/<token_mint>?chain_id=501
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "historical_top_holders": [
    {
      "address": "...",
      "current_balance": "100.000000",
      "historical_max_balance": "500.000000"
    }
  ],
  "address_metadata": { ... }
}
```

---

### GET /fresh-addresses/:token_mint

New wallet addresses holding a token (Solana only).

```
GET /fresh-addresses/<token_mint>
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "fresh_addresses": [
    {
      "address": "...",
      "current_balance": "100.000000",
      "historical_max_balance": "500.000000"
    }
  ],
  "address_metadata": { ... }
}
```

---

### GET /signal-dashboard

Network-wide accumulation signals (most recent ~100).

```
GET /signal-dashboard
```

**Auth:** Required. Tier: Pro or Alpha only.

**Response:**
```json
{
  "signals": [
    {
      "id": 12345,
      "chain": "sol",
      "chain_id": 501,
      "contract_address": "...",
      "symbol": "FART",
      "decimals": 9,
      "total_supply": "1000000000",
      "logo_url": "https://...",
      "pattern": "first_stage",
      "signal_time": 1700000000,
      "price_at_signal": "0.001234",
      "current_price": "0.002345",
      "max_price_after_signal": "0.003456",
      "price_change_percent": 90.12,
      "max_price_change_percent": 180.05,
      "cluster_ratio_at_signal": 0.15,
      "current_cluster_ratio": 0.18,
      "signal_history": [
        { "signal_time": 1699999000, "price_at_signal": "0.001000" }
      ]
    }
  ]
}
```

- `pattern`: `first_stage` (rapid/early, ~70/day) or `second_stage` (stable/confirmed, ~30/day)
- `cluster_ratio_at_signal` vs `current_cluster_ratio`: Compare to see if accumulation continued post-signal
- `signal_history`: Previous signals for this token -- backtest quality

---

### GET /signal-history/:address

Historical signals for a specific token.

```
GET /signal-history/<token_address>
```

**Auth:** Bearer API key required.

**Response:** Array of `{"signal_time": int, "price_at_signal": "string"}`.

---

### GET /analyze-dca-limit-orders/:token_mint

Detect DCA (dollar-cost averaging) and limit order usage by holders (Solana only).

```
GET /analyze-dca-limit-orders/<token_mint>
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "token_mint": "...",
  "user_clusters": [
    {
      "user_address": "...",
      "user_balance": "123456.000000",
      "dca_address_balances": [
        { "address": "...", "balance": "1000.000000" }
      ],
      "limit_order_address_balances": [
        { "address": "...", "balance": "500.000000" }
      ],
      "total_cluster_balance": "125000.000000"
    }
  ],
  "address_metadata": { ... }
}
```

DCA addresses with large positions = likely stealth accumulation by operators. Limit orders show tokens temporarily transferred out but still controlled by the same entity.

---

### GET /price-chart

OHLCV price candlestick data.

```
GET /price-chart?token=<address>&after=<unix_ts>&bar=<interval>&limit=<count>
```

| Param | Required | Values |
|-------|----------|--------|
| `token` | Yes | Token address |
| `after` | Yes | Unix timestamp |
| `bar` | Yes | `1m`, `5m`, `15m`, `1H`, `4H`, `1D` |
| `limit` | Yes | 1-1000 |

**Response:** Array of `[timestamp, open, high, low, close, volume, volumeUsd, confirm]` string arrays.

---

### POST /batch-token-prices

Batch price lookup for multiple tokens.

```
POST /batch-token-prices
{ "token_mints": ["<address_1>", "<address_2>"] }
```

**Response:** `{"prices": {"<address>": 0.001234}}` -- prices as float64 in USD.

---

### POST /cluster-wallet-connections

Get the actual fund flow connections between wallets within a cluster -- reveals WHY wallets were grouped.

```
POST /cluster-wallet-connections
{
  "token_mint": "<token_address>",
  "wallets": ["<wallet_1>", "<wallet_2>"]
}
```

**Auth:** Bearer API key required.

**Response:**
```json
{
  "connections": [
    {
      "source": "wallet_1",
      "target": "wallet_2",
      "connection_type": "fund_transfer",
      "discovered_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

Use case: Verify cluster detection logic. Identify key fund chain nodes -- which wallet is the "hub" that connects others.

---

### GET /wallet-assets

Get a wallet's complete token holdings (useful for inspecting other wallets, not just the agent's own).

```
GET /wallet-assets?address=<wallet_address>&chain_id=501
```

**Auth:** Bearer API key required.

**Response:** Returns token holdings with balances and USD values for the specified wallet.

---

## Discovery APIs

### GET /agent/trending-tokens

Returns trending tokens -- the same data source powering the KryptoGO xyz discovery page. Use this to scan the market for new opportunities.

```
GET /agent/trending-tokens?chain_id=501&sort_by=5&period=2&page_size=20
Authorization: Bearer <API_KEY>
```

**Query parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chain_id` | `501` | Chain filter: `501` (Solana), `56` (BSC), `8453` (Base), `143` (Monad), or comma-separated |
| `sort_by` | `5` | Sort field: `1`=market cap, `2`=holders, `3`=liquidity, `4`=tx count, `5`=volume, `6`=price change |
| `period` | `2` | Time window: `1`=5min, `2`=1h, `3`=4h, `4`=24h |
| `page` | `1` | Page number |
| `page_size` | `20` | Results per page (max 50) |
| `marketCapMin` | -- | Min market cap (USD) |
| `marketCapMax` | -- | Max market cap (USD) |
| `holdersMin` | -- | Min holder count |
| `holdersMax` | -- | Max holder count |
| `liquidityMin` | -- | Min liquidity (USD) |
| `liquidityMax` | -- | Max liquidity (USD) |
| `volumeMin` | -- | Min volume (USD) |
| `volumeMax` | -- | Max volume (USD) |
| `tokenAgeMin` | -- | Min token age |
| `tokenAgeMax` | -- | Max token age |
| `tokenAgeType` | -- | Age unit: `1`=min, `2`=hour, `3`=day, `4`=month, `5`=year |

**Response:**
```json
{
  "tokens": [
    {
      "tokenContractAddress": "2BZm...",
      "tokenSymbol": "FARTCOIN",
      "tokenLogoUrl": "https://...",
      "chainId": "501",
      "marketCap": "12345678",
      "holders": "5432",
      "liquidity": "234567",
      "volume": "567890",
      "price": "0.001234",
      "firstPriceTime": "1700000000",
      "change": "15.5"
    }
  ]
}
```

All numeric fields are strings. `change` is the percentage price change over the selected `period`. `firstPriceTime` is a Unix timestamp (seconds) representing token creation time.

**Free tier:** Limited to 10 tokens per request.

**Typical discovery workflow:**
1. Scan for new tokens with high 1h volume: `?sort_by=5&period=2&tokenAgeMax=7&tokenAgeType=3`
2. Filter by market cap range: `?marketCapMin=100000&marketCapMax=5000000`
3. For each interesting token, call `/analyze/:token_mint` for cluster analysis
4. Check `/token-overview?address=<mint>` for fundamentals

---

## Trading APIs

### 1. GET /agent/portfolio

Returns the wallet portfolio including SOL balance, token holdings with USD values, and per-token PnL data.

The API key is tied to your KryptoGO account (for billing and tier). The agent trades with its OWN wallet
(generated during setup), which is separate from the wallet you used to log into kryptogo.xyz.
Always pass the agent's wallet address in the `wallet_address` parameter.

```
GET /agent/portfolio?wallet_address=<optional_wallet_address>
Authorization: Bearer <API_KEY>
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `wallet_address` | No | The wallet to query. Defaults to the API key owner's wallet if omitted. |

**Response:**
```json
{
  "wallet": "3NgU...",
  "sol_balance": "1.5",
  "total_realized_pnl": "0.25",
  "total_unrealized_pnl": "-0.1",
  "total_pnl": "0.15",
  "tokens": [
    {
      "mint": "2BZm...",
      "symbol": "FARTCOIN",
      "logo_url": "https://...",
      "balance": "1000000",
      "usd_value": "50.25",
      "holding_avg_cost": "0.00005",
      "current_price": "0.00005025",
      "realized_pnl": "0.1",
      "unrealized_pnl": "0.05",
      "total_pnl": "0.15",
      "avg_holding_seconds": "3600",
      "holding_period_count": 2
    }
  ]
}
```

### 2. POST /agent/swap

Build an unsigned swap transaction via DEX aggregator.

```
POST /agent/swap
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "input_mint": "So11111111111111111111111111111112",
  "output_mint": "2BZm...",
  "amount": 100000000,
  "slippage_bps": 300,
  "wallet_address": "EQ7CzwjgzkZmpQ1RWThBAdjk3VkVLVrzZWU9ZdCPwAUN"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input_mint` | string | Yes | Token to sell. `So111...112` for SOL. |
| `output_mint` | string | Yes | Token to buy. `So111...112` for SOL. |
| `amount` | integer | Yes | Amount in smallest unit (lamports for SOL). Must be > 0. |
| `slippage_bps` | integer | Yes | Slippage tolerance in basis points (1-5000). 300 = 3%. |
| `wallet_address` | string | No | Caller's wallet to use as tx fee payer / signer. If omitted, defaults to the wallet associated with the API key. **Recommended for local signing.** |

**Response:**
```json
{
  "transaction": "<base64-encoded unsigned V0 transaction>",
  "quote": {
    "input_mint": "So111...112",
    "output_mint": "2BZm...",
    "in_amount": "100000000",
    "out_amount": "1500000000",
    "price_impact_pct": "0.15",
    "platform_fee_lamports": "1000000",
    "platform_fee_rate": "0.01",
    "minimum_out_amount": "1455000000"
  },
  "fee_payer": "EQ7CzwjgzkZmpQ1RWThBAdjk3VkVLVrzZWU9ZdCPwAUN",
  "signers": ["EQ7CzwjgzkZmpQ1RWThBAdjk3VkVLVrzZWU9ZdCPwAUN"]
}
```

**Notes:**
- The transaction contains a recent blockhash which expires after ~60 seconds. Sign and submit promptly.
- Platform fee is embedded as a SOL transfer instruction. Only charged on SOL-involved swaps.
- When `wallet_address` is provided, `fee_payer` and `signers` in the response confirm which keys must sign. **Always verify `fee_payer` matches your wallet before signing.**
- Without `wallet_address`, the API uses the wallet tied to your API key, which may differ from your agent's trading wallet — causing signer mismatch errors during local signing.

### 3. POST /agent/submit

Submit a signed transaction to the Solana network.

```
POST /agent/submit
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "signed_transaction": "<base64-encoded signed transaction>"
}
```

**Response:**
```json
{
  "tx_hash": "5XyZaBcDeFg...",
  "status": "submitted",
  "explorer_url": "https://solscan.io/tx/5XyZaBcDeFg..."
}
```

**Notes:**
- Server verifies the transaction contains a SystemProgram Transfer to the platform wallet.
- `"submitted"` means sent to network -- may still fail on-chain (slippage, etc.).

---

## Error Responses

All endpoints return errors in a consistent format:

```json
{ "error": "Human-readable error message" }
```

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Invalid parameters, missing fields, invalid mint address, blacklisted token |
| 401 | Unauthorized | Missing or malformed `Authorization` header |
| 402 | Quota Exceeded | Daily API call limit reached (response includes `daily_limit` and `tier`) |
| 403 | Forbidden | Insufficient tier for endpoint (e.g., free tier accessing signals) |
| 502 | Bad Gateway | Solana RPC unavailable, DEX aggregator error |
| 504 | Timeout | Analysis took too long (>5 min for cluster analysis) |
