---
name: dex-arb-detector
track: web3-data-intelligence
version: 0.1.0
summary: Detect significant price deltas across DEXs
---

## Description

Detect significant price deltas across decentralized exchanges (DEXs) for potential arbitrage opportunities. Analyzes liquidity and pricing inefficiencies.

## Inputs

```json
{
  "token_pair": "token1/token2",
  "dexes": ["uniswap", "sushiswap"],
  "min_delta": "0.5%"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "opportunities": [],
    "best_spread": "2.3%"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Find Arbitrage
```bash
echo '{"token_pair":"ETH/USDC","dexes":["uniswap","sushiswap"]}' | python3 scripts/main.py
```

## Examples

### Example 1: Detect Arb
```bash
$ echo '{"token_pair":"ETH/USDC","dexes":["uniswap","sushiswap"],"min_delta":"0.5%"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "opportunities": [{"from": "uniswap", "to": "sushiswap", "spread": "1.2%"}],
    "best_spread": "1.2%"
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "token_pair": "Invalid token pair"
  }
}
```
