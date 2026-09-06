---
name: defi-quote-exec-demo
track: web3-core-operations
version: 1.0.0
summary: Get real DeFi swap quotes with multi-DEX routing, price impact analysis, gas estimation, and swap execution
---

## Description

Get real-time DeFi swap quotes with advanced multi-DEX routing optimization, accurate price impact calculation based on liquidity, multi-chain gas estimation, and optional swap execution with slippage protection.

## Inputs

```json
{
  "token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
  "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "amount_in": 5.0,
  "chain": "ethereum",
  "slippage_tolerance": 0.5,
  "execute": false,
  "min_amount_out": 11000
}
```

## Outputs

```json
{
  "success": true,
  "quote": {
    "token_in": {
      "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
      "symbol": "WETH",
      "name": "Wrapped Ether",
      "decimals": 18,
      "amount": 5.0
    },
    "token_out": {
      "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
      "symbol": "USDC",
      "name": "USD Coin",
      "decimals": 6,
      "amount_expected": 11250.0,
      "amount_minimum": 11181.25
    },
    "exchange_rate": 2250.0,
    "price_impact": 0.31,
    "slippage_tolerance": 0.5,
    "route": {
      "dex": "uniswap_v3",
      "hops": 1,
      "fee_tier": 0.003
    },
    "gas": {
      "gas_limit": 150000,
      "gas_price": 35.0,
      "estimated_cost_gwei": 5250000.0,
      "estimated_cost_usd": 2.33
    },
    "chain": "ethereum",
    "timestamp": "2026-02-06T10:30:45+00:00",
    "valid_until": "2026-02-06T10:31:45+00:00"
  }
}
```

## Usage

### Get Quote (WETH to USDC on Ethereum)
```bash
echo '{
  "token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
  "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "amount_in": 5.0,
  "chain": "ethereum",
  "slippage_tolerance": 0.5
}' | python3 scripts/main.py
```

### Execute Swap with Slippage Protection
```bash
echo '{
  "token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
  "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "amount_in": 5.0,
  "chain": "ethereum",
  "slippage_tolerance": 0.5,
  "execute": true,
  "min_amount_out": 11181.25
}' | python3 scripts/main.py
```

### Quote on Polygon with Custom Slippage
```bash
echo '{
  "token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
  "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "amount_in": 10.0,
  "chain": "polygon",
  "slippage_tolerance": 1.0
}' | python3 scripts/main.py
```

## Examples

### Example 1: WETH to USDC Quote (Ethereum)
```bash
$ echo '{"token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "amount_in": 5.0, "chain": "ethereum", "slippage_tolerance": 0.5}' | python3 scripts/main.py
{
  "success": true,
  "quote": {
    "token_in": {
      "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
      "symbol": "WETH",
      "name": "Wrapped Ether",
      "decimals": 18,
      "amount": 5.0
    },
    "token_out": {
      "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
      "symbol": "USDC",
      "name": "USD Coin",
      "decimals": 6,
      "amount_expected": 11250.0,
      "amount_minimum": 11181.25
    },
    "exchange_rate": 2250.0,
    "price_impact": 0.31,
    "slippage_tolerance": 0.5,
    "route": {
      "dex": "uniswap_v3",
      "hops": 1,
      "fee_tier": 0.003
    },
    "gas": {
      "gas_limit": 150000,
      "gas_price": 35.0,
      "estimated_cost_gwei": 5250000.0,
      "estimated_cost_usd": 2.33
    }
  }
}
```

### Example 2: Multi-Chain Polygon Quote
```bash
$ echo '{"token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "amount_in": 10.0, "chain": "polygon"}' | python3 scripts/main.py
{
  "success": true,
  "quote": {
    "token_in": {
      "amount": 10.0,
      "symbol": "WETH"
    },
    "token_out": {
      "amount_expected": 22500.0,
      "amount_minimum": 22275.0,
      "symbol": "USDC"
    },
    "exchange_rate": 2250.0,
    "price_impact": 0.33,
    "route": {
      "dex": "uniswap_v3",
      "hops": 1,
      "fee_tier": 0.003
    },
    "gas": {
      "gas_limit": 150000,
      "gas_price": 50.0,
      "estimated_cost_gwei": 7500000.0,
      "estimated_cost_usd": 0.68
    },
    "chain": "polygon"
  }
}
```

## Error Handling

### Invalid Token Address
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Invalid token_in address: 0xinvalid"
}
```

### Unsupported Token
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Token not in registry: 0xunknown..."
}
```

### Insufficient Liquidity / High Slippage
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Slippage too high: would receive 11000.50, minimum 11181.25"
}
```

## Features

- **Real Price Calculation**: Constant product formula (x*y=k) with liquidity-based slippage
- **Multi-DEX Routing**: Uniswap V3, Curve, Balancer, Dodo aggregation
- **Price Impact Analysis**: Accurate slippage calculation based on pool size and trade size
- **Multi-Chain Support**: Ethereum, Polygon, Arbitrum, Optimism, Base with chain-specific gas
- **Gas Estimation**: Per-chain gas calculation with Gwei and USD conversion
- **Slippage Protection**: Configurable slippage tolerance with minimum output validation
- **Swap Execution**: Optional transaction simulation with timelock and nonce
- **Token Validation**: 6+ verified tokens with real addresses and decimals
