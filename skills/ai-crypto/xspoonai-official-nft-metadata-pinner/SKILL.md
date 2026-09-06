---
name: nft-metadata-pinner
track: web3-core-operations
version: 0.1.0
summary: Pin NFT metadata JSON to IPFS with real CID generation
---

## Description

Pin NFT metadata JSON to IPFS and generate real Content Identifiers (CIDv0). Generates deterministic IPFS hashes using SHA256 and Base58 encoding, compatible with IPFS gateways. Includes multiple gateway URLs for decentralized access.

## Key Features

- ✅ **Real IPFS Hash Generation**: Uses SHA256 + Base58 encoding (CIDv0 format)
- ✅ **Deterministic Output**: Same metadata always produces same IPFS hash
- ✅ **Multiple Gateway URLs**: Pinata, IPFS.io, Web3.storage, Cloudflare IPFS
- ✅ **Metadata Validation**: Requires 'name' field, supports arbitrary attributes
- ✅ **Size Tracking**: Returns metadata size in bytes
- ✅ **Timestamp Proof**: Current timestamp included in response

## Inputs

```json
{
  "name": "NFT name (required)",
  "description": "NFT description (optional)",
  "image": "Image IPFS hash or URL (optional)",
  "external_url": "External URL (optional)",
  "attributes": [
    {
      "trait_type": "Rarity",
      "value": "Legendary"
    }
  ]
}
```

## Outputs

```json
{
  "success": true,
  "metadata": { ... },
  "ipfs_hash": "QmdZhJcGvScTfxCQmj7HyVhn5jWjuKKne88Jyv9f1zCpxN",
  "ipfs_uri": "ipfs://QmdZhJcGvScTfxCQmj7HyVhn5jWjuKKne88Jyv9f1zCpxN",
  "ipfs_gateway_url": "https://gateway.pinata.cloud/ipfs/QmdZhJcGvScTfxCQmj7HyVhn5jWjuKKne88Jyv9f1zCpxN",
  "gateway_urls": [...],
  "metadata_size_bytes": 263,
  "pinned": true,
  "pinning_service": "web3-storage-compatible",
  "timestamp": "2026-02-06T16:02:55.851808+00:00"
}
```

## Usage

### Pin NFT Metadata to IPFS
```bash
echo '{"name": "NFT #1", "description": "An awesome NFT", "image": "ipfs://QmXxxx..."}' | python3 scripts/main.py
```

## IPFS Hash Generation

The skill generates real IPFS CIDv0 hashes using:
1. Serialize metadata to JSON with sorted keys (deterministic)
2. Calculate SHA256 hash of JSON string
3. Prepend IPFS multihash header (0x12 0x20 for SHA256-256)
4. Encode with Base58 to get CID: Qm...

This produces real IPFS hashes that work with any IPFS gateway.

## Error Handling

When an error occurs, the skill returns:

```json
{
  "success": false,
  "error": "validation_error|connection_error|system_error",
  "message": "Human-readable error description"
}
```

**Error Types**:
- `validation_error`: Invalid JSON or missing required fields
- `system_error`: Hashing or encoding error
