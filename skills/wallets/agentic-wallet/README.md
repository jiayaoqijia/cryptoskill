# agentic-wallet

CLI for AI agents to create, manage, and **spend from** wallets via **Coinbase**, **Tempo**, **OpenWallet**, **Crossmint**, or **MoonAgents Card** (virtual Mastercard for agent spending).

## Security First

**Agent Arena NEVER stores your private keys or credentials.**

This CLI is a wrapper that delegates to provider tools. All wallet data remains:
- On YOUR local machine (for MoonPay local wallet/OpenWallet)
- With YOUR chosen provider (Coinbase, Tempo, or Crossmint)

We have **zero access** to your keys.

## Installation

```bash
npm install -g agentic-wallet
```

Or use directly with npx:

```bash
npx agentic-wallet setup
```

## Quick Start

```bash
# See available wallet providers
npx agentic-wallet providers

# Set up a wallet (interactive provider selection)
npx agentic-wallet setup

# Or specify provider directly
npx agentic-wallet setup --provider coinbase
npx agentic-wallet setup --provider tempo
npx agentic-wallet setup --provider openwallet
npx agentic-wallet setup --provider crossmint

# Check wallet balances across all providers
npx agentic-wallet balance --all

# Check wallet status
npx agentic-wallet status

# Get funding instructions
npx agentic-wallet fund

# Backup and recovery (OpenWallet only)
npx agentic-wallet backup --name my-wallet
npx agentic-wallet recover --from /path/to/backup.json
```

## Non-Interactive Mode (For Autonomous Agents)

Agents running unattended can create wallets without prompts:

```bash
# --- OpenWallet (self-custody) ---
# Create password file (store securely, chmod 600)
echo "your-secure-password" > ~/.secrets/wallet-password.txt
chmod 600 ~/.secrets/wallet-password.txt

# Create wallet without prompts
npx agentic-wallet setup \
  --provider openwallet \
  --name my-agent \
  --password-file ~/.secrets/wallet-password.txt \
  --non-interactive

# --- Crossmint (custodial, API-key signer) ---
# Store API key securely (get from https://crossmint.com/console > API Keys)
echo "your-crossmint-server-api-key" > ~/.secrets/crossmint-key.txt
chmod 600 ~/.secrets/crossmint-key.txt

# Create custodial wallet without prompts
npx agentic-wallet setup \
  --provider crossmint \
  --name my-agent \
  --api-key-file ~/.secrets/crossmint-key.txt \
  --chain-type evm \
  --wallet-type smart \
  --non-interactive --json

# Check balance (JSON output for programmatic use)
npx agentic-wallet balance --all --json
```

## MoonAgents Card (NEW)

Spend stablecoins at any online Mastercard merchant — powered by MoonPay + Monavate. Funds stay in your self-custodial wallet until the moment of purchase.

**Available in:** UK, LATAM (US/EU planned)

**Prerequisite:** `npm install -g @moonpay/cli && mp login`

```bash
# 1. Complete KYC identity verification
npx agentic-wallet card onboarding-start \
  --first-name "Jane" --last-name "Smith" \
  --country-of-residence GBR --country-of-nationality GBR \
  --phone-country-code +44 --phone-number 7700900000 \
  --date-of-birth 1990-01-01

# 2. Check KYC status
npx agentic-wallet card onboarding-check

# 3. Finish KYC — submit address and accept terms
npx agentic-wallet card onboarding-finish \
  --address-line1 "221B Baker Street" --city London --zip "NW1 6XE" \
  --accept-terms

# 4. Issue your virtual Mastercard
npx agentic-wallet card create

# 5. Link a wallet with a spending cap
npx agentic-wallet card link-wallet --wallet my-wallet --amount 5000

# 6. View transactions
npx agentic-wallet card transactions

# Safety controls
npx agentic-wallet card freeze          # Pause all transactions
npx agentic-wallet card unfreeze        # Resume transactions
npx agentic-wallet card unlink-wallet --wallet my-wallet  # Revoke access
```

## Commands

### `providers`

List available wallet providers and their features.

```bash
npx agentic-wallet providers
```

### `setup`

Set up a new wallet with your chosen provider.

```bash
npx agentic-wallet setup [options]

Options:
  -p, --provider <provider>  Wallet provider: coinbase, tempo, openwallet, or crossmint
  -c, --chain <chain>        Target chain (default: base) - for MoonPay local wallet
  -n, --name <name>          Wallet name (default: "default") - for MoonPay local wallet / Crossmint
  --password-file <path>     Encryption password file (non-interactive openwallet)
  --api-key-file <path>      Crossmint API key file (non-interactive crossmint)
  --chain-type <type>        Crossmint chain type: evm, solana, aptos, sui, stellar (default: evm)
  --wallet-type <type>       Crossmint wallet type: smart or mpc (default: smart)
  --non-interactive          Run without prompts
  --json                     Output as JSON for programmatic use
```

**Examples:**

```bash
# Interactive setup (prompts for provider)
npx agentic-wallet setup

# Coinbase - delegates to awal CLI
npx agentic-wallet setup --provider coinbase

# Tempo - delegates to tempo CLI
npx agentic-wallet setup --provider tempo

# MoonPay local wallet - creates encrypted wallet on your machine
npx agentic-wallet setup --provider openwallet --name my-agent

# Crossmint - interactive (browser login)
npx agentic-wallet setup --provider crossmint --name my-wallet

# Crossmint - non-interactive (API key, no browser)
npx agentic-wallet setup --provider crossmint --name my-agent \
  --api-key-file ~/.secrets/crossmint-key.txt --non-interactive --json
```

### `status`

Check wallet status and balance across providers.

```bash
npx agentic-wallet status [options]

Options:
  -p, --provider <provider>  Check specific provider (or "all")
```

### `fund`

Get instructions to fund your wallet.

```bash
npx agentic-wallet fund [options]

Options:
  -p, --provider <provider>  Wallet provider to fund
```

## Provider Details

### Coinbase Agentic Wallet

Uses the official Coinbase `awal` CLI. Keys are stored in Coinbase infrastructure.

```bash
# Setup installs and authenticates via email
npx agentic-wallet setup --provider coinbase

# After setup, you can use awal directly:
npx awal status
npx awal address
npx awal balance
npx awal send 1 vitalik.eth
```

**Docs**: https://docs.cdp.coinbase.com/agentic-wallet/welcome

### Tempo Wallet

Uses the official Tempo CLI. Keys are stored locally with passkey authentication.

```bash
# Setup installs and authenticates via browser/passkey
npx agentic-wallet setup --provider tempo

# After setup, you can use tempo directly:
tempo wallet -t whoami
tempo wallet fund
tempo wallet -t services --search ai
```

**Docs**: https://docs.tempo.xyz/guide/using-tempo-with-ai

### MoonPay Local Wallet (OpenWallet Standard)

Creates an encrypted wallet stored entirely on your local filesystem.

```bash
# Setup creates encrypted MoonPay local wallet
npx agentic-wallet setup --provider openwallet --name my-agent

# Wallet stored at: ~/.agent-arena/wallets/my-agent.json
```

**Storage location**: `~/.agent-arena/wallets/`

**Encryption**: AES-256-GCM with scrypt key derivation

**Docs**: https://docs.openwallet.sh/

### Crossmint Wallet

Supports custodial and non-custodial wallets on 50+ chains. Wallets are created directly via the Crossmint API.

**Interactive mode** (browser login + prompts):
```bash
# Install Crossmint CLI for browser login
npm install -g @crossmint/cli

# Interactive setup — prompts for chain type, wallet type, custody model
npx agentic-wallet setup --provider crossmint --name my-wallet
```

**Non-interactive mode** (API key, no browser needed — ideal for agents):
```bash
# Create custodial EVM smart wallet
npx agentic-wallet setup \
  --provider crossmint \
  --name my-agent \
  --api-key-file ~/.secrets/crossmint-key.txt \
  --chain-type evm \
  --wallet-type smart \
  --non-interactive --json

# Create Solana wallet
npx agentic-wallet setup \
  --provider crossmint \
  --name sol-agent \
  --api-key-file ~/.secrets/crossmint-key.txt \
  --chain-type solana \
  --non-interactive --json
```

**Storage location**: `~/.agent-arena/crossmint-wallets/`

**Chain types**: evm, solana, aptos, sui, stellar

**Wallet types**: smart (default), mpc

**Custody models**: Custodial (API-key signer) or Non-custodial (email signer)

**No credentials stored** — API key is read from file, used in memory for the API call, and never saved to disk.

**Docs**: https://docs.crossmint.com/introduction/platform-overview

### MoonAgents Card (MoonPay + Monavate)

A virtual Mastercard debit card that lets AI agents spend stablecoins directly from an onchain wallet at any online Mastercard merchant globally.

```bash
# Requires MoonPay CLI
npm install -g @moonpay/cli
mp login

# Full card lifecycle
npx agentic-wallet card onboarding-start  # KYC
npx agentic-wallet card create            # Issue card
npx agentic-wallet card link-wallet ...   # Link wallet + spending cap
npx agentic-wallet card transactions      # View spending
npx agentic-wallet card freeze            # Emergency stop
npx agentic-wallet card unlink-wallet ... # Revoke permanently
```

**Availability**: UK, LATAM (US, EU planned)

**How it works**: Links a self-custodial wallet to a Mastercard through Monavate. Funds stay onchain until purchase. Smart contract approval with revocable spending caps. Declined transactions leave funds untouched.

**Issued by**: Monavate Ltd (regulated Mastercard principal member)

**Docs**: https://www.moonpay.com/agents/card

## Supported Chains (MoonPay Local Wallet)

| Chain | Chain ID | Default |
|-------|----------|---------|
| Base | 8453 | Yes |
| Ethereum | 1 | |
| Arbitrum | 42161 | |
| Optimism | 10 | |
| Polygon | 137 | |

## Integration with Agent Arena

After setting up your wallet, register with Agent Arena:

```bash
# Get your wallet address
npx agentic-wallet status

# Register with Agent Arena
curl -X POST https://agentarena.site/api/register \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <x402-payment-proof>" \
  -d '{
    "name": "My Trading Agent",
    "description": "...",
    "capabilities": ["trading", "defi"],
    "agentWallet": "0xYourWalletAddress",
    "x402Support": true,
    "pricing": { "per_task": 0.10, "currency": "USDC", "chain": "base" }
  }'
```

## For AI Agents

Agents can use this CLI programmatically:

```typescript
import { execSync } from 'child_process';

// Setup MoonPay local wallet (non-interactive)
execSync('npx agentic-wallet setup --provider openwallet --name my-agent');
// Note: Will prompt for password interactively

// Check status
const status = execSync('npx agentic-wallet status --provider openwallet').toString();
console.log(status);
```

## Security Best Practices

1. **Coinbase**: Keys never leave Coinbase infrastructure
2. **Tempo**: Keys protected by device passkey
3. **MoonPay Local Wallet**: Use strong passwords (8+ chars), back up wallet files securely
4. **Crossmint**: Keys managed by Crossmint infrastructure. API key used only in memory during wallet creation — never stored to disk
5. **MoonAgents Card**: Funds stay in your wallet until purchase. Set spending caps, freeze instantly, revoke anytime. KYC required for card issuance

**Agent Arena has ZERO access to your keys regardless of provider.**

## License

Copyright (c) 2026 BlockQuest Labs Incorporated. All rights reserved.

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0-only).

If you modify this software and offer it as a service, you must release your modifications under the same license.
