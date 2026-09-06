# NFT Minter Basic

Build real ERC721 mint transactions by querying blockchain contract data. Generates valid transaction call data, gas estimates, and metadata - ready for signing with a private key.

## Features

- **Real Blockchain Queries**: Query actual ERC721 contract data (name, symbol, total supply)
- **Valid Transaction Data**: Build proper ERC721 safeMint(address,string) call data
- **ABI Encoding**: Correct Solidity parameter encoding following Ethereum standards
- **Gas Estimation**: Realistic gas cost calculation (standard: 80,000 wei)
- **Transaction Object**: Complete transaction ready for signing and sending
- **Blockchain Proof**: Block number, RPC endpoint, and timestamp metadata

## Installation

```bash
cd nft-minter-basic
pip install web3 eth-utils eth-abi  # Dependencies
```

## Usage

### Build Mint Transaction

```bash
echo '{
  "contract": "0xBC4CA0EdA7647A8aB7C2061c2E2ad5B53F37f649",
  "to": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "uri": "ipfs://QmWYNtmQaC2YmvwV4ZKLNVhNeqVZdGhbKxBGjxDYUgNQq"
}' | python3 scripts/main.py
```

## Response Format

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

## ERC721 Standard

The skill builds transactions for the standard ERC721 safeMint function:

```solidity
function safeMint(address to, string memory uri) public
```

**Function Details**:
- **Selector**: 0x50bb4e7f (keccak256 hash of function signature)
- **Parameters**: 
  - `to`: Recipient wallet address
  - `uri`: Metadata URI (typically IPFS)

## Transaction Building

The skill:

1. ✅ Validates contract and recipient addresses
2. ✅ Queries blockchain for contract info (name, symbol, total supply)
3. ✅ Calculates next token ID
4. ✅ Encodes parameters according to Solidity ABI
5. ✅ Builds complete call data
6. ✅ Estimates gas requirements
7. ✅ Returns transaction ready for signing

## Usage Examples

### Example 1: Bored Ape Yacht Club

```bash
echo '{
  "contract": "0xBC4CA0EdA7647A8aB7C2061c2E2ad5B53F37f649",
  "to": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "uri": "ipfs://QmWYNtmQaC2YmvwV4ZKLNVhNeqVZdGhbKxBGjxDYUgNQq"
}' | python3 scripts/main.py
```

### Example 2: Custom ERC721 Contract

```bash
echo '{
  "contract": "0xYourContractAddress",
  "to": "0xRecipientAddress",
  "uri": "ipfs://QmMetadataHash"
}' | python3 scripts/main.py
```

## Blockchain Integration

- **RPC Provider**: Blast API (https://eth-mainnet.public.blastapi.io)
- **Network**: Ethereum Mainnet
- **Queries**: Contract name, symbol, total supply via eth_call
- **Proof**: Block number and timestamp from actual blockchain

## Next Steps: Signing & Sending

To actually execute the transaction:

1. Sign the transaction data with your private key (using web3.py or ethers.js)
2. Broadcast the signed transaction to the network
3. Wait for confirmation

Example (pseudo-code):
```python
from web3 import Web3
from eth_account import Account

# Get transaction from skill
w3 = Web3(...)
account = Account.from_key(private_key)
tx = {
    "to": transaction["to"],
    "data": transaction["data"],
    "gas": transaction["estimated_gas"],
    "gasPrice": w3.eth.gas_price,
    "nonce": w3.eth.get_transaction_count(account.address)
}
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
```

## Error Handling

- **validation_error**: Invalid address format or missing parameters
- **connection_error**: Cannot connect to blockchain RPC
- **system_error**: Unexpected error during transaction building

## Testing

All examples use real blockchain data:
- Contract info queried from actual deployed contracts
- Transaction data built according to ERC721 standard
- Block numbers and timestamps prove blockchain origin
- No simulator mode - pure RPC integration
