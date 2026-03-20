---
name: near-intents
description: Universal cross-chain swap & bridge skill for OpenClaw using the NEAR Intents 1Click SDK. Supports 14+ blockchains including NEAR, Base, Ethereum, Solana, and Bitcoin.
---

# NEAR Intents Skill — 1Click SDK

## 📋 TL;DR

**What it does**: Universal cross-chain swap & bridge tool powered by the [1Click API](https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api) and the [`@defuse-protocol/one-click-sdk-typescript`](https://github.com/defuse-protocol/one-click-sdk-typescript) SDK.

**Supported chains**: NEAR, Base, Ethereum, Arbitrum, Solana, BSC, Gnosis, Starknet, Bitcoin, Dogecoin, Zcash, Litecoin.

**How it works**:
1. Get a quote from the 1Click API → receive a deposit address
2. Send tokens to the deposit address on the origin chain
3. 1Click handles the swap/bridge automatically
4. Tokens arrive at the recipient address on the destination chain

**Key facts**:
- Minimum ~$0.10 USD per swap
- NEAR account only required when the *origin* asset is on NEAR
- No NEAR account needed for cross-chain swaps from other chains (e.g., Arb USDC → Sol USDC)
- JWT authentication optional but avoids 0.2% fee → register at [partners.near-intents.org](https://partners.near-intents.org/)

---

## Core Concept

All swaps go through the **1Click API** (`https://1click.chaindefuser.com`):

```
User Wallet ──► [Deposit to 1Click address] ──► Market Makers ──► Recipient on Destination Chain
```

There is **no need to interact with `intents.near` directly** — the 1Click API abstracts everything.

---

## `executeIntent()` API

The single entry point exported by `index.ts`:

```typescript
import { executeIntent } from './index';

const result = await executeIntent({
  assetIn: 'NEAR',           // Origin token (see Asset Naming below)
  assetOut: 'base:USDC',     // Destination token
  amount: '1.0',             // Human-readable amount
  recipient: '0x...',        // Destination address (optional if same-chain NEAR)
  mode: 'auto',              // 'auto' (default) or 'manual'
  swapType: 'EXACT_INPUT',   // 'EXACT_INPUT' (default) or 'EXACT_OUTPUT'
});
```

### Parameters

| Parameter   | Type   | Required | Description |
|-------------|--------|----------|-------------|
| `assetIn`   | string | ✅ | Origin asset symbol (e.g., `'NEAR'`, `'base:USDC'`, `'arb:ARB'`) |
| `assetOut`  | string | ✅ | Destination asset symbol |
| `amount`    | string | ✅ | Human-readable amount (e.g., `'1.0'`, `'0.5'`) |
| `recipient` | string | ❌ | Destination address. Required for cross-chain. Defaults to NEAR account |
| `refundAddress` | string | ⚠️ | **REQUIRED for non-NEAR origins**. Address on origin chain for refunds if swap fails. **CRITICAL for fund safety!** |
| `mode`      | string | ❌ | `'auto'` sends deposit automatically from NEAR account. `'manual'` returns quote + deposit address for user to send manually |
| `swapType`  | string | ❌ | `'EXACT_INPUT'` (amount = input), `'EXACT_OUTPUT'` (amount = desired output) |

### ⚠️ CRITICAL: Refund Address Safety

**When `assetIn` is on a non-NEAR chain** (e.g., `'base:USDC'`, `'arb:ARB'`, `'btc:BTC'`):

1. **`refundAddress` is REQUIRED** — the function will throw an error if missing
2. **ALWAYS ask the user** for their wallet address on the origin chain
3. **NEVER assume or guess** — using the wrong address = permanent fund loss
4. **Explain to the user**: "If the swap fails, your tokens will be refunded to this address"

**Example**:
```typescript
// ❌ WRONG - Missing refundAddress for non-NEAR origin
await executeIntent({
  assetIn: 'base:USDC',  // Base origin
  assetOut: 'NEAR',
  amount: '0.5',
  recipient: 'user.near',
  mode: 'manual'
});
// → Error: Cross-chain swap from base:USDC requires refundAddress parameter

// ✅ CORRECT - User's Base wallet address provided
await executeIntent({
  assetIn: 'base:USDC',
  assetOut: 'NEAR',
  amount: '0.5',
  recipient: 'user.near',
  refundAddress: '0x123...',  // User's Base address
  mode: 'manual'
});
```

**Why this matters**:
- Swaps can fail due to market conditions, liquidity issues, or timing
- Failed swaps trigger automatic refunds to `refundAddress` on the **origin chain**
- If `refundAddress` is wrong or belongs to someone else, **funds are permanently lost**

### Returns

- **Auto mode**: `"Swap Successful! 1.0 NEAR → 0.97 USDC\nTransaction: https://nearblocks.io/txns/...\nExplorer: https://explorer.near-intents.org/transactions/..."`
- **Manual mode**: Formatted instructions with deposit address, amounts, tracking URL, and deadline

---

## Asset Naming

Use `chain:SYMBOL` format. Omit chain prefix for NEAR-native tokens.

| Chain     | Prefix     | Examples                          |
|-----------|------------|-----------------------------------|
| NEAR      | *(none)*   | `NEAR`, `USDC`, `USDT`, `wNEAR`  |
| Base      | `base:`    | `base:USDC`                       |
| Ethereum  | `eth:`     | `eth:ETH`, `eth:USDC`             |
| Arbitrum  | `arb:`     | `arb:USDC`, `arb:ARB`             |
| Solana    | `sol:`     | `sol:SOL`, `sol:USDC`             |
| BSC       | `bsc:`     | `bsc:USDC`                        |
| Bitcoin   | `btc:`     | `btc:BTC` *(native only)*         |
| Dogecoin  | `doge:`    | `doge:DOGE` *(native only)*       |
| Zcash     | `zec:`     | `zec:ZEC` *(native only)*         |
| Litecoin  | `ltc:`     | `ltc:LTC` *(native only)*         |

- **Case-insensitive**: `near`, `NEAR`, `Near` all work
- **UTXO chains** (BTC, DOGE, ZEC, LTC): **native tokens only** — no wrapped/ERC-20 equivalents

---

## Modes

### Auto Mode (default)
Automatically sends the deposit from the configured NEAR account.

**Use when**: Origin asset is on NEAR and agent has NEAR credentials in `.env`.

```typescript
await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0xYourBaseAddress',
});
```

### Manual Mode
Returns a quote with deposit address — the user (or agent) sends tokens separately.

**Use when**: Origin is on a non-NEAR chain, or you want to show the user a quote first.

```typescript
const quote = await executeIntent({
  assetIn: 'arb:USDC',
  assetOut: 'sol:USDC',
  amount: '5.0',
  recipient: 'YourSolanaAddress',
  mode: 'manual',
});
// Returns deposit address + instructions
```

### EXACT_OUTPUT
Specify the desired output amount; the 1Click API tells you how much to send.

```typescript
const quote = await executeIntent({
  assetIn: 'USDT',
  assetOut: 'base:USDC',
  amount: '10.0',          // Want exactly 10 USDC out
  recipient: '0x...',
  mode: 'manual',
  swapType: 'EXACT_OUTPUT',
});
```

---

## Examples

### 1. Swap NEAR → USDC on Base (Auto)
```typescript
await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0xYourBaseAddress',
});
```

### 2. Bridge USDC from Arbitrum → Solana (Manual)
```typescript
const quote = await executeIntent({
  assetIn: 'arb:USDC',
  assetOut: 'sol:USDC',
  amount: '5.0',
  recipient: 'YourSolanaAddress',
  refundAddress: '0xYourArbitrumAddress',  // REQUIRED for refunds
  mode: 'manual',
});
// User sends 5 USDC to the deposit address on Arbitrum
```

### 3. Swap NEAR → USDC (same chain)
```typescript
await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'USDC',
  amount: '2.0',
});
```

### 4. Get a quote: How much NEAR for 10 USDC on Arbitrum?
```typescript
const quote = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'arb:USDC',
  amount: '10.0',
  recipient: '0xYourArbAddress',
  mode: 'manual',
  swapType: 'EXACT_OUTPUT',
});
```

### 5. Send BTC to NEAR address
```typescript
const quote = await executeIntent({
  assetIn: 'btc:BTC',
  assetOut: 'NEAR',
  amount: '0.01',
  recipient: 'yourname.near',
  refundAddress: 'bc1q...',  // REQUIRED - Your Bitcoin address
  mode: 'manual',
});
// User sends 0.01 BTC to the deposit address on Bitcoin
```

---

## Configuration

### `.env` file (only needed for auto mode with NEAR origin):
```env
NEAR_ACCOUNT_ID=your-account.near
NEAR_PRIVATE_KEY=ed25519:your_private_key_here
NEAR_RPC_URL=https://rpc.mainnet.fastnear.com
NEAR_NETWORK_ID=mainnet
ONE_CLICK_JWT=optional_jwt_token
```

- `ONE_CLICK_JWT`: Register at [partners.near-intents.org](https://partners.near-intents.org/) to avoid the 0.2% fee.
- Skip `.env` entirely if only using manual mode for non-NEAR-origin swaps.

⚠️ **Never commit `.env` to version control!**

---

## Under the Hood — 1Click SDK Flow

```
executeIntent()
  │
  ├─ 1. resolveToken(assetIn)  →  { symbol, decimals, assetId }
  ├─ 2. resolveToken(assetOut) →  { symbol, decimals, assetId }
  ├─ 3. toSmallestUnit(amount, decimals)
  │
  ├─ 4. OneClickService.getQuote({
  │       originAsset, destinationAsset, amount,
  │       refundTo, recipient, deadline, ...
  │    })
  │    → Returns { depositAddress, amountIn, amountOut }
  │
  ├─ [manual mode] → return quote instructions
  │
  ├─ 5. account.transfer() → send deposit to depositAddress
  ├─ 6. OneClickService.submitDepositTx() → (optional, speeds up)
  └─ 7. OneClickService.getExecutionStatus() → poll until SUCCESS
```

### Swap Statuses
| Status              | Meaning |
|---------------------|---------|
| `PENDING_DEPOSIT`   | Waiting for deposit |
| `PROCESSING`        | Deposit detected, market makers executing |
| `SUCCESS`           | Tokens delivered to recipient |
| `INCOMPLETE_DEPOSIT`| Deposit below required amount |
| `REFUNDED`          | Swap failed, tokens returned to refund address |
| `FAILED`            | Swap failed due to error |

---

## Token Map (built-in)

The code includes a static `TOKEN_MAP` for common tokens:

| Key          | Asset ID (NEP-141)                                              | Decimals |
|--------------|-----------------------------------------------------------------|----------|
| `NEAR`       | `nep141:wrap.near`                                              | 24       |
| `USDC`       | `nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1` | 6 |
| `USDT`       | `nep141:usdt.tether-token.near`                                 | 6        |
| `base:USDC`  | `nep141:base-0x833589fcd6edb6e08f4c7c32d4f71b54bda02913.omft.near` | 6     |
| `arb:USDC`   | `nep141:arb-0xaf88d065e77c8cc2239327c5edb3a432268e5831.omft.near` | 6     |
| `arb:ARB`    | `nep141:arb-0x912ce59144191c1204e64559fe8253a0e49e6548.omft.near` | 18    |
| `eth:ETH`    | `nep141:eth.omft.near`                                          | 18       |
| `eth:USDC`   | `nep141:eth-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.omft.near` | 6     |
| `sol:SOL`    | `nep141:sol.omft.near`                                          | 9        |
| `sol:USDC`   | `nep141:sol-5ce3bf3a31af18be40ba30f721101b4341690186.omft.near` | 6        |

To add more tokens: use `OneClickService.getTokens()` or check `TOKENS.md`.

---

## Decimals Quick Reference

| Token | Decimals | `"1.0"` → smallest unit |
|-------|----------|------------------------|
| NEAR  | 24       | `1000000000000000000000000` |
| USDC  | 6        | `1000000`              |
| USDT  | 6        | `1000000`              |
| ETH   | 18       | `1000000000000000000`  |
| SOL   | 9        | `1000000000`           |
| BTC   | 8        | `100000000`            |

Decimal conversion is handled automatically by `index.ts` using `decimal.js`.

---

## Tracking & Explorer

- **NEAR transactions**: `https://nearblocks.io/txns/<txHash>`
- **1Click swap status**: `https://explorer.near-intents.org/transactions/<depositAddress>`

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Token not found: X` | Check symbol and chain prefix. See `TOKEN_MAP` or `TOKENS.md` |
| `No deposit address in quote response` | Solver couldn't match the pair/amount. Try a different amount or pair |
| `NEAR_ACCOUNT_ID and NEAR_PRIVATE_KEY must be set` | Configure `.env` or use `mode: 'manual'` |
| `Swap failed with status: REFUNDED` | Tokens returned to refund address. Retry with different amount |
| `Status polling timed out` | Check explorer URL manually. Swap may still complete |
| 401 Authentication error | JWT is invalid or expired. Register at partners.near-intents.org |

---

## Dependencies

```json
{
  "@defuse-protocol/one-click-sdk-typescript": "0.1.1",
  "@near-js/accounts": "^2.2.4",
  "@near-js/crypto": "^2.2.4",
  "@near-js/providers": "^2.2.4",
  "@near-js/signers": "^2.2.4",
  "@near-js/tokens": "^2.2.4",
  "decimal.js": "^10.4.3",
  "dotenv": "^16.3.1"
}
```

---

## Files Overview

| File | Purpose |
|------|---------|
| `index.ts` | Main entry — exports `executeIntent()` |
| `lib-1click/` | Step-by-step 1Click SDK examples (get tokens, get quote, send deposit, etc.) |
| `SKILL.md` | This file — **primary AI agent reference** |
| `AI-AGENT-GUIDE.md` | Detailed agent workflow guide |
| `TOKENS.md` | Full token reference with decimals and asset IDs |
| `manifest.json` | Skill manifest for OpenClaw |
| `README.md` | Project documentation |
| `USAGE_GUIDE.md` | Usage patterns and troubleshooting |

---

## Version

**v2.0.0** — Powered by [1Click SDK](https://github.com/defuse-protocol/one-click-sdk-typescript) and [NEAR Intents](https://docs.near-intents.org)

## License

MIT
