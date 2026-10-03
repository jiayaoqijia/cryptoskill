---
name: gdex-onboarding
description: Start here — GDEX overview, architecture, supported chains, available skills, and quickstart for cross-chain DeFi trading via managed-custody wallets
---

# GDEX: Agent Onboarding

GDEX is a cross-chain DeFi trading infrastructure for AI agents. It provides spot trading, perpetual futures (HyperLiquid), portfolio management, token discovery, copy trading, and bridging across Solana, Sui, and 12+ EVM chains — all through a single SDK with managed-custody wallets.

## When to Use

- You're new to GDEX and need to understand the platform
- You need to decide which skill to load for a specific task
- You want a quick overview of supported chains and capabilities

## Architecture

```
Agent → @gemachdao/gdex-skill SDK → GDEX Backend (trade-api.gemach.io/v1) → On-chain Execution
```

**Key concepts:**
- **Managed custody** — GDEX provisions and manages all on-chain trading wallets server-side. Your control wallet only signs in once.
- **Encrypted payloads** — All trades use AES-256-CBC encrypted `computedData` payloads. The API key derives the AES key deterministically via SHA256 hash chain.
- **Session keypairs** — A secp256k1 session key signs trade payloads after initial control-wallet sign-in.
- **Shared API keys** — Pre-configured keys let agents authenticate instantly without wallet signing.

## Quick Start

```bash
npm install @gemachdao/gdex-skill
```

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// No-auth: check trending tokens
const trending = await skill.getTrendingTokens({ chain: 'solana', period: '24h', limit: 5 });

// Auth required: buy a token
const trade = await skill.buyToken({
  chain: 'solana',
  tokenAddress: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
  amount: '0.1',
  slippage: 1,
});
```

**Shared API Keys (pre-configured for all agents):**
- Primary: `9b4e1c73-6a2f-4d88-b5c9-3e7a2f1d6c54`
- Secondary: `2c8f0a91-5d34-4e7b-9a62-f1c3d8e4b705`

## Supported Chains

| Chain | ChainId | DEXes | Perps | Bridge |
|-------|---------|-------|-------|--------|
| Ethereum | `1` | Uniswap v2/v3, Odos | — | Yes |
| Optimism | `10` | Uniswap v3, Odos | — | Yes |
| BSC | `56` | PancakeSwap, Odos | — | Yes |
| Sonic | `146` | — | — | Yes |
| Fraxtal | `252` | Uniswap v3 | — | Yes |
| Robinhood Chain | `4663` | Uniswap v2, KyberSwap | — | No |
| Nibiru | `6900` | — | — | Yes |
| Base | `8453` | Uniswap v3, Odos, Arcadia | — | Yes |
| Arbitrum | `42161` | Uniswap v3, Odos | — | Yes |
| Berachain | `80094` | — | — | Yes |
| Solana | `622112261` / `'solana'` | Raydium, Raydium v2, Orca | — | Yes |
| Sui | `1313131213` / `'sui'` | Cetus, Bluefin | — | Yes |
| HyperLiquid | — | — | Native perp engine | — |

**Chain IDs for managed-custody:** 900 = Solana, 101 = Sui, or standard EVM chain IDs.

## Available Skills

| Category | Skill | Description |
|----------|-------|-------------|
| **Getting Started** | `gdex-onboarding` | **You are here** — Overview, architecture, quickstart |
| **Auth** | `gdex-authentication` | Managed-custody auth, encryption, session key flow |
| **Trading** | `gdex-spot-trading` | Buy/sell tokens on any supported chain |
| | `gdex-perp-trading` | HyperLiquid perpetual futures — positions, orders, leverage |
| | `gdex-perp-funding` | Deposit/withdraw USDC to/from HyperLiquid |
| | `gdex-limit-orders` | Create, cancel, and list limit orders |
| **Data** | `gdex-portfolio` | Cross-chain portfolio, balances, trade history |
| | `gdex-token-discovery` | Token details, trending tokens, OHLCV charts (no auth) |
| **Platform** | `gdex-copy-trading` | Copy trade wallets, create/manage configs, tx history, DEXes (Solana writes only) |
| | `gdex-perp-copy-trading` | HL perp copy trading — top traders, create/manage configs, market data |
| | `gdex-bridge` | Cross-chain bridging with quotes |
| | `gdex-wallet-setup` | Generate EVM wallets, session keys, get wallet info |
| **Frontend** | `gdex-ui-install-setup` | React/Next.js project setup, SDK context providers |
| | `gdex-ui-trading-components` | React component patterns for trading UIs |
| | `gdex-ui-portfolio-dashboard` | Portfolio dashboard components |
| | `gdex-ui-wallet-connection` | Wallet connection UI and auth flows |
| | `gdex-ui-theming` | CSS theming — dark/light mode, trading colors |
| | `gdex-ui-page-layouts` | Full page compositions for trading apps |
| **Developer Tools** | `gdex-sdk-debugging` | Troubleshoot errors, chain quirks, common pitfalls |

## Recommended Next Steps

**If you want to trade tokens (spot):**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-spot-trading** for buy/sell operations

**If you want perpetual futures:**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-perp-funding** to deposit USDC to HyperLiquid
3. Load **gdex-perp-trading** for positions and orders

**If you just need market data (no auth):**
1. Load **gdex-token-discovery** — works immediately, no authentication needed

**If the user has no wallet:**
1. Load **gdex-wallet-setup** to generate an EVM control wallet
2. Load **gdex-authentication** to sign in via managed custody

**If you want to copy successful traders:**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-copy-trading** for tracking wallets and settings

**If you want to bridge assets cross-chain:**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-bridge** for bridging operations

**If you want to build a trading frontend:**
1. Load **gdex-ui-install-setup** for React/Next.js project setup
2. Load **gdex-ui-trading-components** for order forms and position tables
3. Load **gdex-ui-theming** for dark/light mode and trading colors
4. Load **gdex-ui-page-layouts** for full page compositions

**If you're debugging an issue:**
1. Load **gdex-sdk-debugging** for error codes, chain quirks, and common pitfalls

## Key Links

| Resource | URL |
|----------|-----|
| SDK (npm) | https://www.npmjs.com/package/@gemachdao/gdex-skill |
| Repository | https://github.com/GemachDAO/gdex-skill |
| Trading Dashboard | https://gdex.pro |
| Backend API | https://trade-api.gemach.io/v1 |

## Installation

```bash
# Install all skills globally (recommended)
npx skills add GemachDAO/gdex-skill --all --agent '*' -g

# Install specific skill
npx skills add GemachDAO/gdex-skill --skill gdex-spot-trading

# Install SDK
npm install @gemachdao/gdex-skill
```

## MCP Server

For AI clients that support [Model Context Protocol](https://modelcontextprotocol.io),
the GDEX MCP server exposes **117 tools** covering the full SDK surface — spot and
perp trading, HyperLiquid funding, limit orders, copy trading, bridging, portfolio
and token data, transfers/social, and HIP-3/HIP-4 outcome (event) markets (e.g.
`buy_token`, `open_perp_position`, `place_perp_order`, `hl_create_outcome_order`,
`hl_swap_collateral`, `get_account_state`, `estimate_bridge`).

### Auto-configure (one command, no npm account)

```bash
npx -y github:GemachDAO/gdex-skill gdex-mcp-server init --client claude
# clients: claude · cursor · vscode · codex · opencode
```

This writes the MCP config for your agent (e.g. `.mcp.json`) wired to launch the
server straight from GitHub with the shared API key — no npm publish required:

```jsonc
{
  "mcpServers": {
    "gdex-mcp-server": {
      "command": "npx",
      "args": ["-y", "github:GemachDAO/gdex-skill", "gdex-mcp-server"],
      "env": { "GDEX_API_KEY": "9b4e1c73-6a2f-4d88-b5c9-3e7a2f1d6c54" }
    }
  }
}
```

> The skills.sh install configures **skills**, not MCP — run the command above to add
> the MCP server. The skills also work via the SDK without MCP. The first launch
> builds the package from source (cached afterward).

## Autonomous Agent Quickstart

If you're an AI agent operating autonomously (no human to ask), here's the minimum viable flow:

### 1. Initialize
```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gemachdao/gdex-skill';
const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);
```

### 2. Research Before Trading
```typescript
// Check what's trending
const trending = await skill.getTrendingTokens({ chain: 622112261, period: '1h', limit: 10 });

// Get details on a token — CHECK dexId BEFORE buying
const token = await skill.getTokenDetails({ tokenAddress: trending[0].address, chain: 622112261 });
if (token.dexId === 'meteora') {
  // ❌ Meteora tokens FAIL on Solana — skip this token
}
if (token.dexId === 'raydium') {
  // ✅ Safe to buy
}
```

### 3. Full Managed-Custody Setup (for actual trading)
```typescript
import { ethers } from 'ethers';
import {
  generateGdexSessionKeyPair, buildGdexSignInMessage,
  buildGdexSignInComputedData, buildGdexUserSessionData,
} from '@gemachdao/gdex-skill';

const wallet = ethers.Wallet.fromPhrase('your mnemonic...');
const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();
const nonce = String(Date.now());
const msg = buildGdexSignInMessage(wallet.address, nonce, sessionKey);
const sig = await wallet.signMessage(msg);
const payload = buildGdexSignInComputedData({
  apiKey: GDEX_API_KEY_PRIMARY, userId: wallet.address, sessionKey, nonce, signature: sig,
});
await skill.signInWithComputedData({ computedData: payload.computedData, chainId: 1 });
```

### 4. Key Rules for Autonomous Operation
- **Always use control wallet address** (the one that signed in) for `userId`/`walletAddress` in API calls
- **Never use managed wallet address** in API calls (except `getHlUserStats()`)
- **Amounts in raw units** for managed trades (lamports for Solana, wei for EVM)
- **Check `dexId`** before buying on Solana — skip Meteora tokens
- **Generate fresh nonce** for every operation
- **Portfolio/balances use raw client** — high-level methods send wrong params
- **If `hlCloseAll` fails**, use reduce-only order instead

## Related Skills

- **gdex-authentication** — Managed-custody auth flow and encryption details
- **gdex-spot-trading** — Buy/sell tokens on any chain
- **gdex-perp-trading** — HyperLiquid perpetual futures
- **gdex-token-discovery** — Token info without authentication
- **gdex-wallet-setup** — Wallet generation for new users
- **gdex-ui-install-setup** — Frontend project setup with React/Next.js
- **gdex-sdk-debugging** — Error troubleshooting and debugging guide

---

# Live-Tested Operational Playbook

_Consolidated reference (migrated from the umbrella skill). Critical notes and an autonomous-agent playbook validated against the live backend._

## Critical Notes (Live-Tested)

> **walletAddress = CONTROL address, NOT managed address.** All HL write operations (`hlCreateOrder`, `hlCloseAll`, `perpDeposit`, etc.) require `walletAddress` set to the **control wallet address** used during sign-in — NOT the managed-custody address returned by `/v1/user`. The backend verifies the session key signature against the sign-in `userId`. Passing the managed address causes `400 Unauthorized (code 103)`.

> **`hlCloseAll` / `/v1/hl/close_all_positions` is unreliable.** It frequently returns `TIMEOUT` or JSON parse errors. To close positions reliably, place a **reduce-only** `hl_create_order` sell/buy for the exact position size instead.

> **`hlUpdateLeverage` / `/v1/hl/update_leverage` is not implemented** on the backend (returns 404). Leverage is set automatically when placing orders — pass the desired leverage indirectly via position sizing.

> **Solana chainId is `622112261`, NOT `900`.** The correct Solana chain ID is `ChainId.SOLANA = 622112261`. Using `900` falls back to the EVM managed address with `balance: null`. The `/v1/user` endpoint returns a **different managed wallet** per `chainId`:
> - `chainId=1` → EVM managed: `0x9967...`
> - `chainId=622112261` → Solana managed: `CFSi4YimeCbfSNqH2WmHwJKwj1YYG1cWBtQyVPB4sCe1` (base58)
> Always use `ChainId.SOLANA` from the SDK's enum to avoid this mistake.

> **Solana Meteora swaps are broken (backend bug).** Tokens that route through Meteora DLMM (e.g. BONK) fail with `Program error: 1` because the backend doesn’t wrap SOL into WSOL before calling `Swap2`. **Raydium-routed tokens work correctly** (e.g. WIF). Check `token.dexId` — if it's `"meteora"`, the swap will fail. Prefer tokens with `isRaydium: true` or `dexId: "raydium"`.

> **Solana trades need ~0.01 SOL minimum.** ATA (Associated Token Account) creation costs ~0.002 SOL per new token, plus priority fees (default 0.0005 SOL) and base tx fees. First trade on a new token needs ~0.007 SOL overhead beyond the swap amount.

> **Bridge endpoints use different paths than expected.** The actual backend routes are `GET /v1/bridge/estimate_bridge`, `POST /v1/bridge/request_bridge`, and `GET /v1/bridge/bridge_orders`. The `request_bridge` endpoint requires ABI-encoded + signed + AES-encrypted `computedData` (same pattern as managed trades). Bridge is **native tokens only** and uses ChangeNow as provider. Amounts must be in **raw token units** (wei/lamports). See **gdex-bridge** skill for full details.

> **Copy trade write operations (create/delete) use `chainId: 622112261` for sign-in, NOT `chainId: 1`.** The chainId field in the ABI is `uint256` (not string). The update endpoint uses 16 ABI fields (not 15): `[traderWallet, copyTradeName, chainId(uint256), gasPrice, buyMode, copyBuyAmount, isBuyExistingToken, lossPercent, profitPercent, nonce, copySell, excludedDexNumbers, copyTradeId, isDelete, isChangeStatus, excludedProgramIds]`. Both `isDelete='1'` and `isChangeStatus='1'` permanently delete the trade — there is no toggle. Boolean fields use `''` (empty string) for false and `'1'` for true; string `'0'` is truthy and will trigger deletion.

> **Limit order endpoints are `limit_buy` / `limit_sell` / `update_order` — NOT `orders/create` / `orders/cancel`.** Use `limitBuy()` for buy orders, `limitSell()` for sell orders (auto-classifies TP vs SL), and `updateOrder({ isDelete: true })` to cancel. Listing uses `GET /v1/orders` with `userId` + encrypted `data` + `chainId`. All write endpoints use ABI-encoded + signed + AES-encrypted `computedData` (same managed-custody pattern). Minimum order is ~0.01 native token. See **gdex-limit-orders** skill for full details.

> **HL perp copy trading is completely separate from Solana copy trading.** Uses `chainId: 1` (EVM), ABI methods `hl_create`/`hl_update` (8 and 11 string fields), and goes through `buildHlComputedData()`. Both `isDelete` and `isChangeStatus` permanently **DELETE** the trade (same as Solana — there is no toggle). Both TP and SL are **mandatory** (> 0). Max 3 copy trades per user. Supports opposite-direction copying via `oppositeCopy`. Backend stores ABI byte-offsets for `copyMode` and `oppositeCopy` (e.g., `copyMode=416`), not the actual values. `user_stats` requires the managed wallet address, not the control wallet. See **gdex-perp-copy-trading** skill for full details.

## Autonomous Agent Playbook

> **This section contains everything an autonomous AI agent needs to trade without human help.**

### Portfolio / Balances — Backend Param Mismatch (Live-Tested)

The high-level `getPortfolio()` and `getBalances()` methods send `walletAddress` + `chain`, but the backend expects `userId` + `chainId` + `data` (encrypted session key). **Workaround — use the raw client directly:**

```typescript
import { buildGdexUserSessionData } from '@gemachdao/gdex-skill';
const data = buildGdexUserSessionData(sessionKey, apiKey);

// Portfolio (balances embedded under portfolio.balances[])
const portfolio = await skill.client.get('/v1/portfolio', {
  params: { userId: controlAddress, chainId: 622112261, data }
});

// Balances — read from /v1/portfolio (balances embedded under portfolio.balances[]).
// There is no separate /v1/balances endpoint on backend v1.1.0.
const balances = portfolio.balances ?? [];
```

### Trade History — Different Param Names (Live-Tested)

Backend expects `user` (not `userId`), and the managed Solana chainId for trade history is `900` (not `622112261`):

```typescript
const history = await skill.client.get('/v1/user_history', {
  params: { user: controlAddress, chainId: 900, data, page: 1, limit: 20 }
});
```

### OHLCV / TopTraders — Numeric chainId Required (Live-Tested)

Backend needs numeric `chainId`, not string `chain`. These work:
```typescript
await skill.getOHLCV({ tokenAddress, chain: 622112261, resolution: '60', from, to });
await skill.getTopTraders({ chain: 622112261, period: '7d', limit: 5 });
```

### Spot Trading (Managed Custody) — Raw Units Required (Live-Tested)

For managed-custody trades, amounts must be in **raw units** (lamports for Solana, wei for EVM), NOT float:
```typescript
// ❌ WRONG: amount: '0.01'
// ✅ CORRECT: amount: '10000000' (0.01 SOL = 10000000 lamports)
```

### Limit Orders — profitPercent/lossPercent MUST Be uint256 (Live-Tested)

The `limit_buy` and `update_order` ABI schemas use `uint256` for `profitPercent` and `lossPercent` — NOT `string`. The backend decodes them as uint256 and validates 0-100 range. Using `string` type produces ABI byte-offsets (e.g. 192) that always fail. The SDK handles this correctly.

### Endpoints That Don't Work (Live-Tested)

| Endpoint | Status | Alternative |
|----------|--------|-------------|
| `hlCloseAll` / `/v1/hl/close_all_positions` | Returns TIMEOUT/400 | Use `hlCreateOrder` with `reduceOnly: true, isMarket: true` |
| `hlUpdateLeverage` / `/v1/hl/update_leverage` | Returns 404 | Leverage is set automatically by the backend per order |
| `getGbotUsdcBalance` | Returns 404 | Use `getHlAccountState()` to check USDC balance |
| `getHlUserStats(controlAddress)` | Returns 400 | Must pass the **managed** wallet address, not control |

### Error Recovery for Autonomous Agents

| Error | What to Do |
|-------|------------|
| `400 Unauthorized (103)` | Check: (1) using control address not managed, (2) ABI types match exactly, (3) session key is from the same sign-in |
| `Insufficient balance` | Check managed wallet balance on the correct chain. For HL, check USDC deposit amount. |
| `TIMEOUT` on hlCloseAll | Use reduce-only order instead (see above) |
| `Program error: 1` on Solana | Token routes through Meteora DLMM. Swap to a Raydium-routed token instead. |
| `lossPercent must be between 0 and 100` | ABI encoding bug — profitPercent/lossPercent must be uint256, not string |
| `404` on leverage | Expected — leverage is auto-set. Control via position sizing. |
| `Reused nonce` | Always generate fresh: `String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000))` |
| Rate limited (429) | SDK auto-retries with exponential backoff. If manual, wait `retryAfter` seconds. |

### Live-Tested E2E Results (39/42 Pass)

| Section | Tests | Pass | Notes |
|---------|-------|------|-------|
| Auth & Portfolio | 7 | 7/7 | Sign-in, resolve user, portfolio (raw client), balances, trade history |
| Token Discovery | 3 | 3/3 | Token details, trending, OHLCV |
| Top Traders | 1 | 1/1 | Top traders by PnL |
| Spot Trading | 3 | 3/3 | Buy WIF (Solana), sell WIF, poll status |
| HL Perp Trading | 10 | 8/10 | Deposit, create order, positions, close (reduce-only). `getGbotUsdcBalance` 404, `hlCloseAll` 400 |
| Limit Orders | 4 | 4/4 | List, create (limit buy), verify, cancel |
| Copy Trading Reads | 4 | 4/4 | Wallets, custom wallets, gems, DEXes |
| HL Copy Trading Reads | 8 | 7/8 | Top traders, top by PnL, assets, DEXes, deposit tokens. `getHlUserStats` needs managed addr |
| Bridge Estimate | 1 | 1/1 | ETH→ARB estimate |
| Wallet Generation | 1 | 1/1 | Offline EVM wallet |

## Quick Start

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// No-auth endpoints work immediately
const trending = await skill.getTrendingTokens({ chain: 'solana', period: '24h', limit: 5 });

// Auth-required endpoints
const trade = await skill.buyToken({
  chain: 'solana',
  tokenAddress: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
  amount: '0.1',
  slippage: 1,
});
```

**Shared API Keys:** `9b4e1c73-6a2f-4d88-b5c9-3e7a2f1d6c54` (primary), `2c8f0a91-5d34-4e7b-9a62-f1c3d8e4b705` (secondary)

## Installation

```bash
# Install all skills
npx skills add GemachDAO/gdex-skill --all --agent '*' -g

# Install SDK (from GitHub — builds on install; imports stay '@gemachdao/gdex-skill')
npm install github:GemachDAO/gdex-skill
```
| userId | Control wallet address (from sign-in), NOT managed wallet |
| Bridge receiver | `0x2Df1c51E09aECF9cacB7bc98cB1742757f163dF7` |

### HL Signature Format

All HL write operations sign with the **session private key** (registered during sign-in):
```
message = "{action}-{userId.toLowerCase()}-{dataHex}" // e.g. "hl_deposit-0x53d0...-0000..."
digest  = keccak256(utf8Bytes(message))
output  = r(64hex) + s(64hex) + v(2hex)  // 130 chars, v=00/01, no 0x prefix
```

### HL Error Codes

| Code | Error | Common Cause |
|---|---|---|
| 103 | Unauthorized | Wrong ABI type (uint256 instead of uint64), wrong userId, or signing with wrong key |
| 102 | Invalid chainId | chainId is not 42161 |
| 102 | Invalid params | Reused nonce or unsupported token |
| — | Insufficient balance | Managed wallet needs more USDC + fee on Arbitrum |
| — | Too low amount | Amount < 10 USDC (10000000 smallest unit) |
