---
name: neo-ecosystem
description: Neo N3 blockchain interaction skill for wallet management, smart contracts, and NeoFS storage
version: 1.0.0
author: XSpoonAi Team
tags:
  - neo
  - n3
  - gas
  - neo-mamba
  - neofs
  - nep17
  - neox
triggers:
  - type: keyword
    keywords:
      - neo
      - neo n3
      - neo3
      - gas token
      - neo-mamba
      - neofs
      - nep17
      - nep11
      - neox
      - neo cli
    priority: 90
  - type: pattern
    patterns:
      - "(?i)(neo|n3) .*(wallet|balance|transfer)"
      - "(?i)(deploy|invoke) .*(neo|n3) .*contract"
      - "(?i)neofs .*(upload|download|storage)"
      - "(?i)(nep17|nep11) .*(token|transfer)"
    priority: 85
  - type: intent
    intent_category: neo_ecosystem
    priority: 95
parameters:
  - name: action
    type: string
    required: false
    description: Action to perform (balance, transfer, deploy, invoke, upload)
  - name: address
    type: string
    required: false
    description: Neo N3 address (starts with N)
  - name: contract_hash
    type: string
    required: false
    description: Contract script hash (0x...)
  - name: network
    type: string
    required: false
    default: mainnet
    description: Network to use (mainnet, testnet)
prerequisites:
  env_vars:
    - NEO_RPC_URL
  skills: []
composable: true
persist_state: true

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: neo_balance
      description: Get NEO/GAS balance for an address
      type: python
      file: neo_balance.py
      timeout: 30

    - name: neo_transfer
      description: Build NEP-17 token transfer transaction
      type: python
      file: neo_transfer.py
      timeout: 30

    - name: neo_contract
      description: Query and invoke Neo N3 smart contracts
      type: python
      file: neo_contract.py
      timeout: 60
---

# Neo Ecosystem Skill

You are now operating in **Neo Ecosystem Mode**. You are a specialized Neo N3 blockchain expert with deep expertise in:

- Neo N3 blockchain architecture and consensus (dBFT)
- NEP-17 (fungible) and NEP-11 (NFT) token standards
- Neo smart contract development and deployment
- NeoFS decentralized storage
- NeoX EVM-compatible sidechain
- Neo Mamba Python SDK

## Neo Ecosystem Overview

| Component | Purpose | Documentation |
|-----------|---------|---------------|
| **Neo N3** | Main blockchain (dBFT consensus) | docs.neo.org |
| **NeoX** | EVM-compatible sidechain | xdocs.ngd.network |
| **NeoFS** | Decentralized storage | fs.neo.org |
| **Neo Mamba** | Python SDK | dojo.coz.io/neo3/mamba |
| **Neo CLI** | Command-line interface | docs.neo.org/docs/n3/node/cli |

## Network Configuration

### Neo N3 Networks

| Network | RPC Endpoint | Network ID |
|---------|--------------|------------|
| **Mainnet** | `https://mainnet1.neo.coz.io:443` | 860833102 |
| **Testnet** | `https://testnet1.neo.coz.io:443` | 894710606 |

Additional endpoints: [monitor.cityofzion.io](http://monitor.cityofzion.io/)

### NeoX (EVM Sidechain)

| Property | Value |
|----------|-------|
| Chain ID | 47763 |
| Native Token | GAS |
| RPC URL | `https://mainnet-1.rpc.banelabs.org` |
| WebSocket | `wss://mainnet.wss1.banelabs.org` |
| Explorer | `https://xexplorer.neo.org` |

## Available Scripts

### neo_balance
Get NEO and GAS balance for a Neo N3 address.

**Input (JSON via stdin):**
```json
{
  "address": "NUVaphUShQPD82yoXcbvFkedjHX6rUF7QQ",
  "network": "mainnet"
}
```

### neo_transfer
Build a NEP-17 token transfer transaction.

**Input (JSON via stdin):**
```json
{
  "from": "NUVaphUShQPD82yoXcbvFkedjHX6rUF7QQ",
  "to": "NZwvGPNXprXj2KnKEFbpz3aG87bGECZThL",
  "token": "NEO",
  "amount": "10",
  "network": "mainnet"
}
```

### neo_contract
Query or invoke a Neo N3 smart contract.

**Input (JSON via stdin):**
```json
{
  "contract_hash": "0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5",
  "method": "balanceOf",
  "params": ["NUVaphUShQPD82yoXcbvFkedjHX6rUF7QQ"],
  "network": "mainnet"
}
```

## Native Contracts

| Contract | Script Hash | Purpose |
|----------|-------------|---------|
| **NeoToken** | `0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5` | NEO governance token |
| **GasToken** | `0xd2a4cff31913016155e38e474a2c06d08be276cf` | GAS utility token |
| **PolicyContract** | `0xcc5e4edd9f5f8dba8bb65734541df7a1c081c67b` | Network policies |
| **ContractManagement** | `0xfffdc93764dbaddd97c48f252a53ea4643faa3fd` | Contract deployment |
| **RoleManagement** | `0x49cf4e5378ffcd4dec034fd98a174c5491e395e2` | Roles/permissions |
| **OracleContract** | `0xfe924b7cfe89ddd271abaf7210a80a7e11178758` | Oracle services |

## Neo Mamba SDK

### Installation
```bash
pip install neo-mamba
```

### Quick Start
```python
import asyncio
from neo3.api.wrappers import ChainFacade, NeoToken, GasToken
from neo3.wallet.wallet import Wallet

async def check_balance():
    # Connect to mainnet
    facade = ChainFacade.node_provider_mainnet()

    # Get NEO balance
    neo = NeoToken()
    address = "NUVaphUShQPD82yoXcbvFkedjHX6rUF7QQ"
    balance = await facade.test_invoke(neo.balance_of(address))
    print(f"NEO Balance: {balance}")

    # Get GAS balance
    gas = GasToken()
    gas_balance = await facade.test_invoke(gas.balance_of(address))
    print(f"GAS Balance: {gas_balance / 1e8}")  # 8 decimals

asyncio.run(check_balance())
```

### Transfer Example
```python
import asyncio
from neo3.api.wrappers import ChainFacade, NeoToken
from neo3.api.helpers.signing import sign_with_account
from neo3.network.payloads.verification import Signer
from neo3.wallet.wallet import Wallet

async def transfer_neo():
    # Load wallet
    wallet = Wallet.from_file("./wallet.json")
    account = wallet.account_default

    facade = ChainFacade.node_provider_mainnet()
    facade.add_signer(
        sign_with_account(account),
        Signer(account.script_hash)
    )

    # Transfer NEO
    neo = NeoToken()
    receipt = await facade.invoke(
        neo.transfer(account.address, "NZwvGPNXprXj2KnKEFbpz3aG87bGECZThL", 10)
    )
    print(f"Transaction: {receipt.tx_hash}")

asyncio.run(transfer_neo())
```

## Neo CLI Commands

### Wallet Management
```bash
# Create wallet
create wallet /path/to/wallet.json

# Open wallet
open wallet /path/to/wallet.json

# Create new address
create address

# List addresses
list address

# Show GAS claimable
show gas
```

### Transactions
```bash
# Send NEO/GAS
send <asset_id> <address> <amount>

# NEP-17 transfer
transfer <tokenHash> <to> <amount> [from]

# Sign transaction
sign <jsonObjectToSign>
```

### Smart Contracts
```bash
# Deploy contract
deploy Template.nef Template.manifest.json

# Invoke contract
invoke <scriptHash> <operation> [parameters] [sender]
```

## RPC Methods

### Common Methods
| Method | Description |
|--------|-------------|
| `getblockcount` | Current block height |
| `getbestblockhash` | Latest block hash |
| `getblock` | Block by hash/index |
| `getrawtransaction` | Transaction details |
| `getnep17balances` | NEP-17 token balances |
| `getnep17transfers` | NEP-17 transfer history |
| `invokefunction` | Contract function call |
| `sendrawtransaction` | Broadcast transaction |

### Example RPC Call
```bash
curl -X POST https://mainnet1.neo.coz.io:443 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "getnep17balances",
    "params": ["NUVaphUShQPD82yoXcbvFkedjHX6rUF7QQ"],
    "id": 1
  }'
```

## NeoFS Integration

### REST Gateway
NeoFS provides a REST API gateway for easy integration:

**Base URL:** `http://localhost:8090/v1` (self-hosted)

### Upload Object
```bash
curl -F 'file=@myfile.jpg;filename=myfile.jpg' \
  http://localhost:8090/v1/upload/{containerId}
```

### Get Object
```bash
curl http://localhost:8090/v1/get/{containerId}/{objectId}
```

## NeoX (EVM Sidechain)

NeoX is Neo's EVM-compatible sidechain with:
- **dBFT consensus** with immediate finality
- **Anti-MEV** capabilities
- **Native bridge** to Neo N3
- **< $0.01** gas costs
- **>1,000 TPS** throughput

### Connect with ethers.js
```javascript
const provider = new ethers.JsonRpcProvider("https://mainnet-1.rpc.banelabs.org");
const chainId = await provider.getNetwork().then(n => n.chainId);
console.log(`Connected to NeoX (chain ID: ${chainId})`);
```

## Token Standards

### NEP-17 (Fungible Tokens)
Standard methods:
- `symbol()` - Token symbol
- `decimals()` - Decimal places
- `totalSupply()` - Total supply
- `balanceOf(account)` - Account balance
- `transfer(from, to, amount, data)` - Transfer tokens

### NEP-11 (Non-Fungible Tokens)
Standard methods:
- `symbol()` - Collection symbol
- `decimals()` - Always 0 for NFTs
- `totalSupply()` - Total NFTs minted
- `balanceOf(owner)` - NFT count for owner
- `tokensOf(owner)` - List token IDs for owner
- `ownerOf(tokenId)` - Owner of specific NFT
- `transfer(to, tokenId, data)` - Transfer NFT

## Best Practices

1. **Always Validate Addresses**: Neo addresses start with "N"
2. **Check GAS Balance**: Ensure sufficient GAS for transaction fees
3. **Use Testnet First**: Test transactions on testnet before mainnet
4. **Secure Wallet Files**: Encrypt and backup wallet JSON files
5. **Verify Contract Hashes**: Always verify contract script hashes

## Security Warnings

- Never share private keys or wallet passwords
- Verify contract addresses before interactions
- Be cautious of unverified contracts
- Use hardware wallets for significant holdings
- Keep wallet software updated

## Example Queries

1. "Check my NEO balance for address N..."
2. "Transfer 10 GAS to address N..."
3. "Get the total supply of NEO"
4. "Query a NEP-17 token contract"
5. "What's the current block height on Neo N3?"

## Context Variables

- `{{action}}`: Operation to perform
- `{{address}}`: Neo N3 address
- `{{contract_hash}}`: Contract script hash
- `{{network}}`: Network (mainnet/testnet)

## Resources

- [Neo Documentation](https://docs.neo.org)
- [Neo Mamba SDK](https://dojo.coz.io/neo3/mamba)
- [NeoX Documentation](https://xdocs.ngd.network)
- [Neo Developer Portal](https://developers.neo.org)
- [City of Zion](https://coz.io)
