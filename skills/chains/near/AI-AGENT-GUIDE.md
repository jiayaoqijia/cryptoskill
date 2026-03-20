# NEAR Intents Skill — AI Agent Workflow Guide

This guide explains how an AI agent should use the `executeIntent()` function effectively.

## Quick Reference

```typescript
import { executeIntent } from './index';

// Auto mode — sends from configured NEAR account
const result = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0x...',
});

// Manual mode — returns quote + deposit address
const quote = await executeIntent({
  assetIn: 'arb:USDC',
  assetOut: 'sol:USDC',
  amount: '5.0',
  recipient: 'SolanaAddr...',
  mode: 'manual',
});
```

---

## Decision Tree for Agents

```
User request → Parse assetIn, assetOut, amount, recipient
                    │
          Is origin token on NEAR?
                /           \
              YES             NO
               │               │
     Has NEAR credentials?    Use mode: 'manual'
           /       \            │
         YES       NO          Return deposit address
          │         │          + instructions to user
  mode: 'auto'   mode: 'manual'
  (auto-send)    (return quote)
```

### When to Use Auto Mode
- Agent has `NEAR_ACCOUNT_ID` and `NEAR_PRIVATE_KEY` configured
- Origin asset is on NEAR (e.g., `'NEAR'`, `'USDC'`, `'USDT'`)
- Agent should execute the swap end-to-end without user intervention

### When to Use Manual Mode
- Origin asset is on a non-NEAR chain (e.g., `'base:USDC'`, `'arb:ARB'`)
- User needs to send from their own wallet
- Agent wants to show the quote before committing
- No NEAR credentials available

### ⚠️ CRITICAL: Refund Address for Cross-Chain Swaps

**When origin is NOT NEAR** (e.g., Base, Arbitrum, Ethereum, Solana):
1. **ALWAYS ask the user for their refund address** on the origin chain
2. **NEVER assume or guess** the refund address
3. **Explain why**: "If the swap fails, your funds will be returned to this address"

**Why this matters**:
- If the swap fails, tokens are refunded to `refundAddress` on the **origin chain**
- Using the wrong address = **permanent fund loss**
- The refund address must be controlled by the user

**Example conversation**:
```
User: "Swap 0.5 USDC from Base to ETH on NEAR"
Agent: "Got it! Before I generate the quote, I need your Base wallet address 
        for refunds (in case the swap fails). What Base address will you be 
        sending the USDC from?"
User: "0xabc..."
Agent: [proceeds with refundAddress: '0xabc...']
```

---

## Common Agent Workflows

### Workflow 1: "Swap 1 NEAR to USDC on Base"

```typescript
const result = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0xUserBaseAddress',
  // mode: 'auto' (default)
});
// → "Swap Successful! 1.0 NEAR → 0.97 USDC"
```

### Workflow 2: "Bridge 5 USDC from Arbitrum to Solana"

**Step 1: Ask for refund address**
```
Agent: "I'll help you bridge USDC from Arbitrum to Solana. 
        What's your Arbitrum wallet address? (This is where 
        refunds will go if the swap fails)"
User: "0x123..."
```

**Step 2: Generate quote**
```typescript
const quote = await executeIntent({
  assetIn: 'arb:USDC',
  assetOut: 'sol:USDC',
  amount: '5.0',
  recipient: 'UserSolanaAddress',
  refundAddress: '0x123...',  // User's Arbitrum address
  mode: 'manual',
});
// → Returns deposit address on Arbitrum for user to send USDC
```

### Workflow 3: "I want exactly 10 USDC on Base, how much NEAR?"

```typescript
const quote = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '10.0',
  recipient: '0x...',
  mode: 'manual',
  swapType: 'EXACT_OUTPUT',
});
// → Returns: "You need to send: X.XX NEAR"
```

### Workflow 4: Same-chain swap on NEAR

```typescript
const result = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'USDC',
  amount: '2.0',
  // No need for recipient — stays on NEAR
});
```

### Workflow 5: "Send BTC to my NEAR account"

**Step 1: Ask for refund address**
```
Agent: "I'll generate a Bitcoin deposit address. What's your 
        Bitcoin wallet address? (For refunds if the swap fails)"
User: "bc1q..."
```

**Step 2: Generate quote**
```typescript
const quote = await executeIntent({
  assetIn: 'btc:BTC',
  assetOut: 'NEAR',
  amount: '0.01',
  recipient: 'user.near',
  refundAddress: 'bc1q...',  // User's Bitcoin address
  mode: 'manual',
});
// → Returns a Bitcoin deposit address for user to send BTC
```

---

## Response Parsing

### Auto Mode Response
```
Swap Successful! 0.1 NEAR → 0.105328 USDC
Transaction: https://nearblocks.io/txns/46rkUnrk...
Explorer: https://explorer.near-intents.org/transactions/2dc254...
```

**Extract from response**:
- Transaction hash: regex `nearblocks.io/txns/(\S+)`
- Explorer URL: regex `explorer.near-intents.org/transactions/(\S+)`

### Manual Mode Response
```
🎯 Manual Mode: Quote Generated

You need to send: 0.519188 USDT
You will receive: 0.5 USDC

📋 Instructions:
1. Send 0.519188 USDT to:
   de6eba71e700601d2c46ac9722e6b249e5efed59a423edf7fadfe37909eadeef

2. Track your swap:
   https://explorer.near-intents.org/transactions/de6eba...

3. Your USDC will arrive at:
   0x30FE694284a082a5D1adfF6D25C0B9B6bF61F77D

⏰ Deadline: 2026-02-16T02:43:56.552Z
```

**Extract from response**:
- Deposit address: the long hex string after "Send ... to:"
- Amount to send: regex `You need to send: ([\d.]+) (\w+)`
- Tracking URL: regex `explorer.near-intents.org/transactions/(\S+)`
- Deadline: regex `Deadline: (.+)`

---

## Swap Statuses

When polling in auto mode, the SDK goes through these statuses:

| Status | Meaning | Agent Action |
|--------|---------|-------------|
| `PENDING_DEPOSIT` | Waiting for deposit | Wait |
| `PROCESSING` | Market makers executing | Wait |
| `SUCCESS` | Complete | Report success |
| `INCOMPLETE_DEPOSIT` | Deposit too small | Report error |
| `REFUNDED` | Tokens returned | Report failure, suggest retry |
| `FAILED` | Error occurred | Report failure |

---

## Error Handling for Agents

```typescript
try {
  const result = await executeIntent({ ... });
  // Success — return result to user
} catch (error) {
  const msg = error.message;

  if (msg.includes('Token not found')) {
    // Invalid token symbol — check TOKENS.md
    // Suggest correct symbol to user
  }

  if (msg.includes('No deposit address')) {
    // Solver couldn't match — likely low liquidity or bad pair
    // Suggest larger amount or different pair
  }

  if (msg.includes('NEAR_ACCOUNT_ID')) {
    // Missing credentials — switch to manual mode
    // Or ask user to configure .env
  }

  if (msg.includes('REFUNDED')) {
    // Swap failed but tokens safe — returned to refund address
    // User can retry
  }

  if (msg.includes('timed out')) {
    // Polling timed out — swap may still complete
    // Direct user to explorer URL
  }
}
```

---

## Supported Asset Symbols

Use `chain:SYMBOL` format. Common examples:

**NEAR chain** (no prefix): `NEAR`, `wNEAR`, `USDC`, `USDT`
**Base**: `base:USDC`
**Arbitrum**: `arb:USDC`, `arb:ARB`
**Ethereum**: `eth:ETH`, `eth:USDC`
**Solana**: `sol:SOL`, `sol:USDC`
**Bitcoin**: `btc:BTC` *(native only)*
**Dogecoin**: `doge:DOGE` *(native only)*

Full list: see `TOKENS.md` or call `OneClickService.getTokens()`.

---

## Configuration

Required `.env` variables for auto mode:
```env
NEAR_ACCOUNT_ID=your-account.near
NEAR_PRIVATE_KEY=ed25519:...
NEAR_RPC_URL=https://rpc.mainnet.fastnear.com
NEAR_NETWORK_ID=mainnet
ONE_CLICK_JWT=optional_jwt_token
```

- `ONE_CLICK_JWT` is optional but avoids 0.2% fee
- Register at [partners.near-intents.org](https://partners.near-intents.org/)

---

## Tips for AI Agents

1. **🚨 ALWAYS ask for refundAddress** when origin is not NEAR — never assume or guess
2. **Default to manual mode** unless you control the NEAR account and origin is NEAR
3. **Use EXACT_OUTPUT** when user specifies desired output amount
4. **Always provide the recipient address** for cross-chain swaps
5. **Quotes expire in ~10 minutes** — act promptly after getting a quote
6. **Monitor swap status** via explorer URL: `https://explorer.near-intents.org/transactions/<depositAddress>`
7. **UTXO chains** (BTC, DOGE, ZEC, LTC) only support native tokens — no wrapped/ERC-20
8. **Parse amounts carefully** — all inputs should be human-readable (e.g., `'1.0'` not `'1000000'`)

---

## Testing

```bash
# Run unit tests
npm test

# Run a live 1Click swap test (uses real NEAR)
npm run swap:test

# Test manual mode
npx ts-node test-manual-mode.ts
```

---

## References

- **1Click SDK**: [github.com/defuse-protocol/one-click-sdk-typescript](https://github.com/defuse-protocol/one-click-sdk-typescript)
- **1Click API Docs**: [docs.near-intents.org](https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api)
- **SDK Examples**: `lib-1click/` directory in this skill
- **NEAR Intents Explorer**: [explorer.near-intents.org](https://explorer.near-intents.org)

---

**Version**: 2.0.0
**Status**: ✅ Production Ready
