"""Benchmark a simple strategy against buy-and-hold on Koinju data.

Default strategy is a 20/50-day SMA crossover, long-only. Replace `signal`
with your own to compare a different rule.

Run:
    uv run python backtest_buy_and_hold.py                              # BTC-USDT, 365d; opens equity curve in browser
    uv run python backtest_buy_and_hold.py --market ETH-USDT --days 730

Requires KOINJU_DB_HOST, KOINJU_DB_USER, KOINJU_DB_PASSWORD — see references/auth.md.
"""

from __future__ import annotations

import argparse
import os
import sys


REQUIRED = ("KOINJU_DB_HOST", "KOINJU_DB_USER", "KOINJU_DB_PASSWORD")


def _autosource_koinju_env() -> None:
    for path in (".koinju.env", os.path.expanduser("~/.koinju.env")):
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[7:]
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key.strip(), value)


def load_credentials() -> dict[str, str]:
    _autosource_koinju_env()
    missing = [v for v in REQUIRED if not os.environ.get(v)]
    if missing:
        sys.exit(
            f"Missing env vars: {', '.join(missing)}. "
            "Don't have credentials? Sign up at https://koinju.io/pricing — you'll receive "
            "an email with a https://dataroom.koinju.io/ link. Already a customer but stuck? "
            "Email support@koinju.io. See references/auth.md."
        )
    return {
        "db_host":     os.environ["KOINJU_DB_HOST"],
        "db_port":     os.environ.get("KOINJU_DB_PORT", "8443"),
        "db_user":     os.environ["KOINJU_DB_USER"],
        "db_password": os.environ["KOINJU_DB_PASSWORD"],
        "db_database": os.environ.get("KOINJU_DB_DATABASE", "api"),
    }


def _decimals_to_float(df):
    """Cast object-dtype Decimal columns to float64. ClickHouse Decimal isn't JSON-serializable, so Plotly fails on it."""
    import decimal
    for col in df.columns:
        non_null = df[col].dropna()
        if len(non_null) > 0 and isinstance(non_null.iloc[0], decimal.Decimal):
            df[col] = df[col].astype(float)
    return df


def fetch_prices(creds, exchange: str, market: str, days: int):
    import clickhouse_connect

    client = clickhouse_connect.get_client(
        host=creds["db_host"], port=int(creds["db_port"]), secure=True,
        username=creds["db_user"], password=creds["db_password"],
        database=creds["db_database"],
    )
    df = client.query_df("""
        SELECT start AS date, close
        FROM api.ohlcv(candle_duration_in_minutes = 1440)
        WHERE exchange = %(exchange)s
          AND market   = %(market)s
          AND start   >= now() - INTERVAL %(days)s DAY
        ORDER BY start
    """, parameters={"exchange": exchange, "market": market, "days": days})
    return _decimals_to_float(df)


def signal(df):
    """Default SMA(20/50) crossover. Returns a 0/1 position series shifted by 1 bar."""
    df["sma20"] = df["close"].rolling(20).mean()
    df["sma50"] = df["close"].rolling(50).mean()
    return (df["sma20"] > df["sma50"]).astype(int).shift(1).fillna(0)


def sharpe(returns, freq: int = 365) -> float:
    import numpy as np
    if returns.std() == 0:
        return float("nan")
    return float(np.sqrt(freq) * returns.mean() / returns.std())


def max_drawdown(equity) -> float:
    return float((equity / equity.cummax() - 1).min())


def plot_equity(dates, bh_equity, strat_equity, market: str) -> None:
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=bh_equity,    name="Buy & hold",  mode="lines"))
    fig.add_trace(go.Scatter(x=dates, y=strat_equity, name="Strategy",    mode="lines"))
    fig.update_layout(
        title=f"{market} — strategy vs buy-and-hold",
        yaxis_title="growth of $1",
        xaxis_title="date",
    )
    fig.show()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--exchange", default="binance")
    p.add_argument("--market",   default="BTC-USDT")
    p.add_argument("--days",     type=int, default=365)
    args = p.parse_args()

    creds = load_credentials()
    prices = fetch_prices(creds, args.exchange, args.market, args.days)
    if prices.empty:
        sys.exit(f"No daily candles for {args.exchange} {args.market} in the last {args.days}d.")

    prices["ret"]      = prices["close"].pct_change().fillna(0)
    prices["pos"]      = signal(prices)
    prices["strat_ret"] = prices["pos"] * prices["ret"]

    bh_equity    = (1 + prices["ret"]).cumprod()
    strat_equity = (1 + prices["strat_ret"]).cumprod()

    bh_total    = float(bh_equity.iloc[-1] - 1)
    strat_total = float(strat_equity.iloc[-1] - 1)

    print(f"{args.exchange} {args.market} | {len(prices)} daily bars")
    print(f"  buy-and-hold: total={bh_total:>8.1%}  sharpe={sharpe(prices['ret']):>5.2f}  mdd={max_drawdown(bh_equity):>8.1%}")
    print(f"  strategy    : total={strat_total:>8.1%}  sharpe={sharpe(prices['strat_ret']):>5.2f}  mdd={max_drawdown(strat_equity):>8.1%}")

    plot_equity(prices["date"], bh_equity, strat_equity, args.market)


if __name__ == "__main__":
    main()
