---
name: hedera-tx-builder
description: Build and sign Hedera transactions. Use for: (1) Creating HBAR transfers, (2) Token operations, (3) Smart contract calls, (4) Submitting to Hedera network.
---

# Hedera Transaction Builder

## Setup

```bash
npm install @hashgraph/sdk
```

## Client Setup

```typescript
import { Client, AccountBalanceQuery, Hbar } from '@hashgraph/sdk';

const client = Client.forMainnet();
// Or for testnet:
const client = Client.forTestnet();
```

## Transfer HBAR

```typescript
import { TransferTransaction, Hbar } from '@hashgraph/sdk';

const tx = new TransferTransaction()
  .addHbarTransfer(fromAccountId, new Hbar(-100)) // send
  .addHbarTransfer(toAccountId, new Hbar(100))    // receive
  .setTransactionMemo("Payment for goods");

// Sign with hashpack or operator
const signTx = await tx.sign(operatorKey);
const result = await signTx.execute(client);
```

## Key Transaction Types

### AccountCreate
```typescript
new AccountCreateTransaction()
  .setKey(publicKey)
  .setInitialBalance(new Hbar(10))
  .setAccountMemo("My account");
```

### TokenAssociate
```typescript
new TokenAssociateTransaction()
  .setAccountId(accountId)
  .setTokenIds([tokenId1, tokenId2]);
```

### TopicMessage
```typescript
new TopicMessageTransaction()
  .setTopicId(topicId)
  .setMessage("Hello Hedera!");
```

## Network Endpoints

- **Mainnet**: `https://mainnet.hashio.io/api`
- **Testnet**: `https://testnet.hashio.io/api`

## Important Concepts

- **Hbar**: 1 HBAR = 100,000,000 tinybars
- **Account ID**: Format `shard.realm.num` (e.g., `0.0.12345`)
- **Transaction Fee**: Small HBAR fee for each transaction
- **Transaction Valid Duration**: 180 seconds by default
