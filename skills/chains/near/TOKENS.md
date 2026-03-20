# Token Reference for NEAR Intents — 1Click SDK

Static reference for commonly used tokens including their decimals, contract addresses, and intent asset IDs used by the 1Click API.

## Why Decimals Matter

Blockchain tokens have different decimal precision:
- **NEAR**: 24 decimals (1 NEAR = 10^24 yoctoNEAR)
- **USDC**: 6 decimals (1 USDC = 10^6 microUSDC)
- **ETH**: 18 decimals (1 ETH = 10^18 wei)
- **BTC**: 8 decimals (1 BTC = 10^8 satoshi)

**Critical**: If decimals are wrong, transactions will fail or send wrong amounts!

The `executeIntent()` function handles decimal conversion automatically. This file is for reference.

## How to Get Live Token Data

```typescript
import { OneClickService } from '@defuse-protocol/one-click-sdk-typescript';

// Fetch all supported tokens from 1Click API
const tokens = await OneClickService.getTokens();

// Each token has: blockchain, symbol, assetId, contractAddress, price, decimals
```

Or run the example:
```bash
npx ts-node lib-1click/1-get-tokens.ts
```

---

## Token Reference

### NEAR Ecosystem

| Token  | Symbol | Decimals | Asset ID |
|--------|--------|----------|----------|
| NEAR   | NEAR   | 24       | `nep141:wrap.near` |
| wNEAR  | wNEAR  | 24       | `nep141:wrap.near` |
| USDC   | USDC   | 6        | `nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1` |
| USDT   | USDT   | 6        | `nep141:usdt.tether-token.near` |
| DAI    | DAI    | 18       | `nep141:576f222612ecf8f8b75a4f7c1e3cbf5a52384e431870` |

### Ethereum (via Defuse bridge)

| Token  | Symbol | Decimals | Asset ID |
|--------|--------|----------|----------|
| ETH    | ETH    | 18       | `nep141:eth.omft.near` |
| USDC   | USDC   | 6        | `nep141:eth-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.omft.near` |

### Base (L2)

| Token  | Symbol | Decimals | Asset ID |
|--------|--------|----------|----------|
| USDC   | USDC   | 6        | `nep141:base-0x833589fcd6edb6e08f4c7c32d4f71b54bda02913.omft.near` |

### Arbitrum

| Token  | Symbol | Decimals | Asset ID |
|--------|--------|----------|----------|
| USDC   | USDC   | 6        | `nep141:arb-0xaf88d065e77c8cc2239327c5edb3a432268e5831.omft.near` |
| ARB    | ARB    | 18       | `nep141:arb-0x912ce59144191c1204e64559fe8253a0e49e6548.omft.near` |

### Solana

| Token  | Symbol | Decimals | Asset ID |
|--------|--------|----------|----------|
| SOL    | SOL    | 9        | `nep141:sol.omft.near` |
| USDC   | USDC   | 6        | `nep141:sol-5ce3bf3a31af18be40ba30f721101b4341690186.omft.near` |

### Bitcoin (Native UTXO)

| Token  | Symbol | Decimals | Asset ID | Notes |
|--------|--------|----------|----------|-------|
| BTC    | BTC    | 8        | `nep141:btc.omft.near` | **Native only** |

### Dogecoin (Native UTXO)

| Token  | Symbol | Decimals | Asset ID | Notes |
|--------|--------|----------|----------|-------|
| DOGE   | DOGE   | 8        | `nep141:doge.omft.near` | **Native only** |

### Zcash (Native UTXO)

| Token  | Symbol | Decimals | Asset ID | Notes |
|--------|--------|----------|----------|-------|
| ZEC    | ZEC    | 8        | `nep141:zec.omft.near` | **Native only** |

### Litecoin (Native UTXO)

| Token  | Symbol | Decimals | Asset ID | Notes |
|--------|--------|----------|----------|-------|
| LTC    | LTC    | 8        | `nep141:ltc.omft.near` | **Native only** |

---

## Using in `executeIntent()`

You don't need raw asset IDs. Use the `chain:SYMBOL` format:

```typescript
// NEAR chain (no prefix)
{ assetIn: 'NEAR', assetOut: 'USDC', amount: '1.0' }

// Cross-chain
{ assetIn: 'NEAR', assetOut: 'base:USDC', amount: '1.0', recipient: '0x...' }

// Arbitrum to Solana
{ assetIn: 'arb:USDC', assetOut: 'sol:USDC', amount: '5.0', recipient: 'SolAddr...' }
```

The code maps symbols to asset IDs via the built-in `TOKEN_MAP`.

---

## Common Decimals Reference

| Token | Decimals | `"1.0"` → smallest unit |
|-------|----------|------------------------|
| NEAR  | 24       | `1000000000000000000000000` |
| USDC  | 6        | `1000000` |
| USDT  | 6        | `1000000` |
| ETH   | 18       | `1000000000000000000` |
| SOL   | 9        | `1000000000` |
| BTC   | 8        | `100000000` |
| ARB   | 18       | `1000000000000000000` |

---

## UTXO Chains — Native Only

**⚠️ BTC, DOGE, ZEC, LTC only support native tokens!**

- ✅ `btc:BTC`, `doge:DOGE`, `zec:ZEC`, `ltc:LTC`
- ❌ `btc:USDC`, `btc:WBTC` — **NOT SUPPORTED**

```typescript
// ✅ Works
await executeIntent({
  assetIn: 'NEAR', assetOut: 'btc:BTC', amount: '10.0',
  recipient: 'bc1q...', mode: 'manual',
});

// ❌ Does NOT work
await executeIntent({
  assetIn: 'NEAR', assetOut: 'btc:USDC',  // NOT SUPPORTED
  amount: '10.0', recipient: 'bc1q...',
});
```

---

## Adding New Tokens

1. Run `npx ts-node lib-1click/1-get-tokens.ts` to see all available tokens
2. Find the token's `assetId`, `decimals`, and `symbol`
3. Add to the `TOKEN_MAP` in `index.ts`
4. Update this file for reference

---

**Version**: 2.0.0
**Source**: [1Click API](https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api)
