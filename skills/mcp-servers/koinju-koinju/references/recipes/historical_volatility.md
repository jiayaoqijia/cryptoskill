# Historical Volatility

<!-- Synced from `api/python_vs_sql/historical_volatility/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Historical Volatility (Deribit Insights / cryptarbitrage)

- **Article**: https://insights.deribit.com/dev-hub/historical-volatility-calculations-python-code/
- **Companion code**: https://github.com/cryptarbitrage-code/historical-volatility-calculations

## What it computes

Historical realised volatility on Bitcoin daily candles, two ways:

1. **Close-to-close** — σ over a rolling window of daily log returns
   `ln(close[t] / close[t-1])`, annualised by `√365` (crypto trades 365
   sessions/year, not 252).
2. **Parkinson** — exploits intraday range:
   `σ_P = √( (1 / (4·N·ln2)) · Σ ln(H/L)² ) · √365`. Lower variance estimator
   than close-to-close because it uses the high and low.

Both are reported for rolling windows of 7, 30, 60, 90 and 180 days. The article's
GUI and multi-window plotting code is out of scope — we keep just the maths. We
focus the published example on the **30-day window** (most common reference for
realised vol) but the SQL trivially extends to the other windows.

## Source data swap

Original code reads daily OHLC from a Yahoo Finance CSV (`BTC-USD`). The
condensed Python and the SQL both read from `api.ohlcv(candle_duration_in_minutes
= 1440)` with `exchange = 'binance'` and `market = 'BTC-USDT'`.

## Parity-test pin

Parity uses a fixed historical window (`2024-01-01` → `2024-12-31`) so the
result is deterministic across runs. The GitBook page shows the relative
`now() - interval N month` form for copy-paste use.

## Numerical conventions

- Sample standard deviation (`ddof=1` in NumPy / `stddevSamp` in ClickHouse).
- Skip the article's quirky first row treatment (`ln(close[0]/open[0])`) — it
  only affects the very first day and is not representative of a rolling-vol
  estimator. Our window starts once we have N close-to-close returns.

# Historical volatility — Python vs SQL

**Source article**: [Deribit Insights — Historical volatility calculations (Python)](https://insights.deribit.com/dev-hub/historical-volatility-calculations-python-code/)
**Reference repo**: [cryptarbitrage-code/historical-volatility-calculations](https://github.com/cryptarbitrage-code/historical-volatility-calculations)
**Published doc**: [`sql-cookbook/historical-volatility`](https://docs.koinju.io/sql-cookbook/historical-volatility)

## Why SQL

The original article reads a year of daily OHLC into pandas and computes
30-day rolling close-to-close + Parkinson volatilities — about 80 lines of
Python (excluding the Tkinter GUI). The SQL version replaces all of it with
a single ~25-line query that runs server-side in under a second.

| | Lines | Notes |
|---|---|---|
| Original Python | ~80 | NumPy loops, pandas-friendly DataFrame |
| Condensed Python (`original.py`) | ~50 | Vectorised pandas, koinju as data source |
| ClickHouse SQL (`query.sql`) | ~25 | Single CTE, `stddevSamp` + window sum |

## Running the parity test

The parity test compares the condensed Python pipeline and the SQL query on
the same input window (`2024-01-01` → `2024-12-31`) and asserts agreement
within `1e-9` per cell.

```bash
KOINJU_SQL_USER=<user> KOINJU_SQL_PASSWORD=<pass> \
    uv run pytest api/python_vs_sql/historical_volatility/ -m parity
```

Use the `api_gw_biz` user from the `api_sql_users` AWS secret (or any tier
that grants enough rows for one year of daily candles).

## ClickHouse SQL

```sql
WITH
    '2024-01-01' AS start_date,
    '2024-12-31' AS end_date,
    30 AS window_days,
    365 AS sessions_per_year,
    candles AS (
        SELECT toDate(start) AS day, open, high, low, close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = 'binance'
          AND market = 'BTC-USDT'
          AND start >= start_date
          AND start <= end_date
    ),
    returns AS (
        SELECT day, high, low, close,
               ln(close / nullIf(lagInFrame(close, 1) OVER (ORDER BY day), 0)) AS log_return,
               pow(ln(high / low), 2) AS hl_log_sq
        FROM candles
    ),
    vols AS (
        SELECT day,
               stddevSamp(log_return) OVER w * sqrt(sessions_per_year) * 100 AS vol_30d_cc_pct,
               sqrt(sum(hl_log_sq) OVER w / (4 * window_days * ln(2))) * sqrt(sessions_per_year) * 100 AS vol_30d_park_pct,
               count(log_return) OVER w AS valid_returns
        FROM returns
        WINDOW w AS (ORDER BY day ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
    )
SELECT day, vol_30d_cc_pct, vol_30d_park_pct
FROM vols
WHERE valid_returns = window_days
ORDER BY day
```

## Python reference implementation

```python
"""Condensed Python reference for Deribit Insights' historical-volatility article.

Pinned to a deterministic window so the parity test is stable. Reads BTC-USDT
daily candles from the koinju SQL API and reports the rolling 30-day
close-to-close and Parkinson volatilities, annualised by sqrt(365).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGE = "binance"
MARKET = "BTC-USDT"
START = "2024-01-01"
END = "2024-12-31"
WINDOW = 30
SESSIONS_PER_YEAR = 365


def fetch_daily_candles(client: Client) -> pd.DataFrame:
    query = f"""
        SELECT toDate(start) AS day, open, high, low, close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = '{EXCHANGE}'
          AND market = '{MARKET}'
          AND start >= '{START}'
          AND start <= '{END}'
        ORDER BY day
    """
    df = client.query_df(query)
    return df.astype({"open": float, "high": float, "low": float, "close": float})


def compute_volatilities(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df["hl_log_sq"] = np.log(df["high"] / df["low"]) ** 2

    df["vol_30d_cc_pct"] = (
        df["log_return"].rolling(WINDOW).std(ddof=1) * np.sqrt(SESSIONS_PER_YEAR) * 100
    )

    parkinson_factor = 1.0 / (4.0 * WINDOW * np.log(2.0))
    df["vol_30d_park_pct"] = (
        np.sqrt(parkinson_factor * df["hl_log_sq"].rolling(WINDOW).sum())
        * np.sqrt(SESSIONS_PER_YEAR)
        * 100
    )

    return df.dropna(subset=["vol_30d_cc_pct", "vol_30d_park_pct"]).reset_index(
        drop=True
    )[["day", "vol_30d_cc_pct", "vol_30d_park_pct"]]


def run(client: Client) -> pd.DataFrame:
    return compute_volatilities(fetch_daily_candles(client))
```
