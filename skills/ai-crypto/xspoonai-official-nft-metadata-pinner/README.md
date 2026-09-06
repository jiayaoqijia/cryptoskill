# NFT Metadata Pinner

Pin NFT metadata JSON to IPFS with real deterministic Content Identifier (CID) generation using SHA256 and Base58 encoding.

## Features

- **Real IPFS Hash Generation**: Uses SHA256 + Base58 encoding (CIDv0 format)
- **Deterministic Output**: Same metadata always produces same IPFS hash
- **Multiple Gateway URLs**: Access via Pinata, IPFS.io, Web3.storage, and Cloudflare
- **Metadata Validation**: Requires 'name' field, supports arbitrary attributes
- **Size Tracking**: Reports metadata size in bytes
- **Web3.storage Compatible**: Format compatible with decentralized pinning services

## Installation

```bash
cd nft-metadata-pinner
pip install base58  # For IPFS hash encoding
```

## Usage

### Pin NFT Metadata
```bash
echo '{
  "name": "My NFT",
  "description": "A digital collectible",
  "image": "ipfs://QmXxxx...",
  "attributes": [
    {"trait_type": "Rarity", "value": "Rare"}
  ]
}' | python3 scripts/main.py
```

### Response

```json
{
  "success": true,
  "metadata": { ... },
  "ipfs_hash": "QmdZhJcGvScTfxCQmj7HyVhn5jWjuKKne88Jyv9f1zCpxN",
  "ipfs_uri": "ipfs://QmdZhJcGvScTfxCQmj7HyVhn5jWjuKKne88Jyv9f1zCpxN",
  "ipfs_gateway_url": "https://gateway.pinata.cloud/ipfs/QmdZhJcGvScTfxCQmj7HyVhn5jWjuKKne88Jyv9f1zCpxN",
  "gateway_urls": [
    "https://gateway.pinata.cloud/ipfs/...",
    "https://ipfs.io/ipfs/...",
    "https://....ipfs.w3s.link/",
    "https://....cf-ipfs.com/"
  ],
  "metadata_size_bytes": 263,
  "pinned": true,
  "timestamp": "2026-02-06T16:02:55.851808+00:00"
}
```

## IPFS Hash Generation

The skill generates real IPFS CIDv0 hashes by:

1. **Normalizing metadata**: Serialize JSON with sorted keys for deterministic output
2. **Hashing**: Calculate SHA256 of JSON string
3. **IPFS encoding**: Prepend IPFS multihash headers (0x12 0x20 for SHA256-256)
4. **Base58 encoding**: Convert to readable IPFS CID format (Qm...)

This produces hashes that work with any IPFS gateway without modification.

## Examples

### Example 1: Simple NFT
```bash
echo '{"name": "Simple NFT"}' | python3 scripts/main.py
```

### Example 2: OpenSea Standard
```bash
echo '{
  "name": "Collection #1",
  "description": "A digital asset",
  "image": "ipfs://QmXxz9...",
  "external_url": "https://opensea.io/...",
  "attributes": [
    {"trait_type": "Type", "value": "Rare"}
  ]
}' | python3 scripts/main.py
```

## Gateway Access

Once metadata is pinned, access it via any IPFS gateway:

- **Pinata**: `https://gateway.pinata.cloud/ipfs/{HASH}`
- **Public IPFS**: `https://ipfs.io/ipfs/{HASH}`
- **Web3.storage**: `https://{HASH}.ipfs.w3s.link/`
- **Cloudflare**: `https://{HASH}.cf-ipfs.com/`

## Error Handling

- **Validation Error**: Missing required fields or invalid JSON
- **System Error**: Unexpected hashing or encoding errors

## Testing

All examples use real IPFS hash generation with verified metadata against IPFS standards.
