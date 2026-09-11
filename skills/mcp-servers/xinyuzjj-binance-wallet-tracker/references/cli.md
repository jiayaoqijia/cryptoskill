# binance-wallet-tracker — CLI Reference

Complete reference for all `baw tracker` subcommands (excluding leaderboard — see `binance-leaderboard` skill).

**Invocation pattern**: `baw tracker <subcommand> [options] --json`
**Auth**: Commands with `--group-id` require `agentSessionId`. Commands with `--tag-type` (SMY/KOL data) require no auth. `--tag-type` and `--group-id` are mutually exclusive.

---

## `tracker token query` — Token Monitor

```bash
# Private — own group data (must specify --group-id or --tag-type)
baw tracker token query -c 56 --group-id 1 --json
baw tracker token query -c 56 --group-id 1 --period 4h --json

# Public — SMY/KOL data
baw tracker token query -c 56 --tag-type kol --json        # KOL
baw tracker token query -c CT_501 --tag-type smy --json    # Smart Money
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--group-id` | number | no | — | Target group; omit to query all own groups (private mode) |
| `--tag-type` | string | no | — | `kol` / `smy` (public mode; omit for private own-group mode) |
| `--token-size` | int | no | `70` | Max tokens to return |
| `--period` | enum | no | `24h` | `1m` / `5m` / `1h` / `4h` / `24h` |
| `--filter-risk` | flag | no | — | Filter risk tokens |

**Private mode**: use `--group-id` (or omit both to query all own groups). **Public mode**: use `--tag-type kol` or `--tag-type smy` (no `--group-id`).

### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `tokenName` | string | Token name |
| `ca` | string | Contract address |
| `tokenIconUrl` | string | Token icon URL |
| `protocol` | number | Protocol type (may be absent in private mode) |
| `launchTime` | number | Token launch timestamp (ms) — use for pioneer sorting |
| `price` | string | Current price |
| `marketCap` | string | Market cap |
| `volume` | string | Trading volume |
| `priceChangeRate` | string | Price change rate (%) |
| `tokenDecimals` | number | Token decimals |
| `tokenRiskLevel` | int | Risk level 0-5 (≥3 = high risk) |
| `rwaType` | number | RWA type |
| `addressList` | array | Per-address flow data (see below) |
| `tokenTag` | object | Token tag map |
| `consensusCount` | number | **CLI-aggregated**: `addressList.length` (consensus count) |
| `netInflow` | number | **CLI-aggregated**: Σ `addressList[].inflow` (net inflow) |
| `countBuy` | number | **CLI-aggregated**: Σ `addressList[].buyCount` (accumulation count) |
| `countSell` | number | **CLI-aggregated**: Σ `addressList[].sellCount` (distribution count) |

**CLI aggregation**: The API does not return top-level `traderNum`, `inFlow`, `countBuy`, or `countSell`. The CLI aggregates these from `addressList[]` and exposes them as `consensusCount`, `netInflow`, `countBuy`, `countSell` on each token object. Use these aggregated fields directly for Accumulation vs Distribution analysis.

### Per-Address Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Wallet address |
| `label` | string\|null | Address label |
| `buyCount` | number | Buy transaction count (use for Accumulation analysis) |
| `sellCount` | number | Sell transaction count (use for Distribution analysis) |
| `inflow` | number | Net inflow (positive = net buy) |
| `tokenQty` | number\|null | Holding quantity |
| `latestTxTime` | number | Latest transaction timestamp (ms) |
| `lastTrade` | number | Last trade timestamp (ms) |
| `addressLogoUrl` | string\|null | Address logo URL |

**`buyCount`/`sellCount` are returned directly** — no need to aggregate `tradeSideCategory`.

### Sorting (client-side)

The API does not provide server-side sort for consensus/inflow/volume/pioneer. Sort client-side using CLI-aggregated fields:
- **Consensus** (consensus): sort by `consensusCount` descending
- **Inflow** (Net Inflow): sort by `netInflow` descending
- **Volume** (volume): sort by `volume` (string field, parse to number) descending
- **Pioneer** (pioneer): sort by `launchTime` ascending, filter `consensusCount ≤ 2`

---

## `tracker tx query` — Trade Monitor

```bash
# Private — own group trade flow
baw tracker tx query -c 56 --group-id 1 --json

# Public — SMY/KOL trade flow
baw tracker tx query -c 56 --tag-type smy --json

# Filter by trade side
baw tracker tx query -c 56 --group-id 1 --trade-side 19 --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--group-id` | number | no | — | Target group (private mode) |
| `--tag-type` | string | no | — | `kol` / `smy` (public mode; omit for private) |
| `--trade-side` | string | no | — | Comma-separated: `19`=buy, `11`=first-buy, `29`=sell, `21`=clear |
| `--min-value` | number | no | — | Min tx USD value |
| `--max-value` | number | no | — | Max tx USD value |
| `--filter-risk` | flag | no | — | Filter risk tokens |

**Private mode**: use `--group-id`. **Public mode**: use `--tag-type kol` or `--tag-type smy` (no `--group-id`).

### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `chainId` | string | Chain ID |
| `txHash` | string | Transaction hash |
| `logId` | string | Log ID (can locate a single tx) |
| `address` | string | Sender address |
| `label` | string\|null | Address label |
| `addressLogoUrl` | string\|null | Address logo URL |
| `toAddress` | string | Receiver address |
| `toLabel` | string\|null | Receiver label |
| `toAddressLogoUrl` | string\|null | Receiver address logo URL |
| `ts` | number | Timestamp (**seconds**, not ms — 10-digit Unix timestamp) |
| `tradeSideCategory` | int | `11`=first-buy, `19`=buy, `21`=clear, `29`=sell. **May include undocumented values** — filter defensively, don't assume only these four. |
| `txUsdValue` | string | Transaction USD value |
| `txNativeTokenQty` | string | Native token quantity traded |
| `nativePrice` | string | Native token price |
| `tokenPrice` | string | Price at trade time |
| `currentPrice` | string | Current price |
| `ca` | string | Token contract address |
| `tokenName` | string | Token name |
| `tokenIconUrl` | string | Token icon URL |
| `tokenDecimals` | number | Token decimals |
| `tokenSupply` | string | Token total supply |
| `marketCap` | string | Market cap |
| `launchTime` | number | Token launch time (ms) |
| `tokenRiskLevel` | int | Risk level 0-5 |
| `rwaType` | number | RWA type |
| `tokenTag` | object | Token tag map |

**Field availability**: Live-verified — all 26 fields above are returned by both private (own group) and public (SMY/KOL) modes via `baw tracker tx query`.

**No pagination** — returns all matching records in one response.

**ca/address filtering (Skill responsibility)**: The A3 API does NOT accept `ca` or `address` as filter parameters. The Skill must filter: fetch all records via `tx query`, then filter by matching `ca` (contract address) or `address` (wallet) in the results. This is the approach for the core scenario "who in a group is buying a specific token" — fetch the group's full trade flow, then filter by `ca`.

---

## `tracker follow` — Query Follow List

```bash
baw tracker follow -c 56 --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |

### Return Fields

Returns a map where key = followed address, value = `{label}`.

**Limitation**: Only queries the **current user's** follow list. No `address` param — cannot query other users' follow lists. Default sorted by follow time.

---

## `tracker ws` — WebSocket Real-Time Push

Subscribe to WSP WebSocket push events for real-time trade monitoring.

```bash
# Smart Money buy/sell signals (all chains)
baw tracker ws --smy --duration 15 --json

# KOL activity on BSC, 60s
baw tracker ws --kol -c 56 --duration 60 --json

# Chain-level wallet activity (multi-chain)
baw tracker ws --wallet BSC,SOL --duration 15 --json

# Specific address monitoring
baw tracker ws --address 0xabc... -c 56 --duration 15 --json

# Batch address monitoring from file
baw tracker ws --address-list addresses.txt -c 56 --duration 15 --json

# Monitor my followings' activity
baw tracker ws --following -c 56 --duration 15 --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `--smy` | flag | no | Listen to Smart Money events (all chains, no `-c` needed) |
| `--kol` | flag | no | Listen to KOL events (requires `-c`) |
| `--wallet` | string | no | Listen to chain-level events. Comma-separated chain names: `BSC,SOL,BASE,ETH` |
| `--following` | flag | no | Listen to current user's followings' trades (requires login + `-c`, mutually exclusive with other filters) |
| `--address` | string | no | Listen to specific address events (requires `-c`) |
| `--address-list` | string | no | Path to file with addresses (one per line, requires `-c`, max 100) |
| `-c, --chain-id` | string | conditional | Chain ID (required for `--kol`, `--address`, `--address-list`, `--following`) |
| `--duration` | number | yes* | Auto-disconnect after N seconds. Default 15. Omit only when the user explicitly requests an unlimited stream. Extract from user instruction when available (e.g. "monitor for 60 seconds" → `--duration 60`). |

### Filter Combinations

At least one of `--smy`, `--kol`, `--wallet`, `--following`, `--address`, `--address-list` is required. `--following` is mutually exclusive with all other filters. Multiple non-following filters can be combined (e.g. `--smy --kol -c 56` subscribes to both streams concurrently).

### JSON Output

In `--json` mode, only push message JSON is written to stdout — no meta info (streams, subKeys, connection status). This enables pipeline processing with `| jq`. In terminal mode, connection info and human-readable event summaries are printed.

Push message fields vary by stream type but typically include: `address`, `ticker`/`tokenName`, `tradeSide`, `txUsdValue`, `tokenPrice`, `timestamp`, `chainId`, `contractAddress`.

### Fallback Filtering (`--following` with large lists)

When `--following` is used with a large follow list, the CLI may fall back to a broader chain-level wallet stream. Push events will then include trades from all wallets on the chain, not just the user's followings. If the user only wants their followed addresses' events, filter push messages by `address` against the follow list (`tracker follow -c <chainId> --json`). This filtering is optional — only apply it when the user specifically wants followed-address-only events.

---

## `tracker group list` — List Groups

```bash
baw tracker group list -c 56 --json
baw tracker group list -c 56 --no-all-group --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `--no-all-group` | flag | no | Exclude the "All" virtual group (default: includes All) |

### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `groupId` | number | Group ID |
| `groupName` | string | Group name |
| `addressCount` | number | Address count in group |
| `displayOrder` | number | Display order (All=-1, Default=0, others sequential) |

**Field name**: `displayOrder`. Sort groups by `displayOrder`: All=-1, Default=0, others sequential.

---

## `tracker group create` — Create Group

```bash
baw tracker group create -c 56 -n "Base-Sniper" --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-n, --name` | string | yes | Group name |

### Return

`Long` — new group ID.

---

## `tracker group update` — Rename Group

```bash
baw tracker group update -c 56 -g 1 -n "NewName" --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-g, --group-id` | number | yes | Group ID |
| `-n, --name` | string | yes | New group name |

### Return

`Void`.

---

## `tracker address search` — Fuzzy Search

```bash
baw tracker address search -c 56 -g 1 -a 0xabc --json
baw tracker address search -c 56 -g 1 --label "whale" --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-g, --group-id` | number | yes | Group ID |
| `-a, --address` | string | no | Address keyword |
| `--label` | string | no | Label keyword |

### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `chainId` | string | Chain ID |
| `address` | string | Wallet address |
| `label` | string | Address label |
| `emoji` | string | Emoji tag |
| `color` | string | Color tag |
| `groupId` | number | Group ID |
| `groupName` | string | Group name |
| `isFollowed` | boolean | Whether the address is followed by current user |
| `addressLogoUrl` | string | Address logo URL |
| `genericAddressTagList` | array | Generic tags |
| `lastActiveTime` | number | Last active timestamp (ms) |
| `nativeTokenQty` | string | Native token quantity |

---

## `tracker address list` — Paginated List

```bash
baw tracker address list -c 56 -g 1 --page 1 --size 20 --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--group-id` | number | yes | — | Group ID |
| `--address` | string | no | — | Address filter |
| `--label` | string | no | — | Label filter |
| `--page` | int | yes | `1` | Page number (from 1, min 1) |
| `--size` | int | no | `20` | Page size (max 100) |

### Return

Returns `{ total: number, rows: [...] }` where rows contain the same fields as search above.

---

## `tracker address add` — Add Single Address

Wraps `import` with `enforce=false` and single-item list.

```bash
baw tracker address add -c 56 -g 1 -a 0xabc --label "Whale1" --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-g, --group-id` | number | no | Target group |
| `-a, --address` | string | yes | Wallet address |
| `--label` | string | no | Address label |

### Return

`Integer` — count of imported addresses (1 or 0).

---

## `tracker address batch` — Batch Import

```bash
baw tracker address batch -c 56 -g 1 -a 0xabc,0xdef --json
# Or with labels: -a '[{"address":"0xabc","label":"Whale1"},{"address":"0xdef"}]'
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID (single chain per call) |
| `-g, --group-id` | number | no | — | Target group |
| `-a, --addresses` | string | yes | — | Comma-separated addresses, or JSON array of `[{address, label?}]` |
| `--no-overwrite` | flag | no | — | Do not overwrite existing labels |

### Return

`Integer` — count of imported addresses.

**No new/exist/overwrite breakdown**: The API only returns a single Integer (imported count). The CLI cannot provide new/exist/overwrite breakdown. To track duplicates, compare the address list before/after import via `address list`.

**⚠️ `allowOverwrite` defaults to `true`** — existing labels are overwritten silently. Use `--no-overwrite` to get 409 conflicts instead.

**Cross-chain auto-dispatch**: CLI requires a single `-c` per call. When the user provides mixed EVM + Solana addresses, the Skill must classify by address format (EVM: `^0x[a-fA-F0-9]{40}$` → BSC/Base; Solana: Base58 → `CT_501`), group by chain, and call `batch` once per chain. Aggregate results across all chains.

---

## `tracker address update` — Update Label

```bash
baw tracker address update -c 56 -a 0xabc --label "NewLabel" --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-a, --address` | string | yes | Wallet address |
| `--label` | string | no | New label |

**⚠️ `groupId` is deprecated** for `update`. Use `tracker address link` to change group.

### Return

`Void`.

---

## `tracker address link` — Link to Group

```bash
baw tracker address link -c 56 -a 0xabc -g 2 --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-a, --address` | string | yes | Wallet address |
| `-g, --group-id` | number | no | Target group (null = default group) |

### Return

`Void`.

---

## `tracker address delete` — Delete Addresses

```bash
baw tracker address delete -c 56 -g 1 -a 0xabc,0xdef -y --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-g, --group-id` | number | yes | Group ID |
| `-a, --addresses` | string | yes | Comma-separated addresses to delete |
| `-y, --yes` | flag | no | Skip confirmation prompt |

### Return

`Void`.

---

## `tracker address follow` — Follow Address

```bash
baw tracker address follow -c 56 -g 1 -a 0xabc --label "Follow1" --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-g, --group-id` | number | no | Group ID |
| `-a, --address` | string | yes | Wallet address |
| `--label` | string | no | Label for the followed address |

### Return

Returns `{address, followed: true}`. `followed` is a boolean status flag.

---

## `tracker address unfollow` — Unfollow Address

```bash
baw tracker address unfollow -c 56 -a 0xabc --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `-a, --address` | string | yes | Wallet address |

### Return

Returns `{address, followed: false}`.
