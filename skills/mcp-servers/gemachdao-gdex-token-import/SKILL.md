---
name: gdex-token-import
description: Import user-defined custom tokens so they appear in token details, balances, and portfolio across the platform
---

# GDEX: Token Import

Register a user-defined custom token so it is recognised by the backend's
token-details, balances, and portfolio endpoints. Useful for long-tail tokens
that are not yet indexed.

## When to Use

- A user wants to see a brand-new (or otherwise un-indexed) token in their
  portfolio or token-search results
- Pre-registering a token before launch so trading UI can resolve metadata

## Prerequisites

- `@gemachdao/gdex-skill` installed
- Authenticated via shared API key or wallet sign-in — see
  **gdex-authentication**
- The token's on-chain address (contract address on EVM, mint address on
  Solana, object id on Sui)

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/v1/import_token` | Register a user-imported custom token |

## SDK Usage

```typescript
import { GdexSkill, buildImportTokenComputedData } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(process.env.GDEX_API_KEY!);

// Structured shape — SDK builds computedData internally
await skill.importToken({
  tokenAddress: '0xCustomToken',
  chainId: 8453,
  managed: {
    apiKey: process.env.GDEX_API_KEY!,
    walletAddress: '0xWallet',
    sessionPrivateKey: '0x…',
    userId: '0xWallet',
  },
});

// Or raw shape — caller pre-built computedData
await skill.importToken({
  computedData: buildImportTokenComputedData({
    apiKey: process.env.GDEX_API_KEY!,
    walletAddress: '0xWallet',
    sessionPrivateKey: '0x…',
    userId: '0xWallet',
    tokenAddress: '0xCustomToken',
    chainId: '8453',
  }),
  chainId: 8453,
});
```

## Notes

- `import_token` uses managed-custody **encrypted `computedData`**:
  ABI `['import_token', [tokenAddress, chainId, nonce]]`,
  sig message `import_token-${userId}-${data}`.
- The backend deduplicates imports per `(userId, chain, tokenAddress)`.
- After import, queries such as `getTokenDetails`, `getBalances`, and
  `getPortfolio` will start returning data for the token (subject to
  indexer latency).
