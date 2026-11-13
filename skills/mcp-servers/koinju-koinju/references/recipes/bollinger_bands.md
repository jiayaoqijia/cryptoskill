# Bollinger Bands

<!-- Synced from `api/python_vs_sql/bollinger_bands/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Bollinger Bands (deepml1818)

- **Article**: https://medium.com/@deepml1818/building-a-cryptocurrency-trading-strategy-technical-analysis-with-python-and-ccxt-610de23029cc

## What we compute

Standard 20-period, 2σ **Bollinger Bands** on daily closes:

```
middle_band[t] = mean of close[t-19 … t]
std_20[t]      = population std of close[t-19 … t]   (ddof = 0)
upper_band[t]  = middle_band[t] + 2 · std_20[t]
lower_band[t]  = middle_band[t] − 2 · std_20[t]
signal[t]      = +1 if close < lower_band   (oversold → potential long)
                 −1 if close > upper_band   (overbought → potential short)
                  0 otherwise
```

## Source data swap and basket choice

The article uses ccxt + Huobi 1-minute BTC/USDT for ~10 hours. We
retarget to **`binance/BTC-USDT` daily** for cross-page consistency
with HV / Sortino / Calmar / Correlation / DCA / Mean reversion.

## What we keep / drop from the article

The article computes **MACD, RSI, Bollinger, Donchian** all in one
pass via TA-Lib. We keep just **Bollinger** here — RSI / MACD /
Donchian could each be their own doc page if needed (none of them
benefit from collapsing into a single SQL block; each is a clean
window-function expression).

We also drop the boolean "signal table" pattern and replace it with
a single integer `signal` column (matching the Mean reversion z-score
page's convention).

## Why pop std (not sample) for Bollinger

The canonical Bollinger Bands definition uses the **population**
standard deviation, and TA-Lib's `BBANDS()` follows that — it divides
by `N`, not `N - 1`. Pandas' `.rolling(N).std()` defaults to
`ddof = 1` (sample), so the reproducible Python uses
`.rolling(20).std(ddof=0)` explicitly.

Difference is `√(N / (N − 1)) ≈ 1.026` for `N = 20` — small
numerically but the parity test would fail at `1e-9` if pop / sample
were mixed.

## Parity-test pin

Window: `2024-01-01` → `2024-12-31`. With a 20-period rolling
lookback, the first 19 of the 366 daily rows are dropped — output is
**347 rows × 6 columns**.

# Bollinger Bands — Python vs SQL

**Source article**: [deepml1818 — Building a Cryptocurrency Trading Strategy: Technical Analysis with Python and CCXT](https://medium.com/@deepml1818/building-a-cryptocurrency-trading-strategy-technical-analysis-with-python-and-ccxt-610de23029cc)
**Published doc**: [`sql-cookbook/bollinger-bands`](https://docs.koinju.io/sql-cookbook/bollinger-bands)

## Why SQL

The article computes MACD, RSI, Bollinger and Donchian via TA-Lib in
a tight Python loop. We pull just the **Bollinger** half here — RSI,
MACD, Donchian could each be their own page if needed (each is one
or two window functions away).

The SQL replaces TA-Lib's `BBANDS()` call with one CTE chain:
`avg(close) OVER w` for the middle band, `± n_std · stddevPop(close)
OVER w` for the upper / lower bands, plus an `if/elif/else` for the
band-cross signal column.

Notable: TA-Lib uses **population** std (`ddof = 0`), not the
pandas-default sample std. We use `stddevPop` and explicitly
`.rolling(20).std(ddof=0)` to match — same parity-test gotcha as
mean-reversion z-score, just inverted.

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/bollinger_bands/ -m parity
```

The test compares the 347-row time series (2024-01-01 → 2024-12-31,
first 19 days dropped because rolling-20 hasn't filled) between the
Python pipeline (pandas `rolling` + `np.where`) and the SQL query,
asserting agreement to `1e-9` per cell across `day, close, middle_band,
upper_band, lower_band, signal`.

## ClickHouse SQL

```sql
WITH
    '2024-01-01' AS start_date,
    '2024-12-31' AS end_date,
    20 AS window_size,
    2.0 AS n_std,
    candles AS (
        SELECT toDate(start) AS day, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = 'binance'
          AND market = 'BTC-USDT'
          AND start BETWEEN start_date AND end_date
    ),
    bands AS (
        SELECT day, close,
               avg(close) OVER w AS middle_band,
               avg(close) OVER w + n_std * stddevPop(close) OVER w AS upper_band,
               avg(close) OVER w - n_std * stddevPop(close) OVER w AS lower_band,
               count(*) OVER w AS valid_rows
        FROM candles
        WINDOW w AS (ORDER BY day ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)
    )
SELECT day, close, middle_band, upper_band, lower_band,
       if(close < lower_band, 1, if(close > upper_band, -1, 0)) AS signal
FROM bands
WHERE valid_rows = window_size
ORDER BY day
```

## Python reference implementation

```python
"""Condensed Python reference for deepml1818's Bollinger Bands article."""

from __future__ import annotations

import numpy as np
import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGE = "binance"
MARKET = "BTC-USDT"
START = "2024-01-01"
END = "2024-12-31"
WINDOW = 20
N_STD = 2.0


def fetch_daily_closes(client: Client) -> pd.DataFrame:
    query = f"""
        SELECT toDate(start) AS day, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = '{EXCHANGE}'
          AND market = '{MARKET}'
          AND start >= '{START}'
          AND start <= '{END}'
        ORDER BY day
    """
    return client.query_df(query)


def compute_bollinger(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("day").reset_index(drop=True)
    df["middle_band"] = df["close"].rolling(window=WINDOW).mean()
    std_20 = df["close"].rolling(window=WINDOW).std(ddof=0)
    df["upper_band"] = df["middle_band"] + N_STD * std_20
    df["lower_band"] = df["middle_band"] - N_STD * std_20
    df["signal"] = np.where(
        df["close"] < df["lower_band"],
        1,
        np.where(df["close"] > df["upper_band"], -1, 0),
    ).astype("int64")
    return df.dropna(subset=["middle_band"]).reset_index(drop=True)[
        ["day", "close", "middle_band", "upper_band", "lower_band", "signal"]
    ]


def run(client: Client) -> pd.DataFrame:
    return compute_bollinger(fetch_daily_closes(client))
```
