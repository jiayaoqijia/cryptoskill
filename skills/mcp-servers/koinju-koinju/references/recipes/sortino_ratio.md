# Sortino Ratio

<!-- Synced from `api/python_vs_sql/sortino_ratio/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Sortino ratio (Codearmo)

- **Article**: https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python

## Why this page

The article covers Sharpe + Sortino + Calmar in one go. Sharpe is already
documented in
[`sql-cookbook/backtesting-simple-sma-strategy.md`](https://docs.koinju.io/sql-cookbook/backtesting-simple-sma-strategy).
This subdirectory backs the **Sortino-only** GitBook page; max-drawdown +
Calmar lives in `../max_drawdown_calmar/`.

## What we compute

Annualised Sortino ratio on a daily-return series:

```
sortino = (E[r] · N − r_f) / (σ_neg · √N)
```

where `r` is the daily simple return (`pct_change`), `σ_neg` is the sample
std of just the negative subset of `r`, `N = 365` (crypto sessions/year),
and `r_f = 0` (we drop the risk-free term — easy to add back if needed).

## Source data swap

Codearmo uses 5 US stocks (AAPL, AMZN, MSFT, GOOGL, FB) over Jan 2013 →
Oct 2020 via `pandas_datareader` / Yahoo Finance. We retarget to a single
crypto (`binance/BTC-USDT`) over a fixed historical window for parity
stability. The methodology is the same — applying `pct_change`, then
filtering negatives for the denominator.

## Parity-test pin

Window: `2024-01-01` → `2024-12-31`. Single-pass scalar result (one row).

## Numerical conventions

- **Simple returns** (`(close − close[t-1]) / close[t-1]`) to match the
  article's `pct_change()` rather than log returns.
- **Sample std** (`ddof=1` / `stddevSamp`) to match `pandas.Series.std()`'s
  default.
- `r_f = 0`, `N = 365`. The doc page mentions the formula extension if a
  caller wants to subtract a non-zero risk-free rate.

# Sortino ratio — Python vs SQL

**Source article**: [Codearmo — Sharpe, Sortino and Calmar Ratios with Python](https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python)
**Published doc**: [`sql-cookbook/sortino-ratio`](https://docs.koinju.io/sql-cookbook/sortino-ratio)

## Why SQL

The Codearmo article computes Sharpe / Sortino / Calmar on a 5-stock
universe (FAANG) using `pandas_datareader` + `yfinance`. We split the
article into two SQL examples:

- **Sortino** (this page) — see also `../max_drawdown_calmar/`.
- Sharpe is already documented in
  [`backtesting-simple-sma-strategy.md`](https://docs.koinju.io/sql-cookbook/backtesting-simple-sma-strategy).

The article's `df.apply(metric_fn, axis=0)` over multiple columns
collapses to a single SQL `GROUP BY market` — no manual loop, no pandas.

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/sortino_ratio/ -m parity
```

## ClickHouse SQL

```sql
WITH
    '2024-01-01' AS start_date,
    '2024-12-31' AS end_date,
    365 AS sessions_per_year,
    0.01 AS risk_free_rate,
    candles AS (
        SELECT toDate(start) AS day, market, toFloat64(close) AS close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = 'binance'
          AND market IN ('BTC-USDT', 'ETH-USDT', 'SOL-USDT', 'ADA-USDT', 'DOGE-USDT')
          AND start BETWEEN start_date AND end_date
    ),
    market_returns AS (
        SELECT day, market,
               close / lagInFrame(toNullable(close), 1) OVER (PARTITION BY market ORDER BY day) - 1 AS ret
        FROM candles
    ),
    all_returns AS (
        SELECT day, market, ret FROM market_returns WHERE ret IS NOT NULL
        UNION ALL
        SELECT day, 'PORTFOLIO' AS market, avg(ret) AS portfolio_ret
        FROM market_returns WHERE ret IS NOT NULL GROUP BY day
    )
SELECT market,
       (avg(ret) * sessions_per_year - risk_free_rate)
       / (stddevSamp(if(ret < 0, ret, NULL)) * sqrt(sessions_per_year)) AS sortino
FROM all_returns
GROUP BY market
ORDER BY market
```

## Python reference implementation

```python
"""Condensed Python reference for Codearmo's Sortino ratio.

Multi-asset version: ranks 5 crypto majors plus an equal-weight portfolio,
mirroring the article's FAANG bar-chart structure.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGE = "binance"
MARKETS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ADA-USDT", "DOGE-USDT"]
START = "2024-01-01"
END = "2024-12-31"
SESSIONS_PER_YEAR = 365
RISK_FREE_RATE = 0.01


def fetch_daily_closes(client: Client) -> pd.DataFrame:
    markets_csv = ", ".join(f"'{m}'" for m in MARKETS)
    query = f"""
        SELECT toDate(start) AS day, market, close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = '{EXCHANGE}'
          AND market IN ({markets_csv})
          AND start >= '{START}'
          AND start <= '{END}'
        ORDER BY day, market
    """
    df = client.query_df(query)
    return df.astype({"close": float})


def _sortino(rets: pd.Series) -> float:
    mean_annual = rets.mean() * SESSIONS_PER_YEAR - RISK_FREE_RATE
    downside_std_annual = rets[rets < 0].std(ddof=1) * np.sqrt(SESSIONS_PER_YEAR)
    return mean_annual / downside_std_annual


def compute_sortinos(df: pd.DataFrame) -> pd.DataFrame:
    wide = df.pivot(index="day", columns="market", values="close").astype(float)
    returns = wide.pct_change().dropna()
    returns["PORTFOLIO"] = returns.mean(axis=1)
    sortinos = returns.apply(_sortino, axis=0)
    return (
        sortinos.reset_index()
        .rename(columns={"index": "market", 0: "sortino"})
        .sort_values("market")
        .reset_index(drop=True)
    )


def run(client: Client) -> pd.DataFrame:
    return compute_sortinos(fetch_daily_closes(client))
```
