---
name: crypto-price
description: "Query cryptocurrency prices and market data via CoinGecko API. Use when: (1) checking current crypto prices, (2) viewing market cap rankings, (3) monitoring 24h price changes, (4) searching for specific cryptocurrencies, or (5) any crypto price-related queries. Supports BTC, ETH, and 10,000+ coins."
---

# Crypto Price Skill

Query real-time cryptocurrency prices and market data using the free CoinGecko API.

## When to Use

- Check current price of Bitcoin, Ethereum, or any crypto
- View top cryptocurrencies by market cap
- Monitor 24-hour price changes
- Search for specific coins by name or symbol
- Convert prices to different currencies (USD, CNY, EUR, etc.)

## Quick Start

### Get Bitcoin Price in USD
```bash
python3 scripts/crypto-price.py get bitcoin
```

### Get Ethereum Price in CNY
```bash
python3 scripts/crypto-price.py get ethereum cny
```

### View Top 10 Cryptocurrencies
```bash
python3 scripts/crypto-price.py top 10
```

### Search for a Coin
```bash
python3 scripts/crypto-price.py search solana
```

## Commands

### `search <keyword>`
Search for cryptocurrencies by name or symbol.

Example:
```bash
python3 scripts/crypto-price.py search bitcoin
# Output: BTC - Bitcoin, ID: bitcoin
```

### `get <coin_id> [currency]`
Get price for a specific cryptocurrency.

- `coin_id`: The CoinGecko ID (e.g., bitcoin, ethereum, solana)
- `currency`: Optional, defaults to 'usd'. Supported: usd, cny, eur, jpy, gbp, krw, etc.

Example:
```bash
python3 scripts/crypto-price.py get bitcoin cny
# Output: 💰 BITCOIN
#         价格: ¥460,123.45
#         24h 涨跌: 🟢 +5.23%
```

### `top [limit] [currency]`
View top cryptocurrencies by market cap.

- `limit`: Number of coins to show (1-100), default 10
- `currency`: Optional, defaults to 'usd'

Example:
```bash
python3 scripts/crypto-price.py top 5 cny
# Shows top 5 coins with prices in CNY
```

## Finding Coin IDs

Use the `search` command to find the correct `coin_id`:

```bash
python3 scripts/crypto-price.py search "binance"
# Output: BNB - BNB, ID: binancecoin
```

Popular coin IDs:
- bitcoin, ethereum, solana, cardano, polkadot
- ripple (XRP), binancecoin (BNB), dogecoin, chainlink

## Notes

- Uses free CoinGecko API with rate limits
- If you see "API 请求过于频繁", wait a minute and retry
- Prices are for reference only, not financial advice
