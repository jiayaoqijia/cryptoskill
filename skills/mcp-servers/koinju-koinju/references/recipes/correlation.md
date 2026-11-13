# Correlation

<!-- Synced from `api/python_vs_sql/correlation/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Correlation (deepml1818)

- **Article**: https://medium.com/@deepml1818/analyzing-correlations-in-crypto-markets-with-python-8376925ecaec

## What we compute

A pairwise **Pearson correlation matrix** of daily simple returns across
five top-cap crypto majors. The output is a long-form
`(market_a, market_b, correlation)` table — 25 rows for the 5 × 5 matrix,
including the symmetric pairs and the diagonal `corr(x, x) = 1`.

## Source data swap and basket choice

The article uses 4 stocks-tickers via Yahoo Finance: `BTC-USD`, `ETH-USD`,
`LTC-USD`, `BNB-USD` over 2023. We retarget to the same five crypto
majors used in the [Sortino](sortino-ratio.md) and
[Calmar](max-drawdown-calmar.md) pages — `BTC-USDT, ETH-USDT, SOL-USDT,
ADA-USDT, DOGE-USDT` on `binance` — for cross-page consistency. SOL/ADA
are more relevant cycle-leaders today than LTC/BNB; the methodology is
identical.

## What we drop from the article

The article continues into a **pairs-trading strategy** (threshold rule,
trade signals, cumulative P&L). That's a different concept from "compute
the correlation matrix" and is more procedural than SQL-friendly. We
keep just the correlation-matrix half — that's the one-shot SQL win
(`pct_change().corr()` → one query) and the cleanest "Python vs SQL"
demo.

## Parity-test pin

Window: `2024-01-01` → `2024-12-31`. 25-row scalar output.

## Numerical conventions

- **Simple returns** (`pct_change()`) to match the article.
- **Pearson** correlation. Pandas `df.corr()` and ClickHouse `corr()`
  both compute the standard Pearson formula
  `Σ(xᵢ−x̄)(yᵢ−ȳ) / √(Σ(xᵢ−x̄)² · Σ(yᵢ−ȳ)²)` — the `(n−1)` / `n` factors
  cancel out, so sample vs population doesn't apply here.
- Day alignment via `JOIN market_returns a JOIN market_returns b ON
  a.day = b.day` — only days where both markets have a valid return
  contribute, matching pandas' implicit pairwise-complete behaviour.

# Correlation — Python vs SQL

**Source article**: [deepml1818 — Analyzing Correlations in Crypto Markets with Python](https://medium.com/@deepml1818/analyzing-correlations-in-crypto-markets-with-python-8376925ecaec)
**Published doc**: [`sql-cookbook/correlation`](https://docs.koinju.io/sql-cookbook/correlation)

## Why SQL

The article uses `yfinance` + `pandas.DataFrame.corr()` + a Seaborn
heatmap to show pairwise correlations across four crypto tickers. The
pandas API is already short (`df.pct_change().corr()`), but the data
acquisition + dropna handling + heatmap setup ramp it to ~100 lines of
Python. The SQL equivalent is a self-join with `corr()` aggregated
per `(market_a, market_b)` pair — ~22 lines, no external data fetch,
no client-side reshape.

The article continues with a pairs-trading strategy and trade-signal
loop. We **drop that half** — it's procedural, not a SQL win, and a
different concept from "compute the correlations".

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/correlation/ -m parity
```

The parity test compares the long-form 25-row output of the Python
pipeline (built via pandas pivot → `pct_change()` → `corr()` → `melt()`)
against the SQL self-join, asserting agreement to `1e-9` per cell.

## ClickHouse SQL

```sql
WITH
    '2024-01-01' AS start_date,
    '2024-12-31' AS end_date,
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
    )
SELECT a.market AS market_a, b.market AS market_b,
       corr(a.ret, b.ret) AS correlation
FROM market_returns a
JOIN market_returns b ON a.day = b.day
WHERE a.ret IS NOT NULL AND b.ret IS NOT NULL
GROUP BY market_a, market_b
ORDER BY market_a, market_b
```

## Python reference implementation

```python
"""Condensed Python reference for deepml1818's crypto-correlations article.

We compute the full pairwise Pearson-correlation matrix on a 5-major
crypto basket and reshape it to long form for parity testing.
"""

from __future__ import annotations

import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGE = "binance"
MARKETS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ADA-USDT", "DOGE-USDT"]
START = "2024-01-01"
END = "2024-12-31"


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


def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    wide = df.pivot(index="day", columns="market", values="close").astype(float)
    returns = wide.pct_change().dropna()
    corr = returns.corr().rename_axis("market_a").reset_index()
    long = corr.melt(id_vars="market_a", var_name="market_b", value_name="correlation")
    return long.sort_values(["market_a", "market_b"]).reset_index(drop=True)


def run(client: Client) -> pd.DataFrame:
    return compute_correlations(fetch_daily_closes(client))
```
