---
name: WalletPilot
description: Universal browser wallet automation for AI agents. Supports 10 wallets including MetaMask, Rabby, Phantom, Trust Wallet, OKX, Coinbase, and more. EVM + Solana. Configurable guardrails with spend limits, chain allowlists, and approval thresholds.
tags:
  - crypto
  - wallet
  - ethereum
  - solana
  - defi
  - web3
  - blockchain
  - automation
  - browser
  - metamask
  - rabby
  - coinbase
  - rainbow
  - phantom
  - trust-wallet
  - zerion
  - exodus
  - okx
  - backpack
---

# WalletPilot

Universal browser wallet automation for AI agents. Control any browser-based crypto wallet with configurable permission guardrails.

## Supported Wallets

| Wallet | EVM | Solana | Users |
|--------|-----|--------|-------|
| MetaMask | ✅ | - | 100M+ |
| Rabby | ✅ | - | 1M+ |
| Coinbase Wallet | ✅ | - | 1M+ |
| Rainbow | ✅ | - | 500K+ |
| Phantom | ✅ | ✅ | 3M+ |
| Trust Wallet | ✅ | ✅ | 1M+ |
| Zerion | ✅ | ✅ | 100K+ |
| Exodus | ✅ | ✅ | 100K+ |
| OKX Wallet | ✅ | ✅ | 1M+ |
| Backpack | ✅ | ✅ | 500K+ |

## Overview

WalletPilot allows AI agents to interact with dapps and execute transactions through any supported browser wallet. All operations are subject to user-defined constraints.

**Security Model:** The agent controls a *separate* wallet in an isolated browser profile. Never use your main wallet.

## Setup

### 1. Install Dependencies

```bash
cd wallet-pilot
npm install
npx playwright install chromium
```

### 2. Configure Wallet Provider

Edit `config.json` to select your wallet:

```json
{
  "wallet": {
    "provider": "metamask",  // or: rabby, coinbase, rainbow, phantom
    "extensionPath": null    // auto-detect from Chrome, or provide path
  }
}
```

### 3. Create Agent Wallet Profile

```bash
npm run setup
```

This opens a browser where you:
- Install/setup your chosen wallet extension
- Create a NEW wallet (fresh seed phrase)
- The profile is saved for future automation

### 4. Fund the Wallet

Transfer a small amount to your agent wallet:
- Native token for gas (0.01-0.05 ETH/SOL recommended)
- Tokens for operations (start small, e.g., $50 USDC)

### 5. Configure Permissions

Edit `permissions.json`:

```json
{
  "constraints": {
    "spendLimit": {
      "daily": "50000000",
      "perTx": "10000000"
    },
    "allowedChains": [1, 137, 42161, 8453],
    "allowedProtocols": ["0x...uniswap", "0x...1inch"]
  }
}
```

## Available Actions

### Connect to Dapp
```
connect <dapp-url>
```
Navigates to dapp and connects the agent wallet.

### Execute Swap
```
swap <amount> <token-in> for <token-out> [on <dex>]
```
Executes a token swap on an allowed DEX.

### Send Tokens
```
send <amount> <token> to <address>
```
Sends tokens to an address (within spend limits).

### Sign Message
```
sign <message>
```
Signs an arbitrary message.

### Check Balance
```
balance [token]
```
Returns wallet balances.

### View History
```
history [count]
```
Shows recent agent transactions.

## Constraints

| Constraint | Description |
|------------|-------------|
| `spendLimit.daily` | Max USD value per 24h period |
| `spendLimit.perTx` | Max USD value per transaction |
| `allowedChains` | Whitelisted chain IDs |
| `allowedProtocols` | Whitelisted contract addresses |
| `blockedMethods` | Forbidden function selectors |
| `requireApproval.above` | Threshold requiring user confirmation |

## Adding New Wallets

WalletPilot uses a plugin architecture. To add a new wallet:

1. Create a new adapter in `src/wallets/`
2. Implement the `WalletAdapter` interface
3. Add selectors for the wallet's UI elements
4. Register in `src/wallets/index.ts`

See `src/wallets/metamask.ts` for reference implementation.

## Safety

- **Isolated Profile:** Agent uses separate browser profile
- **Separate Wallet:** Completely separate from your main wallet
- **Spend Caps:** Hard limits prevent runaway spending
- **Protocol Allowlist:** Only whitelisted contracts can be called
- **Full Logging:** Every transaction is logged
- **Revocation:** Set `"revoked": true` to disable all actions

## Architecture

```
src/
├── index.ts              # Main entry point
├── browser.ts            # Playwright browser management
├── guard.ts              # Permission enforcement
├── logger.ts             # Transaction logging
├── price.ts              # USD price estimation
├── types.ts              # TypeScript types
├── config.ts             # Configuration loading
└── wallets/
    ├── index.ts          # Wallet adapter registry
    ├── adapter.ts        # Base adapter interface
    ├── metamask.ts       # MetaMask
    ├── rabby.ts          # Rabby
    ├── coinbase.ts       # Coinbase Wallet
    ├── rainbow.ts        # Rainbow
    ├── phantom.ts        # Phantom
    ├── trust.ts          # Trust Wallet
    ├── zerion.ts         # Zerion
    ├── exodus.ts         # Exodus
    ├── okx.ts            # OKX Wallet
    └── backpack.ts       # Backpack
```

## Comparison: WalletPilot vs MetaMask-only

| Feature | WalletPilot | MetaMask Agent Wallet |
|---------|-------------|----------------------|
| Wallets | 5+ supported | MetaMask only |
| Chains | EVM + Solana | EVM only |
| Setup | Choose your wallet | MetaMask required |
| Complexity | Higher | Lower |
| Use case | Multi-wallet orgs | MM-only users |

Choose **WalletPilot** if you need flexibility across wallets or Solana support.
Choose **MetaMask Agent Wallet** for simpler MetaMask-only setup.
