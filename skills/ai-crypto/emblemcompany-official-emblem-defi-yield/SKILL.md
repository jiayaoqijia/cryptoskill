---
name: emblem-defi-yield
description: >
  DeFi yield research and liquid staking via EmblemAI. Discover yield opportunities,
  compare protocols, check DeFi positions with Nansen, and enter liquid staking via token swaps.
  Use when the user wants to research yields, find staking options, or review DeFi positions.
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

# Emblem DeFi Yield

DeFi yield research and liquid staking powered by **EmblemAI**. Research yield opportunities across protocols, review existing DeFi positions via Nansen, and enter liquid staking positions through token swaps on Solana, Ethereum, Base, BSC, Polygon, and Hedera.

**Requires**: `npm install -g @emblemvault/agentwallet`

---

## What This Skill Can Do

| Capability | How | Tools Used |
|-----------|-----|------------|
| Research yield opportunities | Ask about yields, APYs, protocols | LLM knowledge + `birdeyeTradeData`, `birdeyeTrendingTokens` |
| Review existing DeFi positions | Check LP, lending, staking, farming positions for any wallet | `nansen_defi_portfolio` |
| Liquid staking (Solana) | Swap SOL for LSTs (mSOL, JitoSOL, bSOL, jupSOL) | `splBuyIntent` |
| Token swaps for DeFi entry | Swap into DeFi tokens on any chain | `splBuyIntent`, `ethSwap`, `baseSwap`, `bscSwap`, `polygonSwap`, `hederaTokensSwap` |
| Protocol comparison | Compare yield strategies across DEXs | LLM knowledge + market data tools |
| Rug-pull checks | Verify token safety before entering positions | `rugcheck` |
| Smart money DeFi tracking | See what whales are farming | `nansen_smart_money_holdings`, `nansen_defi_portfolio` |

### Not Supported (Yet)

These features require direct LP pool management tools that are not currently available:

- Adding/removing liquidity to DEX pools
- Opening/closing concentrated liquidity (CLMM) positions
- Staking LP tokens
- Claiming farming rewards
- Pool APY rankings with live on-chain data

For these operations, use the DEX UIs directly (Raydium, Orca, Uniswap, etc.).

---

## Quick Start

```bash
npm install -g @emblemvault/agentwallet

# Research yield opportunities
emblemai --agent --profile default -m "What are the best yield farming opportunities on Solana right now?"

# Check DeFi positions for a wallet (uses nansen_defi_portfolio)
emblemai --agent --profile default -m "Use nansen_defi_portfolio to show DeFi positions for wallet 0x1234...abcd on ethereum"

# Enter liquid staking via swap
emblemai --agent --profile default -m "Swap 5 SOL for JitoSOL using splBuyIntent"
```

**Trigger phrases:**
- "Find yield opportunities"
- "What are the best APYs?"
- "Show DeFi positions for this wallet"
- "Swap SOL for JitoSOL"
- "What liquid staking options exist?"

---

## Supported Chains

| Chain | Swap Tool | Balances | Conditional Orders |
|-------|-----------|----------|--------------------|
| Solana | `splBuyIntent` | `solanaBalances` | Yes |
| Ethereum | `ethSwap` | `ethGetBalances` | Yes |
| Base | `baseSwap` | `baseGetBalances` | Yes |
| BSC | `bscSwap` | `bscGetBalances` | Yes |
| Polygon | `polygonSwap` | `polygonGetBalances` | Yes |
| Hedera | `hederaTokensSwap` | `hederaGetBalances` | Yes |

---

## Workflow: Research and Enter Yield

### Step 1: Research Opportunities
Ask about current yield landscape. The agent uses its knowledge plus live token data.
```bash
emblemai --agent --profile default -m "What are the best yield farming opportunities on Solana right now? Use birdeyeTrendingTokens to see what's hot."
```

### Step 2: Check a Wallet's DeFi Positions
Use Nansen to see existing LP, lending, staking, and farming positions.
```bash
emblemai --agent --profile default -m "Use nansen_defi_portfolio to check DeFi positions for wallet 0x1234...abcd on ethereum"
```

### Step 3: Verify Balances
Check what you have available before swapping.
```bash
emblemai --agent --profile default -m "Use solanaBalances to show my Solana balances"
```

### Step 4: Enter a Position via Swap
Swap into liquid staking tokens or DeFi tokens.
```bash
emblemai --agent --profile default -m "Use splBuyIntent to swap 5 SOL for JitoSOL"
```
Requires user confirmation in safe mode.

### Step 5: Verify
Confirm the swap executed.
```bash
emblemai --agent --profile default -m "Use solanaBalances to show my updated balances"
```

---

## DeFi Patterns

### Yield Research
```bash
emblemai --agent --profile default -m "What are the best yield farming opportunities on Solana? Include liquid staking, LP strategies, and lending protocols."
emblemai --agent --profile default -m "Compare Marinade (mSOL), Jito (JitoSOL), and BlazeStake (bSOL) for SOL liquid staking."
```

### DeFi Position Tracking (Nansen)
```bash
emblemai --agent --profile default -m "Use nansen_defi_portfolio to show DeFi positions for wallet 0xABC123 on ethereum"
emblemai --agent --profile default -m "Use nansen_defi_portfolio to check what DeFi protocols wallet 2J9Xrm...BL5WBJ is using on solana"
```

### Smart Money DeFi Analysis
```bash
emblemai --agent --profile default -m "Use nansen_smart_money_holdings to see what tokens smart money is holding on solana"
emblemai --agent --profile default -m "Use nansen_smart_money_trades to see recent smart money trades for JitoSOL"
```

### Liquid Staking (Solana)
```bash
emblemai --agent --profile default -m "Use splBuyIntent to swap 10 SOL for mSOL"
emblemai --agent --profile default -m "Use splBuyIntent to get a quote for swapping 5 SOL to JitoSOL"
```

### Safety Checks
```bash
emblemai --agent --profile default -m "Use rugcheck to verify token So11111111111111111111111111111111111111112"
```

### Protocol Comparison
```bash
emblemai --agent --profile default -m "Compare yields for SOL liquid staking across Marinade, Jito, BlazeStake, and Jupiter"
```

---

## Communication Tips

When asking about DeFi, be specific:
1. **Name the tool** — mention exact tool names for reliable execution
2. **Specify chain** — which blockchain
3. **Specify wallet** — for position lookups
4. **Specify tokens** — which tokens to swap

| Bad | Good |
|-----|------|
| `"show yield"` | `"What are the best yield opportunities on Solana? Include APYs and risks."` |
| `"check positions"` | `"Use nansen_defi_portfolio to show DeFi positions for wallet 0x123 on ethereum"` |
| `"stake SOL"` | `"Use splBuyIntent to swap 5 SOL for JitoSOL"` |

---

## Safety

All value-moving operations require user confirmation:
- Token swaps (entering liquid staking, DeFi tokens)
- Cross-chain bridges

Read-only operations execute immediately:
- Yield research
- DeFi position viewing (Nansen)
- Balance checks
- Rug-pull checks

---

## Helper Script

```bash
bash scripts/yield-scan.sh [chain]
```

Scans yield landscape for a chain. See [scripts/yield-scan.sh](scripts/yield-scan.sh).

---

## Links

- [Agent Wallet CLI](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [EmblemVault Docs — canonical](https://emblemvault.ai/docs)
- [EmblemVault Docs — interactive](https://emblemvault.dev)
