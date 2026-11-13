"""Plot the BTC option smile across one or more exchanges.

Pulls the nearest-future expiration from `api.option_smile` for each exchange
and plots IV vs strike, one trace per exchange.

Run:
    uv run python plot_option_smile.py                            # opens the smile in a browser tab
    uv run python plot_option_smile.py --underlying ETH --exchanges deribit okx

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


def fetch_smile(creds, underlying: str, exchanges: list[str]):
    import clickhouse_connect

    client = clickhouse_connect.get_client(
        host=creds["db_host"], port=int(creds["db_port"]), secure=True,
        username=creds["db_user"], password=creds["db_password"],
        database=creds["db_database"],
    )
    # Source of truth: api.option_chains (plural). There is no api.option_smile view.
    #
    # Two non-obvious bits:
    #   1. Snapshot cadence varies by exchange (Deribit sub-minute, OKX/Bybit ~30 min),
    #      so a fixed `timestamp >= now() - INTERVAL 10 MINUTE` filter silently drops
    #      everything for the slower venues. Use per-exchange max(timestamp) instead.
    #   2. `s.exchange AS exchange` alias is required — without it, `JOIN ... ON`
    #      returns the column as `s.exchange` and downstream pandas indexing breaks.
    query = """
        WITH per_exchange AS (
            SELECT exchange,
                   min(expiration) AS exp,
                   max(timestamp)  AS latest_ts
            FROM api.option_chains
            WHERE underlying_asset = %(underlying)s
              AND exchange IN %(exchanges)s
              AND expiration > now()
              AND timestamp >= now() - INTERVAL 1 DAY
            GROUP BY exchange
        )
        SELECT s.exchange    AS exchange,
               s.strike,
               s.mark_iv     AS iv,
               s.option_type,
               s.expiration
        FROM api.option_chains s
        INNER JOIN per_exchange p ON s.exchange = p.exchange
        WHERE s.underlying_asset = %(underlying)s
          AND s.expiration = p.exp
          AND s.timestamp  = p.latest_ts
        ORDER BY s.exchange, s.strike
    """
    df = client.query_df(query, parameters={
        "underlying": underlying,
        "exchanges":  exchanges,
    })
    return _decimals_to_float(df)


def plot(df, underlying: str) -> None:
    import plotly.express as px

    title = f"{underlying} option smile — {', '.join(sorted(df['exchange'].unique()))} (nearest expiry)"
    fig = px.scatter(
        df, x="strike", y="iv", color="exchange",
        hover_data=["expiration"],
        title=title,
    )
    # mark_iv is already a percentage value (25.0 = 25%), NOT a decimal (0.25).
    # Use ticksuffix="%" — not tickformat=".0%" which would scale by 100 and display 2500%.
    fig.update_yaxes(ticksuffix="%", title="implied volatility")
    fig.update_xaxes(title="strike")
    fig.show()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--underlying", default="BTC")
    p.add_argument("--exchanges", nargs="+", default=["okx", "bybit"])
    args = p.parse_args()

    creds = load_credentials()
    df = fetch_smile(creds, args.underlying, args.exchanges)
    if df.empty:
        sys.exit(
            f"No smile rows returned for {args.underlying} on {args.exchanges}. "
            "Check `SELECT DISTINCT exchange FROM api.option_chains` for live coverage."
        )
    print(f"fetched {len(df)} rows across {df['exchange'].nunique()} exchanges, "
          f"expirations: {sorted(df['expiration'].unique())}")
    plot(df, args.underlying)


if __name__ == "__main__":
    main()
