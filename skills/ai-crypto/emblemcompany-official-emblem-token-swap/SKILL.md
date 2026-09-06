---
name: emblem-token-swap
description: >
  Execute token swaps across 6 blockchains via EmblemAI. Automatic route optimization and
  cross-chain bridging via ChangeNow. Use when the user wants to swap tokens, exchange crypto,
  convert between currencies, or bridge assets cross-chain.
license: MIT
compatibility: >
  Requires Node.js >= 18.0.0, @emblemvault/agentwallet CLI, and internet access.
  Works on Claude Code, Cursor, Codex, OpenClaw, and other agents following the Agent Skills spec.
metadata:
  author: EmblemAI
  version: "1.1.0"
  homepage: https://emblemvault.ai
  docs: https://emblemvault.ai/docs
  docs-interactive: https://emblemvault.dev
---

# Emblem Token Swap

Guided token swapping powered by **EmblemAI**. Swap tokens on Solana, Ethereum, Base, BSC, Polygon, and Hedera with automatic routing. Cross-chain bridging via ChangeNow.

**Requires**: `npm install -g @emblemvault/agentwallet`

---

## What This Skill Can Do

| Chain | Quote Tool | Swap Tool | Balance Tool | Token Search |
|-------|-----------|-----------|-------------|--------------|
| Solana | `splBuyIntent` (quote mode) | `splBuyIntent` (swap mode) | `solanaBalances` | `findSolanaSwapToken` |
| Ethereum | `ethSwapQuote` | `ethSwap` | `ethGetBalances` | `searchCryptoByName` |
| Base | `baseSwapQuote` | `baseSwap` | `baseGetBalances` | `searchEvmTokensBirdeye` |
| BSC | `bscSwapQuote` | `bscSwap` | `bscGetBalances` | `searchEvmTokensBirdeye` |
| Polygon | `polygonSwapQuote` | `polygonSwap` | `polygonGetBalances` | `searchEvmTokensBirdeye` |
| Hedera | `hederaTokensSwapQuote` | `hederaTokensSwap` | `hederaGetBalances` | `hederaFindTokens` |
| Cross-chain | `getChangeNowSwapQuote` | `swapUsingChangeNow` | — | `getChangeNowSupportedCurrencies` |

### Notes

- **Solana** uses `splBuyIntent` for both quotes and execution — it handles token lookup by name/symbol/CA and flexible amounts ($USD, SOL, or token quantity)
- **EVM chains** (Ethereum, Base, BSC, Polygon) route through automatic DEX aggregation
- **Cross-chain** bridges via ChangeNow support 500+ currencies
- Bitcoin has balance support (`getBTCBalances`) but no on-chain swap tools — use ChangeNow for BTC bridges

---

## Quick Start

```bash
npm install -g @emblemvault/agentwallet

# Solana swap (uses splBuyIntent)
emblemai --agent --profile default -m "Use splBuyIntent to swap 5 SOL for USDC on Solana"

# Cross-chain bridge (uses ChangeNow)
emblemai --agent --profile default -m "Use getChangeNowSwapQuote to get a quote for bridging 0.05 ETH from Ethereum to SOL on Solana"
```

**Trigger phrases:**
- "Swap SOL to USDC"
- "Exchange ETH for USDT"
- "Convert my tokens"
- "Bridge tokens to Base"

---

## Workflow: Safe Token Swap

### Step 1: Check Balance
Confirm you have enough of the source token.
```bash
emblemai --agent --profile default -m "Use solanaBalances to show my Solana token balances"
```

### Step 2: Get a Quote
Preview the swap before executing.
```bash
emblemai --agent --profile default -m "Use splBuyIntent to get a quote for swapping 5 SOL to USDC"
```

### Step 3: Execute the Swap
```bash
emblemai --agent --profile default -m "Use splBuyIntent to swap 5 SOL for USDC on Solana"
```
Safe mode requires your confirmation before executing.

### Step 4: Verify
Confirm the new balance.
```bash
emblemai --agent --profile default -m "Use solanaBalances to show my updated balances"
```

---

## Swap Patterns

### Solana Swaps
```bash
# By token amount
emblemai --agent --profile default -m "Use splBuyIntent to swap 0.5 SOL for USDC"

# By dollar amount
emblemai --agent --profile default -m "Use splBuyIntent to swap $20 of SOL for JUP"

# By token name
emblemai --agent --profile default -m "Use splBuyIntent to swap 100 USDC for BONK"
```

### EVM Swaps
```bash
# Ethereum
emblemai --agent --profile default -m "Use ethSwapQuote to get a quote for swapping 0.01 ETH to USDC, then use ethSwap to execute"

# Base
emblemai --agent --profile default -m "Use baseSwapQuote to quote 0.005 ETH to USDC on Base"

# BSC
emblemai --agent --profile default -m "Use bscSwapQuote to quote 0.1 BNB to USDT on BSC"

# Polygon
emblemai --agent --profile default -m "Use polygonSwapQuote to quote 10 POL to USDC on Polygon"
```

### Hedera Swaps
```bash
emblemai --agent --profile default -m "Use hederaTokensSwapQuote to get a quote for 100 HBAR to USDC, then use hederaTokensSwap to execute"
```

### Cross-Chain Bridge
```bash
emblemai --agent --profile default -m "Use getChangeNowSwapQuote to quote bridging 0.1 ETH to SOL"
emblemai --agent --profile default -m "Use getChangeNowSupportedCurrencies to show available bridge currencies"
```

---

## Communication Rules

**Always include these in swap requests:**
1. **Tool name** — specify the exact tool for reliable routing
2. **Amount** — dollar value or token quantity
3. **Source token** — what you're swapping from
4. **Target token** — what you're swapping to

| Bad | Good |
|-----|------|
| `"swap sol usdc"` | `"Use splBuyIntent to swap 5 SOL for USDC"` |
| `"buy eth"` | `"Use ethSwap to swap 100 USDC to ETH on Ethereum"` |
| `"bridge"` | `"Use getChangeNowSwapQuote to bridge 0.05 ETH to SOL"` |

---

## Safety

All swaps require explicit user confirmation (safe mode). The agent will:
1. Show you the swap details (amount, route, estimated output)
2. Wait for your approval before executing
3. Report the transaction result

Never bypasses confirmation for any value-moving operation.

---

## Helper Script

```bash
bash scripts/swap-helper.sh
```

See [scripts/swap-helper.sh](scripts/swap-helper.sh) for an interactive swap walkthrough.

---

## Links

- [Agent Wallet CLI](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [EmblemVault Docs — canonical](https://emblemvault.ai/docs)
- [EmblemVault Docs — interactive](https://emblemvault.dev)
