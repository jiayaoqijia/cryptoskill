---
name: gdex-perp-copy-trading
description: HyperLiquid perpetual futures copy trading — discover top perp traders, create/manage perp copy trades, fill history, opposite-direction copying, and market data
---

# GDEX: Perp Copy Trading (HyperLiquid)

Automatically mirror perpetual futures positions (long/short) from top-performing HyperLiquid traders. Supports opposite-direction copying, fixed or proportional sizing, and TP/SL controls.

> **This is completely separate from Solana spot copy trading (`gdex-copy-trading`).** Different chain (EVM, chainId=1 vs Solana 622112261), different ABI methods (`hl_create`/`hl_update` vs `create_copy_trade`/`update_copy_trade`), different field schemas. On both chains `isDelete` deletes the configuration and `isChangeStatus` toggles `isActive` (pause/resume); neither closes positions.

## When to Use

- Browsing top HyperLiquid perp traders (by volume, PnL, or deposit)
- Getting detailed trading stats for a specific trader
- Creating a perp copy trade to follow a trader's long/short positions
- Updating or deleting a perp copy trade
- Viewing perp copy trade fill history with enrichment
- Checking market data (assets, DEXes, clearinghouse state, open orders)
- Checking deposit tokens and USDC balance

## Prerequisites

- `@gemachdao/gdex-skill` installed
- For discovery: `loginWithApiKey()` only
- For read (list/tx_list): Full sign-in with session key (`chainId: 1`)
- For write (create/update): Full sign-in + computedData

## Auth Tiers

| Tier | Endpoints | Auth Needed |
|------|-----------|-------------|
| Discovery | `top_traders`, `top_traders_by_pnl`, `user_stats`, `perp_dexes`, `all_assets`, `clearinghouse_state`, `open_orders`, `deposit_tokens`, `usdc_balance` | API key only |
| Read | `list`, `tx_list` | Session-key auth (`userId` + encrypted `data`) |
| Write | `create`, `update` | computedData (ABI-encode + sign + AES-encrypt) |

## Key Differences from Solana Copy Trading

| Feature | Solana (`gdex-copy-trading`) | HL Perp (`gdex-perp-copy-trading`) |
|---------|---------|------|
| Chain | Solana (622112261) | EVM (chainId = 1) |
| Asset Type | Spot tokens | Perpetual futures (long/short) |
| ABI Methods | `create_copy_trade` / `update_copy_trade` | `hl_create` / `hl_update` |
| ABI Fields | 12 create / 15 update (typed: uint64, bool, uint64[]) | 8 create / 11 update (typed: copyMode uint64, bool flags) |
| Opposite Copy | ❌ Not supported | ✅ `oppositeCopy` flag |
| `isChangeStatus` | Toggles `isActive` (use `pauseCopyTrade`/`resumeCopyTrade`) | Toggles `isActive` (use `pauseHlCopyTrade`/`resumeHlCopyTrade`) |
| Copy Modes | 1=fixed SOL, 2=% of trader | 1=fixed USD per order, 2=proportion of trader's size |
| TP/SL | Optional | **Mandatory** (both > 0, lossPercent < 100) |
| Max Copies | `config.maxCopyTrades` | Default 3 (`hyperLiquidConfig.maxFuturesCopy`) |

## Discovery Endpoints (No Auth)

### Top Traders by Volume/TradeCount/Deposit

```typescript
const topByVolume = await skill.getHlTopTraders('volume');
const topByTrades = await skill.getHlTopTraders('tradeCount');
const topByDeposit = await skill.getHlTopTraders('deposit');
// Cached 15 minutes
```

### Top 30 Traders by PnL

```typescript
const topPnl = await skill.getHlTopTradersByPnl();
// Response: { isSuccess: true, topTraders: { day: [...], week: [...], month: [...] } }
// Each entry: { ethAddress, accountValue, windowPerformances: [{ window, percentage, pnl }] }
```

### Detailed User Stats

```typescript
// NOTE: Requires the MANAGED wallet address, not the control wallet.
// Control wallet and external trader addresses return "Wallet not found".
const stats = await skill.getHlUserStats('0xManagedWalletAddress');
// Cached 1 hour in Redis
```

#### HlUserStats Shape

```typescript
interface HlUserStats {
  '24h': number;        // PnL last 24 hours
  '7d': number;         // PnL last 7 days
  '30d': number;        // PnL last 30 days
  week: number;
  dailyPnls: Array<{
    timeMs: number;
    date: string;
    pnl: number;
    pnlPercentage: number;
    capitalDeployed: number;
  }>;
  volumes: Record<string, number>;
  tradesCount: Record<string, { win: number; lose: number; total: number }>;
  percentagePnl: Record<string, number>;
  capitalDeployed: Record<string, number>;
  allTime: { pnl: number; pnlPercentage: number; capitalDeployed: number };
}
```

### Perp DEXes

```typescript
const dexes = await skill.getHlPerpDexes();
// { isSuccess: true, perpDexes: ['HyperLiquid', ...] }
```

### All Tradeable Assets

```typescript
const assets = await skill.getHlAllAssets();
// { isSuccess: true, count: N, assets: [...] }
```

### Clearinghouse State (Account Positions)

```typescript
// Single DEX
const state = await skill.getHlClearinghouseState('0xTraderAddress');

// All DEXes
const stateAll = await skill.getHlClearinghouseStateAll('0xTraderAddress');
```

### Open Orders

```typescript
// Single DEX
const orders = await skill.getHlOpenOrdersForCopy('0xTraderAddress');

// All DEXes
const ordersAll = await skill.getHlOpenOrdersAllForCopy('0xTraderAddress');
```

### Deposit Tokens

```typescript
const tokens = await skill.getHlDepositTokens();
// { isSuccess: true, tokens: { "42161": [{ name, symbol, address, chainId, decimals, minDeposit, HLReceiver }] } }
// Key is chain ID ("42161" = Arbitrum One)
```

### USDC Balance (Arbitrum)

```typescript
const balance = await skill.getHlUsdcBalanceForCopy('0xTraderAddress');
```

## Read Endpoints (Session-Key Auth)

Require `userId` and `data` (AES-encrypted session key from `buildGdexUserSessionData`).

### List User's HL Copy Trades

```typescript
import { buildGdexUserSessionData } from '@gemachdao/gdex-skill';

const data = buildGdexUserSessionData(sessionKey, apiKey);
const list = await skill.getHlCopyTradeList({ userId, data });
// { isSuccess: true, count: 2, allCopyTrades: [...] }
```

#### HlCopyTradeConfig Shape

```typescript
interface HlCopyTradeConfig {
  copyTradeId: string;
  copyTradeName: string;
  copyMode: number;              // 1 or 2; configs written by SDK <= 4.12 hold 416/480 (string-encoded ABI)
  chainId: number;               // Always 1 (EVM)
  isActive: boolean;
  userId: string;
  userWallet: string;            // MANAGED wallet address
  traderWallet: string;          // EVM address
  lossPercent: number;
  profitPercent: number;
  fixedAmountCostPerOrder: string;
  oppositeCopy: boolean;         // configs written by SDK <= 4.12 hold true regardless of the request
  createdAt: number;
  lastUpdated: number;
  totalTrades: number;
  totalVolumes: number;
  totalPnl: number;
}
```

### Fill History

```typescript
const txList = await skill.getHlCopyTradeTxList({
  userId,
  data,
  page: '1',
  limit: '20',  // max 100
});
// { isSuccess: true, totalCount: 42, txes: [...] }
// Cached 15 seconds
```

#### HlCopyTradeTx Shape

```typescript
interface HlCopyTradeTx {
  coin: string;              // e.g. "BTC"
  px: string;                // Fill price
  sz: string;                // Fill size
  side: string;              // "B" (buy) or "S" (sell)
  time: number;              // Unix ms
  closedPnl: string;
  oid: string;               // HyperLiquid order ID
  dir: string;               // e.g. "Open Long"
  copyTradeName: string;     // or "N/A"
  traderTxHash: string;      // or "N/A"
  traderSize: string;        // or "N/A"
  traderPrice: string;       // or "N/A"
  traderWallet: string;      // or "N/A"
}
```

## Write Endpoints (ComputedData Auth)

### Create an HL Perp Copy Trade

```typescript
await skill.createHlCopyTrade({
  apiKey,
  userId,
  sessionPrivateKey,
  traderWallet: '0xTraderEvmAddress',
  copyTradeName: 'BTC Whale Follower',
  copyMode: 1,                    // Fixed USD amount per order
  fixedAmountCostPerOrder: '50000000',  // $50 per copied trade (raw USDC, 6 decimals)
  lossPercent: '25',              // 25% stop-loss (mandatory, > 0)
  profitPercent: '100',           // 100% take-profit (mandatory, > 0)
  oppositeCopy: false,            // Copy same direction
});
```

**ABI Schema (`hl_create`, 8 fields, typed as backend decoder.ts decodes it):**

| # | Field | Type | Description |
|---|-------|------|-------------|
| 0 | traderWallet | string | EVM address to copy |
| 1 | copyTradeName | string | Human-readable label |
| 2 | copyMode | uint64 | 1 or 2 |
| 3 | fixedAmountCostPerOrder | string | Mode 1: raw USDC, 6 decimals (`'50000000'` = $50); mode 2: percentage |
| 4 | lossPercent | string | Stop-loss % |
| 5 | profitPercent | string | Take-profit % |
| 6 | nonce | string | Auto-generated |
| 7 | oppositeCopy | bool | |

### Update, Pause, Resume, Delete

Use the explicit operations. Each reads the current configuration first (the
backend rewrites every field on update), so pass only what changes.

```typescript
const ids = { apiKey, userId, sessionPrivateKey, copyTradeId: 'abc123...' };

// Settings only; never deletes or pauses. Omitted fields keep current values.
await skill.updateHlCopyTradeSettings({ ...ids, copyMode: 2, fixedAmountCostPerOrder: '0.5', oppositeCopy: false });

await skill.pauseHlCopyTrade(ids);   // isActive=false, no-op if already paused
await skill.resumeHlCopyTrade(ids);  // isActive=true, no-op if already active
await skill.deleteHlCopyTrade(ids);  // permanent
```

| Operation | Backend effect (`ServiceHyperLiquid.update`) | Open perp positions / TP-SL |
|---|---|---|
| `updateHlCopyTradeSettings` | rewrites the config fields | unchanged |
| `pauseHlCopyTrade` | toggle → `isActive=false`; the copier skips inactive configs for opens AND closes | stay open and will not follow the trader's exits; TP/SL stays |
| `resumeHlCopyTrade` | toggle → `isActive=true` | fills made while paused are not replayed |
| `deleteHlCopyTrade` | `HLFuturesCopySetting.deleteOne` | NOT closed, TP/SL NOT cancelled |

Pause/resume raise `PAUSE_STATE_UNVERIFIED` when the current state cannot be
read (nothing is sent) and `PAUSE_UNSUPPORTED` when the stored `copyMode` is not
1 or 2 (a config written by SDK <= 4.12): repair it with
`updateHlCopyTradeSettings({ copyMode, fixedAmountCostPerOrder, oppositeCopy })`
first, or delete (positions stay open). The low-level `updateHlCopyTrade` still
exists; setting both `isDelete` and `isChangeStatus` is rejected.

**ABI Schema (`hl_update`, 11 fields, typed):**

| # | Field | Type | Description |
|---|-------|------|-------------|
| 0 | traderWallet | string | EVM address |
| 1 | copyTradeName | string | Label |
| 2 | copyMode | uint64 | 1 or 2 |
| 3 | fixedAmountCostPerOrder | string | Amount or ratio |
| 4 | lossPercent | string | Stop-loss % |
| 5 | profitPercent | string | Take-profit % |
| 6 | nonce | string | Auto-generated |
| 7 | isDelete | bool | |
| 8 | isChangeStatus | bool | toggles isActive |
| 9 | copyTradeId | string | Existing trade ID |
| 10 | oppositeCopy | bool | |

## Backend Quirks (Live E2E Findings)

> These are verified behaviors observed during live E2E testing.

1. **Legacy `copyMode` values.** SDK versions up to 4.12 encoded every `hl_create`/`hl_update` field as an ABI string. The backend decodes `copyMode` as `uint64` and the flags as `bool`, so it stored the head-slot offset (416 after create, 480 after update) as `copyMode` and `true` for `oppositeCopy`, and read `isDelete=true` on every update (which is why updates "always deleted"). The SDK now sends the typed ABI. Configs created by old versions keep the bad values until you call `updateHlCopyTradeSettings` with explicit ones.

2. **`isChangeStatus` toggles `isActive`** (`isActive = !existing.isActive`); it does not delete. Only `isDelete` deletes. Neither closes positions.

3. **The copier only mirrors `isActive: true` configs** (`copyTradeHyperLiquid.ts`), for both opens and closes.

4. **`user_stats` requires the MANAGED wallet address** (`userWallet` from the copy trade config), not the control wallet address. The control wallet and external trader wallets return `{"code":103,"error":"Wallet not found"}`.

5. **Discovery endpoints use different query params:**
   - `user_stats`: `?user=<address>` (managed wallet only)
   - `clearinghouse_state`, `clearinghouse_state_all`: `?address=<address>`
   - `open_orders`, `open_orders_all`: `?address=<address>`
   - `usdc_balance`: `?address=<address>`

6. **`top_traders_by_pnl`** returns nested structure: `{ day: [...], week: [...], month: [...] }` where each entry has `ethAddress`, `accountValue`, and `windowPerformances`.

7. **`deposit_tokens`** response keys are chain IDs (e.g., `"42161"` for Arbitrum), not chain names. Each token includes `name`, `symbol`, `address`, `chainId`, `decimals`, `minDeposit`, `HLReceiver`.

## Backend Validation Rules

- **TP/SL mandatory**: Both `lossPercent` > 0 (and < 100) and `profitPercent` > 0
- **Copy modes**: Mode 1 = fixed USD per order, Mode 2 = proportion of trader's size
- **Max copies**: Default 3 per user (`hyperLiquidConfig.maxFuturesCopy`)
- **No self-copy**: Can't copy your own wallet
- **Circular dependency**: Full DFS graph cycle detection (A→B→C→A prevented)
- **No duplicates**: Can't copy the same trader wallet twice

## How Copies Execute

Copies are NOT executed at API call time. A background watcher monitors tracked traders:
1. Detects trader's new perp position (open/close/modify)
2. Calculates your position size based on copyMode
3. Opens/closes a mirrored position (or opposite if `oppositeCopy=true`)
4. Applies TP/SL based on your lossPercent/profitPercent settings
5. Tracks fill in `HLCopyTradeTrack` collection for tx_list

## Example: Full HL Perp Copy Trading Flow

```typescript
import {
  GdexSkill,
  buildGdexUserSessionData,
  generateGdexSessionKeyPair,
  buildGdexSignInMessage,
  buildGdexSignInComputedData,
} from '@gemachdao/gdex-skill';
import { ethers } from 'ethers';

const skill = new GdexSkill();
skill.loginWithApiKey(apiKey);

// 1. Sign in (chainId: 1 for HL operations)
const wallet = ethers.Wallet.fromPhrase(mnemonic);
const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();
const nonce = String(Date.now());
const msg = buildGdexSignInMessage(wallet.address, nonce, sessionKey);
const sig = await wallet.signMessage(msg);
const payload = buildGdexSignInComputedData({
  apiKey, userId: wallet.address, sessionKey, nonce, signature: sig,
});
await skill.signInWithComputedData({ computedData: payload.computedData, chainId: 1 }, { sessionPrivateKey });
const data = buildGdexUserSessionData(sessionKey, apiKey);
const userId = wallet.address.toLowerCase();

// 2. Discover top traders
const topTraders = await skill.getHlTopTradersByPnl();
const bestTrader = topTraders.topTraders[0];
console.log(`Top trader: ${bestTrader.address}, volume: $${bestTrader.volume}`);

// 3. Check trader's stats
const stats = await skill.getHlUserStats(bestTrader.address);
console.log(`30d PnL: $${stats.userStats['30d']}`);

// 4. Create a copy trade
await skill.createHlCopyTrade({
  apiKey,
  userId,
  sessionPrivateKey,
  traderWallet: bestTrader.address,
  copyTradeName: `Top PnL: ${bestTrader.address.slice(0, 8)}`,
  copyMode: 1,
  fixedAmountCostPerOrder: '25000000',  // $25 per copied trade (raw USDC, 6 decimals)
  lossPercent: '30',
  profitPercent: '100',
});

// 5. Monitor
const list = await skill.getHlCopyTradeList({ userId, data });
for (const ct of list.allCopyTrades) {
  console.log(`${ct.copyTradeName}: active=${ct.isActive}, trades=${ct.totalTrades}, PnL=$${ct.totalPnl}`);
}

// 6. Check fill history
const fills = await skill.getHlCopyTradeTxList({ userId, data, limit: '20' });
for (const tx of fills.txes) {
  console.log(`${tx.coin} ${tx.dir}: ${tx.sz} @ $${tx.px}, PnL=${tx.closedPnl}`);
}
```

## Autonomous Agent Notes (Live-Tested)

1. **`getHlUserStats()` requires the MANAGED wallet address.** Passing the control address or any external trader address returns 400 `"Wallet not found"`. Use the managed EVM address from `/v1/user?chainId=1`.
2. **All 7 other discovery endpoints (topTraders, topTradersByPnl, allAssets, perpDexes, depositTokens, clearinghouseState, openOrders) work with the control address or any external address.** Only `user_stats` has the managed-address requirement.
3. **A `copyMode` other than 1 or 2 in a response is a legacy config** written by SDK <= 4.12; repair it with `updateHlCopyTradeSettings`.
4. **To pause, call `pauseHlCopyTrade`, never delete.** Pausing leaves copied positions open and unmanaged by the copier.
5. **Sign-in for HL copy trading must use `chainId: 1`** (EVM), not `622112261` (Solana).

## Related Skills

- **gdex-authentication** — Auth setup and sign-in required for read/write
- **gdex-copy-trading** — Solana spot copy trading (separate system)
- **gdex-perp-trading** — HL perp order management, positions, leverage
- **gdex-perp-funding** — Deposit/withdraw USDC to HL account
- **gdex-portfolio** — Monitor portfolio including copied positions
