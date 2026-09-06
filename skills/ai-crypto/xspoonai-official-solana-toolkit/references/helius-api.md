# Helius API Reference

Complete reference for Helius Solana APIs.

## Authentication

All requests require API key:

```
https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY
```

Or via header:

```
Authorization: Bearer YOUR_API_KEY
```

## Rate Limits (Free Tier)

| Endpoint Type   | Limit  |
| --------------- | ------ |
| RPC requests    | 10/sec |
| DAS requests    | 2/sec  |
| sendTransaction | 1/sec  |

## DAS API (Digital Asset Standard)

### getAssetsByOwner

Get all assets (tokens, NFTs) owned by an address.

```typescript
const response = await fetch(RPC_URL, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    id: "req-1",
    method: "getAssetsByOwner",
    params: {
      ownerAddress: "ADDRESS",
      page: 1,
      limit: 1000,
      displayOptions: {
        showFungible: true, // Include SPL tokens
        showNativeBalance: true, // Include SOL balance
        showInscription: true, // Include inscriptions
      },
    },
  }),
});
```

**Response includes:**

- `items[]` — Array of assets
- `nativeBalance` — SOL balance in lamports
- `total` — Total asset count

### getAsset

Get single asset by ID (mint address).

```typescript
params: {
  id: "MINT_ADDRESS";
}
```

### getAssetBatch

Get up to 1000 assets in one request.

```typescript
params: {
  ids: ['MINT_1', 'MINT_2', ...]
}
```

### getTokenAccounts

Get token accounts for a mint or owner.

```typescript
// By owner
params: {
  owner: 'WALLET_ADDRESS',
  page: 1,
  limit: 100
}

// By mint
params: {
  mint: 'TOKEN_MINT',
  page: 1,
  limit: 100
}
```

### searchAssets

Advanced asset search with filters.

```typescript
params: {
  ownerAddress: 'ADDRESS',
  grouping: ['collection', 'COLLECTION_ADDRESS'],
  burnt: false,
  limit: 100
}
```

## Enhanced Transactions API

### getTransactions

Convert raw transactions to human-readable format.

```typescript
const response = await fetch("https://api.helius.xyz/v0/transactions", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    transactions: ["SIGNATURE_1", "SIGNATURE_2"],
  }),
});
```

**Response includes:**

- `type` — Transaction type (TRANSFER, SWAP, NFT_SALE, etc.)
- `source` — Source program (JUPITER, MAGIC_EDEN, etc.)
- `fee` — Transaction fee
- `nativeTransfers[]` — SOL transfers
- `tokenTransfers[]` — Token transfers

### getTransactionsByAddress

Get transaction history for an address.

```typescript
const response = await fetch(
  `https://api.helius.xyz/v0/addresses/${ADDRESS}/transactions?api-key=${KEY}`,
);
```

## Priority Fee API

### getPriorityFeeEstimate

Get recommended priority fees.

```typescript
const response = await fetch(RPC_URL, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    id: "fee-1",
    method: "getPriorityFeeEstimate",
    params: [
      {
        accountKeys: ["PROGRAM_ID", "OTHER_ACCOUNTS"],
        options: {
          priorityLevel: "Medium", // Low, Medium, High, VeryHigh
        },
      },
    ],
  }),
});
```

**Priority levels:**

- `Low` — 25th percentile
- `Medium` — 50th percentile (recommended)
- `High` — 75th percentile
- `VeryHigh` — 95th percentile

## Helius Sender

Ultra-low latency transaction submission. Free, no credits consumed.

**Endpoints:**

- Global: `https://sender.helius-rpc.com/fast`
- Regional (lower latency):
  - `http://slc-sender.helius-rpc.com/fast` (Salt Lake City)
  - `http://ewr-sender.helius-rpc.com/fast` (Newark)
  - `http://fra-sender.helius-rpc.com/fast` (Frankfurt)
  - `http://tyo-sender.helius-rpc.com/fast` (Tokyo)

**Requirements:**

- `skipPreflight: true` (mandatory)
- Include Jito tip (min 0.0002 SOL)
- Include priority fee

**Tip accounts (pick random):**

```
4ACfpUFoaSD9bfPdeu6DBt89gB6ENTeHBXCAi87NhDEE
D2L6yPZ2FmmmTKPgzaMKdhu6EWZcTpLy1Vhx8uvZe7NZ
9bnz4RShgq1hAnLnZbP8kbgBg1kEmcJBYQq3gQbmnSta
5VY91ws6B2hMmBFRsXkoAAdsPHBJwRfBht4DXox3xkwn
```

## Webhooks

Monitor addresses or programs for activity.

### Create Webhook

```typescript
await helius.webhooks.createWebhook({
  webhookURL: "https://your-endpoint.com/webhook",
  transactionTypes: ["TRANSFER", "SWAP"],
  accountAddresses: ["ADDRESS_TO_MONITOR"],
  webhookType: "enhanced",
});
```

**Transaction types:**

- `TRANSFER` — SOL/token transfers
- `SWAP` — DEX swaps
- `NFT_SALE` — NFT sales
- `NFT_LISTING` — NFT listings
- `ANY` — All transactions

## SDK Usage

```typescript
import { createHelius } from 'helius-sdk';

const helius = createHelius({ apiKey: 'YOUR_KEY' });

// DAS
const assets = await helius.getAssetsByOwner({ ownerAddress: 'ADDR' });

// Enhanced transactions
const txs = await helius.enhanced.getTransactions(['SIG1', 'SIG2']);

// Smart transaction (handles fees, retries)
const sig = await helius.tx.sendSmartTransaction({
  instructions: [...],
  signers: [keypair]
});

// Webhooks
const webhook = await helius.webhooks.createWebhook({...});
```
