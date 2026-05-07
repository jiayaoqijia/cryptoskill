---
name: aibtc-bitcoin-wallet
description: Bitcoin L1 wallet for agents - check balances, send BTC, manage UTXOs. Extends to Stacks L2 (STX, DeFi) and Pillar smart wallets (sBTC yield).
license: MIT
metadata:
  author: aibtcdev
  version: 1.51.0 # x-release-please-version
  npm: "@aibtc/mcp-server"
  github: https://github.com/aibtcdev/aibtc-mcp-server
---

# AIBTC Bitcoin Wallet

A skill for managing Bitcoin L1 wallets with optional Pillar smart wallet and Stacks L2 DeFi capabilities.

## Install

One-command installation:

```bash
npx @aibtc/mcp-server@latest --install
```

For testnet:

```bash
npx @aibtc/mcp-server@latest --install --testnet
```

## Quick Start

### Check Balance

Get your Bitcoin balance:

```
"What's my BTC balance?"
```

Uses `get_btc_balance` - returns total, confirmed, and unconfirmed balances.

### Check Fees

Get current network fee estimates:

```
"What are the current Bitcoin fees?"
```

Uses `get_btc_fees` - returns fast (~10 min), medium (~30 min), and slow (~1 hr) rates in sat/vB.

### Send BTC

Transfer Bitcoin to an address:

```
"Send 50000 sats to bc1q..."
"Transfer 0.001 BTC with fast fees to bc1q..."
```

Uses `transfer_btc` - requires an unlocked wallet.

## Wallet Setup

Before sending transactions, set up a wallet:

1. **Create new wallet**: `wallet_create` - generates encrypted BIP39 mnemonic
2. **Import existing**: `wallet_import` - import from mnemonic phrase
3. **Unlock for use**: `wallet_unlock` - required before transactions

Wallets are stored encrypted at `~/.aibtc/`.

## Tool Reference

### Read Operations

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_btc_balance` | Get BTC balance | `address` (optional; requires unlocked wallet if omitted) |
| `get_btc_fees` | Get fee estimates | None |
| `get_btc_utxos` | List UTXOs | `address` (optional; requires unlocked wallet if omitted), `confirmedOnly` |

### Write Operations (Wallet Required)

| Tool | Description | Parameters |
|------|-------------|------------|
| `transfer_btc` | Send BTC | `recipient`, `amount` (sats), `feeRate` |

### Wallet Management

| Tool | Description |
|------|-------------|
| `wallet_create` | Generate new encrypted wallet |
| `wallet_import` | Import wallet from mnemonic |
| `wallet_unlock` | Unlock wallet for transactions |
| `wallet_lock` | Lock wallet (clear from memory) |
| `wallet_list` | List available wallets |
| `wallet_switch` | Switch active wallet |
| `wallet_status` | Get wallet/session status |

### Message Signing

| Tool | Description | Parameters |
|------|-------------|------------|
| `sip018_sign` | Sign structured Clarity data (SIP-018) | `message`, `domain` |
| `sip018_verify` | Verify SIP-018 signature and recover signer | `messageHash`, `signature`, `expectedSigner` (optional) |
| `sip018_hash` | Compute SIP-018 hash without signing | `message`, `domain` |
| `stacks_sign_message` | Sign plain text with Stacks prefix (SIWS-compatible) | `message` |
| `stacks_verify_message` | Verify Stacks message signature and recover signer | `message`, `signature`, `expectedSigner` (optional) |
| `btc_sign_message` | Sign plain text with Bitcoin key (BIP-137/BIP-322) | `message`, `addressType` (optional) |
| `btc_verify_message` | Verify Bitcoin message signature (auto-detects BIP-137/BIP-322) | `message`, `signature`, `address` (optional) |
| `nostr_sign_event` | Sign a Nostr event (NIP-01) with BIP-340 Schnorr using NIP-06 derived key by default (m/44'/1237'/0'/0/0) | `kind`, `content`, `tags` (optional), `created_at` (optional), `keySource` (`"nostr"` default via NIP-06 path, `"taproot"` for P2TR key, `"segwit"` for P2WPKH key) |
| `schnorr_sign_digest` | Sign a raw 32-byte digest with Schnorr/BIP-340 | `digest`, `confirmBlindSign`, `auxRand` (optional) |
| `schnorr_verify_digest` | Verify a BIP-340 Schnorr signature over a digest | `digest`, `signature`, `publicKey` |

## Units and Addresses

**Amounts**: Always in satoshis (1 BTC = 100,000,000 satoshis)

**Addresses**:
- Mainnet: `bc1...` (native SegWit)
- Testnet: `tb1...`

**Fee Rates**: `"fast"`, `"medium"`, `"slow"`, or custom sat/vB number

## Example Workflows

### Daily Balance Check

```
1. "What's my BTC balance?"
2. "Show my recent UTXOs"
3. "What are current fees?"
```

### Send Payment

```
1. "Unlock my wallet" (provide password)
2. "Send 100000 sats to bc1qxyz... with medium fees"
3. "Lock my wallet"
```

### Multi-Wallet Management

```
1. "List my wallets"
2. "Switch to trading wallet"
3. "Unlock it"
4. "Check balance"
```

## Progressive Layers

This skill focuses on Bitcoin L1. Additional capabilities are organized by layer:

### Stacks L2 (Layer 2)

Bitcoin L2 with smart contracts and DeFi:
- STX token transfers
- ALEX DEX token swaps
- Zest Protocol lending/borrowing
- x402 paid API endpoints (AI, storage, utilities) — safe-by-default with probe-before-pay workflow

See: [references/stacks-defi.md](references/stacks-defi.md)

### Pillar Smart Wallet (Layer 3)

sBTC smart wallet with yield automation:
- Passkey or agent-signed transactions
- Send to BNS names (alice.btc)
- Auto-boost yield via Zest Protocol

See: [references/pillar-wallet.md](references/pillar-wallet.md)

### Bitcoin Inscriptions

Inscribe and retrieve digital artifacts on Bitcoin:
- Commit-reveal inscription workflow
- Get inscription content and metadata
- Protect ordinal UTXOs from accidental spending

See: [references/inscription-workflow.md](references/inscription-workflow.md)

### x402 Paid APIs

Pay-per-use APIs with automatic micropayments on Stacks L2:
- Discover available endpoints with `list_x402_endpoints`
- Check cost before paying with `probe_x402_endpoint`
- Execute endpoints with `execute_x402_endpoint` (safe-by-default — probes first)
- Send inbox messages with `send_inbox_message` (use this instead of execute_x402_endpoint for inbox)
- Build new x402 APIs with `scaffold_x402_endpoint` and `scaffold_x402_ai_endpoint`

Always probe before executing paid endpoints. Never call `execute_x402_endpoint` with `autoApprove: true` without checking cost first.

**send_inbox_message** — dedicated tool for aibtc.com inbox messages:
- Parameters: `recipientBtcAddress` (bc1...), `recipientStxAddress` (SP...), `content` (max 500 chars), `paymentTxid` (optional)
- Uses sponsored transactions: sender pays only the sBTC message cost, relay covers STX gas
- Avoids sBTC settlement timeout issues that affect the generic execute_x402_endpoint tool
- Implements the full 5-step x402 v2 payment flow with balance pre-check
- **paymentTxid** (optional): provide a confirmed on-chain sBTC transfer txid to skip the x402 flow and deliver the message using that txid as payment proof — use for manual recovery when a settlement timeout left the sBTC payment confirmed on-chain but the message undelivered
- **Automatic recovery**: if retries are exhausted, the tool checks whether any submitted payment txid confirmed on-chain and, if so, resubmits the message automatically — no agent action required

See: [references/stacks-defi.md](references/stacks-defi.md) for endpoint catalog
See: [references/x402-inbox.md](references/x402-inbox.md) for inbox-specific flow details

### Genesis Lifecycle

Agent identity and reputation on Bitcoin and Stacks:
- L0: Local agent key generation
- L1: Dual-chain plain-message signatures (btc_sign_message + stacks_sign_message)
- L2: X claim + BTC airdrop activation
- L3: On-chain identity registration via ERC-8004 (register_identity)
- L4: Reputation bootstrapping (get_reputation, give_feedback)
- Active: 5-minute check-ins to maintain reputation and liveness

See: [references/genesis-lifecycle.md](references/genesis-lifecycle.md)

## Troubleshooting

### "Wallet not unlocked"

Run `wallet_unlock` with your password before sending transactions.

### "Insufficient balance"

Check `get_btc_balance` - you need enough BTC for amount + fees.

### "Invalid address"

Ensure address matches network:
- Mainnet: starts with `bc1`
- Testnet: starts with `tb1`

See: [references/troubleshooting.md](references/troubleshooting.md)

## More Information

- [CLAUDE.md](../CLAUDE.md) - Full tool documentation
- [GitHub](https://github.com/aibtcdev/aibtc-mcp-server) - Source code
- [npm](https://www.npmjs.com/package/@aibtc/mcp-server) - Package

---

*This skill follows the [Agent Skills](https://agentskills.io) open specification.*
