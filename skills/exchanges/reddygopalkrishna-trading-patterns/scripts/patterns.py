#!/usr/bin/env python3
"""Detect live chart patterns (VCP, breakout, bull flag, cup & handle, double bottom, inside bar, NR7, pocket pivot).

Examples
  python3 scripts/patterns.py AAPL
  python3 scripts/patterns.py AAPL NVDA MSFT --patterns vcp,cup_handle --min-score 60
  python3 scripts/patterns.py --universe watchlist.txt --min-score 70 --json
  python3 scripts/patterns.py --csv bars.csv --symbol XYZ
  python3 scripts/patterns.py --list
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, data, patterns  # noqa: E402

DESCRIPTIONS = {
    "vcp": "Volatility contraction: 2-4 shallower pullbacks in a stage-2 uptrend, volume drying up",
    "breakout": "Close at a new 20-bar high on >= 1.5x average volume",
    "bull_flag": "Sharp pole (>= 15%) then a tight pullback retracing < 50% on lighter volume",
    "cup_handle": "12-35% rounded base, right side near the left peak, shallow handle in the upper half",
    "double_bottom": "Two similar lows >= 10 bars apart with a >= 5% rally between; trigger = neckline",
    "inside_bar": "Today's range inside yesterday's - compression, trigger = mother bar high",
    "nr7": "Narrowest range of the last 7 bars - volatility contraction",
    "pocket_pivot": "Up-day volume above every down-day volume of the prior 10 bars, above the 50-SMA",
}


def md(r):
    out = [f"## Pattern scan - {r['scanned']} symbols, {len(r['hits'])} live setups (min score {r['min_score']})", ""]
    if not r["hits"]:
        out.append("No qualifying patterns right now.")
    else:
        rows = []
        for h in r["hits"]:
            rows.append({"symbol": h["symbol"], "pattern": h["pattern"], "score": h["score"], "close": h["close"],
                         "pivot": h["pivot"], "stop": h["stop"], "to_pivot_%": h["to_pivot_pct"],
                         "risk_%": h["risk_pct"]})
        out.append(cli.md_table(rows, ["symbol", "pattern", "score", "close", "pivot", "stop", "to_pivot_%", "risk_%"]))
        out.append("")
        for h in r["hits"][:10]:
            det = ", ".join(f"{k}={v}" for k, v in h["details"].items())
            out.append(f"- **{h['symbol']} {h['pattern']}**: {det}")
    if r["errors"]:
        out.append("")
        out.append("Errors: " + "; ".join(f"{k}: {v}" for k, v in r["errors"].items()))
    out.append("")
    out.append("_pivot = trigger price, stop = pattern invalidation. Confirm with trading-chart; "
               "plan with trading-plan. Patterns fail often - size for being wrong._")
    return "\n".join(out)


def main():
    p = cli.parser(__doc__)
    p.add_argument("symbols", nargs="*")
    p.add_argument("--symbol")
    p.add_argument("--universe", help="file or comma list")
    data.add_data_args(p, period="2y")
    p.add_argument("--patterns", help="comma list; default all")
    p.add_argument("--min-score", type=int, default=0)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--list", action="store_true", help="describe available patterns")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.list:
        cli.emit(DESCRIPTIONS, a.json, lambda d: "\n".join(f"- **{k}**: {v}" for k, v in d.items()))
        return
    which = [x.strip() for x in a.patterns.split(",")] if a.patterns else None
    series, errors = {}, {}
    if a.csv:
        b = data.load_bars(a.symbol or (a.symbols[0] if a.symbols else None), a.csv, a.interval)
        series[b.symbol] = b
    else:
        syms = data.load_universe(a.universe, (a.symbols or []) + ([a.symbol] if a.symbol else []))
        if not syms:
            cli.fail("give symbols, --universe or --csv")
        series, errors = data.get_many(syms, a.interval, a.period, a.provider, workers=a.workers)
    hits = []
    for sym, b in series.items():
        for h in patterns.scan(b, which):
            if h["score"] < a.min_score:
                continue
            c = b.close[-1]
            h["close"] = round(c, 4)
            h["to_pivot_pct"] = round((h["pivot"] / c - 1) * 100, 2)
            h["risk_pct"] = round((h["pivot"] - h["stop"]) / h["pivot"] * 100, 2) if h["pivot"] else None
            hits.append(h)
    hits.sort(key=lambda h: h["score"], reverse=True)
    cli.emit({"scanned": len(series), "min_score": a.min_score, "hits": hits, "errors": errors}, a.json, md)


if __name__ == "__main__":
    cli.run(main)
