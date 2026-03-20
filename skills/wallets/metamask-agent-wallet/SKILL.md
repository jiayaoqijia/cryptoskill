---
name: MetaMask Agent Wallet
description: Control a sandboxed MetaMask browser extension wallet for autonomous blockchain transactions. Features configurable permission guardrails including spend limits, chain allowlists, protocol restrictions, and approval thresholds. MetaMask-only (other wallets not supported).
tags:
  - crypto
  - metamask
  - wallet
  - ethereum
  - defi
  - web3
  - blockchain
  - automation
  - browser
---

# MetaMask Agent Wallet Skill

Controls a sandboxed MetaMask wallet for autonomous blockchain transactions with configurable permission guardrails.

## Overview

This skill allows AI agents to interact with dapps and execute transactions through a dedicated MetaMask wallet. All operations are subject to user-defined constraints (spend limits, protocol allowlists, approval thresholds).

**Security Model:** The agent controls a *separate* wallet in an isolated browser profile. Never use your main wallet.

## Setup

### 1. Install Dependencies

```bash
cd metamask-agent-skill
npm install
npx playwright install chromium
```

### 2. Create Agent Wallet Profile

```bash
npm run setup
```

This will:
- Create a fresh Chrome profile at `~/.agent-wallet/chrome-profile`
- Install MetaMask extension
- Guide you through wallet creation (use a NEW seed phrase)

### 3. Fund the Wallet

Transfer a small amount to your agent wallet:
- ETH for gas (0.01-0.05 ETH recommended)
- Tokens for operations (start small, e.g., $50 USDC)

### 4. Configure Permissions

Edit `permissions.json` to set your constraints:

```json
{
  "constraints": {
    "spendLimit": {
      "daily": "50000000",    // $50 in 6-decimal format
      "perTx": "10000000"     // $10 max per transaction
    },
    "allowedChains": [1, 137, 42161],
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

**Example:** `connect https://app.uniswap.org`

### Execute Swap
```
swap <amount> <token-in> for <token-out> [on <dex>]
```
Executes a token swap on an allowed DEX.

**Example:** `swap 0.01 ETH for USDC on uniswap`

### Send Tokens
```
send <amount> <token> to <address>
```
Sends tokens to an address (within spend limits).

**Example:** `send 10 USDC to 0x1234...`

### Sign Message
```
sign <message>
```
Signs an arbitrary message. Use with caution.

### Check Balance
```
balance [token]
```
Returns wallet balances.

### View Transaction History
```
history [count]
```
Shows recent agent transactions with outcomes.

## Constraints

All operations check against `permissions.json` before execution:

| Constraint | Description |
|------------|-------------|
| `spendLimit.daily` | Max USD value per 24h period |
| `spendLimit.perTx` | Max USD value per transaction |
| `allowedChains` | Whitelisted chain IDs |
| `allowedProtocols` | Whitelisted contract addresses |
| `blockedMethods` | Forbidden function selectors |
| `requireApproval.above` | Threshold requiring user confirmation |

### Approval Flow

When a transaction exceeds `requireApproval.above`:
1. Agent pauses execution
2. Transaction details are logged
3. Agent reports: "Transaction requires approval: [details]"
4. User must explicitly approve before agent continues

## Safety

- **Isolated Profile:** Agent uses separate Chrome profile, never your main browser
- **Separate Wallet:** Agent wallet is completely separate from your main wallet  
- **Spend Caps:** Hard limits prevent runaway spending
- **Protocol Allowlist:** Only whitelisted contracts can be called
- **Full Logging:** Every transaction intent and outcome is logged
- **Revocation:** Set `"revoked": true` in permissions.json to disable all actions

## Logging

All transactions are logged to `~/.agent-wallet/logs/`:

```json
{
  "timestamp": 1706900000000,
  "action": "swap",
  "intent": { "to": "0x...", "value": "0", "data": "0x..." },
  "guardResult": { "allowed": true },
  "outcome": "confirmed",
  "txHash": "0x..."
}
```

Use `history` command to view recent transactions.

## Troubleshooting

### "Protocol not allowed"
Add the contract address to `allowedProtocols` in permissions.json.

### "Exceeds daily limit"
Wait 24h or increase `spendLimit.daily`.

### MetaMask popup not detected
Ensure the browser profile path is correct and MetaMask is installed.

### Transaction simulation failed
The dapp may be trying to call a blocked method or unsupported chain.

## Architecture

```
src/
├── index.ts          # Main entry point
├── browser.ts        # Playwright browser management
├── wallet.ts         # MetaMask interaction primitives
├── guard.ts          # Permission enforcement
├── logger.ts         # Transaction logging
├── price.ts          # USD price estimation
├── types.ts          # TypeScript types
└── config.ts         # Configuration loading
```

## Integration with Gator

When Gator accounts are available, permissions.json can be replaced with on-chain permission attestations. The guard will validate against Gator's permission registry instead of local config.
