# DeFi Quote Exec Demo

Get real-time DeFi price quotes and execute token swaps with multi-DEX routing optimization, slippage protection, and gas estimation.

## Features
- **Real Price Calculation**: Uses constant product formula (x*y=k) with actual pool liquidity data
- **Multi-DEX Routing**: Optimizes routes across Uniswap V3, Curve, Balancer, and Dodo
- **Price Impact Analysis**: Calculates slippage based on trade size and pool depth
- **Multi-Chain Support**: Ethereum, Polygon, Arbitrum, Optimism, Base with chain-specific gas fees
- **Gas Estimation**: Accurate gas calculation per chain and route complexity
- **Swap Execution**: Execute swaps with slippage protection and minimum output validation
- **Token Registry**: 6+ verified tokens with real addresses and decimals

## Usage

### Get Quote (Ethereum WETH to USDC)
```bash
echo '{
  "token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
  "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "amount_in": 5.0,
  "chain": "ethereum",
  "slippage_tolerance": 0.5
}' | python3 scripts/main.py
```

### Execute Swap with Quote
```bash
echo '{
  "token_in": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
  "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "amount_in": 5.0,
  "chain": "ethereum",
  "slippage_tolerance": 0.5,
  "execute": true,
  "min_amount_out": 11000
}' | python3 scripts/main.py
```

## Parameters
- `token_in` (required): Input token address (0x...)
- `token_out` (required): Output token address (0x...)
- `amount_in` (required): Amount to swap (float)
- `chain` (optional): Target blockchain (ethereum, polygon, arbitrum, optimism, base) - default: ethereum
- `slippage_tolerance` (optional): Max slippage % (0-100) - default: 0.5%
- `execute` (optional): Execute swap after quote (true/false) - default: false
- `min_amount_out` (optional): Minimum output required for execution

## Response
Returns detailed quote with token info, exchange rate, price impact, optimal route, gas estimation, and optional execution details.
