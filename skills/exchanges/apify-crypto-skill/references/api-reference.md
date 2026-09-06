# Crypto Skill API Reference

## KuCoin Functions

### get_ohlcv(symbol, timeframe, limit=100) -> list[OHLCVCandle]

Fetch OHLCV candlestick data from KuCoin.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | required | Trading pair (e.g. "BTC/USDT") |
| timeframe | str | required | Candle interval: "1m", "5m", "15m", "30m", "1h", "4h", "1d" |
| limit | int | 100 | Number of candles to fetch |

**OHLCVCandle fields:** `date` (str), `open` (float), `high` (float), `low` (float), `close` (float), `volume` (float), `symbol` (str)

### get_realtime_price(symbol) -> RealtimePrice

Fetch current price for a trading pair.

| Param | Type | Description |
|-------|------|-------------|
| symbol | str | Trading pair (e.g. "ETH/USDT") |

**RealtimePrice fields:** `symbol` (str), `price` (float), `date` (str)

### get_all_coins_ohlcv(timeframe, limit=100) -> list[OHLCVCandle]

Fetch OHLCV data for all available KuCoin coins. May hit 300s timeout for large requests — use small limit values.

## CoinGecko Functions

All CoinGecko functions return `MarketCoin` objects. The actor returns the same market-data format regardless of scrape mode.

**MarketCoin fields:** `id`, `symbol`, `name`, `current_price`, `market_cap`, `market_cap_rank`, `total_volume`, `high_24h`, `low_24h`, `price_change_24h`, `price_change_percentage_24h`, `circulating_supply`, `total_supply`, `max_supply`, `ath`, `atl`, `last_updated`

### get_simple_prices(coin_ids, vs_currencies=None) -> list[MarketCoin]

Fetch data for specific coins.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| coin_ids | list[str] | required | Coin IDs (e.g. ["bitcoin", "ethereum"]) |
| vs_currencies | list[str] or None | ["usd"] | Quote currencies |

### get_market_data(vs_currency="usd", category=None, max_results=100) -> list[MarketCoin]

Fetch top coins by market cap.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| vs_currency | str | "usd" | Quote currency |
| category | str or None | None | Filter by category (e.g. "layer-1", "defi") |
| max_results | int | 100 | Max coins to return |

### get_coin_detail(coin_id, include_details=True) -> MarketCoin

Fetch data for a single coin. Raises `ActorDataError` if coin not found.

### get_historical(coin_id, days=30, vs_currency="usd") -> MarketCoin

Fetch coin data in historical mode. Raises `ActorDataError` if coin not found.

### get_trending() -> list[MarketCoin]

Fetch currently trending cryptocurrencies.

### get_categories() -> list[MarketCoin]

Fetch cryptocurrency data by categories.

## Exceptions

All inherit from `CryptoSkillError`.

| Exception | When |
|-----------|------|
| `ApifyAuthError` | `APIFY_API_TOKEN` missing or invalid (401/403) |
| `ApifyActorError` | Actor run failed, rate limited (429), or connection error |
| `ApifyTimeoutError` | Actor run exceeded 300s timeout (408) |
| `ActorDataError` | Response doesn't match expected schema or is empty |

## Popular Trading Pairs (KuCoin)

BTC/USDT, ETH/USDT, XRP/USDT, ADA/USDT, DOGE/USDT, SOL/USDT, LTC/USDT, DOT/USDT, AVAX/USDT, TRX/USDT

## Popular CoinGecko Coin IDs

bitcoin, ethereum, tether, ripple, cardano, dogecoin, solana, polkadot, avalanche-2, chainlink
