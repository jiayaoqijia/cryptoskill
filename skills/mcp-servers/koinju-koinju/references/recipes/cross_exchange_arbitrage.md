# Cross Exchange Arbitrage

<!-- Synced from `api/python_vs_sql/cross_exchange_arbitrage/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Cross-exchange arbitrage (maxme)

- **Article / repo**: https://github.com/maxme/bitcoin-arbitrage (~2,500 lines of Python — eleven custom exchange-API adapters, threaded fetcher, alert dispatcher)

## What we compute

Per-minute **cross-exchange spread matrix** for `BTC-USDT` across four
top spot venues. For every minute and every ordered exchange pair
`(buy_ex < sell_ex)`, output the spread

```
spread_pct[t, a, b] = (close[t, b] − close[t, a]) / close[t, a] × 100
```

That's exactly the comparison the maxme repo's threaded fetcher
produces — **with the entire 11-exchange adapter stack collapsed into
one self-JOIN**. The article's compute logic, post-fetch, is one
`if spread > threshold: alert(...)` line.

## Source data swap and basket choice

The repo polls 11 exchanges via individual REST-API client classes.
We use **`api.ohlcv(candle_duration_in_minutes = 1)`** for the four
exchanges that have full 1-minute `BTC-USDT` coverage on the test day:
`binance, okx, kucoin, gateio`. C(4, 2) = 6 ordered pairs ×
1,440 minutes = 8,640 rows.

(Adding more exchanges is one entry in the `IN (...)` list — no extra
adapter code, no auth handling, no threading.)

## What we keep / drop from the article

The repo's value is in the **comparison logic** — given simultaneous
prices across N exchanges, pull out the cross-exchange pairs and
their spreads. That's what the SQL self-JOIN handles in 12 lines.

We drop:
- The 11 exchange-API client classes (HTTP wrappers, auth, response
  parsing) — replaced by `api.ohlcv(...)`.
- Threaded fetch coordination — `JOIN` is naturally simultaneous.
- The Slack/IRC alert dispatcher — out of scope for a SQL-translation
  doc, but a simple `WHERE spread_pct > threshold` SELECT covers it.
- Order execution — not a SQL concern.

## Parity-test pin

Window: full **2024-12-31** (1,440 minutes), 4 exchanges. **8,640
output rows × 6 columns**: `start, buy_ex, sell_ex, buy_price,
sell_price, spread_pct`.

`spread_pct` is signed: a row with `buy_ex='binance', sell_ex='okx',
spread_pct=0.05` means okx is 5 bps higher than binance at that
minute. Negative means okx is lower.

## Numerical conventions

- Self-merge / self-JOIN on `start`. The condition `a.exchange <
  b.exchange` is the standard "ordered-pair" trick to avoid
  `(binance, okx)` and `(okx, binance)` both showing up.
- `(b.close − a.close) / a.close · 100` — same in both Python and SQL.
- For test stability across runs, no `LIMIT` / `ORDER BY DESC` — sort
  deterministically by `(start, buy_ex, sell_ex)`. The doc page can
  show the top spreads as a derivative SELECT.

# Cross-exchange arbitrage — Python vs SQL

**Source repo**: [maxme/bitcoin-arbitrage](https://github.com/maxme/bitcoin-arbitrage) (~2,500 lines of Python: 11 exchange-API client classes, threaded fetcher, alert dispatcher)
**Published doc**: [`sql-cookbook/cross-exchange-arbitrage`](https://docs.koinju.io/sql-cookbook/cross-exchange-arbitrage)

## Why SQL

The repo is the canonical "compare prices across many exchanges"
project. The vast majority of its code is plumbing — eleven
hand-written REST clients, JSON parsing, retry logic, threading,
authentication. The actual comparison logic is one self-JOIN.

This is the most one-sided "Python vs SQL" article in the series:
**2,500 → 12 lines, 99 % reduction**. The repo's GitHub stars come
from solving the plumbing, not the maths.

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/cross_exchange_arbitrage/ -m parity
```

The test compares the 8,640-row (1440 min × 6 ordered pairs) spread
matrix between the Python pipeline (pandas self-merge on `start` +
`buy_ex < sell_ex` filter) and the SQL self-JOIN, asserting agreement
to `1e-9` per cell across `start, buy_ex, sell_ex, buy_price,
sell_price, spread_pct`.

## ClickHouse SQL

```sql
WITH
    '2024-12-31' AS day,
    p AS (
        SELECT start, exchange, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1)
        WHERE market = 'BTC-USDT'
          AND exchange IN ('binance', 'okx', 'kucoin', 'gateio')
          AND start >= toDateTime(day)
          AND start <  toDateTime(day) + INTERVAL 1 DAY
    )
SELECT a.start,
       a.exchange AS buy_ex,
       b.exchange AS sell_ex,
       a.close AS buy_price,
       b.close AS sell_price,
       (b.close - a.close) / a.close * 100 AS spread_pct
FROM p a
JOIN p b ON a.start = b.start
WHERE a.exchange < b.exchange
ORDER BY a.start, buy_ex, sell_ex
```

## Python reference implementation

```python
"""Condensed Python reference for maxme's bitcoin-arbitrage repo.

Cross-exchange BTC-USDT spread matrix for one day of 1-minute candles.
"""

from __future__ import annotations

import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGES = ["binance", "okx", "kucoin", "gateio"]
MARKET = "BTC-USDT"
DAY = "2024-12-31"


def fetch_minute_closes(client: Client) -> pd.DataFrame:
    exchanges_csv = ", ".join(f"'{e}'" for e in EXCHANGES)
    query = f"""
        SELECT start, exchange, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1)
        WHERE market = '{MARKET}'
          AND exchange IN ({exchanges_csv})
          AND start >= toDateTime('{DAY}')
          AND start <  toDateTime('{DAY}') + INTERVAL 1 DAY
    """
    return client.query_df(query)


def compute_spreads(df: pd.DataFrame) -> pd.DataFrame:
    a = df.rename(columns={"exchange": "buy_ex", "close": "buy_price"})
    b = df.rename(columns={"exchange": "sell_ex", "close": "sell_price"})
    merged = a.merge(b, on="start", how="inner")
    merged = merged[merged["buy_ex"] < merged["sell_ex"]].copy()
    merged["spread_pct"] = (
        (merged["sell_price"] - merged["buy_price"]) / merged["buy_price"] * 100
    )
    return (
        merged[["start", "buy_ex", "sell_ex", "buy_price", "sell_price", "spread_pct"]]
        .sort_values(["start", "buy_ex", "sell_ex"])
        .reset_index(drop=True)
    )


def run(client: Client) -> pd.DataFrame:
    return compute_spreads(fetch_minute_closes(client))
```
