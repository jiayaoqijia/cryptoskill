# Spot Futures Perp Spreads

<!-- Synced from `api/python_vs_sql/spot_futures_perp_spreads/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Spot / Futures / Perp Spreads (Sigma Quantiphi)

- **Article**: https://medium.com/@sigmaquantiphi/visualizing-bitcoin-spot-futures-and-perpetual-spreads-with-cryptopandas-ccxt-and-plotly-13bb8abe8a32

## What we compute

For each derivative BTC contract, the daily-close **price spread**
(absolute and percent) against the spot reference `binance/BTC-USDT`:

```
spread[t, c]      = close[t, c]     − close[t, spot]
spread_pct[t, c]  = spread[t, c]    / close[t, spot] × 100
```

Per-contract time series, all aligned on the same `day`. Long format:
one row per `(day, contract)` pair.

## Source data swap and basket choice

The article uses CryptoPandas + CCXT to enumerate every BTC pair on
Binance (USDT, USDC, USD; spot, linear/inverse future, linear/inverse
swap) and plots all spreads against `BTC/USDT` spot. That's >15
contracts at hourly resolution.

We pick a **representative four-contract basket** on the binance
ecosystem that captures the article's structure (one contract per
derivative type) without bloating the doc:

| Contract                     | Exchange               | Market               | Type            |
| ---------------------------- | ---------------------- | -------------------- | --------------- |
| Spot                         | `binance`              | `BTC-USDT`           | reference (spread = 0) |
| USDM perpetual swap          | `binance-usdm-future`  | `BTC-USDT`           | linear perp     |
| Coin-M perpetual swap        | `binance-coinm-future` | `BTC-USD-PERP`       | inverse perp    |
| USDM quarterly future        | `binance-usdm-future`  | `BTC-USDT-2025-03-28`| linear future   |

Daily candles instead of hourly — for cross-page consistency and
because the spread structure is well visible at daily granularity
(intraday noise dominates at hourly).

## What we keep / drop

**Keep**: the per-contract spread to a spot reference — that's the
chart the article builds in `cryptopandas + plotly`.

**Drop**:
- The **stacked-volume sub-chart** — same data, different presentation;
  trivially added back as another column or sibling SELECT.
- The **plotly visualisation infrastructure** — out of scope for a
  SQL-translation doc.
- The **dynamic market enumeration via CCXT `load_markets()`** — we
  hard-code four representative contracts. The SQL is happy with as
  many `IN (...)` entries as you want.

## Parity-test pin

Window: **`2024-12-01` → `2024-12-31`** (31 daily rows). Output is
`31 days × 3 derivative contracts = 93 rows × 7 columns`
(`day, exchange, market, close, spot_close, spread, spread_pct`). The
spot row itself is excluded from the output (its spread vs itself is
identically zero).

## Numerical conventions

- Daily candles, close prices.
- Inner-JOIN against the spot CTE on `day` — derivatives without a
  matching spot day are dropped. With our pinned window every contract
  has all 31 days, so this is a no-op for the test, but the right
  behaviour if a contract was listed mid-period.
- Inverse perpetual (`BTC-USD-PERP` on `binance-coinm-future`) trades
  in USD-per-BTC just like the linear contracts, so the `close - spot`
  arithmetic is unit-consistent. (The "inverse" naming is about the
  **margin currency**, not the quote.)

# Spot / Futures / Perp Spreads — Python vs SQL

**Source article**: [Sigma Quantiphi — Visualizing Bitcoin Spot, Futures and Perpetual Spreads with CryptoPandas, CCXT, and Plotly](https://medium.com/@sigmaquantiphi/visualizing-bitcoin-spot-futures-and-perpetual-spreads-with-cryptopandas-ccxt-and-plotly-13bb8abe8a32)
**Published doc**: [`sql-cookbook/spot-futures-perp-spreads`](https://docs.koinju.io/sql-cookbook/spot-futures-perp-spreads)

## Why SQL

The article enumerates every BTC contract on Binance via
`cryptopandas.load_markets()`, fetches them one-symbol-at-a-time over
ccxt, merges spot back in as a reference column, computes the spread,
then renders a Plotly dual-subplot. Most of the code is data-shaping
plumbing — fetch, concat, merge.

The SQL version puts the entire fetch + align + diff in a single CTE
chain (~22 lines): one `WHERE` block lists the basket, one inner-JOIN
attaches the spot reference, one final `SELECT` outputs the long-form
spread time series. Visualisation is whatever the consumer wants.

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/spot_futures_perp_spreads/ -m parity
```

The test compares the 93-row spread time series (Dec 2024, 4-contract
basket — 1 spot + 3 derivatives, with the spot row excluded) between
the Python pipeline (pandas merge + arithmetic) and the SQL inner-JOIN,
asserting agreement to `1e-9` per cell across `day, exchange, market,
close, spot_close, spread, spread_pct`.

## ClickHouse SQL

```sql
WITH
    '2024-12-01' AS start_date,
    '2024-12-31' AS end_date,
    candles AS (
        SELECT toDate(start) AS day, exchange, market, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE (
                  (exchange = 'binance' AND market = 'BTC-USDT')
               OR (exchange = 'binance-usdm-future' AND market IN ('BTC-USDT', 'BTC-USDT-2025-03-28'))
               OR (exchange = 'binance-coinm-future' AND market = 'BTC-USD-PERP')
              )
          AND start BETWEEN start_date AND end_date
    ),
    spot AS (
        SELECT day, close AS spot_close
        FROM candles
        WHERE exchange = 'binance' AND market = 'BTC-USDT'
    )
SELECT c.day, c.exchange, c.market,
       c.close, s.spot_close,
       c.close - s.spot_close AS spread,
       (c.close - s.spot_close) / s.spot_close * 100 AS spread_pct
FROM candles c
JOIN spot s ON c.day = s.day
WHERE NOT (c.exchange = 'binance' AND c.market = 'BTC-USDT')
ORDER BY c.day, c.exchange, c.market
```

## Python reference implementation

```python
"""Condensed Python reference for Sigma Quantiphi's spot/futures/perp article.

Daily spread time series of representative BTC derivative contracts
against the binance BTC-USDT spot reference.
"""

from __future__ import annotations

import pandas as pd
from clickhouse_connect.driver import Client

START = "2024-12-01"
END = "2024-12-31"

# (exchange, market) basket; first entry is the spot reference.
BASKET = [
    ("binance", "BTC-USDT"),
    ("binance-usdm-future", "BTC-USDT"),
    ("binance-coinm-future", "BTC-USD-PERP"),
    ("binance-usdm-future", "BTC-USDT-2025-03-28"),
]
SPOT_EXCHANGE, SPOT_MARKET = BASKET[0]


def fetch_daily_closes(client: Client) -> pd.DataFrame:
    pairs = " OR ".join(f"(exchange = '{ex}' AND market = '{mk}')" for ex, mk in BASKET)
    query = f"""
        SELECT toDate(start) AS day, exchange, market, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE ({pairs})
          AND start BETWEEN '{START}' AND '{END}'
        ORDER BY day, exchange, market
    """
    return client.query_df(query)


def compute_spreads(df: pd.DataFrame) -> pd.DataFrame:
    spot = df[(df["exchange"] == SPOT_EXCHANGE) & (df["market"] == SPOT_MARKET)][
        ["day", "close"]
    ].rename(columns={"close": "spot_close"})
    merged = df.merge(spot, on="day", how="inner")
    derivatives = merged[
        ~((merged["exchange"] == SPOT_EXCHANGE) & (merged["market"] == SPOT_MARKET))
    ].copy()
    derivatives["spread"] = derivatives["close"] - derivatives["spot_close"]
    derivatives["spread_pct"] = derivatives["spread"] / derivatives["spot_close"] * 100
    return (
        derivatives[
            [
                "day",
                "exchange",
                "market",
                "close",
                "spot_close",
                "spread",
                "spread_pct",
            ]
        ]
        .sort_values(["day", "exchange", "market"])
        .reset_index(drop=True)
    )


def run(client: Client) -> pd.DataFrame:
    return compute_spreads(fetch_daily_closes(client))
```
