---
name: cdcx-market-intel
description: Fetch and analyze market data — prices, orderbook depth, candles, recent trades
---

# Market Intelligence

## When to Use

- User asks for current price, price history, or market conditions for a crypto instrument
- Need to assess liquidity (orderbook depth) before placing an order
- Building a market summary or watchlist
- Comparing prices across multiple instruments

## Tools Used

| Tool                           | Purpose                                   |
|--------------------------------|-------------------------------------------|
| cdcx_market_ticker             | Current price for one or all instruments  |
| cdcx_market_book               | Orderbook depth                           |
| cdcx_market_candlestick        | Historical OHLCV bars                     |
| cdcx_market_trades             | Recent public trades                      |
| cdcx_market_instruments        | All tradable instruments and metadata     |
| cdcx_market_valuations         | Mark / index / funding values             |
| cdcx_market_settlement_prices  | Settlement prices for expired contracts   |
| cdcx_market_insurance          | Insurance Fund balance by currency        |
| cdcx_market_risk_params        | Smart Cross Margin risk parameters        |

All tools are read-only (no auth required, no acknowledgement needed).

## Workflow

### Single Instrument Price

```
cdcx market ticker BTC_USDT -o json
```

Returns: `last`, `b` (best bid), `k` (best ask), `h`/`l` (24h high/low), `v` (volume), `c` (24h change ratio — multiply by 100 for percent).

### All Tickers (Market Scan)

```
cdcx market ticker -o json
```

Omit the instrument argument to get every tradable instrument in one call. Ideal for market scans, watchlists, or computing leaders/laggards.

### Orderbook Depth

```
cdcx market book BTC_USDT --depth 10 -o json
```

`--depth` caps at 50. Use for liquidity assessment before sizing a trade: sum top-N asks for a worst-case buy-through price.

### Candlestick History

```
cdcx market candlestick BTC_USDT --timeframe 1h --count 24 -o json
```

Supported timeframes: `1m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1D, 7D, 14D, 1M`. Use `--start-ts` / `--end-ts` (Unix seconds) for explicit windows. Default window is 1 day.

### Recent Trades

```
cdcx market trades BTC_USDT -o json
```

Last prints, up to 7 days back. Useful for spotting large prints or sudden activity.

### Instrument Metadata

```
cdcx market instruments -o json
```

Returns every instrument with: `instrument_name`, `base_ccy`, `quote_ccy`, `quantity_tick_size`, `price_tick_size`, `min_quantity`, `max_quantity`, `tradable`. Essential before placing any order — the price/quantity you submit must conform to these tick sizes.

### Composite Market Snapshot

```
cdcx market ticker BTC_USDT          # current price
cdcx market book BTC_USDT --depth 5  # liquidity snapshot
cdcx market candlestick BTC_USDT --timeframe 1D --count 7  # weekly trend
cdcx market trades BTC_USDT          # recent activity
```

Combine into a one-shot briefing for the user.

### Derivatives-Only

```
cdcx market valuations BTC-PERP --valuation-type mark_price -o json
cdcx market settlement-prices BTC-PERP -o json
cdcx market insurance USDT -o json
cdcx market risk-params -o json
```

Only relevant for perpetual/futures instruments.

## Streaming

For continuous updates prefer `cdcx stream` over polling:

```
cdcx stream ticker BTC_USDT ETH_USDT  # NDJSON to stdout
cdcx stream book BTC_USDT
cdcx stream trades BTC_USDT
```

Stream commands print one JSON object per line. Ctrl+C to stop.

## Notes

- Prices in the API are strings — cast to float/decimal before arithmetic
- `c` in ticker is a ratio, not a percentage: `0.0257` means +2.57%
- Instrument names: spot uses `_USDT` (e.g. `BTC_USDT`), perps use `-PERP` (e.g. `BTC-PERP`)
- All market data endpoints are public — no credentials needed
