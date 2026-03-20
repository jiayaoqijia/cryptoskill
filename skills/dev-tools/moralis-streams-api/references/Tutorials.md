# Streams API Tutorials

Real-world examples and tutorials for common Moralis Streams API use cases. All examples use curl with the correct HTTP methods as per the Streams API swagger specification.

## Track Specific ERC20 Token Transfers From a List of Wallets

Monitor a list of wallets and filter only for a specific ERC20 token transfers using the built-in `moralis_streams_contract_address` filter.

### Step 1: Create the Stream

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x38"],
  "description": "Listen to a list of wallets for BUSD transfers",
  "tag": "busd-transfers",
  "webhookUrl": "https://webhook.site/e04c2edc-afb9-45b8-aff5-20724b2b1561",
  "includeContractLogs": true,
  "topic0": ["Transfer(address,address,uint256)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "name": "from", "type": "address"},
        {"indexed": true, "name": "to", "type": "address"},
        {"indexed": false, "name": "value", "type": "uint256"}
      ],
      "name": "Transfer",
      "type": "event"
    }
  ],
  "advancedOptions": [
    {
      "topic0": "Transfer(address,address,uint256)",
      "filter": {
        "eq": ["moralis_streams_contract_address", "0x55d398326f99059ff775485246999027b3197955"]
      }
    }
  ]
}'
```

### Step 2: Add Addresses to Monitor

Replace `STREAM_ID` with the ID returned from step 1.

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/STREAM_ID/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "addressToAdd": ["0x1234567890123456789012345678901234567890", "0x8765432109876543210987654321098765432109", "0x5432109876543210987654321098765432109876"]
}'
```

**Reference:** [Track Specific ERC20 Token Transfers](https://docs.moralis.com/streams-api/evm/how-to-track-specific-erc20-token-transfers-from-a-list-of-wallets)

---

## Track New Tokens and Pairs (DEX Pair Creation)

Monitor for new tokens by tracking DEX pair creation events. This is more reliable than monitoring minting events because it indicates tokens being launched with actual liquidity.

### Single DEX (Uniswap V2 on Ethereum)

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x1"],
  "description": "Track new Uniswap V2 pairs",
  "tag": "uniswap_v2_pairs",
  "webhookUrl": "https://YOUR_WEBHOOK_URL",
  "includeContractLogs": true,
  "topic0": ["PairCreated(address,address,address,uint256)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "internalType": "address", "name": "token0", "type": "address"},
        {"indexed": true, "internalType": "address", "name": "token1", "type": "address"},
        {"indexed": false, "internalType": "address", "name": "pair", "type": "address"},
        {"indexed": false, "internalType": "uint256", "name": "", "type": "uint256"}
      ],
      "name": "PairCreated",
      "type": "event"
    }
  ],
  "advancedOptions": [
    {
      "topic0": "PairCreated(address,address,address,uint256)",
      "includeNativeTxs": true
    }
  ]
}'
```

### Add Factory Address

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/STREAM_ID/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "addressToAdd": ["0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"]
}'
```

### Multiple DEXes (Ethereum, BSC, Polygon)

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x1", "0x38", "0x89"],
  "description": "Track pairs across multiple DEXes",
  "tag": "multidex_pairs",
  "webhookUrl": "https://YOUR_WEBHOOK_URL",
  "includeContractLogs": true,
  "topic0": ["PairCreated(address,address,address,uint256)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "internalType": "address", "name": "token0", "type": "address"},
        {"indexed": true, "internalType": "address", "name": "token1", "type": "address"},
        {"indexed": false, "internalType": "address", "name": "pair", "type": "address"},
        {"indexed": false, "internalType": "uint256", "name": "", "type": "uint256"}
      ],
      "name": "PairCreated",
      "type": "event"
    }
  ],
  "advancedOptions": [
    {
      "topic0": "PairCreated(address,address,address,uint256)",
      "includeNativeTxs": true
    }
  ]
}'
```

### Add Multiple Factory Addresses

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/STREAM_ID/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "addressToAdd": [
    "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac",
    "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
    "0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32"
  ]
}'
```

**Factory Addresses:**
- Uniswap V2: `0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f`
- SushiSwap: `0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac`
- PancakeSwap V2: `0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73`
- QuickSwap: `0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32`

**Use Cases:**
- Token Discovery Platforms
- DeFi Analytics
- Trading Bots
- Portfolio Trackers
- Security Monitoring

**Reference:** [Track New Tokens and Pairs](https://docs.moralis.com/streams-api/evm/how-to-track-new-tokens-and-pairs)

---

## Listen to All Events from a Contract Factory

Monitor all events from a contract factory using the `allAddresses` feature. This requires a custom ABI specific to your contracts to avoid receiving events from other contracts with the same ABI.

> **Note:** The `allAddresses` feature is only available on Business and Enterprise plans.

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x1"],
  "description": "monitor a contract factory",
  "tag": "contract_Factory",
  "webhookUrl": "https://YOUR_WEBHOOK_URL",
  "includeContractLogs": true,
  "allAddresses": true,
  "topic0": ["factoryEvent(address,address,address)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "name": "from", "type": "address"},
        {"indexed": true, "name": "to", "type": "address"},
        {"indexed": true, "name": "contract", "type": "address"}
      ],
      "name": "factoryEvent",
      "type": "event"
    }
  ]
}'
```

**Important:** Use a unique ABI that is specific to your contracts to avoid receiving events from other contracts using the same ABI structure.

**Reference:** [Listen to Contract Factory Events](https://docs.moralis.com/streams-api/evm/how-to-listen-all-events-from-a-contract-factory)

---

## Monitor NFT Transfers from Specific Wallet Addresses

Monitor all NFT transfers sent from a specific address using filters with the `allAddresses` feature.

> **Note:** The `allAddresses` feature is only available on Business and Enterprise plans.
> **Note:** Some NFT contracts like CryptoPunks don't follow standard ERC721 and won't trigger webhooks.

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x1"],
  "description": "monitor all NFT transfers",
  "tag": "NFT_transfers",
  "webhookUrl": "https://YOUR_WEBHOOK_URL",
  "includeContractLogs": true,
  "allAddresses": true,
  "topic0": ["Transfer(address,address,uint256)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "name": "from", "type": "address"},
        {"indexed": true, "name": "to", "type": "address"},
        {"indexed": true, "name": "tokenId", "type": "uint256"}
      ],
      "name": "Transfer",
      "type": "event"
    }
  ],
  "advancedOptions": [
    {
      "topic0": "Transfer(address,address,uint256)",
      "filter": {
        "eq": ["from", "0x283af0b28c62c092c9727f1ee09c02ca627eb7f5"]
      }
    }
  ]
}'
```

**Advanced Options Explained:**
- Uses `Transfer(address,address,uint256)` topic (ERC721 Transfer event with indexed `tokenId`)
- Filters for events where `from` equals the specified address
- Only receives NFT transfers originating from that address

**Reference:** [Monitor NFT Transfers from Specific Wallet](https://docs.moralis.com/streams-api/evm/how-to-listen-to-all-nft-transfers-sent-from-a-specific-address)

---

## Monitor High-Value ENS Domain Registrations

Track when high-value ENS domains are registered by monitoring the `NameRegistered` event on the ENS Registry.

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x1"],
  "description": "Monitor high-value ENS domain registrations",
  "tag": "ens-registrations",
  "webhookUrl": "https://YOUR_WEBHOOK_URL",
  "includeContractLogs": true,
  "topic0": ["NameRegistered(string,bytes32,address,uint256,uint256)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": false, "name": "name", "type": "string"},
        {"indexed": true, "name": "label", "type": "bytes32"},
        {"indexed": true, "name": "owner", "type": "address"},
        {"indexed": false, "name": "cost", "type": "uint256"},
        {"indexed": false, "name": "expires", "type": "uint256"}
      ],
      "name": "NameRegistered",
      "type": "event"
    }
  ],
  "advancedOptions": [
    {
      "topic0": "NameRegistered(string,bytes32,address,uint256,uint256)",
      "filter": {
        "gt": ["cost", "1000000000000000000"]
      }
    }
  ]
}'
```

### Add ENS Registry Address

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/STREAM_ID/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "addressToAdd": ["0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"]
}'
```

**Key details:**
- Filters for registrations costing more than 1 ETH (`1000000000000000000` wei)
- ENS Registry: `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e`

**Reference:** [Monitor ENS Domain Registrations](https://docs.moralis.com/streams-api/evm/how-to-monitor-ens-domain-registrations)

---

## Track ERC20 Token Mints and Burns (USDC)

Monitor a specific ERC20 token for mint and burn events by detecting transfers to/from the zero address.

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x1"],
  "description": "Track USDC mints and burns",
  "tag": "usdc-mints-burns",
  "webhookUrl": "https://YOUR_WEBHOOK_URL",
  "includeContractLogs": true,
  "topic0": ["Transfer(address,address,uint256)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "name": "from", "type": "address"},
        {"indexed": true, "name": "to", "type": "address"},
        {"indexed": false, "name": "value", "type": "uint256"}
      ],
      "name": "Transfer",
      "type": "event"
    }
  ],
  "advancedOptions": [
    {
      "topic0": "Transfer(address,address,uint256)",
      "filter": {
        "or": [
          {
            "and": [
              {"eq": ["from", "0x0000000000000000000000000000000000000000"]},
              {"eq": ["moralis_streams_contract_address", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"]}
            ]
          },
          {
            "and": [
              {"eq": ["to", "0x0000000000000000000000000000000000000000"]},
              {"eq": ["moralis_streams_contract_address", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"]}
            ]
          }
        ]
      }
    }
  ]
}'
```

### Add USDC Contract Address

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/STREAM_ID/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "addressToAdd": ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"]
}'
```

**Key details:**
- **Mint**: `from` is the zero address (`0x000...000`)
- **Burn**: `to` is the zero address (`0x000...000`)
- USDC on Ethereum: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- Uses `moralis_streams_contract_address` to ensure only USDC transfers are matched

---

## Monitor Specific NFTs by Token ID (CryptoPunks)

Track transfers of specific CryptoPunks by token ID using the non-standard `PunkTransfer` event and the `in` filter operator.

> **Note:** CryptoPunks use a non-standard contract that does not follow ERC721. Standard `Transfer(address,address,uint256)` events won't work.

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "chainIds": ["0x1"],
  "description": "Monitor specific CryptoPunk transfers",
  "tag": "cryptopunks-tracker",
  "webhookUrl": "https://YOUR_WEBHOOK_URL",
  "includeContractLogs": true,
  "topic0": ["PunkTransfer(address,address,uint256)"],
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "name": "from", "type": "address"},
        {"indexed": true, "name": "to", "type": "address"},
        {"indexed": false, "name": "punkIndex", "type": "uint256"}
      ],
      "name": "PunkTransfer",
      "type": "event"
    }
  ],
  "advancedOptions": [
    {
      "topic0": "PunkTransfer(address,address,uint256)",
      "filter": {
        "in": ["punkIndex", ["1000", "2000", "3000", "4000", "5000"]]
      }
    }
  ]
}'
```

### Add CryptoPunks Contract

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/STREAM_ID/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "addressToAdd": ["0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB"]
}'
```

**Key details:**
- CryptoPunks: `0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB`
- Uses the `in` filter operator to match specific token IDs
- Non-standard `PunkTransfer` event (not ERC721 `Transfer`)

---

## Common Patterns

### Filter by Token Amount

Only receive transfers above a certain threshold:

```bash
"advancedOptions": [
  {
    "topic0": "Transfer(address,address,uint256)",
    "filter": {
      "gt": ["value", "1000000000000000000"]
    }
  }
]
```

### Monitor Multiple Specific Tokens

```bash
"advancedOptions": [
  {
    "topic0": "Transfer(address,address,uint256)",
    "filter": {
      "or": [
        {"eq": ["moralis_streams_contract_address", "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"]},
        {"eq": ["moralis_streams_contract_address", "0xdac17f958d2ee523a2206206994597c13d831ec7"]}
      ]
    }
  }
]
```

### Track Mints and Burns

```bash
"advancedOptions": [
  {
    "topic0": "Transfer(address,address,uint256)",
    "filter": {
      "or": [
        {"eq": ["from", "0x0000000000000000000000000000000000000000"]},
        {"eq": ["to", "0x0000000000000000000000000000000000000000"]}
      ]
    }
  }
]
```

---

## HTTP Method Reference

| Action | HTTP Method | Endpoint |
|--------|-------------|----------|
| Create stream | `PUT` | `/streams/evm` |
| Update stream | `POST` | `/streams/evm/:id` |
| Delete stream | `DELETE` | `/streams/evm/:id` |
| Get streams | `GET` | `/streams/evm` |
| Get stream | `GET` | `/streams/evm/:id` |
| Add address | `POST` | `/streams/evm/:id/address` |
| Replace addresses | `PATCH` | `/streams/evm/:id/address` |
| Delete address | `DELETE` | `/streams/evm/:id/address/:address` |
| Update status | `POST` | `/streams/evm/:id/status` |
