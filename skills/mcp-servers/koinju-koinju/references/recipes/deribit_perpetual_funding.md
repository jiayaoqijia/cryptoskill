# Deribit Perpetual Funding

<!-- Synced from `api/python_vs_sql/deribit_perpetual_funding/` by `koinju skill sync-recipes`. Edit the source, not this file. -->

## Source article

# Deribit Perpetual Funding (cryptarbitrage / Deribit Dev Hub)

- **Article**: https://insights.deribit.com/dev-hub/deribit-perpetual-funding-python/
- **Companion code**: https://github.com/cryptarbitrage-code/deribit-perpetual-funding

## What it computes

The article walks through a Tkinter / Matplotlib desktop app that pulls
historical funding for one Deribit perpetual instrument and produces:

1. **8-hour funding rate over time** — Deribit's `interest_8h`, the rolling
   sum of `interest_1h` over the last 8 hours at each settlement instant.
2. **Cumulative funding** — running sum from the start of the requested
   window. Helps a trader estimate the realised funding cost (or gain) on
   a position held for the period.
3. **Monthly funding totals** — month-by-month aggregation, which the
   article highlights as a way to spot regime changes (sustained
   contango/backwardation).

## How we extend it

The original article pulls funding for **one** instrument from Deribit. We
generalize to a **cross-exchange comparison**: how much does a long-perp
position pay on **Deribit** vs **Binance USDT-M** for the same underlying
(`BTC-USD-PERP`) over the same window? Both exchanges' funding hits the
same Koinju canonical market name via `api.funding_rate`, so the
comparison drops to one `WHERE` clause + `GROUP BY exchange, month`.

The Python reference fetches Deribit's hourly `interest_1h` and Binance's
8-hourly `fundingRate` directly from each exchange's public API, then
joins on month — exactly what an external user would have to write
without `api.funding_rate`.

## Source data

- **Deribit**: `/api/v2/public/get_funding_rate_history` (hourly accrual,
  paginated backward via `end_timestamp`).
- **Binance USDT-M**: `/fapi/v1/fundingRate?symbol=BTCUSDT` (8-hourly
  settlements, paginated forward via `startTime`).
- **SQL side**: `api.funding_rate` exposes both with
  `market = 'BTC-USD-PERP'`.

## Parity-test pin

Window pinned to `2025-06-01` → `2026-05-01` — 11 months where prod has
full Binance and Deribit BTC-USD-PERP coverage. Both sides are
deterministic, so the parity test is stable.

# Deribit Perpetual Funding

ClickHouse SQL replacement for the
[Deribit Insights perpetual-funding article](https://insights.deribit.com/dev-hub/deribit-perpetual-funding-python/)

The article's Python tool pages through Deribit's
`get_funding_rate_history` REST endpoint (one HTTP call per ~744 hourly
events, paginated) and aggregates to monthly funding totals plus the
running cumulative. With a single SQL CTE against `api.funding_rate`,
the same result drops out in one round-trip — no pagination, no rate
limiting, and the dataset is already normalized across exchanges so
comparisons (Deribit vs Binance USDT-M, etc.) are a `WHERE` clause away.

```bash
uv run pytest api/python_vs_sql/deribit_perpetual_funding/ -m parity
```

Published page: https://docs.koinju.io/api/data/funding-rate

## ClickHouse SQL

```sql
WITH
    '2025-06-01' AS start_date,
    '2026-05-01' AS end_date,
    monthly AS (
        SELECT
            formatDateTime(timestamp, '%Y-%m') AS month,
            exchange,
            sum(toFloat64(funding_rate)) * 100 AS funding_pct
        FROM api.funding_rate
        WHERE market = 'BTC-USD-PERP'
          AND exchange IN ('deribit', 'binance')
          AND timestamp >= toDateTime64(start_date, 9, 'UTC')
          AND timestamp < toDateTime64(end_date, 9, 'UTC')
        GROUP BY month, exchange
    )
SELECT
    month,
    sumIf(funding_pct, exchange = 'deribit') AS deribit_funding_pct,
    sumIf(funding_pct, exchange = 'binance') AS binance_funding_pct,
    sumIf(funding_pct, exchange = 'binance')
        - sumIf(funding_pct, exchange = 'deribit') AS spread_pct
FROM monthly
GROUP BY month
ORDER BY month
```

## Python reference implementation

```python
"""Condensed Python reference for the cross-exchange BTC-USD-PERP funding article.

Pulls hourly Deribit funding and 8-hourly Binance Coin-M funding directly
from each exchange's public REST API, aggregates to monthly totals (in
percent of notional), and reports both side-by-side with the spread.

Both Deribit `BTC-PERPETUAL` and Binance Coin-M `BTCUSD_PERP` are USD-quoted
inverse perpetuals — apples-to-apples comparison. The Koinju canonical
view exposes both under the same `BTC-USD-PERP` symbol.

Pinned to a deterministic 11-month window so the parity test against
`api.funding_rate` is stable.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime

import pandas as pd
import requests
from clickhouse_connect.driver import Client

DERIBIT_URL = "https://www.deribit.com/api/v2/public/get_funding_rate_history"
BINANCE_URL = "https://dapi.binance.com/dapi/v1/fundingRate"
DERIBIT_INSTRUMENT = "BTC-PERPETUAL"
BINANCE_SYMBOL = "BTCUSD_PERP"
START = "2025-06-01"
END = "2026-05-01"
DERIBIT_PAGE_SIZE = 744
BINANCE_PAGE_SIZE = 1000


def _to_ms(date_str: str) -> int:
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def fetch_deribit(start: str, end: str) -> pd.DataFrame:
    """Walk Deribit's history backward — API returns the most recent
    `count` events within the requested window. `start_timestamp` is
    exclusive and `end_timestamp` is inclusive; we shift by 1 ms on both
    so the returned window is `[start_ms, end_ms)`.
    """
    start_ms, end_ms = _to_ms(start), _to_ms(end)
    rows: list[dict] = []
    cursor_end = end_ms - 1
    while cursor_end > start_ms - 1:
        response = requests.get(
            DERIBIT_URL,
            params={
                "instrument_name": DERIBIT_INSTRUMENT,
                "start_timestamp": start_ms - 1,
                "end_timestamp": cursor_end,
                "count": DERIBIT_PAGE_SIZE,
            },
            timeout=30,
        )
        response.raise_for_status()
        page = response.json()["result"]
        if not page:
            break
        rows.extend(page)
        if len(page) < DERIBIT_PAGE_SIZE:
            break
        cursor_end = page[0]["timestamp"] - 1
        time.sleep(0.5)
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df["funding_rate"] = df["interest_1h"].astype(float)
    return (
        df.drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)
    )


def fetch_binance(start: str, end: str) -> pd.DataFrame:
    """Walk Binance's history forward — API returns the next `limit`
    events from `startTime`, so we move `startTime` past the last seen
    `fundingTime`. Both bounds are inclusive.
    """
    start_ms, end_ms = _to_ms(start), _to_ms(end)
    rows: list[dict] = []
    cursor = start_ms
    while cursor < end_ms:
        response = requests.get(
            BINANCE_URL,
            params={
                "symbol": BINANCE_SYMBOL,
                "startTime": cursor,
                "endTime": end_ms - 1,
                "limit": BINANCE_PAGE_SIZE,
            },
            timeout=30,
        )
        response.raise_for_status()
        page = response.json()
        if not page:
            break
        rows.extend(page)
        if len(page) < BINANCE_PAGE_SIZE:
            break
        cursor = int(page[-1]["fundingTime"]) + 1
        time.sleep(0.2)
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
    df["funding_rate"] = df["fundingRate"].astype(float)
    return (
        df.drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)
    )


def monthly_total(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month"] = df["timestamp"].dt.strftime("%Y-%m")
    return df.groupby("month", as_index=False).agg(
        funding_pct=("funding_rate", lambda s: s.sum() * 100)
    )


def run(client: Client) -> pd.DataFrame:
    del client
    deribit = monthly_total(fetch_deribit(START, END)).rename(
        columns={"funding_pct": "deribit_funding_pct"}
    )
    binance = monthly_total(fetch_binance(START, END)).rename(
        columns={"funding_pct": "binance_funding_pct"}
    )
    merged = deribit.merge(binance, on="month", how="outer").fillna(0.0)
    merged["spread_pct"] = merged["binance_funding_pct"] - merged["deribit_funding_pct"]
    return merged.sort_values("month").reset_index(drop=True)
```
