# Basic Swap Example

## User Input

```
1 ETH to USDC on ethereum from 0xYourWalletAddress
```

## Expected Output

```
## KyberSwap Swap Transaction

**1 ETH → 2345.67 USDC** on Ethereum

| Detail | Value |
|---|---|
| Input | 1 ETH (~$2345.67) |
| Expected output | 2345.67 USDC (~$2345.67) |
| Minimum output (after slippage) | 2333.94 USDC |
| Slippage tolerance | 0.5% |
| Gas estimate | 250000 units (~$3.45) |

### Transaction Details

| Field | Value |
|---|---|
| To (Router) | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` |
| Value | `1000000000000000000` (in wei) |
| Data | `0x...` |
| Sender | `0xYourWalletAddress` |
| Recipient | `0xYourWalletAddress` |

> **WARNING:** Review the transaction details carefully before submitting on-chain.
```

## JSON Output

```json
{
  "type": "kyberswap-swap",
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
  "tx": {
    "to": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
    "data": "0x...",
    "value": "1000000000000000000",
    "gas": "250000",
    "gasUsd": "3.45"
  },
  "sender": "0xYourWalletAddress",
  "recipient": "0xYourWalletAddress",
  "slippageBps": 50
}
```
