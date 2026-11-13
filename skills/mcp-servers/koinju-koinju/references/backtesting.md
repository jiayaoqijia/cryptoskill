# Backtesting & benchmarking with Koinju data

Workflow: pull OHLCV → compute per-bar returns → compute the strategy's PnL → compare to buy-and-hold on (total return, Sharpe, max drawdown).

For a runnable starting point: [`scripts/backtest_buy_and_hold.py`](../scripts/backtest_buy_and_hold.py) — runs a SMA crossover vs buy-and-hold on any market.

**For per-metric depth, prefer the cookbook recipes** in [`recipes/`](recipes/) — each one is a CI-validated parity test between a Python implementation and a single ClickHouse SQL query:

- [`recipes/sortino_ratio.md`](recipes/sortino_ratio.md), [`recipes/max_drawdown_calmar.md`](recipes/max_drawdown_calmar.md) — risk-adjusted return metrics
- [`recipes/historical_volatility.md`](recipes/historical_volatility.md) — annualized realized vol
- [`recipes/bollinger_bands.md`](recipes/bollinger_bands.md), [`recipes/mean_reversion_zscore.md`](recipes/mean_reversion_zscore.md) — signal patterns
- [`recipes/dca_vs_lump_sum.md`](recipes/dca_vs_lump_sum.md), [`recipes/spot_futures_perp_spreads.md`](recipes/spot_futures_perp_spreads.md), [`recipes/cross_exchange_arbitrage.md`](recipes/cross_exchange_arbitrage.md) — strategy templates

This page covers the *workflow* (loading → returns → strategy → comparison → plot); the recipes own the *per-metric depth*.

## Load 1 year of daily OHLCV

```python
import os, pandas as pd, clickhouse_connect

ch = clickhouse_connect.get_client(
    host=os.environ["KOINJU_DB_HOST"], port=8443, secure=True,
    username=os.environ["KOINJU_DB_USER"], password=os.environ["KOINJU_DB_PASSWORD"],
    database="api",
)

prices = ch.query_df("""
    SELECT start AS date, close
    FROM api.ohlcv(candle_duration_in_minutes = 1440)
    WHERE exchange = %(exchange)s
      AND market   = %(market)s
      AND start   >= now() - INTERVAL %(days)s DAY
    ORDER BY start
""", parameters={"exchange": "binance", "market": "BTC-USDT", "days": 365})
prices["close"] = prices["close"].astype(float)  # ClickHouse Decimal → float, otherwise Plotly later fails on JSON encoding
# Note: there is no `api.ohlcv_1d` convenience view — use the parameterized `api.ohlcv` with 1440 minutes.
prices["ret"] = prices["close"].pct_change().fillna(0)
```

## Buy-and-hold baseline

```python
bh_equity = (1 + prices["ret"]).cumprod()
bh_total  = bh_equity.iloc[-1] - 1
```

## Strategy (plug in your own signal)

Example — 20/50-day SMA crossover, long-only:

```python
prices["sma20"] = prices["close"].rolling(20).mean()
prices["sma50"] = prices["close"].rolling(50).mean()
prices["pos"]   = (prices["sma20"] > prices["sma50"]).astype(int).shift(1).fillna(0)
prices["strat_ret"] = prices["pos"] * prices["ret"]
strat_equity = (1 + prices["strat_ret"]).cumprod()
strat_total  = strat_equity.iloc[-1] - 1
```

## Metrics

```python
import numpy as np

def sharpe(returns, freq=365):
    return float("nan") if returns.std() == 0 else \
           np.sqrt(freq) * returns.mean() / returns.std()

def max_drawdown(equity):
    return float((equity / equity.cummax() - 1).min())

print(f"buy-and-hold: total={bh_total:7.1%}  sharpe={sharpe(prices['ret']):5.2f}  mdd={max_drawdown(bh_equity):7.1%}")
print(f"strategy:     total={strat_total:7.1%}  sharpe={sharpe(prices['strat_ret']):5.2f}  mdd={max_drawdown(strat_equity):7.1%}")
```

## Plot equity curves

```python
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=prices["date"], y=bh_equity,    name="Buy & hold"))
fig.add_trace(go.Scatter(x=prices["date"], y=strat_equity, name="Strategy"))
fig.update_layout(title="Equity curves vs buy-and-hold", yaxis_title="growth of $1")
fig.show()
```

## Picking a candle granularity

- **Day candles** for multi-year, low-frequency strategies (SMA crossover, momentum, mean reversion on weekly bars).
- **Hour candles** for medium-frequency (intraday signals with overnight holds).
- **Minute candles** (`api.ohlcv_1m`) when slippage and intra-day timing matter — but constrain the time range tightly.
- **Tick trades** (`api.trade`) for HFT / microstructure work; scan cost is significant, time-bound aggressively.

## Common pitfalls

- **Look-ahead bias** — `shift(1)` the position so today's bar is traded on yesterday's signal, not today's close.
- **Single-exchange testing** — BTC-USDT on Binance ≠ Bybit ≠ OKX in volume and microstructure. Pick one explicitly; don't accidentally average across.
- **Survivorship** — `api.spot_markets` / `api.future_markets` show currently-listed markets. For delisted, query `api.ohlcv` for the historical name directly.
- **Costs** — subtract a fee + slippage assumption (5–10 bps per round-trip is a reasonable default for a major pair on a top-3 venue) before comparing.
- **Compounding granularity** — `(1 + ret).cumprod()` for arithmetic returns; `exp(log_ret.cumsum())` for log returns. Don't mix.
- **Annualization** — Sharpe `freq` is bars/year: 365 for daily, 24*365 for hourly, etc. Crypto trades 24/7 so don't use 252.
