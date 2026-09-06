# Basic Quote Example

## Scenario
Get a quote for swapping 1 ETH to USDC on Ethereum mainnet.

## Expected Workflow

### Step 1: Parse Input
- **Amount**: 1
- **TokenIn**: ETH
- **TokenOut**: USDC
- **Chain**: ethereum (default)

### Step 2: Resolve Token Addresses
From `references/token-registry.md` (project root):

**ETH** (native token):
- Address: `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`
- Decimals: 18

**USDC** on Ethereum:
- Address: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- Decimals: 6

### Step 3: Get Gas Price
```
GET https://open-api.openocean.finance/v4/eth/gasPrice
```

Example response:
```json
{
  "code": 200,
  "data": {
    "base": 605865956,
    "standard": {
      "legacyGasPrice": 605865956,
      "maxPriorityFeePerGas": 500000000,
      "maxFeePerGas": 1366388318,
      "waitTimeEstimate": 45000
    }
  }
}
```

Use `standard.legacyGasPrice`: `605865956` wei

### Step 4: Convert Amount to Wei
```
1 ETH = 1 * 10^18 = 1000000000000000000 wei
```

### Step 5: Call Quote API
```
GET https://open-api.openocean.finance/v4/eth/quote?inTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&outTokenAddress=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&amountDecimals=1000000000000000000&gasPriceDecimals=605865956
```

### Step 6: Format Response

**Example Response:**
```json
{
  "code": 200,
  "data": {
    "inToken": {
      "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
      "decimals": 18,
      "symbol": "ETH",
      "name": "Ethereum",
      "usd": "2345.67",
      "volume": 2345.67
    },
    "outToken": {
      "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "decimals": 6,
      "symbol": "USDC",
      "name": "USD Coin",
      "usd": "1.00",
      "volume": 2345.67
    },
    "inAmount": "1000000000000000000",
    "outAmount": "2345670000",
    "estimatedGas": "129211",
    "dexes": [
      {
        "dexIndex": 0,
        "dexCode": "UniswapV3",
        "swapAmount": "1000000000000000000"
      }
    ],
    "path": {...},
    "save": -0.0018,
    "price_impact": "0.01%",
    "exchange": "0x6352a56caadC4F1E25CD6c75970Fa768A3304e64"
  }
}
```

### Step 7: Calculate Human-Readable Output
```
outAmount (wei): 2345670000
USDC decimals: 6
humanAmountOut = 2345670000 / 10^6 = 2345.67 USDC
```

### Step 8: Calculate Exchange Rate
```
rate = 2345.67 / 1 = 2345.67 USDC per ETH
```

### Step 9: Format Output

```
## OpenOcean Quote

**1 ETH → 2345.67 USDC** on Ethereum

| Detail | Value |
|---|---|
| Input | 1 ETH (~$2345.67) |
| Output | 2345.67 USDC (~$2345.67) |
| Rate | 1 ETH = 2345.67 USDC |
| Gas estimate | 129211 units |
| Price impact | 0.01% |
| Savings | -0.18% |

### Route
UniswapV3: 2345.67 USDC

### Transaction Details
- Router: `0x6352a56caadC4F1E25CD6c75970Fa768A3304e64`
- Gas price: 0.605865956 Gwei
```

## Key Points

1. **Native Token Handling**: ETH uses special address `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`
2. **Decimal Conversion**: ETH has 18 decimals, USDC has 6 decimals
3. **Wei Format**: Amounts must be plain integer strings (no decimals, no scientific notation)
4. **Gas Price**: Use current market rates from gasPrice endpoint
5. **Route Display**: Show which DEXes are used in the route

## Common Issues

1. **Wrong Decimals**: Using wrong decimal places for token conversion
2. **Scientific Notation**: Python/JavaScript may output scientific notation for large numbers
3. **Gas Price Units**: Confusing wei vs gwei (API expects wei)
4. **Chain Parameter**: Using chain name vs chain ID (both work)

## Verification

Always verify:
- Token addresses match the chain
- Amount conversion is correct
- Gas price is reasonable for current network conditions
- Route makes sense for the token pair