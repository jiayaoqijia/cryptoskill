"""Welcome demo: pull 7d of BTC-USDT 1h candles from Koinju and plot them.

Run:
    uv run python welcome_btc_usdt.py            # opens the candlestick chart in a browser tab

Requires KOINJU_API_KEY, KOINJU_DB_HOST, KOINJU_DB_USER, KOINJU_DB_PASSWORD
in the environment — see references/auth.md.
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


def fetch_ohlcv(creds: dict[str, str], exchange: str, market: str, days: int):
    import clickhouse_connect

    client = clickhouse_connect.get_client(
        host=creds["db_host"],
        port=int(creds.get("db_port", 8443)),
        secure=True,
        username=creds["db_user"],
        password=creds["db_password"],
        database=creds.get("db_database", "api"),
    )
    query = """
        SELECT start, open, high, low, close, volume
        FROM api.ohlcv(candle_duration_in_minutes = 60)
        WHERE exchange = %(exchange)s
          AND market = %(market)s
          AND start >= now() - INTERVAL %(days)s DAY
        ORDER BY start
    """
    df = client.query_df(
        query, parameters={"exchange": exchange, "market": market, "days": days}
    )
    return _decimals_to_float(df)


def plot(df) -> None:
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["start"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="BTC-USDT",
            )
        ]
    )
    fig.update_layout(
        title="BTC-USDT — Binance — 1h candles (last 7 days, from api.ohlcv)",
        xaxis_title="time (UTC)",
        yaxis_title="USDT",
        xaxis_rangeslider_visible=False,
    )
    fig.show()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exchange", default="binance")
    parser.add_argument("--market", default="BTC-USDT")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    creds = load_credentials()
    df = fetch_ohlcv(creds, args.exchange, args.market, args.days)
    if df.empty:
        sys.exit(
            f"No candles returned for {args.exchange} {args.market} in the last {args.days}d."
        )
    print(
        f"fetched {len(df)} candles, range {df['start'].min()} .. {df['start'].max()}"
    )
    plot(df)


if __name__ == "__main__":
    main()
