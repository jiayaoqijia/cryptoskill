---
name: emblem-portfolio-tracker
description: >
  Track crypto portfolio across 7 blockchains via EmblemAI. Aggregated balances with USD values,
  conditional trade P&L, and DeFi position tracking via Nansen. Use when the user wants to check
  their portfolio, see balances across chains, or review trade positions.
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

# Emblem Portfolio Tracker

Cross-chain crypto portfolio monitoring powered by **EmblemAI**. Aggregated balances with USD values across Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin. Conditional trade P&L tracking and DeFi position viewing via Nansen.

**Requires**: `npm install -g @emblemvault/agentwallet`

---

## What This Skill Can Do

| Capability | Tools Used |
|-----------|------------|
| Wallet addresses (all chains) | `wallet` |
| Solana balances + USD values | `solanaBalances` |
| Ethereum balances + USD values | `ethGetBalances` |
| Base balances + USD values | `baseGetBalances` |
| BSC balances + USD values | `bscGetBalances` |
| Polygon balances + USD values | `polygonGetBalances` |
| Hedera balances | `hederaGetBalances` |
| Bitcoin balances | `getBTCBalances` |
| Crypto price lookup | `getCryptoPrice` |
| Conditional trade positions & P&L | `getAllPositions`, `listPositions` |
| DeFi positions (LP, staking, farming) | `nansen_defi_portfolio` |

### Not Supported

These features have no backing tools:

- Transaction history — no tool returns past wallet transactions on any chain
- Tax reporting / transaction exports — no historical transaction data available
- Unrealized P&L on held tokens — only realized P&L from conditional trade positions
- 24h portfolio change — no historical balance snapshots; only current balances
- Portfolio allocation percentages — agent must compute from individual chain balance calls

---

## Quick Start

```bash
npm install -g @emblemvault/agentwallet

# Check balances across all chains
emblemai --agent --profile default -m "Use wallet to show my addresses, then use solanaBalances, ethGetBalances, baseGetBalances, bscGetBalances, polygonGetBalances, hederaGetBalances, and getBTCBalances to show all my balances"

# Check trade positions
emblemai --agent --profile default -m "Use getAllPositions to show my open and closed trade positions with P&L"
```

**Trigger phrases:**
- "Check my portfolio"
- "Show balances across all chains"
- "What's my P&L?"
- "Show my trade positions"

---

## Workflow: Full Portfolio Review

### Step 1: Wallet Addresses
```bash
emblemai --agent --profile default -m "Use wallet to list all my wallet addresses across every chain"
```

### Step 2: Balance Snapshot
Check each chain. Name the tools explicitly for reliable execution.
```bash
emblemai --agent --profile default -m "Use solanaBalances to show my Solana tokens with USD values"
emblemai --agent --profile default -m "Use ethGetBalances to show my Ethereum tokens with USD values"
emblemai --agent --profile default -m "Use baseGetBalances to show my Base tokens"
emblemai --agent --profile default -m "Use bscGetBalances to show my BSC tokens"
emblemai --agent --profile default -m "Use polygonGetBalances to show my Polygon tokens"
emblemai --agent --profile default -m "Use hederaGetBalances to show my Hedera tokens"
emblemai --agent --profile default -m "Use getBTCBalances to show my Bitcoin balance"
```

Or ask for all at once:
```bash
emblemai --agent --profile default -m "Show my balances across all chains with USD values. Use the balance tools for each chain: solanaBalances, ethGetBalances, baseGetBalances, bscGetBalances, polygonGetBalances, hederaGetBalances, getBTCBalances"
```

### Step 3: Trade Positions & P&L
```bash
emblemai --agent --profile default -m "Use getAllPositions to show my conditional trade positions with realized P&L"
```

Note: P&L data only covers conditional trade positions (limit orders, stop-losses, take-profits) created through EmblemAI. General wallet holdings do not have cost basis tracking.

### Step 4: DeFi Positions (Optional)
For wallets indexed by Nansen (typically high-value wallets):
```bash
emblemai --agent --profile default -m "Use nansen_defi_portfolio to check DeFi positions for wallet [ADDRESS] on [CHAIN]"
```

---

## Use Cases

### Daily Check-In
```bash
emblemai --agent --profile default -m "Quick portfolio check — use solanaBalances, ethGetBalances, and getBTCBalances to show my main holdings"
```

### Chain-Specific Deep Dive
```bash
emblemai --agent --profile default -m "Use solanaBalances to show all my Solana token balances with current prices"
emblemai --agent --profile default -m "Use ethGetBalances to show my Ethereum positions"
```

### Trade Performance
```bash
emblemai --agent --profile default -m "Use getAllPositions to show my closed positions with realized P&L and win/loss rate"
```

### Price Check
```bash
emblemai --agent --profile default -m "Use getCryptoPrice to show current prices for BTC, ETH, SOL, and BNB"
```

---

## Communication Tips

Name the exact tools for reliable execution:

| Bad | Good |
|-----|------|
| `"balances"` | `"Use solanaBalances and ethGetBalances to show my balances"` |
| `"PnL"` | `"Use getAllPositions to show my trade positions with realized P&L"` |
| `"portfolio"` | `"Use wallet to show addresses, then check balances on each chain"` |

---

## Helper Script

```bash
bash scripts/portfolio-report.sh
```

See [scripts/portfolio-report.sh](scripts/portfolio-report.sh) for a ready-to-use portfolio report.

---

## Links

- [Agent Wallet CLI](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [EmblemVault Docs — canonical](https://emblemvault.ai/docs)
- [EmblemVault Docs — interactive](https://emblemvault.dev)
