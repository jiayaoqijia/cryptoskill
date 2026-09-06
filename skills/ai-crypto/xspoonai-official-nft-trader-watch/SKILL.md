---
name: nft-trader-watch
track: web3-data-intelligence
version: 0.2.0
summary: Real NFT trader analysis with OpenSea API integration
---

## Description

Track NFT trader activity and detect flipping patterns with real sale data from OpenSea API. Analyzes buy/sell volumes, profit margins, and identifies high-value flips. Supports popular collections like BAYC, CryptoPunks, and Pudgy Penguins.

## Inputs (API Mode)

```json
{
  "use_api": true,
  "collection": "0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE",
  "collection_slug": "boredapeyachtclub",
  "min_volume": 5
}
```

## Inputs (Parameter Mode)

```json
{
  "collection": "0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE",
  "trades": [
    {
      "type": "buy",
      "nft_id": "1234",
      "price_eth": 45.5,
      "timestamp": "2026-02-07T08:00:00Z"
    },
    {
      "type": "sell",
      "nft_id": "1234",
      "price_eth": 52.75,
      "timestamp": "2026-02-07T10:30:00Z"
    }
  ]
}
```

## Outputs (API Mode)

```json
{
  "ok": true,
  "data": {
    "source": "opensea_api",
    "collection": "0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE",
    "eth_price": 1850.5,
    "total_traders": 42,
    "flips_detected": 18,
    "traders": [
      {
        "trader": "0x1234...5678",
        "buys": 8,
        "sells": 7,
        "buy_volume_eth": 156.5,
        "sell_volume_eth": 178.2,
        "profit_eth": 21.7,
        "profit_usd": 40155.5
      }
    ],
    "top_flips": [
      {
        "nft_id": "1234",
        "buy_price_eth": 45.5,
        "sell_price_eth": 52.75,
        "profit_eth": 7.25,
        "profit_pct": 15.93
      }
    ]
  }
}
```

## Usage

### Fetch Real OpenSea Data
```bash
python scripts/main.py --params '{"use_api":true,"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","collection_slug":"boredapeyachtclub"}'
```

### Analyze Custom Trades
```bash
python scripts/main.py --params '{"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","trades":[{"type":"buy","nft_id":"1234","price_eth":45.5}]}'
```

## Examples

### Example 1: BAYC Trader Analysis (API)
```bash
$ python scripts/main.py --params '{"use_api":true,"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","collection_slug":"boredapeyachtclub"}'
{
  "ok": true,
  "data": {
    "source": "opensea_api",
    "total_traders": 42,
    "flips_detected": 18,
    "traders": [
      {
        "profit_eth": 21.7,
        "profit_usd": 40155.5
      }
    ]
  }
}
```

### Example 2: Custom Trade Analysis
```bash
$ python scripts/main.py --params '{"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","trades":[{"type":"buy","nft_id":"1234","price_eth":45.5},{"type":"sell","nft_id":"1234","price_eth":52.75}]}'
{
  "ok": true,
  "data": {
    "source": "parameters",
    "profit_eth": 7.25,
    "profit_usd": 13416.25,
    "flips_detected": 1
  }
}
```

## Supported Collections

- **bored_ape** → boredapeyachtclub
- **cryptopunks** → cryptopunks
- **pudgy_penguins** → pudgy-penguins
- **cool_cats** → cool-cats-nft
- **art_blocks** → artblocks-engine
