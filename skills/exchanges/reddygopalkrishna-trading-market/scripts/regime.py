#!/usr/bin/env python3
"""Market regime: trend, volatility and breadth of an index -> regime label + suggested exposure.

Examples
  python3 scripts/regime.py                      # uses account.benchmark from config
  python3 scripts/regime.py --index ^GSPC --universe assets/watchlists/us-mega-caps.txt
  python3 scripts/regime.py --index BTC-USD --json
  python3 scripts/regime.py --index ^GSPC ^NDX ^FTSE ^N225     # compare several markets
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import analysis, cli, config, data  # noqa: E402


def md(res):
    out = []
    for r in res["regimes"]:
        out.append(f"## {r['index']}: {r['regime'].upper()} - suggested exposure {r['suggested_exposure_pct']}%")
        out.append(f"As of {r['date']} | score {r['score']:+d} | {r['drawdown_from_52w_high_pct']:+.1f}% from 52w high | "
                   f"3m momentum {cli.num(r['momentum_3m_pct'])}% | 20d vol {cli.num(r['realized_vol_20d_pct'])}% "
                   f"(1y percentile {cli.num(r['vol_percentile_1y'], 0)})")
        if r.get("breadth"):
            b = r["breadth"]
            out.append(f"Breadth ({b['symbols']} symbols): {b['pct_above_sma50']}% above 50-SMA, "
                       f"{b['pct_above_sma200']}% above 200-SMA, {b['near_52w_highs']} near highs vs "
                       f"{b['near_52w_lows']} near lows")
        out.append("")
        out += [f"- {n}" for n in r["notes"]]
        out.append("")
    for k, v in res["errors"].items():
        out.append(f"- {k}: {v}")
    out.append("Exposure guide: 100% risk-on, 75% selective, 50% choppy, 25% correction, 0% risk-off. "
               "Lower exposure = fewer/smaller new positions and tighter stops, not necessarily selling everything.")
    return "\n".join(out)


def main():
    p = cli.parser(__doc__)
    p.add_argument("--index", nargs="*", help="index/ETF symbols (default: config account.benchmark)")
    p.add_argument("--universe", help="symbols for breadth (file or comma list)")
    p.add_argument("--csv", help="index bars from a CSV file")
    p.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    idx = a.index or ([config.load()["account"].get("benchmark")] if config.load()["account"].get("benchmark") else [])
    if not idx and not a.csv:
        cli.fail("no index: pass --index SYMBOL or set one with trading-setup (account.benchmark)")
    uni = None
    if a.universe:
        syms = data.load_universe(a.universe)
        uni, _ = data.get_many(syms, "1d", "2y", a.provider)
    regimes, errors = [], {}
    if a.csv:
        regimes.append(analysis.regime(data.load_bars(None, a.csv, min_bars=220), uni))
    for s in idx:
        try:
            regimes.append(analysis.regime(data.get_bars(s, "1d", "2y", provider=a.provider, min_bars=220), uni))
        except Exception as e:  # noqa: BLE001
            errors[s] = str(e)
    if not regimes:
        cli.fail("; ".join(f"{k}: {v}" for k, v in errors.items()) or "no data")
    cli.emit({"regimes": regimes, "errors": errors}, a.json, md)


if __name__ == "__main__":
    cli.run(main)
