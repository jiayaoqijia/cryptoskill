---
name: crypto-price
description: "Get real-time cryptocurrency prices, market data, and portfolio tracking"
homepage: https://docs.coingecko.com/
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": { "bins": ["curl", "jq"] },
        "credentials": [],
      },
  }
---
# Crypto Price Tracker

Get real-time cryptocurrency prices, market cap, volume, and track your portfolio value.

## Quick Price Check

Get current price for any cryptocurrency:

```bash
# Bitcoin price in USD
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true" | jq

# Multiple coins at once
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true" | jq

# Price in multiple currencies
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd,eur,gbp,btc" | jq
```

## Detailed Market Data

Get comprehensive market information:

```bash
# Full market data for a coin
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin" | jq '{
  name: .name,
  symbol: .symbol,
  price: .market_data.current_price.usd,
  market_cap: .market_data.market_cap.usd,
  volume_24h: .market_data.total_volume.usd,
  change_24h: .market_data.price_change_percentage_24h,
  change_7d: .market_data.price_change_percentage_7d,
  ath: .market_data.ath.usd,
  ath_date: .market_data.ath_date.usd
}'
```

## Top Cryptocurrencies

List top coins by market cap:

```bash
# Top 10 by market cap
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1" | jq '.[] | {rank: .market_cap_rank, name: .name, symbol: .symbol, price: .current_price, change_24h: .price_change_percentage_24h}'

# Top gainers (sort by 24h change)
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1" | jq 'sort_by(.price_change_percentage_24h) | reverse | .[0:10] | .[] | {name: .name, change_24h: .price_change_percentage_24h}'
```

## Portfolio Tracking

Calculate portfolio value:

```bash
# Define your holdings and calculate total value
# Format: coin_id:amount
HOLDINGS="bitcoin:0.5,ethereum:2.5,solana:50"

# Get prices and calculate
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd" | jq --arg holdings "$HOLDINGS" '
  . as $prices |
  ($holdings | split(",") | map(split(":") | {coin: .[0], amount: (.[1] | tonumber)})) |
  map(. + {price: $prices[.coin].usd, value: (.amount * $prices[.coin].usd)}) |
  {holdings: ., total: (map(.value) | add)}
'
```

## Price Alerts (Simple)

Check if price crosses threshold:

```bash
# Alert if BTC drops below $50,000
BTC_PRICE=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" | jq -r '.bitcoin.usd')
if (( $(echo "$BTC_PRICE < 50000" | bc -l) )); then
  echo "ALERT: Bitcoin is below $50,000! Current: $BTC_PRICE"
fi
```

## Historical Data

Get price history:

```bash
# Last 7 days of prices
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7" | jq '.prices | .[-10:] | .[] | {timestamp: (.[0]/1000 | strftime("%Y-%m-%d %H:%M")), price: .[1]}'

# Price on specific date (OHLC)
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=30" | jq '.[-1] | {date: (.[0]/1000 | strftime("%Y-%m-%d")), open: .[1], high: .[2], low: .[3], close: .[4]}'
```

## Gas Prices (Ethereum)

Check current gas prices:

```bash
# ETH gas prices (requires Etherscan API key)
# Free tier: 5 calls/second
curl -s "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken" | jq '.result | {low: .SafeGasPrice, average: .ProposeGasPrice, high: .FastGasPrice}'
```

## Trending Coins

See what's trending:

```bash
curl -s "https://api.coingecko.com/api/v3/search/trending" | jq '.coins | .[] | .item | {name: .name, symbol: .symbol, market_cap_rank: .market_cap_rank}'
```

## Tips

- CoinGecko API is free with rate limits (10-50 calls/minute)
- Use `jq` to format and filter JSON responses
- Cache responses locally to avoid rate limits
- For production use, consider paid APIs like CoinMarketCap or CryptoCompare

## Resources

- [CoinGecko API Docs](https://docs.coingecko.com/)
- [CoinMarketCap API](https://coinmarketcap.com/api/)
- [Etherscan API](https://docs.etherscan.io/)
