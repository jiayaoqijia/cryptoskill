# Token API Reference

Full documentation for Alchemy's Token API endpoints.

## Methods

### alchemy_getTokenBalances
Get all ERC-20 token balances for an address.

```bash
POST https://{chain}.g.alchemy.com/v2/{apiKey}
```

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "alchemy_getTokenBalances",
  "params": [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "erc20"
  ],
  "id": 1
}
```

**Params:**
- `address`: Wallet address
- `tokenType`: "erc20" (default) or array of contract addresses

**Response:**
```json
{
  "result": {
    "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "tokenBalances": [
      {
        "contractAddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "tokenBalance": "0x5f5e100",
        "error": null
      }
    ]
  }
}
```

### alchemy_getTokenMetadata
Get metadata for a specific token.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "alchemy_getTokenMetadata",
  "params": ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"],
  "id": 1
}
```

**Response:**
```json
{
  "result": {
    "name": "USD Coin",
    "symbol": "USDC",
    "decimals": 6,
    "logo": "https://static.alchemyapi.com/images/assets/usdc.png"
  }
}
```

### alchemy_getTokenAllowance
Get token allowance for spender.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "alchemy_getTokenAllowance",
  "params": [{
    "contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "owner": "0x...",
    "spender": "0x..."
  }],
  "id": 1
}
```

## Common Token Addresses

### Ethereum Mainnet
| Token | Address |
|-------|---------|
| USDC | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 |
| USDT | 0xdAC17F958D2ee523a2206206994597C13D831ec7 |
| WETH | 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 |
| DAI | 0x6B175474E89094C44Da98b954EescdeCE80C40 |
| LINK | 0x514910771AF9Ca656af840dff83E8264EcF986CA |

### Polygon
| Token | Address |
|-------|---------|
| USDC | 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 |
| USDT | 0xc2132D05D31c914a87C6611C10748AEb04B58e8F |
| WMATIC | 0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270 |

## Price Data

For token prices, use:
- `alchemy_getTokenPrices` (where available)
- Or integrate with price feeds (Chainlink, CoinGecko)
