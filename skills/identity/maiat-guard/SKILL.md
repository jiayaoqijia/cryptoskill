---
name: maiat-guard
description: Universal trust middleware for viem — auto-checks Maiat trust scores before every on-chain transaction. Drop-in wallet protection for AI agents. Blocks transactions to untrusted addresses.
version: 0.9.0
author: JhiNResH
tags:
  - wallet-protection
  - trust
  - viem
  - middleware
  - transaction-safety
  - base
homepage: https://github.com/JhiNResH/maiat-protocol/tree/master/packages/guard
triggers:
  - "protect my wallet"
  - "add trust checks to transactions"
  - "block untrusted transactions"
  - "guard agent wallet"
  - "viem trust middleware"
config:
  MAIAT_API_URL:
    description: "Maiat API endpoint (default: https://app.maiat.io)"
    default: "https://app.maiat.io"
---

# Maiat Guard — Wallet Trust Middleware

Drop-in viem middleware that auto-checks Maiat trust scores before every transaction your agent sends. If the recipient is untrusted, the transaction is blocked before signing.

## Use This When...

- "Protect my agent's wallet from scams"
- "Add trust verification before transactions"
- "Block sends to untrusted addresses"
- "Set up wallet guard for my agent"

## Installation

```bash
npm install @jhinresh/viem-guard
```

## Usage

```typescript
import { createWalletClient, http } from 'viem';
import { base } from 'viem/chains';
import { withMaiatGuard } from '@jhinresh/viem-guard';

// Wrap any viem wallet client
const client = withMaiatGuard(
  createWalletClient({
    chain: base,
    transport: http(),
  }),
  {
    threshold: 50,           // minimum trust score (0-100)
    blockUntrusted: true,    // block if score < threshold
    apiUrl: 'https://app.maiat.io',
  }
);

// Transactions are now auto-checked
// If recipient trust score < 50 → transaction blocked
await client.sendTransaction({ to: '0x...', value: 1000n });
```

## How It Works

1. Agent initiates a transaction via viem
2. Guard intercepts and queries `app.maiat.io/api/v1/agent/{address}/profile`
3. If `trustScore >= threshold` → transaction proceeds
4. If `trustScore < threshold` → transaction blocked, error thrown
5. If address has no score → configurable (block or allow)

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `threshold` | number | 50 | Minimum trust score to allow transaction |
| `blockUntrusted` | boolean | true | Block transactions to addresses below threshold |
| `blockUnknown` | boolean | false | Block transactions to addresses with no score |
| `apiUrl` | string | `https://app.maiat.io` | Maiat API endpoint |
| `onBlock` | function | - | Callback when transaction is blocked |

## Framework Plugins

Guard is also available as plugins for popular agent frameworks:

- **AgentKit**: `@jhinresh/agentkit-plugin`
- **ElizaOS**: `@jhinresh/elizaos-plugin`
- **GAME**: `@jhinresh/game-maiat-plugin`
- **Virtuals**: `@jhinresh/virtuals-plugin`
