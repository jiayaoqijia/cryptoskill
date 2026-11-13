# Dca Vs Lump Sum

<!-- Synced from `api/python_vs_sql/dca_vs_lump_sum/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# DCA vs Lump-Sum (Greyhound Analytics)

- **Article**: https://greyhoundanalytics.com/blog/backtest-your-dollar-cost-average-strategy-easily-in-python/

## What we compute

A side-by-side **monthly running comparison** of two investment strategies on the same total contribution schedule:

- **DCA (Dollar-Cost Averaging)** — invest a fixed `$1000` at the start of each month, accumulating BTC at whatever the price is that month.
- **Lump-sum** — at every month `T`, this represents "what if I had invested all `T × $1000` at month 0's price instead?". The BTC count grows linearly with the cumulative contribution; the dollar value moves only with the price.

Both columns sit on the same row so you can read DCA's smoothing-out effect at a glance.

## Source data swap and basket choice

The article uses the `backtesting.py` library's bundled `GOOG` test dataset. We swap to **`binance/BTC-USDT` daily candles** to keep cross-page consistency with the rest of the Compute Engine examples (HV, Sortino, Calmar, Correlation), aggregated to **monthly buckets**. The methodology is identical; just the asset and the contribution amount change.

## What we drop from the article

The article is a `backtesting.py` tutorial (`Strategy.next()`, `self.buy(...)`, weekly Mondays, `bt.run(...)`). All of that procedural infrastructure collapses to a single CTE chain because the comparison is a deterministic running aggregate — no event-driven simulation needed.

The article also has an "extended strategy" that double-buys on dips. **Out of scope** for this page (different concept; a separate doc page could cover threshold-conditional buys later).

## Lump-sum benchmark — what we add

The article's title is "DCA vs Lump-Sum" but the source code only implements DCA. Per the Notion entry's note (_"Lump-sum benchmark inclus dans même requête"_) we extend the example to include the lump-sum side natively in the SQL — a real value-add over the article's source.

## Parity-test pin

Window: `2020-01-01` → `2024-12-31`. **60 monthly rows** in the output. Single-asset (BTC-USDT on binance).

## Numerical conventions

- **Monthly bucket** via `toStartOfMonth(toDate(start))`. The "open" price is the **first close in the month** (`argMin(close, start)`), matching `groupby('month').first()` in pandas.
- **Both DCA and lump-sum value their portfolio at the current month's open price**, not month-end close. Trade-offs: cleaner semantics (buy and value at the same price), the latest row's contribution always shows zero return (honest), earlier contributions reflect appreciation since they were made.
- **DCA** uses a running `sum(...) OVER (ORDER BY month)`. **Lump-sum** uses `first_value(open_price) OVER (ORDER BY month)` to anchor to month 0's price.
- 60 rows × 7 columns — well within all tier row caps.

# DCA vs Lump-Sum — Python vs SQL

**Source article**: [Greyhound Analytics — Backtest your Dollar-Cost-Average strategy easily in Python](https://greyhoundanalytics.com/blog/backtest-your-dollar-cost-average-strategy-easily-in-python/)
**Published doc**: [`sql-cookbook/dca-vs-lump-sum`](https://docs.koinju.io/sql-cookbook/dca-vs-lump-sum)

## Why SQL

The article relies on the `backtesting.py` library — a `Strategy` class
with a `next()` event-driven simulation loop, weekly Mondays via
`dayofweek == 1`, `self.buy(...)` calls, then post-hoc trade-list
aggregation. All of that procedural infrastructure is unnecessary
because DCA's running totals are deterministic — one CTE chain with
`sum(...) OVER (ORDER BY month)` does it.

We also **add the lump-sum benchmark** (which the article's title
implies but the source code didn't include) using `first_value(open_price)
OVER w` to anchor to month 0's price. So the published doc shows both
strategies side by side on every row — exactly the comparison readers
of the article are looking for.

## Running the parity test

```bash
set -a && . ./.env && set +a   # KOINJU_SQL_USER / KOINJU_SQL_PASSWORD
uv run pytest api/python_vs_sql/dca_vs_lump_sum/ -m parity
```

The test compares the 60-row monthly time series (2020-01-01 →
2024-12-31) between the Python pipeline (pandas `groupby` + `cumsum`
arithmetic) and the SQL query, asserting agreement to `1e-9` per cell.

## ClickHouse SQL

```sql
WITH
    '2020-01-01' AS start_date,
    '2024-12-31' AS end_date,
    1000 AS monthly_contribution,
    monthly AS (
        SELECT toStartOfMonth(toDate(start)) AS month,
               argMin(toFloat64(close), start) AS open_price
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = 'binance'
          AND market = 'BTC-USDT'
          AND start BETWEEN start_date AND end_date
        GROUP BY month
    )
SELECT month,
       open_price,
       sum(monthly_contribution) OVER w AS cumulative_invested,
       sum(monthly_contribution / open_price) OVER w AS dca_btc,
       sum(monthly_contribution / open_price) OVER w * open_price AS dca_portfolio_value,
       sum(monthly_contribution) OVER w / first_value(open_price) OVER w AS lumpsum_btc,
       sum(monthly_contribution) OVER w / first_value(open_price) OVER w * open_price AS lumpsum_portfolio_value
FROM monthly
WINDOW w AS (ORDER BY month)
ORDER BY month
```

## Python reference implementation

```python
"""Condensed Python reference for Greyhound Analytics' DCA vs Lump-Sum article.

Single-asset BTC-USDT on binance, monthly contributions of $1000 from
2020-01-01 to 2024-12-31. Output is a per-month time series with both
DCA and lump-sum cumulative metrics on the same row.
"""

from __future__ import annotations

import pandas as pd
from clickhouse_connect.driver import Client

EXCHANGE = "binance"
MARKET = "BTC-USDT"
START = "2020-01-01"
END = "2024-12-31"
MONTHLY_CONTRIBUTION = 1000.0


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


def compute_dca_vs_lumpsum(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month"] = df["day"].apply(lambda d: d.replace(day=1))
    monthly = (
        df.groupby("month", as_index=False)
        .agg(open_price=("close", "first"))
        .sort_values("month")
        .reset_index(drop=True)
    )
    n = len(monthly)
    monthly["cumulative_invested"] = MONTHLY_CONTRIBUTION * pd.Series(range(1, n + 1))
    monthly["dca_btc"] = (MONTHLY_CONTRIBUTION / monthly["open_price"]).cumsum()
    monthly["dca_portfolio_value"] = monthly["dca_btc"] * monthly["open_price"]
    first_price = float(monthly["open_price"].iloc[0])
    monthly["lumpsum_btc"] = monthly["cumulative_invested"] / first_price
    monthly["lumpsum_portfolio_value"] = monthly["lumpsum_btc"] * monthly["open_price"]
    return monthly[
        [
            "month",
            "open_price",
            "cumulative_invested",
            "dca_btc",
            "dca_portfolio_value",
            "lumpsum_btc",
            "lumpsum_portfolio_value",
        ]
    ]


def run(client: Client) -> pd.DataFrame:
    return compute_dca_vs_lumpsum(fetch_daily_closes(client))
```
