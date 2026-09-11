# binance-leaderboard — CLI Reference

Complete reference for all `baw leaderboard` subcommands.

**Invocation pattern**: `baw leaderboard <subcommand> [options] --json`
**Auth**: `query` requires no auth. All other subcommands (alpha-radar, preset, alpha-radar-config) require `agentSessionId` (set by `baw` CLI automatically).

---

## `leaderboard query` — Leaderboard Query

Public endpoint, no auth required.

```bash
baw leaderboard query -c 56 --period 7d --tag ALL --json
baw leaderboard query -c CT_501 --period 30d --tag KOL \
  --sort-by 20 --page 0 --size 20 --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | `56` (BSC) · `CT_501` (Solana) · `8453` (Base) · `1` (ETH) |
| `-p, --period` | enum | no | `30d` | `7d` / `30d` / `90d` |
| `-t, --tag` | enum | no | `ALL` | `ALL` / `KOL` / `MPC` |
| `--sort-by` | int | no | `0` | `0`=PnL · `20`=Win Rate · `30`=Total Volume · `50`=Trade Count · `60`=Recent Activity · `70`=Profit Rate · `80`=Token Count |
| `--order-by` | int | no | `0` | `0`/`2`=Descending · `1`=Ascending |
| `--page` | int | no | `0` | Page number (**from 0**) |
| `--size` | int | no | `20` | Page size (**max 20**) |

### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Wallet address |
| `addressLogo` | string | Address avatar URL |
| `addressLabel` | string | Address label (KOL / Smart Money etc.) |
| `addressTwitterUrl` | string | Twitter profile URL |
| `balance` | string | Current balance |
| `tags` | string[] | Address tags (smart money, kol, etc.) |
| `realizedPnl` | string | Realized PnL (USD) |
| `realizedPnlPercent` | string | Realized PnL percentage |
| `dailyPNL` | array | Daily PnL list: `[{dt: "yyyy-MM-dd", realizedPnl: ...}]` |
| `winRate` | number | Win rate (0-100) |
| `totalVolume` | string | Total trading volume (USD) |
| `buyVolume` | string | Buy volume (USD) |
| `sellVolume` | string | Sell volume (USD) |
| `avgBuyVolume` | string | Average buy volume (USD) |
| `totalTxCnt` | number | Total transaction count |
| `buyTxCnt` | number | Buy transaction count |
| `sellTxCnt` | number | Sell transaction count |
| `totalTradedTokens` | number | Number of distinct tokens traded |
| `tokenDistribution` | object | Token PnL distribution: `{gt500Cnt, between0And500Cnt, between0AndNegative50Cnt, ltNegative50Cnt}` |
| `lastActivity` | number | Last activity timestamp (ms) |
| `genericAddressTagList` | array | Generic address tags |
| `topEarningTokens` | array | Top earning tokens: `[{tokenAddress, tokenSymbol, tokenUrl, realizedPnl, profitRate}]` |

### Pagination

Response: `{ data: [...], current: pageNo, size: pageSize, pages: totalPages }`. `pageNo` starts from 0. `pageSize` max is 20.

---

## `leaderboard analyze` — Single Address Analysis

Evaluates a single wallet address using the 6-dimension scoring model + AI overlay.

```bash
baw leaderboard analyze -c 56 -a 0xabc... --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `-a, --address` | string | yes | — | Wallet address to analyze |
| `-p, --period` | enum | no | `30d` | `7d` / `30d` / `90d` |

### Flow

1. Query leaderboard top 250 entries (internally calls `query` with appropriate pagination)
2. Reverse-lookup the target address in the results
3. If found: compute 6-dimension scores + AI overlay → output rating
4. If not found: return "250 beyond top" (beyond top 250)

### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Analyzed address |
| `found` | boolean | Whether address was in top 250 |
| `scores` | object | Per-dimension scores: `{winrate, stability, drawdown, tags, pnl, follow_friendly}` |
| `totalScore` | number | Sum of 6 dimensions (0-100) |
| `archetype` | string | AI archetype: `sniper` / `swing` / `accumulator` / `farmer` / `mixed` |
| `behaviorFlags` | string[] | AI behavior flags |
| `aiAdjustment` | number | AI adjustment (±10) |
| `aiReason` | string | AI adjustment reason (required for audit) |
| `finalScore` | number | `totalScore + aiAdjustment` |
| `rating` | string | `⭐⭐⭐` / `⭐⭐` / `⭐` / `❌` |

### Rating Thresholds

| Rating | Score |
|--------|-------|
| ⭐⭐⭐ | ≥ 80 |
| ⭐⭐ | ≥ 65 |
| ⭐ | ≥ 50 |
| ❌ | < 50 |

Full scoring details: [`scoring.md`](scoring.md)

---

## `leaderboard alpha-radar` — Gem Hunter Query

Private endpoint, requires `agentSessionId`. Finds wallets that hold specific tokens.

```bash
baw leaderboard alpha-radar -c 56 \
  -t 0xtoken1,0xtoken2 \
  -m 1 --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-t, --tokens` | string | yes | Comma-separated token addresses |
| `-m, --match-count` | int | yes | Minimum match count (≥ 1) |
| `-p, --period` | string | no | `7d` / `30d` / `90d` (default: `30d`) |
| `--page` | int | no | Page number, from 0 (default: `0`) |
| `--size` | int | no | Page size, max 20 (default: `20`) |

### Return Fields

Same fields as leaderboard query, but `topEarningTokens` replaced by:

| Field | Type | Description |
|-------|------|-------------|
| `marchedTokens` | array | Matched tokens from the query list. Fields: `[{tokenAddress, tokenSymbol, tokenUrl, realizedPnl, profitRate}]` |

**Note**: The field is spelled `marchedTokens` (not "matched") in the CLI output.

---

## `leaderboard preset save` — Save Preset Filters

Private endpoint. Saves or clears preset filter conditions.

```bash
# Save presets (note: PNL fields use uppercase PNLMin/PNLMax, others are camelCase)
baw leaderboard preset save \
  --config '[{"name":"MyPreset","period":"7d","PNLMin":10000,"winRateMin":50,"volumeMin":10000}]' --json

# Clear all presets (pass empty/null)
baw leaderboard preset save --config '[]' --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `--config` | array | yes | Preset items (JSON array). `null` or empty = clear all |

### Preset Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Preset name |
| `period` | string | `7d` / `30d` / `90d` |
| `PNLMin` / `PNLMax` | number | PnL range (USD) |
| `winRateMin` / `winRateMax` | number | Win rate range (0-100) |
| `txMin` / `txMax` | number | Trade count range |
| `volumeMin` / `volumeMax` | number | Volume range (USD) |

---

## `leaderboard preset list` — List Preset Filters

Private endpoint. Returns all saved presets.

```bash
baw leaderboard preset list --json
```

### Parameters

None.

### Return Fields

Returns an array of preset objects (same fields as save).

---

## `leaderboard alpha-radar-config save` — Save Gem Hunter Config

Private endpoint. Saves or clears Gem Hunter configs.

```bash
baw leaderboard alpha-radar-config save -c 56 \
  --config '[{"uuid":"u1","name":"MyRadar","matchTokenCount":2,
    "tokenAddressList":[{"tokenAddress":"0xabc","tokenSymbol":"USDT"}]}]' --json

# Clear all configs
baw leaderboard alpha-radar-config save -c 56 --config '[]' --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `--config` | array | yes | Config items (JSON array). `null` or empty = clear all |

### Config Fields

| Field | Type | Description |
|-------|------|-------------|
| `uuid` | string | Config UUID |
| `name` | string | Config name |
| `matchTokenCount` | int | Minimum match count |
| `tokenAddressList` | array | Token list (objects, NOT strings) |

### Token Fields

| Field | Type | Description |
|-------|------|-------------|
| `tokenAddress` | string | Token contract address (required) |
| `tokenSymbol` | string | Token symbol (optional) |
| `tokenUrl` | string | Token icon URL (optional) |

---

## `leaderboard alpha-radar-config list` — List Gem Hunter Config

Private endpoint. Returns all saved configs for a chain.

```bash
baw leaderboard alpha-radar-config list -c 56 --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |

### Return Fields

Returns an array of config objects (same fields as save).
