# Max Drawdown Calmar

<!-- Synced from `api/python_vs_sql/max_drawdown_calmar/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Maximum drawdown & Calmar ratio (Codearmo)

- **Article**: https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python

## Why this page

Companion to `../sortino_ratio/` — covers the second half of Codearmo's
article. Max drawdown is the interesting SQL pattern (running peak via a
window function over cumulative product), and Calmar follows as a simple
ratio on top of it.

## What we compute

```
cum_return[t] = ∏ (1 + r[i])  for i ≤ t
peak[t]       = max(cum_return[s] for s ≤ t)
drawdown[t]   = cum_return[t] / peak[t] − 1   (always ≤ 0)
max_drawdown  = min(drawdown)                 (most negative)

calmar = (E[r] · N) / |max_drawdown|
```

with `r = pct_change(close)`, `N = 365`.

## Source data swap

Same swap as the Sortino page: BTC-USDT daily on `binance` instead of the
article's 5 US stocks.

## Parity-test pin

Window: `2024-01-01` → `2024-12-31`. Single-row scalar result (max DD and
Calmar). The intermediate per-day drawdown series is also exposed for the
GitBook walkthrough table.

## Numerical conventions

- Cumulative returns built with `(1 + r).cumprod()` matching the article's
  `(return_series + 1).cumprod()`.
- Running peak via `max(cum_return) OVER (ORDER BY day ROWS BETWEEN
  UNBOUNDED PRECEDING AND CURRENT ROW)` — matches pandas'
  `.expanding(min_periods=1).max()`.
- Calmar uses `mean(r) · 365` (same as the article's `df.mean() * 255`,
  rescaled for crypto).

# Maximum drawdown & Calmar — Python vs SQL

**Source article**: [Codearmo — Sharpe, Sortino and Calmar Ratios with Python](https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python)
**Published doc**: [`sql-cookbook/max-drawdown-calmar`](https://docs.koinju.io/sql-cookbook/max-drawdown-calmar)

## Why SQL

Companion to `../sortino_ratio/` — covers the second half of the same
Codearmo article. The interesting SQL pattern is the **running peak**:
`max(cum_return) OVER (PARTITION BY market ORDER BY day ROWS BETWEEN
UNBOUNDED PRECEDING AND CURRENT ROW)` — exactly equivalent to pandas'
`.expanding().max()`. Combined with `exp(sum(log(1 + ret)))` for the
cumulative-product trick, the entire drawdown pipeline lives in two
window functions.

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/max_drawdown_calmar/ -m parity
```

## ClickHouse SQL

```sql
WITH
    '2024-01-01' AS start_date,
    '2024-12-31' AS end_date,
    365 AS sessions_per_year,
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
    ),
    cumulative AS (
        SELECT market, day, ret, exp(sum(log(1 + ret)) OVER w) AS cum_return
        FROM all_returns
        WINDOW w AS (PARTITION BY market ORDER BY day
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    ),
    drawdowns AS (
        SELECT market, ret, cum_return / max(cum_return) OVER w - 1 AS drawdown
        FROM cumulative
        WINDOW w AS (PARTITION BY market ORDER BY day
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    )
SELECT market,
       min(drawdown) AS max_drawdown,
       avg(ret) * sessions_per_year / abs(min(drawdown)) AS calmar
FROM drawdowns
GROUP BY market
ORDER BY market
```

## Python reference implementation

```python
"""Condensed Python reference for Codearmo's max drawdown + Calmar ratio.

Multi-asset version: 5 crypto majors plus an equal-weight portfolio.
"""

from __future__ import annotations

import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGE = "binance"
MARKETS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ADA-USDT", "DOGE-USDT"]
START = "2024-01-01"
END = "2024-12-31"
SESSIONS_PER_YEAR = 365


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


def _max_drawdown(rets: pd.Series) -> float:
    cum_return = (1 + rets).cumprod()
    peak = cum_return.expanding(min_periods=1).max()
    return (cum_return / peak - 1).min()


def compute_drawdowns(df: pd.DataFrame) -> pd.DataFrame:
    wide = df.pivot(index="day", columns="market", values="close").astype(float)
    returns = wide.pct_change().dropna()
    returns["PORTFOLIO"] = returns.mean(axis=1)

    rows = []
    for col in returns.columns:
        rets = returns[col]
        max_dd = _max_drawdown(rets)
        annual_return = rets.mean() * SESSIONS_PER_YEAR
        rows.append(
            {
                "market": col,
                "max_drawdown": max_dd,
                "calmar": annual_return / abs(max_dd),
            }
        )
    return pd.DataFrame(rows).sort_values("market").reset_index(drop=True)


def run(client: Client) -> pd.DataFrame:
    return compute_drawdowns(fetch_daily_closes(client))
```
