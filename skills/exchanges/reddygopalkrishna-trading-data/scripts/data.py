#!/usr/bin/env python3
"""Fetch OHLCV bars and quotes for any market through the configured provider.

Examples
  python3 scripts/data.py bars AAPL --interval 1d --period 1y
  python3 scripts/data.py bars BTC-USD --interval 1h --period 1mo --out btc.csv
  python3 scripts/data.py bars RELIANCE.NS --start 2020-01-01 --end 2024-12-31 --json
  python3 scripts/data.py quote AAPL MSFT EURUSD=X ^GSPC
  python3 scripts/data.py many --universe watchlist.txt --period 2y
  python3 scripts/data.py clear-cache
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

import shutil  # noqa: E402

from tradekit import cli, config, data  # noqa: E402


def cmd_bars(a):
    b = data.get_bars(a.symbol, a.interval, a.period, start=a.start, end=a.end, provider=a.provider,
                      use_cache=not a.no_cache)
    if a.out:
        b.to_csv(a.out)
    rows = b.rows()
    if a.json:
        print(cli.dump({"symbol": b.symbol, "interval": b.interval, "bars": len(b), "meta": b.meta,
                        "saved_to": os.path.abspath(a.out) if a.out else None,
                        "rows": rows if a.all else rows[-a.tail:]}))
        return
    last = b.last()
    first = b.close[0]
    print(f"## {b.symbol} {b.interval}  ({len(b)} bars, {b.date[0]} -> {b.date[-1]}, source {b.meta.get('source')})")
    if b.meta.get("currency"):
        print(f"Currency {b.meta['currency']} | exchange {b.meta.get('exchange')} | tz {b.meta.get('timezone')}")
    print(f"Last close {last['close']:,.4f} | period change {((last['close'] / first) - 1) * 100:+.2f}% | "
          f"high {max(b.high):,.4f} low {min(b.low):,.4f}")
    if a.out:
        print(f"Saved CSV: {os.path.abspath(a.out)}")
    print()
    print(cli.md_table(rows[-a.tail:], ["date", "open", "high", "low", "close", "volume"]))


def cmd_quote(a):
    prov = data.get_provider(a.provider)
    out, errs = [], {}
    for s in a.symbols:
        try:
            out.append(prov.quote(s))
        except Exception as e:  # noqa: BLE001
            errs[s] = str(e)
    if a.json:
        print(cli.dump({"quotes": out, "errors": errs}))
        return
    print(cli.md_table(out, ["symbol", "price", "change_pct", "date", "currency", "source"]))
    for s, e in errs.items():
        print(f"- {s}: {e}")
    if any(q.get("delayed") for q in out):
        print("\n_Free data may be delayed. Verify prices with your broker before trading._")


def cmd_many(a):
    syms = data.load_universe(a.universe, a.symbols)
    if not syms:
        cli.fail("no symbols: pass --universe FILE|A,B,C or symbols")
    got, errs = data.get_many(syms, a.interval, a.period, provider=a.provider, workers=a.workers)
    if a.out_dir:
        for s, b in got.items():
            b.to_csv(os.path.join(a.out_dir, s.replace(":", "_").replace("/", "_") + ".csv"))
    summary = [{"symbol": s, "bars": len(b), "first": b.date[0], "last": b.date[-1], "close": b.close[-1]}
               for s, b in got.items()]
    if a.json:
        print(cli.dump({"fetched": summary, "errors": errs}))
        return
    print(f"Fetched {len(got)}/{len(syms)} symbols" + (f" into {a.out_dir}" if a.out_dir else " (cached)"))
    print(cli.md_table(summary, ["symbol", "bars", "first", "last", "close"]))
    for s, e in errs.items():
        print(f"- {s}: {e}")


def cmd_clear(a):
    d = config.home() / "cache"
    if d.exists():
        shutil.rmtree(d)
    print("Cache cleared.")


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("bars")
    b.add_argument("symbol")
    b.add_argument("--interval", default="1d", choices=data.INTERVALS)
    b.add_argument("--period", default="1y", choices=data.PERIODS)
    b.add_argument("--start")
    b.add_argument("--end")
    b.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    b.add_argument("--out", help="write CSV here")
    b.add_argument("--tail", type=int, default=10, help="rows to print")
    b.add_argument("--all", action="store_true", help="with --json, include every row")
    b.add_argument("--no-cache", action="store_true")
    b.add_argument("--json", action="store_true")
    q = sub.add_parser("quote")
    q.add_argument("symbols", nargs="+")
    q.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    q.add_argument("--json", action="store_true")
    m = sub.add_parser("many")
    m.add_argument("symbols", nargs="*")
    m.add_argument("--universe")
    m.add_argument("--interval", default="1d", choices=data.INTERVALS)
    m.add_argument("--period", default="2y", choices=data.PERIODS)
    m.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    m.add_argument("--out-dir")
    m.add_argument("--workers", type=int, default=4)
    m.add_argument("--json", action="store_true")
    sub.add_parser("clear-cache")
    a = p.parse_args()
    {"bars": cmd_bars, "quote": cmd_quote, "many": cmd_many, "clear-cache": cmd_clear}[a.cmd](a)


if __name__ == "__main__":
    cli.run(main)
