#!/usr/bin/env python3
"""Technical analysis snapshot: trend, momentum, volatility, volume, levels, multi-timeframe.

Examples
  python3 scripts/analyze.py AAPL
  python3 scripts/analyze.py INFY.NS --period 5y --json
  python3 scripts/analyze.py BTC-USD --interval 1h --period 3mo --no-mtf
  python3 scripts/analyze.py --csv mydata.csv --symbol XYZ
  python3 scripts/analyze.py AAPL --eval "close > sma(200) and rsi(14) < 40"
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import analysis, cli, data, expr  # noqa: E402


def md(r):
    d = r["daily"]
    out = [f"## {d['symbol']} - {d['bias'].upper()} (score {d['score']:+d})  |  {d['stage']}",
           f"Price {d['price']:,.4f} on {d['date']} ({d['interval']}), source {r['source']}", ""]
    if r.get("higher_tf"):
        w = r["higher_tf"]
        agree = (d["score"] > 0) == (w["score"] > 0)
        out.append(f"**Weekly:** {w['bias']} (score {w['score']:+d}) - timeframes "
                   f"{'AGREE' if agree else 'DISAGREE (be selective / smaller size)'}")
        out.append("")
    t, m, v, vol = d["trend"], d["momentum"], d["volatility"], d["volume"]
    rng = d["range_52w"]
    rows = [
        ("Trend", f"SMA20 {cli.num(t['sma20'])} / SMA50 {cli.num(t['sma50'])} / SMA200 {cli.num(t['sma200'])}; "
                  f"ADX {cli.num(t['adx'], 1)} (+DI {cli.num(t['plus_di'], 1)} / -DI {cli.num(t['minus_di'], 1)}); "
                  f"Supertrend {'up' if t['supertrend_dir'] == 1 else 'down'} @ {cli.num(t['supertrend'])}"
                  + (f"; trend template {t['trend_template']}" if t.get("trend_template") else "")),
        ("Momentum", f"RSI14 {cli.num(m['rsi14'], 1)}; MACD hist {cli.num(m['macd_hist'], 4)}; "
                     "ROC " + ", ".join(f"{k} {v_:+.1f}%" for k, v_ in m["roc_pct"].items() if v_ is not None)),
        ("Volatility", f"ATR14 {cli.num(v['atr14'])} ({cli.num(v['atr_pct'])}% of price); BB width "
                       f"{cli.num(v['bb_width_pct'])}% (percentile {cli.num(v['bb_width_percentile'], 0)})"
                       + (" - SQUEEZE" if v["squeeze"] else "")),
        ("Volume", f"relative volume {cli.num(vol['relative'])}x 50-day avg; OBV trend {vol['obv_trend']}"),
        ("52-week", f"high {cli.num(rng['high'])} ({rng['pct_from_high']:+.1f}%), low {cli.num(rng['low'])} "
                    f"({rng['pct_from_low']:+.1f}%)"),
    ]
    out.append("| Area | Reading |\n|---|---|")
    out += [f"| {a} | {b} |" for a, b in rows]
    lv = d["levels"]
    out.append("")
    out.append("**Resistance:** " + (", ".join(f"{x['price']:,.2f} ({x['distance_pct']:+.1f}%, {x['touches']}x)"
                                             for x in lv["resistance"]) or "none nearby (blue sky)"))
    out.append("**Support:** " + (", ".join(f"{x['price']:,.2f} ({x['distance_pct']:+.1f}%, {x['touches']}x)"
                                          for x in lv["support"]) or "none found"))
    out.append("")
    out.append("**Score breakdown:** " + "; ".join(d["reasons"]))
    if r.get("eval"):
        out.append("")
        out.append(f"**Rule** `{r['eval']['rule']}` on the last bar -> **{r['eval']['value']}**")
    out.append("")
    out.append("_Indicator readings describe the past; they are not predictions._")
    return "\n".join(out)


def main():
    p = cli.parser(__doc__)
    p.add_argument("symbol", nargs="?")
    p.add_argument("--symbol", dest="symbol_opt")
    data.add_data_args(p, period="2y")
    p.add_argument("--no-mtf", action="store_true", help="skip the weekly (higher timeframe) read")
    p.add_argument("--eval", help="also evaluate a rule on the last bar")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    sym = a.symbol or a.symbol_opt
    b = data.load_bars(sym, a.csv, a.interval, a.period, a.provider, min_bars=30)
    res = {"source": b.meta.get("source"), "daily": analysis.snapshot(b)}
    if not a.no_mtf and not b.intraday and b.interval == "1d":
        wk = b.resample("1wk")
        if len(wk) >= 30:
            res["higher_tf"] = analysis.snapshot(wk)
    if a.eval:
        res["eval"] = {"rule": a.eval, "value": expr.evaluate_last(a.eval, b)}
    cli.emit(res, a.json, md)


if __name__ == "__main__":
    cli.run(main)
