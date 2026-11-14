---
name: trading-data
description: Fetch price history (OHLCV bars) and quotes for stocks, ETFs, indices, forex, futures and crypto in any market - free via Yahoo Finance with no API key, from local CSV files, or from a broker feed. Use when the user asks for a price, chart data, historical candles, intraday bars, wants to download or export data to CSV, or when another skill needs data. Handles daily, weekly, monthly and intraday intervals.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Market Data (`trading-data`)

The data layer for the whole pack. Every other skill fetches through the same provider and cache.

Run from this skill's directory: `python3 scripts/data.py <command>`.

## Commands

```bash
python3 scripts/data.py bars AAPL --interval 1d --period 1y          # last 10 rows + summary
python3 scripts/data.py bars BTC-USD --interval 1h --period 1mo --out btc_1h.csv
python3 scripts/data.py bars 7203.T --start 2019-01-01 --json --all  # full JSON
python3 scripts/data.py quote AAPL ^GSPC EURUSD=X GC=F               # latest prices
python3 scripts/data.py many --universe watchlist.txt --period 2y --out-dir data/
python3 scripts/data.py clear-cache
```

Intervals: `1m 2m 5m 15m 30m 60m 1h 1d 1wk 1mo`. Periods: `1d 5d 1mo 3mo 6mo 1y 2y 5y 10y max`
(or `--start/--end YYYY-MM-DD`). Yahoo limits intraday history (1m: 7 days, 5-30m: 60 days, 1h: ~2 years).

## Symbols (Yahoo conventions)

- Stocks: `AAPL`, `SHEL.L`, `RY.TO`, `INFY.NS`, `RELIANCE.BO`, `7203.T`, `0700.HK`, `BHP.AX`, `SAP.DE`
- Indices: `^GSPC`, `^NDX`, `^FTSE`, `^N225`, `^NSEI`, `^GDAXI`, `^HSI`
- FX: `EURUSD=X`, `USDJPY=X`  - Futures: `ES=F`, `GC=F`, `CL=F`  - Crypto: `BTC-USD`, `ETH-USD`
- Kite provider: `EXCHANGE:SYMBOL`, e.g. `NSE:INFY`

If a symbol fails, suggest the likely Yahoo spelling (exchange suffix) and retry once.

## Providers

| provider | key needed | notes |
|---|---|---|
| `yahoo` (default) | no | unofficial endpoint; daily bars split/dividend adjusted; may be delayed or rate-limited |
| `csv` | no | `data.csv_dir/SYMBOL.csv` with `date,open,high,low,close,volume` (column names flexible) |
| `kite` | Kite Connect data plan | unadjusted candles; `EXCHANGE:SYMBOL` symbols |

Switch with `trading-setup`: `setup.py set data.provider csv`. Override per call with `--provider`.

Cache: `~/.trading-skills/cache/`, TTL `data.cache_ttl_minutes` (60). Use `--no-cache` for fresh prices.

## Guardrails

- Always state the data source and the last bar's date when quoting numbers.
- Free data can be delayed or wrong. Before any live order, the price must be checked against the broker.
- Do not hammer the free endpoint: use `many` (4 workers) rather than looping hundreds of single calls.
