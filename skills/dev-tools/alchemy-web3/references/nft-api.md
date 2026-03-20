# NFT API Reference

Full documentation for Alchemy's NFT API endpoints.

## Base URL
```
https://{chain}.g.alchemy.com/nft/v3/{apiKey}
```

## Endpoints

### getNFTsForOwner
Get all NFTs owned by an address.

```bash
GET /getNFTsForOwner?owner={address}&pageSize={n}
```

**Parameters:**
- `owner` (required): Wallet address or ENS name
- `pageSize`: Number of NFTs per page (max 100)
- `pageKey`: Pagination cursor
- `contractAddresses[]`: Filter by specific contracts
- `excludeFilters[]`: Exclude spam, airdrops
- `includeFilters[]`: Include specific types
- `orderBy`: Sort order

**Response:**
```json
{
  "ownedNfts": [{
    "contract": { "address": "0x...", "name": "CryptoPunks" },
    "tokenId": "1234",
    "tokenType": "ERC721",
    "name": "CryptoPunk #1234",
    "description": "...",
    "image": { "originalUrl": "https://..." }
  }],
  "totalCount": 150,
  "pageKey": "..."
}
```

### getNFTMetadata
Get metadata for a specific NFT.

```bash
GET /getNFTMetadata?contractAddress={contract}&tokenId={id}
```

**Parameters:**
- `contractAddress` (required): NFT contract address
- `tokenId` (required): Token ID
- `refreshCache`: Force refresh metadata

### getNFTsForContract
Get all NFTs in a collection.

```bash
GET /getNFTsForContract?contractAddress={contract}&limit={n}
```

### getOwnersForNFT
Get all owners of a specific NFT (for ERC-1155).

```bash
GET /getOwnersForNFT?contractAddress={contract}&tokenId={id}
```

### getOwnersForContract
Get all owners in a collection.

```bash
GET /getOwnersForContract?contractAddress={contract}
```

### getContractMetadata
Get collection-level metadata.

```bash
GET /getContractMetadata?contractAddress={contract}
```

### getFloorPrice
Get floor price for a collection.

```bash
GET /getFloorPrice?contractAddress={contract}
```

### getNFTSales
Get recent sales for NFTs.

```bash
GET /getNFTSales?contractAddress={contract}&tokenId={id}
```

### computeRarity
Compute rarity scores for NFT attributes.

```bash
GET /computeRarity?contractAddress={contract}&tokenId={id}
```

## Spam Detection

Alchemy automatically detects spam NFTs. Use filters:

```bash
# Exclude spam
?excludeFilters[]=SPAM

# Exclude airdrops
?excludeFilters[]=AIRDROPS
```

## Supported Chains

NFT API is available on:
- Ethereum (mainnet, sepolia)
- Polygon (mainnet, amoy)
- Arbitrum (mainnet, sepolia)
- Optimism (mainnet, sepolia)
- Base (mainnet, sepolia)
- And more...
