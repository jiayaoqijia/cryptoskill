# Multi-Chain Quote Example

## User Input

```
100 USDC to ETH on arbitrum
```

## Expected Output

```
## KyberSwap Quote

**100 USDC → 0.0426 ETH** on Arbitrum

| Detail | Value |
|---|---|
| Input | 100 USDC (~$100.00) |
| Output | 0.0426 ETH (~$99.85) |
| Rate | 1 USDC = 0.000426 ETH |
| Gas estimate | 450000 units (~$0.12) |
| L1 fee | ~$0.08 |
| Router | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` |

### Route
USDC → ETH via [uniswap-v3]
```

## Notes

- L2 chains (Arbitrum, Optimism, Base, Linea) include an L1 fee row
- Gas costs are typically lower on L2s
- Router address may vary by chain
