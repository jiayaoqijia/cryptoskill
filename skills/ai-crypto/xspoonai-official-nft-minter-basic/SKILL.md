---
name: nft-minter-basic
track: web3-core-operations
version: 0.1.0
summary: Build Real ERC721 Mint Transactions from Blockchain Data
---

## Description

Build real ERC721 mint transactions by querying blockchain contract data. Generates valid transaction call data with proper ABI encoding, gas estimation, and metadata. Transactions are fully built but not signed/sent - requires private key for blockchain execution.

## Key Features

- ✅ **Real Blockchain Queries**: Query actual ERC721 contract data from chain
- ✅ **Valid Transaction Data**: Build proper safeMint(address,string) call data
- ✅ **ABI Encoding**: Correct Solidity parameter encoding for transactions
- ✅ **Gas Estimation**: Realistic gas cost calculation (standard: 80,000 wei)
- ✅ **Contract Info**: Fetch contract name, symbol, and next token ID
- ✅ **Transaction Details**: Full transaction object ready for signing
- ✅ **Blockchain Metadata**: Block number, RPC endpoint, and timestamp proof

## Inputs

```json
{
  "contract": "0x... (ERC721 contract address)",
  "to": "0x... (recipient address)",
  "uri": "ipfs://... (metadata URI)"
}
```

## Outputs

```json
{
  "success": true,
  "contract": "0xBC4CA0EdA7647A8aB7C2061c2E2ad5B53F37f649",
  "contract_name": "BoredApeYachtClub",
  "contract_symbol": "BAYC",
  "next_token_id": 10000,
  "recipient": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "uri": "ipfs://QmWYNtmQaC2YmvwV4ZKLNVhNeqVZdGhbKxBGjxDYUgNQq",
  "transaction": {
    "from": "0x0000000000000000000000000000000000000000",
    "to": "0xBC4CA0EdA7647A8aB7C2061c2E2ad5B53F37f649",
    "function": "safeMint(address,string)",
    "function_selector": "0x50bb4e7f",
    "parameters": {...},
    "data": "0x50bb4e7f...",
    "estimated_gas": 80000,
    "gas_price_gwei": 50,
    "total_estimated_cost_eth": 0.004
  },
  "block_number": 24398887,
  "rpc_used": "https://eth-mainnet.public.blastapi.io",
  "timestamp": "2026-02-06T16:10:08.712885+00:00"
}
```

## Usage

### Build NFT Mint Transaction
```bash
echo '{
  "contract": "0xBC4CA0EdA7647A8aB7C2061c2E2ad5B53F37f649",
  "to": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "uri": "ipfs://QmWYNtmQaC2YmvwV4ZKLNVhNeqVZdGhbKxBGjxDYUgNQq"
}' | python3 scripts/main.py
```

## ERC721 Standard Implementation

The skill builds transactions for the standard ERC721 safeMint function:

```solidity
function safeMint(address to, string memory uri) public
```

**Function Selector**: `0x50bb4e7f` (keccak256 of function signature)

**Parameters**:
- `to`: Recipient address (32 bytes)
- `uri`: Metadata URI string (variable length, padded to 32-byte boundary)

## Transaction Building Process

1. **Contract Validation**: Verify contract address is valid Ethereum address
2. **Recipient Validation**: Verify recipient address is valid
3. **Contract Queries**: Fetch name, symbol, total supply from blockchain
4. **Token ID**: Calculate next token ID as totalSupply + 1
5. **ABI Encoding**: Encode parameters according to Solidity ABI spec
6. **Call Data**: Build complete transaction call data
7. **Gas Estimation**: Calculate realistic gas requirements
8. **Metadata**: Include block number and timestamp as proof of real data

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
- `validation_error`: Invalid address format or missing fields
- `connection_error`: Cannot connect to blockchain RPC
- `system_error`: Unexpected error during transaction building
