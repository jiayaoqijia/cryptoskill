# Custom Signal — `baw signal` CLI Reference

Complete reference for all `baw signal` subcommands.

**Invocation pattern**: `baw signal <subcommand> [options] --json`
**Exit codes**: `0` success · `1` usage/upstream error · `3` network failure
**JSON mode**: Always pass `--json` for structured output. The CLI wraps responses as `{ success, data, error }`.

---

## `baw signal list` — Signal Feed

Multi-source signal feed. By default fetches all three sources concurrently and merges.

```bash
baw signal list -c 56 --json
baw signal list -c 56 --source user --sort-by maxGain --time-range 24h --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | no | `56` | Chain ID (`56` BSC, `CT_501` Solana) |
| `-n, --page-size` | number | no | `100` | Items per source |
| `-s, --source` | enum | no | `all` | `all` / `user` / `meme` / `smart-money` |
| `--strategy-id` | string | no | — | Filter by strategy ID (USER_STRATEGY only). When specified with `--source all`, CLI auto-switches to `user` source. |
| `--strategy-type` | enum | no | — | `meme-rush` / `fomo-call` (USER_STRATEGY only; aliases: `meme`, `fomo`). Filtered client-side since the API ignores this parameter. |
| `--sort-by` | enum | no | `time` | `time` / `maxGain` |
| `--time-range` | enum | no | — | `5m` / `1h` / `24h` |

### JSON Output Structure

**When `--source all`** (default), output is a wrapper object with partial failure info:

```json
{
  "success": true,
  "data": {
    "list": [ /* SignalItem[] */ ],
    "allSucceeded": true,
    "failedSources": []
  }
}
```

**When `--source user|meme|smart-money`** (specific source), output is a flat array:

```json
{
  "success": true,
  "data": [ /* SignalItem[] */ ]
}
```

### SignalItem Fields

| Field | Type | SMART_MONEY | USER/MEME | Description |
|-------|------|:-----------:|:---------:|-------------|
| `signalId` | number | ✅ | ✅ | Unique signal ID |
| `ticker` | string | ✅ | ✅ | Token ticker |
| `signalSource` | string | ✅ | ✅ | `SMART_MONEY` / `USER_STRATEGY` / `MEME_OFFICIAL` |
| `strategyType` | string | — | ✅ | `meme-rush` / `fomo-call` |
| `direction` | string | ✅ | — | `buy` / `sell` |
| `alertPrice` | string | ✅ | ✅ | Trigger price |
| `alertMarketCap` | string | ✅ | ✅ | Trigger market cap |
| `currentPrice` | string | ✅ | — | Current price (SMART_MONEY only) |
| `currentMarketCap` | string | ✅ | — | Current market cap (SMART_MONEY only) |
| `highestPrice` | string | ✅ | ✅ | Highest price since trigger |
| `highestPriceTime` | number | ✅ | ✅ | Timestamp of peak (ms) |
| `maxGain` | string | ✅ | ✅ | Decimal fraction (0.25 = 25%) |
| `peakArrivalCostMs` | number | — | ✅ | Time from trigger to peak (ms) |
| `smartMoneyCount` | number | ✅ | — | Smart money count |
| `smartSignalType` | string | ✅ | — | `SMART_KOL` etc |
|| `exitRate` | number | ✅ | ✅ | Exit rate (0-100 integer; primarily meaningful for SMART_MONEY; ≥ 70 = may have passed) |
| `goldenRate` | number | — | ✅ | Golden dog rate (0-1) |
| `silverDogRate` | number | — | ✅ | Silver dog rate (0-1) |
| `bronzeDogRate` | number | — | ✅ | Bronze dog rate (0-1) |
| `winRate` | number | — | ✅ | Win rate (0-1) |
|| `status` | string | ✅ | ✅ | Signal status: `valid` (fresh), `timeout` (stale), `outDecline` (price declining), `exitRate` (exit threshold reached), or `null` |
| `jobId` | string | — | ✅ | Job ID for strategy operations |
| `strategyId` | string | — | ✅ | Strategy ID |
| `strategyName` | string | — | ✅ | Strategy name |
| `signalTriggerTime` | number | ✅ | ✅ | Trigger timestamp (ms) |
| `tokenTag` | object | ✅ | ✅ | Categorized tags (e.g. `{"Launch Platform": [{"tagName": "Pumpfun"}]}`) |
| `isAlpha` | boolean | ✅ | ✅ | Alpha token flag |
| `alphaPoint` | number | ✅ | ✅ | Alpha points |
| `launchPlatform` | string | ✅ | ✅ | Launch platform name |
| `isExclusiveLaunchpad` | boolean | ✅ | ✅ | Exclusive launchpad flag |
| `latestBacktestTime` | number | — | ✅ | Last backtest run timestamp (ms) |

### Partial Failure

When `--source all`, some sources may fail while others succeed:

```json
{
  "success": true,
  "data": {
    "allSucceeded": false,
    "failedSources": [{ "source": "smart-money", "error": "Network timeout" }],
    "list": [/* partial results */]
  }
}
```

If all sources fail: `success: false`. Treat as an error, not "no signals".

---

## `baw signal strategy create` — Create Strategy

```bash
# config is a transparent JSON passthrough — the backend defines the schema.
# Known config fields: selectedGroups (fomo-call), backtest.enabled (--run-backtest).
# meme-rush requires a real config with filter params — empty {} returns 13323012.
# Config is chain-specific: BSC uses protocol codes 2xxx + BSC anchors (BNB, CAKE, ASTER…);
# Solana uses 1xxx + SOL/USDC anchors. See field tables below for valid values per chain.

# BSC (chainId=56) — full config example
baw signal strategy create -c 56 -t meme-rush -n "MyStrategy" --config '{"protocol_code":[[2001,2002]],"pair_anchor_address":["BNB","USD1","USDT","ASTER","CAKE","U","FORM","OTHER"],"liquidity":[{"min":10,"max":null}],"volume":[{"min":1,"max":null}],"tx_count":[{"min":30,"max":null}],"top10_holders_percentage":[{"min":null,"max":30}],"kol_holding_percentage":[{"min":null,"max":20}],"dev_holding_percentage":[{"min":null,"max":20}],"sniper_holding_percentage":[{"min":null,"max":20}],"insider_holding_percentage":[{"min":null,"max":20}],"bundler_holding_percentage":[{"min":null,"max":20}],"new_wallet_holding_percentage":[{"min":null,"max":20}],"backtest":{"enabled":true,"time_range":"30d"}}' --json

# Solana (chainId=CT_501) — full config example
baw signal strategy create -c CT_501 -t meme-rush -n "MyStrategy" --config '{"protocol_code":[[1001,1004,1008,1012,1011,1010,1013]],"pair_anchor_address":["SOL","USD1","USDT","USDC","OTHER"],"liquidity":[{"min":5,"max":null}],"volume":[{"min":1,"max":null}],"tx_count":[{"min":60,"max":null}],"top10_holders_percentage":[{"min":null,"max":30}],"kol_holding_percentage":[{"min":null,"max":20}],"dev_holding_percentage":[{"min":null,"max":20}],"sniper_holding_percentage":[{"min":null,"max":20}],"insider_holding_percentage":[{"min":null,"max":20}],"bundler_holding_percentage":[{"min":null,"max":20}],"new_wallet_holding_percentage":[{"min":null,"max":20}],"backtest":{"enabled":true,"time_range":"30d"}}' --json

# fomo-call (any chain)
baw signal strategy create -c 56 -t fomo-call -n "FomoStrategy" --config '{"signalName":"My KOL FOMO","isOpen":true,"selectedGroups":{"presetGroup":"KOL"},"strategy":{"type":"moderate","minWallets":2,"timeWindowMinutes":15,"minBuyAmountPerWalletUSD":200},"tokenMarketCapRange":{"type":"mid","minUSD":100000,"maxUSD":500000}}' --run-backtest --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-t, --type` | enum | yes | `meme-rush` / `fomo-call` (aliases: `meme`, `fomo`) |
| `-n, --name` | string | yes | Strategy name (≤ 20 chars; CLI rejects >20 chars with error) |
| `--config` | JSON | yes | Strategy config JSON string |
| `--wallet-group-id` | number | no | Custom wallet group ID (fomo-call only). Sets `config.selectedGroups = {presetGroup: null, customGroupId: N}`. For preset groups, use `--config '{"selectedGroups":{"presetGroup":"KOL"}}'` instead. |
| `--run-backtest` | flag | no | Trigger backtest on creation |

### Internal Flow

1. **Estimate**: calls `count-signals` API to get estimated signals/day. This is async — the CLI polls every 2s (up to 30 attempts / 60s max). `PENDING` and `FAILED` statuses both retry. The backend returns `totalSignalCount` for the entire backtest period; the CLI divides by `backtestDays` (from `config.backtest.time_range`, default 30d) to get a daily average.
2. **Validate**: < 1/day → CLI hard-aborts (too strict). > 300/day → CLI hard-aborts (too noisy). Normal: 5–300/day.
3. **Check limit**: calls `check-backtest-limit` API
4. **Create**: calls `create-strategy` API

**fomo-call skips steps 1–3** entirely — no estimate, no backtest-limit check. Proceeds directly to create.

### Config Schema

The `--config` parameter is a **transparent JSON passthrough** — the CLI does not define or validate the schema; the backend custom-signal service owns it. Known config fields from CLI source:

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `selectedGroups` | `{presetGroup: "KOL"|"SMY"|null, customGroupId: number|null}` | fomo-call | Single object (not array). `--wallet-group-id N` sets `{presetGroup: null, customGroupId: N}`. |
| `strategy` | `{type, minWallets?, timeWindowMinutes?, minBuyAmountPerWalletUSD?}` | fomo-call | Required. `type`: `"loose"` / `"moderate"` / `"strict"` / `"custom"`. |
| `tokenMarketCapRange` | `{type: "low"|"mid"|"large"|"custom", minUSD?, maxUSD?}` | fomo-call | Optional. `type` values are lowercase. |
| `signalName` | string | fomo-call | Optional. CamelCase (not `signal_name`). |
| `isOpen` | boolean | fomo-call | Optional. Whether signal is active. |
| `backtest.enabled` | boolean | both | Auto-set to `true` by `--run-backtest` flag. |

For meme-rush, a real config with filter params is required — empty `{}` returns error 13323012. Refer to existing strategies via `baw signal explore` for reference. See config example below.

### Meme-rush Config — Chain-Specific Reference

The meme-rush config is **chain-specific**: `protocol_code` ranges and valid `pair_anchor_address` values differ between BSC and Solana. Always match the config to the chain ID being used.

#### `protocol_code` by chain

`protocol_code` is a `number[][]` — each inner array is a group of protocol codes (logical OR between groups, AND within a group). Code ranges are chain-specific:

| Chain | chainId | Code range | Protocol codes |
|-------|---------|------------|----------------|
| BSC | `56` | `2xxx` | `2001` (FourMeme), `2002` (Flap) |
| Solana | `CT_501` | `1xxx` | `1001` (PumpFun), `1004` (LaunchLab), `1008` (Bonk), `1009` (DynamicBC), `1010` (Moonshot), `1011` (JupiterStudio), `1012` (Bags), `1013` (Believe) |

> Protocol codes may be updated by the backend over time. To discover currently valid codes for a chain, run `baw signal explore -c <chainId> --json` and inspect existing strategies.

#### `pair_anchor_address` by chain

Valid anchor token symbols differ per chain:

| Chain | Valid anchor tokens |
|-------|---------------------|
| BSC (`56`) | `BNB`, `USD1`, `USDT`, `ASTER`, `CAKE`, `U`, `FORM`, `OTHER` |
| Solana (`CT_501`) | `SOL`, `USD1`, `USDT`, `USDC`, `OTHER` |

#### Full config example (BSC)

```json
{
  "protocol_code": [[2001, 2002]],
  "pair_anchor_address": ["BNB", "USD1", "USDT", "ASTER", "CAKE", "U", "FORM", "OTHER"],
  "liquidity": [{"min": 10, "max": null}],
  "volume": [{"min": 1, "max": null}],
  "tx_count": [{"min": 30, "max": null}],
  "top10_holders_percentage": [{"min": null, "max": 30}],
  "kol_holding_percentage": [{"min": null, "max": 20}],
  "dev_holding_percentage": [{"min": null, "max": 20}],
  "sniper_holding_percentage": [{"min": null, "max": 20}],
  "insider_holding_percentage": [{"min": null, "max": 20}],
  "bundler_holding_percentage": [{"min": null, "max": 20}],
  "new_wallet_holding_percentage": [{"min": null, "max": 20}],
  "backtest": {"enabled": true, "time_range": "30d"}
}
```

#### Full config example (Solana)

```json
{
  "protocol_code": [[1001, 1004, 1008, 1012, 1011, 1010, 1013]],
  "pair_anchor_address": ["SOL", "USD1", "USDT", "USDC", "OTHER"],
  "liquidity": [{"min": 5, "max": null}],
  "volume": [{"min": 1, "max": null}],
  "tx_count": [{"min": 60, "max": null}],
  "top10_holders_percentage": [{"min": null, "max": 30}],
  "kol_holding_percentage": [{"min": null, "max": 20}],
  "dev_holding_percentage": [{"min": null, "max": 20}],
  "sniper_holding_percentage": [{"min": null, "max": 20}],
  "insider_holding_percentage": [{"min": null, "max": 20}],
  "bundler_holding_percentage": [{"min": null, "max": 20}],
  "new_wallet_holding_percentage": [{"min": null, "max": 20}],
  "backtest": {"enabled": true, "time_range": "30d"}
}
```

### Fomo-call Config Example

```json
{
  "signalName": "My KOL FOMO",
  "isOpen": true,
  "selectedGroups": {"presetGroup": "KOL"},
  "strategy": {
    "type": "moderate",
    "minWallets": 2,
    "timeWindowMinutes": 15,
    "minBuyAmountPerWalletUSD": 200
  },
  "tokenMarketCapRange": {"type": "mid", "minUSD": 100000, "maxUSD": 500000}
}
```

> **Note**: `selectedGroups` is a single object, not an array. Use `presetGroup: "KOL"` or `"SMY"` for preset groups, or `customGroupId: <id>` for custom wallet groups. `--wallet-group-id N` CLI flag sets `{presetGroup: null, customGroupId: N}`.

| Field | Type | Description |
|-------|------|-------------|
| `protocol_code` | `number[][]` | Protocol codes — **chain-specific** (BSC: `2xxx`, Solana: `1xxx`). See [protocol_code by chain](#protocol_code-by-chain) above. |
| `pair_anchor_address` | `string[]` | Anchor tokens — **chain-specific** (BSC: `BNB`,`USD1`,`USDT`,`ASTER`,`CAKE`,`U`,`FORM`,`OTHER`; Solana: `SOL`,`USD1`,`USDT`,`USDC`,`OTHER`). See [pair_anchor_address by chain](#pair_anchor_address-by-chain) above. |
| `liquidity` | `[{min, max}]` | Liquidity range in USD (null = no limit) |
| `volume` | `[{min, max}]` | 24h volume range in USD |
| `tx_count` | `[{min, max}]` | 24h transaction count range |
| `top10_holders_percentage` | `[{min, max}]` | Top 10 holders percentage range |
| `kol_holding_percentage` | `[{min, max}]` | KOL holding percentage range |
| `dev_holding_percentage` | `[{min, max}]` | Dev holding percentage range |
| `sniper_holding_percentage` | `[{min, max}]` | Sniper holding percentage range |
| `insider_holding_percentage` | `[{min, max}]` | Insider holding percentage range |
| `bundler_holding_percentage` | `[{min, max}]` | Bundler holding percentage range |
| `new_wallet_holding_percentage` | `[{min, max}]` | New wallet holding percentage range |
| `backtest` | `{enabled, time_range}` | Backtest config. `--run-backtest` sets `enabled=true` |

### JSON Output

```json
{ "success": true, "data": { "jobId": "string", "strategyId": "string" } }
```

---

## `baw signal strategy update` — Update Strategy

```bash
baw signal strategy update -c 56 -t meme-rush --job-id <jobId> -n "NewName" -y --json
# Config update must use a full, chain-appropriate config (same rules as create — no empty {})
baw signal strategy update -c 56 -t meme-rush --job-id <jobId> --config '{"protocol_code":[[2001,2002]],"pair_anchor_address":["BNB","USD1","USDT","ASTER","CAKE","U","FORM","OTHER"],"liquidity":[{"min":10,"max":null}],"volume":[{"min":1,"max":null}],"tx_count":[{"min":30,"max":null}],"top10_holders_percentage":[{"min":null,"max":30}],"kol_holding_percentage":[{"min":null,"max":20}],"dev_holding_percentage":[{"min":null,"max":20}],"sniper_holding_percentage":[{"min":null,"max":20}],"insider_holding_percentage":[{"min":null,"max":20}],"bundler_holding_percentage":[{"min":null,"max":20}],"new_wallet_holding_percentage":[{"min":null,"max":20}],"backtest":{"enabled":true,"time_range":"30d"}}' -y --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-t, --type` | enum | yes | Strategy type |
| `--job-id` | string | yes | Job ID |
| `-n, --name` | string | no* | New strategy name (≤ 20 chars) |
| `--config` | JSON | no* | New strategy config JSON |
| `-y, --yes` | flag | no | Skip confirmation prompt |

*At least one of `--name` or `--config` must be provided.

### Internal Flow

**`--name` and `--config` take different API paths:**

- **`--name` only**: calls `update-job-name` API (job-level, no estimate needed)
- **`--config` (with or without `--name`)**: first calls `count-signals` (estimate, same polling as create), validates <1/>300 thresholds, then calls `update-single` API. When `--name` is also provided, it's passed alongside config in the same `update-single` call.

**Note**: `--config` update depends on `count-signals`. Empty config `{}` for meme-rush returns 13323012 — always use a real config with filter params.

### copyTradeStatus Check

If the strategy has `copyTradeStatus=ACTIVE`, the CLI warns before updating. Use `-y` to skip the interactive prompt when the user has confirmed.

---

## `baw signal strategy delete` — Delete Strategy

```bash
baw signal strategy delete -c 56 -t meme-rush --job-id <jobId> -y --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-t, --type` | enum | yes | Strategy type |
| `--job-id` | string | yes | Job ID |
| `-y, --yes` | flag | no | Skip confirmation prompt |

Delete has two confirmation checks: (1) copyTradeStatus check (if ACTIVE), (2) delete confirmation prompt ("This will delete the strategy and all associated backtests. Continue?"). Use `-y` to skip both.

API: `/backtest/delete-job`, param `jobIds: [jobId]`, returns `{ successJobIds, failedJobIds }`.

---

## `baw signal strategy follow` — Follow Strategy

```bash
# Follow an owned strategy
baw signal strategy follow -c 56 -t meme-rush --job-id <jobId> --json

# Follow a strategy-hall strategy (not owned) — auto-copies into your account first
baw signal strategy follow -c 56 -t meme-rush --job-id <hallJobId> -n "MyCopy" -y --json
```

### Behavior

Following an **owned** strategy attaches directly. Following a **strategy-hall** strategy (official / other-user, not owned) is not allowed directly — the CLI first **copies** the hall strategy's full config into a new strategy under the user's account, then follows that copy. In interactive mode it warns and asks for confirmation before copying; `-y` skips that prompt. Always confirm with the user before creating a copy. The copy counts toward the 10-enabled-strategy limit.

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-t, --type` | enum | yes | Strategy type (`meme-rush` \| `fomo-call`) |
| `--job-id` | string | yes | Job ID of the target strategy |
| `--task-id` | string | no | Task ID used to look up the strategy (hall strategies default to `1`) |
| `-n, --name` | string | no | Name for the copied strategy, ≤20 chars (only used when copying a hall strategy) |
| `-y, --yes` | flag | no | Skip the copy confirmation prompt |

### JSON Output

```json
{ "success": true, "copied": true, "jobId": "<newCopyJobId>" }
```

`copied` is `true` when the target was a hall strategy that was copied first — `jobId` is then the **new copy's** jobId. `copied` is `false` when an owned strategy was followed directly (`jobId` unchanged). Use the returned `jobId` for any follow-up operation.

---

## `baw signal strategy unfollow` — Unfollow Strategy

```bash
baw signal strategy unfollow -c 56 -t meme-rush --strategy-id <strategyId> -y --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-t, --type` | enum | yes | Strategy type |
| `--strategy-id` | string | yes | Strategy ID |
| `-y, --yes` | flag | no | Skip confirmation prompt |

### copyTradeStatus Check

If the followed strategy has `copyTradeStatus=ACTIVE`, the CLI warns before unfollowing.

### JSON Output

```json
{
  "success": true,
  "data": {
    "success": { "followed": false, "strategy_id": "string" }
  }
}
```

Note: `data.success` is an object (not boolean) — the service layer returns the raw API response. `followed: false` means successfully unfollowed.

---

## `baw signal strategy list` — List Owned Strategies

```bash
# List all owned strategies (both meme-rush and fomo-call)
baw signal strategy list -c 56 --json

# Only show enabled (followed) strategies
baw signal strategy list -c 56 --followed --json

# Filter by strategy type
baw signal strategy list -c 56 --type fomo-call --json
baw signal strategy list -c 56 --type meme-rush --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--followed` | flag | no | — | Only show enabled strategies |
| `--type` | enum | no | — | Filter by strategy type: `meme-rush` \| `fomo-call` (aliases: `meme`, `fomo`). When omitted, both types are queried and merged. |

> **Auto-pagination**: This command auto-paginates internally — no `-p`/`-s` parameters needed. It fetches all owned strategies across all pages. When `--type` is omitted, the CLI queries both `meme-rush` and `fomo-call` types concurrently and merges the results.

### JSON Output

```json
{
  "success": true,
  "data": [
    {
      "strategy_id": "string",
      "strategy_name": "string",
      "strategy_type": "meme-rush",
      "job_id": "string",
      "task_id": "string",
      "followed": true
    }
  ]
}
```

> **Note on `strategy_type`**: Due to backend pagination behavior, some entries may have `strategy_type` as null or empty string. When processing the list, deduplicate by `job_id` + `task_id` and fill missing `strategy_type` by inferring from `job_id` prefix (`fomo-call-*` → `fomo-call`, `meme-rush-*` → `meme-rush`). Never expose null/empty `strategy_type` to the user — always display a valid type per the Term Mapping rules.

---

## `baw signal strategy list-followed` — List Followed Strategies

```bash
baw signal strategy list-followed -c 56 --json
```

### JSON Output

```json
{
  "success": true,
  "data": [
    { "strategy_id": "string", "strategy_name": "string", "strategy_type": "string", "job_id": "string" }
  ]
}
```

---

## `baw signal backtest list` — List Backtests

```bash
# Single page (shows pagination info in terminal mode)
baw signal backtest list -c 56 --json
baw signal backtest list -c 56 -p 2 -s 50 --backtest-days 30 --json

# Auto-paginate — fetch all pages, return complete list
baw signal backtest list -c 56 --all --json
baw signal backtest list -c 56 --all --backtest-days 30 --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `-p, --page` | number | no | `1` | Page number (ignored when `--all` is used) |
| `-s, --size` | number | no | `20` | Page size (backend may cap to 10) |
| `--backtest-days` | number | no | — | Backtest period in days |
| `--all` | flag | no | — | Auto-paginate to fetch all pages. Overrides `--page`/`--size`. |

### JSON Output

**Without `--all`** (single page) — returns `TaskStatsPage` with pagination metadata:

```json
{
  "success": true,
  "data": {
    "taskList": [ /* TaskStats[] */ ],
    "page": 1,
    "size": 10,
    "total": 7,
    "totalPages": 1
  }
}
```

**With `--all`** — returns the complete list with total count:

```json
{
  "success": true,
  "data": {
    "total": 7,
    "taskList": [ /* TaskStats[] — all pages merged */ ]
  }
}
```

> **Pagination note**: The backend caps `size` to 10 regardless of the requested page size. When you need the full list (e.g. counting strategies, checking `copyTradeStatus` across all jobs), always use `--all` — without it, only the first page is returned.

| Field | Type | Description |
|-------|------|-------------|
| `jobId` | string | Job ID (use for follow/update/delete/retry) |
| `strategyId` | string | Strategy ID (use for detail/unfollow) |
| `taskName` | string | Strategy name |
| `strategyType` | string | `meme-rush` or `fomo-call` |
| `status` | string | `PENDING` / `RUNNING` / `COMPLETED` / `FAILED` / `CANCELLED` |
| `winRate` | number | Win rate (0-1) |
| `signalCount` | number | Total signals generated |
| `tokenCount` | number | Distinct tokens in signals |
| `goldenRate` | number | Golden dog rate (0-1) |
| `silverDogRate` | number | Silver dog rate (0-1) |
| `bronzeDogRate` | number | Bronze dog rate (0-1) |
| `snipePct` | number | Snipe time-to-peak pct (< 1min, 0-1) |
| `quickFlipPct` | number | Quick Flip pct (1–5min, 0-1) |
| `swingPct` | number | Swing pct (5–60min, 0-1) |
| `holdPct` | number | Hold pct (1–24h, 0-1) |
| `moonPct` | number | Moon pct (> 24h, 0-1) |
| `peakArrivalCostP50Ms` | number | Median time-to-peak (ms) |
| `signalTokenFrequency` | number | Signal frequency (signals/day) |
| `scheduleInterval` | string \| null | Schedule interval or null/OFF |
| `lastRunTime` | number \| null | Last backtest run timestamp (ms) |
| `nextRunTime` | number \| null | Next scheduled run timestamp (ms) |
| `followed` | boolean | Whether current user follows this strategy |
| `isOwner` | boolean | Whether current user owns this strategy |
| `copyTradeStatus` | string \| null | Copy trading status (`ACTIVE` = has active copy trading) |
| `copyTradeStrategyId` | string \| null | Copy trade strategy ID |
| `dailySignalLimit` | number | Daily signal trigger limit |
| `todaySignalCount` | number | Today's signal count |
| `limitReached` | boolean | Whether daily limit reached |
| `needRetest` | boolean | Whether retest is recommended |
| `needRetestReason` | string \| null | Reason for retest recommendation |
| `walletGroupName` | string \| null | Wallet group name (fomo-call) |
| `walletAddressCount` | number \| null | Wallet address count (fomo-call) |
| `triggerMinWallets` | number \| null | Min wallets trigger (fomo-call) |
| `triggerMinBuyAmountUSD` | number \| null | Min buy amount per wallet (fomo-call) |
| `triggerTimeWindowMinutes` | number \| null | Time window in minutes (fomo-call) |
| `tokenDetails` | array | Token list with per-token metrics (same as `tokens` in detail) |
| `tokens` | array | Alias for `tokenDetails` (same data, both fields present) |
| `createdAt` | string | Creation datetime (e.g. `"2026-06-30 12:33:44"`) |
| `createdAtTimestamp` | number | Creation timestamp (ms) |
| `updatedAt` | string | Last update datetime |
| `updatedAtTimestamp` | number | Last update timestamp (ms) |
| `lastSignalTokenTime` | number \| null | Last signal token timestamp (ms) |

**Null safety**: Some fields may be `null` (e.g. `winRate`, `scheduleInterval`) for newly created or pending strategies. Always null-check before arithmetic.

---

## `baw signal backtest detail` — Backtest Detail

```bash
baw signal backtest detail -c 56 --strategy-id <strategyId> --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `--strategy-id` | string | yes | Strategy ID |

### JSON Output

```json
{
  "success": true,
  "data": {
    "info": { /* same fields as backtest list item */ },
    "tokens": [
      {
        "chainId": "string",
        "contractAddress": "string",
        "tokenName": "string",
        "symbol": "string",
        "imageUrl": "string",
        "tokenIcon": "string",
        "alertPrice": "number (float)",
        "alertTime": "string (formatted datetime, e.g. \"2026/06/04 12:02:42\")",
        "alertTimestamp": "number (ms)",
        "alertMc": "number (float)",
        "athPrice": "number (float)",
        "athTime": "string (formatted datetime)",
        "athTimestamp": "number (ms)",
        "athMc": "number (float)",
        "incrPercent": "number (decimal fraction, e.g. 26.12 = 2612%)",
        "peakArrivalCostMs": "number (ms)"
      }
    ]
  }
}
```

API: `/backtest/get-task-vo`, param `{ chainId, strategyId }`.

---

## `baw signal backtest retry` — Retry Failed Job

```bash
# --type is optional (defaults to meme-rush); meme-rush only — fomo-call returns 13323027
baw signal backtest retry -c 56 --job-id <jobId> --json
baw signal backtest retry -c 56 -t meme-rush --job-id <jobId> --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `-t, --type` | enum | no | `meme-rush` | Strategy type (meme-rush only; fomo-call returns 13323027) |
| `--job-id` | string | yes | — | Job ID |

API: `/backtest/retry-job`, param `{ chainId, type?, jobIds: [jobId] }` — `type` is optional on backend, CLI defaults to `meme-rush`.

### JSON Output

```json
{ "success": true, "data": { "success": true } }
```

---

## `baw signal backtest schedule` — Configure Schedule

```bash
# Query current schedule
baw signal backtest schedule -c 56 --job-id <jobId> --json

# Set schedule
baw signal backtest schedule -c 56 --job-id <jobId> --interval 12H --json

# Turn off schedule
baw signal backtest schedule -c 56 --job-id <jobId> --interval OFF --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--job-id` | string | yes | — | Job ID |
| `--interval` | enum | no | — | `4H` / `6H` / `12H` / `24H` / `OFF` (omit to query only) |

### JSON Output

```json
{
  "success": true,
  "data": { "schedule_interval": "12H", "next_run_time": "number (ms)" }
}
```

---

## `baw signal explore` — Explore Official Strategies

```bash
baw signal explore -c 56 --json
baw signal explore -c 56 --backtest-days 30 --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--backtest-days` | number | no | — | Backtest period in days |

Returns a flat `TaskStats[]` array (not `TaskStatsPage`). Explore returns a **subset** of TaskStats — it has NO user-specific fields (`followed`, `isOwner`, `scheduleInterval`, `dailySignalLimit`, `todaySignalCount`, `limitReached`, `copyTradeStatus`, `copyTradeStrategyId`) but adds official strategy fields:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Strategy type (may differ from `strategyType` — explore uses `type` field) |
| `signalNameCn` | string | Official strategy name (Chinese) |
| `signalNameEn` | string | Official strategy name (English) |
| `signalDescCn` | string | Official strategy description (Chinese) |
| `signalDescEn` | string | Official strategy description (English) |
| `createdAt` / `updatedAt` | string | Creation/update datetime |
| `lastSignalTokenTime` | number \| null | Last signal token timestamp (ms) |

---

## `baw signal credits` — Query Credits

```bash
baw signal credits --json
```

### JSON Output

```json
{
  "success": true,
  "data": {
    "balance": "number",
    "dailyLimit": "number",
    "totalVolume": "number",
    "isWhiteList": "boolean"
  }
}
```

Check `balance` before triggering backtests. If `balance` is 0, inform the user that daily credits are exhausted (resets next day).

---

## `baw signal wallet-group` — List Wallet Groups

```bash
baw signal wallet-group -c 56 --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |

### JSON Output

```json
{
  "success": true,
  "data": [
    { "groupId": "number", "groupName": "string", "addressCount": "number", "displayOrder": "number" }
  ]
}
```

Used to resolve wallet group IDs for `baw signal strategy create --wallet-group-id <id>` (fomo-call).

---

## Strategy Type Reference

| Type | Alias | Description | Wallet Group Required |
|------|-------|-------------|----------------------|
| `meme-rush` | `meme` | Early golden dog detection | No |
| `fomo-call` | `fomo` | Follow smart money calls | No (config has `selectedGroups`) |

**fomo-call limitations**: fomo-call does NOT support `backtest retry` (13323027) or `backtest schedule set` (13323006). `schedule/query` (read-only) is supported. Supported operations: `create`, `update` (name/config), `delete` (fixed — now works as of 2025-07-01), `follow`, `unfollow`.

---

## Error Codes

| CLI Error Code | API Code | Description |
|----------------|----------|-------------|
| 60002001 | 13323005 | Strategy not found |
| 60002002 | 13323006 | Not strategy owner |
| 60002003 | 13323010 | Daily signal limit reached |
| 60002004 | 13323011 | Backtest credits exhausted |
| 60002005 | 13323026 | Strategy count limit reached (stop following to enable new) |
| 60002006 | 13323028 | Service temporarily unavailable |
| 60002007 | 13323031 | AI analysis unavailable |
| — | 13323038 | Strategy not found — returned as raw code with no human-readable message for some commands (e.g. `backtest detail`) |
| — | 13323036 | count-signals incomplete — cannot run update-single (estimate must finish first) |
| — | 13323012 | Empty config `{}` for meme-rush — use a real config with filter params |
| — | 13323027 | Operation not supported for fomo-call type (retry) |
| — | 13323006 | Not strategy owner — also returned when setting schedule on fomo-call |

**Note on error precedence**: `delete` and `retry` with a nonexistent jobId typically return `NOT_OWNER` (60002002), not `NOT_FOUND` (60002001) — the backend checks ownership before existence.

### Gold/Silver/Bronze Definitions

| Level | Condition | Meaning |
|-------|-----------|---------|
| 🥇 Gold | maxGain > 5x | High-quality signal |
| 🥈 Silver | maxGain 3–5x | Medium quality |
| 🥉 Bronze | maxGain 1–3x | Valid signal |
| Zero | maxGain < 1x | Invalid signal |

Gold% + Silver% + Bronze% + Zero% = 100%. The API does not return `zeroRate` — compute it as `1 - goldenRate - silverDogRate - bronzeDogRate`.
