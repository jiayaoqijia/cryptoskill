---
name: hedera-token-mint
description: Create and manage tokens on Hedera (HTS). Use for: (1) Minting fungible tokens, (2) Creating NFTs (HTS), (3) Setting up token supplies, (4) Configuring token permissions.
---

# Hedera Token Minting (HTS)

## Setup

```bash
npm install @hashgraph/sdk
```

## Create Fungible Token

```typescript
import { 
  TokenCreateTransaction, 
  TokenSupplyType,
  TokenType 
} from '@hashgraph/sdk';

const tx = await new TokenCreateTransaction()
  .setTokenName("My Token")
  .setTokenSymbol("MTK")
  .setTokenType(TokenType.FungibleCommon)
  .setSupplyType(TokenSupplyType.Infinite)
  .setDecimals(2)
  .setInitialSupply(1000000) // Total supply = 1,000,000
  .setTreasuryAccountId(treasuryId)
  .setAdminKey(adminKey)
  .setSupplyKey(supplyKey)
  .freezeWith(client)
  .sign(treasuryKey);

const result = await tx.execute(client);
const tokenId = result.receipt.tokenId;
```

## Create NFT Collection

```typescript
const tx = await new TokenCreateTransaction()
  .setTokenName("My NFT Collection")
  .setTokenSymbol("MNFT")
  .setTokenType(TokenType.NonFungibleUnique)
  .setTreasuryAccountId(treasuryId)
  .setAdminKey(adminKey)
  .setSupplyKey(supplyKey)
  .freezeWith(client)
  .sign(treasuryKey);
```

## Mint NFTs

```typescript
import { TokenMintTransaction } from '@hashgraph/sdk';

const tx = await new TokenMintTransaction()
  .setTokenId(tokenId)
  .addMetadata(Buffer.from("NFT #1 metadata"))
  .addMetadata(Buffer.from("NFT #2 metadata"))
  .freezeWith(client)
  .sign(supplyKey);

const result = await tx.execute(client);
```

## Token Operations

### Transfer Token
```typescript
import { TransferTransaction } from '@hashgraph/sdk';

await new TransferTransaction()
  .addTokenTransfer(tokenId, fromAccount, -10)
  .addTokenTransfer(tokenId, toAccount, 10)
  .execute(client);
```

### Burn Tokens
```typescript
import { TokenBurnTransaction } from '@hashgraph/sdk';

await new TokenBurnTransaction()
  .setTokenId(tokenId)
  .setAmount(100)
  .execute(client);
```

## Key Points

- **Supply Types**: `Infinite` or `Finite`
- **Token Types**: `FungibleCommon` or `NonFungibleUnique`
- **Royalty**: Use custom fees for NFT royalties
- **Token ID Format**: `0.0.12345`
