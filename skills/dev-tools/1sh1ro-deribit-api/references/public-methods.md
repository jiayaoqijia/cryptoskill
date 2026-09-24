# Deribit Public Method Guide

## Base JSON-RPC endpoint

- `POST https://www.deribit.com/api/v2`

## Common methods

- `public/ticker`
- `public/get_volatility_index_data`
- `public/get_book_summary_by_currency`
- `public/get_book_summary_by_instrument`
- `public/get_index_price`
- `public/get_instruments`
- `public/get_order_book`

## Param notes

- `public/get_volatility_index_data`
  - `currency`: `BTC` or `ETH`
  - `start_timestamp`/`end_timestamp`: epoch milliseconds
  - `resolution`: use `3600` for hour bars in reporting

## Parsing notes

- DVOL response data points are arrays:
  - `[timestamp, open, high, low, close]`
- Ticker volume fields are often in `result.stats`.
