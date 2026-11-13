# Mean Reversion Zscore

<!-- Synced from `api/python_vs_sql/mean_reversion_zscore/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Mean reversion z-score (Hanane D.)

- **Article**: https://machinelearning-basics.com/mean-reversion-trading-strategy-using-python/

## What we compute

A standard **20-day rolling z-score** signal for mean-reversion trades:

```
ma_20[t]   = mean of close[t-19 … t]
std_20[t]  = sample std of close[t-19 … t]   (ddof = 1)
zscore[t]  = (close[t] - ma_20[t]) / std_20[t]
signal[t]  = +1 if zscore < -1.25  (oversold → long)
             -1 if zscore > +1.25  (overbought → short)
              0 otherwise
```

The threshold ±1.25 follows the article's Implementation 2. The first
19 rows of the window aren't yet "full"; we drop them.

## Source data swap

The article uses Yahoo Finance daily NFLX. We retarget to
**`binance/BTC-USDT`** daily candles for cross-page consistency with
HV / Sortino / Calmar / Correlation / DCA. Methodology unchanged.

## What we keep / drop from the article

- **Keep**: Implementation 2 — the rolling 20-day z-score with
  ±1.25 thresholds and integer signal (`+1` long, `-1` short, `0` flat).
- **Drop**: Implementation 1 (the simpler "above-or-below MA" sign rule
  — too trivial for a separate doc page) and Implementation 3 (pair
  trading on AAPL/GOOG spread — different concept worth its own page).
- **Drop the cumulative-strategy-return backtest plot** — that's an
  evaluation step on top of the signal, not the core SQL win. Could
  be a follow-up doc page combining this query with the
  [Calmar](max-drawdown-calmar.md) running-peak pattern.

## Why pop std vs sample std matters here

The Notion prototype used `stddevPop`. The article actually uses
pandas `.rolling(20).std()` which defaults to `ddof = 1` (sample std,
Bessel-corrected). Difference is `√(n/(n−1)) ≈ 1.026` for `n = 20` —
small but visible. Our parity test would fail at `1e-9` if we mixed
them. We use `stddevSamp` to match pandas exactly.

## Parity-test pin

Window: `2024-01-01` → `2024-12-31`. With a 20-day rolling lookback,
the first 19 of the 366 daily rows are dropped — output is **347 rows
× 6 columns**.

# Mean reversion z-score — Python vs SQL

**Source article**: [Hanane D. — Mean Reversion Trading Strategy Using Python](https://machinelearning-basics.com/mean-reversion-trading-strategy-using-python/)
**Published doc**: [`sql-cookbook/mean-reversion-zscore`](https://docs.koinju.io/sql-cookbook/mean-reversion-zscore)

## Why SQL

The article's Implementation 2 chains pandas
`rolling(20).mean()` + `rolling(20).std()` + a vectorised `np.where`
threshold. Short-ish in pandas (~10 lines), but the SQL equivalent is
roughly the same length and replaces the hidden `min_periods` /
`dropna` complexity with one explicit `count(*) OVER w =
window_size` filter. Plus it runs against `api.ohlcv(...)` directly —
no client-side data fetch, no pandas, no NumPy.

Notable: Notion's prototype used `stddevPop`, which is *wrong* against
the article's pandas default. We use `stddevSamp` (`ddof = 1`) — the
parity test would fail at `1e-9` otherwise.

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/mean_reversion_zscore/ -m parity
```

The test compares the 347-row time series (2024-01-01 → 2024-12-31,
first 19 days dropped because rolling-20 hasn't filled) between the
Python pipeline (pandas `rolling` + `np.where`) and the SQL query,
asserting agreement to `1e-9` per cell across `day, close, ma_20,
std_20, zscore, signal`.

## ClickHouse SQL

```sql
WITH
    '2024-01-01' AS start_date,
    '2024-12-31' AS end_date,
    20 AS window_size,
    1.25 AS n_std,
    candles AS (
        SELECT toDate(start) AS day, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = 'binance'
          AND market = 'BTC-USDT'
          AND start BETWEEN start_date AND end_date
    ),
    z AS (
        SELECT day, close,
               avg(close) OVER w AS ma_20,
               stddevSamp(close) OVER w AS std_20,
               (close - avg(close) OVER w) / nullIf(stddevSamp(close) OVER w, 0) AS zscore,
               count(*) OVER w AS valid_rows
        FROM candles
        WINDOW w AS (ORDER BY day ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)
    )
SELECT day, close, ma_20, std_20, zscore,
       if(zscore < -n_std, 1, if(zscore > n_std, -1, 0)) AS signal
FROM z
WHERE valid_rows = window_size
ORDER BY day
```

## Python reference implementation

```python
"""Condensed Python reference for Hanane D.'s mean-reversion z-score article."""

from __future__ import annotations

import numpy as np
import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGE = "binance"
MARKET = "BTC-USDT"
START = "2024-01-01"
END = "2024-12-31"
WINDOW = 20
N_STD = 1.25


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


def compute_zscore_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("day").reset_index(drop=True)
    df["ma_20"] = df["close"].rolling(window=WINDOW).mean()
    df["std_20"] = df["close"].rolling(window=WINDOW).std(ddof=1)
    df["zscore"] = (df["close"] - df["ma_20"]) / df["std_20"]
    df["signal"] = np.where(
        df["zscore"] < -N_STD, 1, np.where(df["zscore"] > N_STD, -1, 0)
    ).astype("int64")
    return df.dropna(subset=["zscore"]).reset_index(drop=True)[
        ["day", "close", "ma_20", "std_20", "zscore", "signal"]
    ]


def run(client: Client) -> pd.DataFrame:
    return compute_zscore_signals(fetch_daily_closes(client))
```
