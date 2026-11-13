# Plotting recipes

Plotly is the default. Bundled scripts call `fig.show()` to open an interactive HTML chart in the user's browser. For file output use `fig.write_html("…")` (no extra deps) or `fig.write_image("…")` (needs `kaleido` — opt-in, see Export tips below).

## Option smile — IV vs strike, multi-exchange

Single underlying (e.g. BTC), nearest expiration, one trace per exchange. Pulled from `api.option_chains` (plural; **there is no `api.option_smile` view**).

For a runnable: [`scripts/plot_option_smile.py`](../scripts/plot_option_smile.py).

```python
import os, plotly.express as px, clickhouse_connect

ch = clickhouse_connect.get_client(
    host=os.environ["KOINJU_DB_HOST"], port=8443, secure=True,
    username=os.environ["KOINJU_DB_USER"], password=os.environ["KOINJU_DB_PASSWORD"],
    database="api",
)

df = ch.query_df("""
    -- per-exchange max(timestamp) — fixed `INTERVAL N MINUTE` drops everything for
    -- exchanges with slow snapshot cadence (OKX/Bybit ~30 min). See data-tables.md
    -- "Gotcha: option-chain snapshots are intermittent" for the full pattern.
    WITH per_exchange AS (
        SELECT exchange,
               min(expiration) AS exp,
               max(timestamp)  AS latest_ts
        FROM api.option_chains
        WHERE underlying_asset = 'BTC'
          AND exchange IN ('okx', 'bybit')
          AND expiration > now()
          AND timestamp >= now() - INTERVAL 1 DAY
        GROUP BY exchange
    )
    SELECT s.exchange AS exchange,    -- explicit alias for the JOIN ... ON column
           s.strike,
           s.mark_iv  AS iv,
           s.option_type,
           s.expiration
    FROM api.option_chains s
    INNER JOIN per_exchange p ON s.exchange = p.exchange
    WHERE s.underlying_asset = 'BTC'
      AND s.expiration = p.exp
      AND s.timestamp  = p.latest_ts
    ORDER BY s.exchange, s.strike
""")
df[["strike", "iv"]] = df[["strike", "iv"]].astype(float)  # ClickHouse Decimal → float for Plotly

fig = px.scatter(df, x="strike", y="iv", color="exchange",
                 title="BTC option smile — OKX vs Bybit (nearest expiry)")
fig.update_yaxes(ticksuffix="%")  # mark_iv is already in percent (25.0 = 25%); tickformat=".0%" would show 2500%
fig.show()
```

Greeks live on the same table: `delta`, `gamma`, `vega`, `theta` (no `rho`). For faster reads when filtering by a single exchange, use the per-exchange materialized view: `api.option_chains_mv_binance`, `_bybit`, `_deribit`, `_okx`.

## Volatility surface (3D)

```python
df = ch.query_df("""
    SELECT strike,
           dateDiff('day', now(), expiration) AS dte,
           mark_iv AS iv
    FROM api.option_chains_mv_deribit
    WHERE underlying_asset = 'BTC'
      AND expiration > now()
      AND timestamp = (
          SELECT max(timestamp) FROM api.option_chains_mv_deribit
          WHERE underlying_asset = 'BTC'
            AND timestamp >= now() - INTERVAL 6 HOUR
      )
""")
df["iv"] = df["iv"].astype(float)  # Decimal → float for Plotly

import plotly.graph_objects as go
fig = go.Figure(data=[go.Mesh3d(
    x=df["strike"], y=df["dte"], z=df["iv"], intensity=df["iv"], opacity=0.85,
)])
fig.update_layout(scene=dict(
    xaxis_title="strike", yaxis_title="days to expiry", zaxis_title="iv",
), title="BTC vol surface — Deribit")
fig.show()
```

## OHLCV candlestick

End-to-end runnable: [`scripts/welcome_btc_usdt.py`](../scripts/welcome_btc_usdt.py).

Inline form:

```python
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df["start"], open=df["open"], high=df["high"], low=df["low"], close=df["close"],
)])
fig.update_layout(xaxis_rangeslider_visible=False, title="BTC-USDT — Binance — 1h")
fig.show()
```

## DVOL time-series — not directly available

**There is no `api.volatility_index` table.** Koinju doesn't expose DVOL as a table; the official series is published by Deribit. Two workarounds for "current bitcoin volatility":

1. **Synthetic ATM IV** — pick the ATM strike's `mark_iv` from a 30-day-out expiration on `api.option_chains` (Deribit). Plot the time series the same way:

   ```python
   df = ch.query_df("""
       SELECT timestamp, mark_iv AS iv
       FROM api.option_chains_mv_deribit
       WHERE underlying_asset = 'BTC'
         AND timestamp >= now() - INTERVAL 30 DAY
         -- pick the contract nearest 30-DTE and ATM:
         AND abs(dateDiff('day', timestamp, expiration) - 30) < 3
         AND abs(strike - underlying_price) / underlying_price < 0.05
       ORDER BY timestamp
   """)
   ```

2. **Official Deribit DVOL** — fetch from Deribit's own REST API (`https://www.deribit.com/api/v2/public/get_volatility_index_data`). Out of scope for this skill.

## Equity curve (strategy vs benchmark)

See the workflow in [`references/backtesting.md`](backtesting.md) — `bh_equity` and `strat_equity` plotted as overlaid scatter traces.

## Export tips

- **`fig.show()` is the default** in the bundled scripts — opens the chart in your default browser as a self-contained interactive HTML page. No extra deps.
- `fig.write_html("smile.html")` — same self-contained HTML, written to a file instead of opening a browser. Use when you want to send the file or open it later.
- `fig.write_image("smile.png", width=1200, height=700, scale=2)` — needs `kaleido` (not in default bootstrap deps; install with `uv add kaleido` if you specifically need static PNG/SVG/PDF). Pulls in ~5 extra packages including a headless browser binary.
- Truly headless contexts (no `DISPLAY`, no browser): `fig.show()` falls back gracefully — tries the browser, prints a notice if it can't, the script still completes.
