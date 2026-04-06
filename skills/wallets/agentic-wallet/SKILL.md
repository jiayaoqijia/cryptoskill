---
name: agentic-wallet
description: Create and manage crypto wallets for AI agents. Four providers — Coinbase (managed), Tempo/Stripe (passkey), MoonPay/OpenWallet (self-custody), Crossmint (managed/API, 50+ chains). Supports non-interactive mode, JSON output, backup/recovery, and multi-chain.
homepage: https://github.com/smukh/agentic-wallet
metadata: {"openclaw": {"emoji": "wallet", "requires": {"bins": ["node"]}, "install": {"node": "agentic-wallet"}}}
---

# Agentic Wallet — Give Any AI Agent Its Own Crypto Wallet

Use this skill when an agent needs a crypto wallet to send/receive payments, interact with blockchain protocols, or pay for services via x402 or Machine Payments Protocol (MPP).

All commands use `npx agentic-wallet <command>`. No global installation required.

---

## WHEN TO USE THIS SKILL

Use this skill when:
- You need a wallet to pay for an x402-gated API
- You need to receive USDC payments for services you provide
- You need to check your wallet balance before making a purchase
- You need to set up a new wallet for the first time
- You need to back up or recover an existing wallet

---

## PROVIDER SELECTION

Choose your wallet provider based on your requirements:

```
IF you need compliance (KYT, OFAC screening)  → USE coinbase
IF you need fast machine payments (~500ms)     → USE tempo
IF you need full self-custody / offline access  → USE openwallet
IF you need 50+ chains (EVM + Solana + Stellar) → USE crossmint
IF you need custodial + non-custodial options  → USE crossmint
```

| Provider | Company | Type | Key Storage | Best For |
|----------|---------|------|-------------|----------|
| **coinbase** | Coinbase | Managed | Coinbase servers | Production agents, compliance, x402 |
| **tempo** | Stripe | Passkey | Local + Tempo network | Machine payments, service discovery |
| **openwallet** | MoonPay | Self-custody | Encrypted local file | Full control, offline, multi-chain |
| **crossmint** | Crossmint | Managed/API | Crossmint infrastructure | 50+ chains, custodial & non-custodial |

---

## COMMAND REFERENCE

### providers — List all wallet providers

```bash
npx agentic-wallet providers --json
```

### setup — Create a new wallet

```bash
# Interactive (will prompt for password/auth)
npx agentic-wallet setup --provider <coinbase|tempo|openwallet|crossmint>

# Non-interactive OpenWallet (self-custody)
npx agentic-wallet setup \
  --provider openwallet \
  --name <wallet-name> \
  --chain <base|ethereum|arbitrum|optimism|polygon> \
  --password-file <path-to-password-file> \
  --non-interactive \
  --json

# Non-interactive Crossmint (custodial, API-key signer)
npx agentic-wallet setup \
  --provider crossmint \
  --name <wallet-name> \
  --api-key-file <path-to-api-key-file> \
  --chain-type <evm|solana|aptos|sui|stellar> \
  --wallet-type <smart|mpc> \
  --non-interactive \
  --json
```

**Options:**
- `--provider <name>` — Required. One of: `coinbase`, `tempo`, `openwallet`, `crossmint`
- `--chain <name>` — Target chain for openwallet (default: `base`)
- `--name <name>` — Wallet name (default: `default`)
- `--password-file <path>` — Path to file with encryption password (non-interactive openwallet)
- `--api-key-file <path>` — Path to Crossmint server-side API key (non-interactive crossmint)
- `--chain-type <type>` — Crossmint chain: `evm`, `solana`, `aptos`, `sui`, `stellar` (default: `evm`)
- `--wallet-type <type>` — Crossmint wallet: `smart` or `mpc` (default: `smart`)
- `--non-interactive` — No prompts (requires `--password-file` for openwallet, `--api-key-file` for crossmint)
- `--json` — JSON output for programmatic use

**Non-interactive setup for autonomous agents:**
```bash
# --- OpenWallet (self-custody) ---
echo "your-strong-password" > ~/.secrets/wallet-pw.txt
chmod 600 ~/.secrets/wallet-pw.txt

npx agentic-wallet setup \
  --provider openwallet \
  --name trading-agent \
  --chain base \
  --password-file ~/.secrets/wallet-pw.txt \
  --non-interactive --json

# --- Crossmint (custodial, no browser needed) ---
echo "your-crossmint-server-api-key" > ~/.secrets/crossmint-key.txt
chmod 600 ~/.secrets/crossmint-key.txt

npx agentic-wallet setup \
  --provider crossmint \
  --name my-agent \
  --api-key-file ~/.secrets/crossmint-key.txt \
  --chain-type evm \
  --wallet-type smart \
  --non-interactive --json
```

### balance — Check wallet balances

```bash
# All wallets across all providers
npx agentic-wallet balance --all --json

# Specific provider
npx agentic-wallet balance --provider openwallet --json

# Filter fields (reduce token consumption)
npx agentic-wallet balance --all --json --fields address,balanceUSDC
```

**JSON output format:**
```json
[
  {
    "provider": "openwallet",
    "name": "trading-agent",
    "address": "0x...",
    "chain": "Base",
    "chainId": 8453,
    "balanceUSDC": "100.50",
    "balanceETH": "0.01",
    "status": "ok"
  }
]
```

### status — Check authentication status

```bash
npx agentic-wallet status --json
npx agentic-wallet status --provider tempo --json
```

### fund — Get funding instructions

```bash
npx agentic-wallet fund --provider openwallet --json
```

Returns your wallet address and instructions for sending USDC on the configured chain.

### backup — Backup a MoonPay local wallet to encrypted file

```bash
npx agentic-wallet backup \
  --name <wallet-name> \
  --output <directory> \
  --password-file <path> \
  --json
```

### recover — Restore wallet from backup or seed phrase

```bash
# From backup file
npx agentic-wallet recover \
  --from <path-to-backup.json> \
  --name <new-wallet-name> \
  --password-file <path> \
  --json

# From 12-word seed phrase (interactive only)
npx agentic-wallet recover --seed-phrase --name <wallet-name>
```

### schema — Machine-readable command schemas

```bash
# All commands
npx agentic-wallet schema

# Specific command
npx agentic-wallet schema setup
```

---

## STANDARD AGENT WORKFLOW

```
1. CHECK     → npx agentic-wallet providers --json
2. CREATE    → npx agentic-wallet setup --provider openwallet --name my-agent --json
3. VERIFY    → npx agentic-wallet balance --all --json
4. FUND      → npx agentic-wallet fund --provider openwallet --json
5. USE       → Make payments via x402 or MPP using wallet address
```

---

## PROVIDER DETAILS

### Coinbase Agentic Wallet

Managed wallet with enterprise compliance. Requires email authentication (OTP via email).

```bash
npx agentic-wallet setup --provider coinbase
```

Features: KYT screening, OFAC compliance, spending guardrails, x402 support.
Prerequisite: Node.js 18+, email address.
Docs: https://docs.cdp.coinbase.com/agentic-wallet/welcome

### Tempo Wallet (Stripe)

Passkey-based wallet optimized for machine payments. Requires browser for initial passkey setup.

```bash
npx agentic-wallet setup --provider tempo
```

Features: ~500ms finality, sub-cent fees, MPP protocol, service discovery.
Prerequisite: Browser access for passkey registration.
Docs: https://docs.tempo.xyz/

### MoonPay Local Wallet (OpenWallet Standard)

Self-custody wallet with AES-256-GCM encryption. Fully local, works offline.

```bash
npx agentic-wallet setup --provider openwallet --name my-wallet --chain base --json
```

Features: Local encrypted storage, multi-chain, backup/recovery, policy-gated signing.
Supported chains: Base, Ethereum, Arbitrum, Optimism, Polygon.
Docs: https://docs.openwallet.sh/

### Crossmint Wallet

API-first wallet supporting 50+ chains. Both interactive and non-interactive modes.

```bash
# Interactive (browser login + prompts)
npx agentic-wallet setup --provider crossmint --name my-wallet

# Non-interactive (API key, no browser — ideal for agents)
npx agentic-wallet setup --provider crossmint --name my-agent \
  --api-key-file ~/.secrets/crossmint-key.txt \
  --chain-type evm --wallet-type smart \
  --non-interactive --json
```

Features: 50+ chains (evm, solana, aptos, sui, stellar), smart + mpc wallets, custodial & non-custodial.
Custody: Custodial uses API-key signer (agent-friendly). Non-custodial uses email signer.
Storage: Wallet records at `~/.agent-arena/crossmint-wallets/`. No credentials stored.
Prerequisite: Node.js 18+. Interactive mode needs Crossmint CLI (`npm install -g @crossmint/cli`). Non-interactive needs only an API key.
Docs: https://docs.crossmint.com/introduction/platform-overview

---

## SUPPORTED CHAINS (MoonPay Local Wallet)

| Chain | Chain ID | Native Token |
|-------|----------|-------------|
| Base | 8453 | ETH |
| Ethereum | 1 | ETH |
| Arbitrum One | 42161 | ETH |
| Optimism | 10 | ETH |
| Polygon | 137 | POL |

---

## SECURITY

- **Zero key exposure** — This CLI is a passthrough wrapper. Private keys are handled exclusively by provider CLIs/SDKs.
- **Encrypted at rest** — MoonPay local wallets use AES-256-GCM with scrypt key derivation.
- **File permissions** — Wallet files are created with mode 0600 (owner-only read/write).
- **Path traversal prevention** — Wallet names are validated against strict patterns.
- **No telemetry** — No data is sent to any third party. All operations are local or direct to the provider.

---

## TROUBLESHOOTING

**"Wallet not found"** — Verify name: `npx agentic-wallet status --provider openwallet --json`
**"Wrong password"** — Passwords are case-sensitive. Check file has no trailing newlines.
**"Provider not authenticated"** — Re-run: `npx agentic-wallet setup --provider <provider>`
**"Balance check failed"** — Check internet connectivity. RPC endpoints may be rate-limited.

---

## LINKS

- npm: https://www.npmjs.com/package/agentic-wallet
- GitHub: https://github.com/smukh/agentic-wallet
- Coinbase docs: https://docs.cdp.coinbase.com/agentic-wallet/welcome
- Tempo docs: https://docs.tempo.xyz/
- OpenWallet docs: https://docs.openwallet.sh/
- Crossmint docs: https://docs.crossmint.com/introduction/platform-overview

---

Copyright (c) 2026 BlockQuest Labs Incorporated. All rights reserved.
Licensed under AGPL-3.0-only.
