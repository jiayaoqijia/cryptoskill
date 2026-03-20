---
name: xrpl-tx-builder
description: Build and sign XRP Ledger transactions. Use for: (1) Creating payment transactions, (2) Building NFT mint/burn transactions, (3) Signing with Xaman wallet, (4) Submitting to XRPL.
---

# XRPL Transaction Builder

## Setup

```bash
npm install xrpl
```

## Basic Payment

```typescript
import { Client, Wallet, Payment } from 'xrpl';

const client = new Client('wss://xrplcluster.com');

// Build payment tx
const tx: Payment = {
  TransactionType: 'Payment',
  Account: wallet.address,
  Destination: 'rDestinationAddress...',
  Amount: '1000000', // drops (1 XRP = 1,000,000 drops)
  DestinationTag: 12345 // optional
};
```

## Submit Transaction (Xaman Signed)

```typescript
// After user signs with Xaman, submit:
const txBlob = signedTransactionBlob; // from Xaman payload
const result = await client.submit(txBlob);
```

## Common Transaction Types

### Payment
```typescript
{
  TransactionType: 'Payment',
  Account: 'r...',
  Destination: 'r...',
  Amount: '1000000', // drops
  DestinationTag: 123
}
```

### NFTokenMint
```typescript
{
  TransactionType: 'NFTokenMint',
  Account: 'r...',
  NFTokenTaxon: 0,
  Issuer: 'r...',
  TransferFee: 5000, // 5% royalty
  Flags: 8, // burnable
  URI: 'ipfs://...'
}
```

### SetAccountRoot
```typescript
{
  TransactionType: 'SetAccountRoot',
  Account: 'r...',
  EmailHash: 'abc123...',
  Domain: 'example.com'
}
```

## Key Concepts

- **Drops**: 1 XRP = 1,000,000 drops
- **Address**: Classic r-address (starts with 'r')
- **Destination Tag**: Optional memo for payments
- **Flags**: Transaction-specific options (see XRPL docs)

## RPC Endpoints

- `wss://xrplcluster.com` (public)
- `wss://s1.ripple.com` (Ripple)
