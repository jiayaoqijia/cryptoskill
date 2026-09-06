---
name: solana-toolkit
description: Comprehensive Solana blockchain interaction using Helius APIs and Jupiter. Create/manage wallets, check balances (SOL + tokens), send transactions, swap tokens via Jupiter, and monitor addresses.
version: 1.0.0
author: with-philia
license: MIT
tags: [Solana, Helius, Jupiter, Wallet, DeFi, Swap]
dependencies: [helius-sdk, @solana/web3.js, @jup-ag/core]
allowed-tools: TypeScript(scripts/*.ts)
---

# Solana Toolkit

A comprehensive toolkit for interacting with the Solana blockchain, leveraging Helius for RPC/API services and Jupiter for DeFi swaps.

## Prerequisites

1.  **Helius API Key**: Get free at [dashboard.helius.dev](https://dashboard.helius.dev/signup).
2.  **Configuration**: Store your key in `~/.config/solana-skill/config.json`:
    ```json
    {
      "heliusApiKey": "your-api-key",
      "network": "mainnet-beta"
    }
    ```

## Core Capabilities

### Wallet Management

- **Create/Import**: Generate new keypairs or import via private key/seed phrase.
- **Secure Storage**: Encrypted local storage for keys.
- **Balance Check**: View SOL and SPL token balances.

### Transactions

- **Send SOL/Tokens**: Transfer assets to any Solana address.
- **History**: View human-readable transaction history.
- **Priority Fees**: Automatic estimation for faster confirmation.

### DeFi (Jupiter)

- **Swap**: Exchange tokens with best price routing via Jupiter.
- **Quotes**: Get real-time price quotes and slippage data.

### Monitoring

- **Address Watch**: Monitor wallets for incoming/outgoing transactions.
- **Webhooks**: Set up notifications for specific events.

## Quick Reference

### Check Balance

```typescript
import { createHelius } from "helius-sdk";

const helius = createHelius({ apiKey: "YOUR_KEY" });
const assets = await helius.getAssetsByOwner({
  ownerAddress: "WALLET_ADDRESS",
  displayOptions: {
    showFungible: true,
    showNativeBalance: true,
  },
});
```

### Send SOL

```typescript
import {
  Connection,
  SystemProgram,
  Transaction,
  sendAndConfirmTransaction,
  LAMPORTS_PER_SOL,
} from "@solana/web3.js";

const connection = new Connection(
  "https://mainnet.helius-rpc.com/?api-key=YOUR_KEY",
);
const tx = new Transaction().add(
  SystemProgram.transfer({
    fromPubkey: sender.publicKey,
    toPubkey: recipientPubkey,
    lamports: amount * LAMPORTS_PER_SOL,
  }),
);
await sendAndConfirmTransaction(connection, tx, [sender]);
```

### Jupiter Swap

```typescript
// 1. Get quote
const quote = await fetch(
  `https://quote-api.jup.ag/v6/quote?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}`,
);

// 2. Build swap transaction
const swap = await fetch("https://quote-api.jup.ag/v6/swap", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    quoteResponse: await quote.json(),
    userPublicKey: wallet.publicKey.toString(),
  }),
});

// 3. Sign and send
```

## API Endpoints

| Service           | Base URL                                      |
| :---------------- | :-------------------------------------------- |
| **Helius RPC**    | `https://mainnet.helius-rpc.com/?api-key=KEY` |
| **Jupiter Quote** | `https://quote-api.jup.ag/v6/quote`           |
| **Jupiter Swap**  | `https://quote-api.jup.ag/v6/swap`            |

## Security Best Practices

- **Never log private keys**: Ensure logs are sanitized.
- **Validate addresses**: Check for valid Solana addresses before sending.
- **Slippage**: Set reasonable slippage limits (default 0.5% - 1%).
- **Simulation**: Simulate transactions before sending to catch errors early.

## References

- [Helius API Documentation](references/helius-api.md)
- [Jupiter Swap Integration](references/jupiter.md)
- [Security Guidelines](references/security.md)
