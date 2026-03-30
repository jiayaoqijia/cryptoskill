# Basic Quote Example

## User Input

```
1 ETH to USDC on ethereum
```

## Expected Output

```
## KyberSwap Quote

**1 ETH → 2345.67 USDC** on Ethereum

| Detail | Value |
|---|---|
| Input | 1 ETH (~$2345.67) |
| Output | 2345.67 USDC (~$2345.67) |
| Rate | 1 ETH = 2345.67 USDC |
| Gas estimate | 250000 units (~$3.45) |
| Router | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` |

### Route
ETH → USDC via [uniswap-v3]
```

## JSON Output

```json
{
  "type": "kyberswap-quote",
  "chain": "ethereum",
  "tokenIn": {
    "symbol": "ETH",
    "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "decimals": 18,
    "amount": "1",
    "amountWei": "1000000000000000000",
    "amountUsd": "2345.67"
  },
  "tokenOut": {
    "symbol": "USDC",
    "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "decimals": 6,
    "amount": "2345.67",
    "amountWei": "2345670000",
    "amountUsd": "2345.67"
  },
  "rate": "2345.67",
  "gas": "250000",
  "gasUsd": "3.45",
  "routerAddress": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5"
}
```
