#!/usr/bin/env python3
"""Daily trading brief: market regime, risk status, open positions vs stops, watchlist scan, live patterns.
Designed to be run by hand or on a schedule (pre-market / end-of-day).

Examples
  python3 scripts/brief.py --watchlist assets/watchlists/us-mega-caps.txt
  python3 scripts/brief.py --watchlist list.txt --preset trend-template --patterns vcp,breakout --report brief.html
  python3 scripts/brief.py --index ^GSPC ^NDX --json
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

import datetime as dt  # noqa: E402

from tradekit import DISCLAIMER, analysis, cli, config, data, expr, patterns, report  # noqa: E402
from tradekit.journal import Journal  # noqa: E402

PRESET_RULES = {
    "trend-template": "close > sma(150) and close > sma(200) and sma(150) > sma(200) and sma(200) > shift(sma(200), 21) "
                      "and sma(50) > sma(150) and close > sma(50) and pct_from_low(252) >= 30 and pct_from_high(252) >= -25",
    "breakout-volume": "close > shift(highest(high, 20), 1) and rel_volume(50) >= 1.5",
    "oversold-in-uptrend": "close > sma(200) and rsi(2) < 10",
    "near-52w-high": "pct_from_high(252) >= -3 and close > sma(50)",
    "squeeze": "percentile(bb_width(20), 120) <= 10 and close > sma(50)",
}


def main():
    p = cli.parser(__doc__)
    p.add_argument("--index", nargs="*", help="indices for regime (default config benchmark)")
    p.add_argument("--watchlist", help="file or comma list to scan")
    p.add_argument("--preset", default="trend-template", choices=sorted(PRESET_RULES))
    p.add_argument("--rule", help="custom rule instead of --preset")
    p.add_argument("--patterns", default="vcp,breakout,bull_flag,cup_handle,pocket_pivot")
    p.add_argument("--min-score", type=int, default=60)
    p.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    p.add_argument("--report")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    cfg = config.load()
    out = {"generated": dt.datetime.now().isoformat(timespec="minutes"), "regimes": [], "errors": {}}

    idx = a.index or ([cfg["account"]["benchmark"]] if cfg["account"].get("benchmark") else [])
    for s in idx:
        try:
            out["regimes"].append(analysis.regime(data.get_bars(s, "1d", "2y", provider=a.provider, min_bars=220)))
        except Exception as e:  # noqa: BLE001
            out["errors"][s] = str(e)

    j = Journal()
    open_t = j.list(status="open")
    positions = []
    if open_t:
        got, errs = data.get_many(sorted({t["symbol"] for t in open_t}), "1d", "3mo", a.provider)
        out["errors"].update(errs)
        for t in open_t:
            b = got.get(t["symbol"])
            last = b.close[-1] if b else None
            row = {"id": t["id"], "symbol": t["symbol"], "side": t["side"], "qty": t["qty"], "entry": t["entry_price"],
                   "stop": t["stop"], "last": round(last, 4) if last else None}
            if last and t["entry_price"]:
                sign = 1 if t["side"] == "long" else -1
                row["open_pnl"] = round((last - t["entry_price"]) * float(t["qty"] or 0) * sign, 2)
                if t["stop"] is not None:
                    risk_u = abs(t["entry_price"] - (t["plan_stop"] if t["plan_stop"] is not None else t["stop"]))
                    row["open_r"] = round((last - t["entry_price"]) * sign / risk_u, 2) if risk_u else None
                    row["to_stop_%"] = round((t["stop"] / last - 1) * 100, 2)
                    row["alert"] = "STOP HIT?" if (sign > 0 and last <= t["stop"]) or (sign < 0 and last >= t["stop"]) else (
                        "near stop" if abs(row["to_stop_%"]) < 2 else "")
            positions.append(row)
    out["positions"] = positions
    heat = sum(abs(t["entry_price"] - t["stop"]) * float(t["qty"]) for t in open_t if t["stop"] is not None and t["qty"])
    out["risk"] = {"kill_switch": config.kill_switch_on(), "open_trades": len(open_t), "open_risk": round(heat, 2),
                   "open_risk_pct": round(heat / cfg["account"]["equity"] * 100, 2),
                   "losing_streak": j.consecutive_losses(),
                   "today_pnl": round(sum(t["pnl"] or 0 for t in j.closed_today()), 2)}

    out["scan"], out["patterns"] = [], []
    if a.watchlist:
        syms = data.load_universe(a.watchlist)
        series, errs = data.get_many(syms, "1d", "2y", a.provider)
        out["errors"].update(errs)
        rule = expr.compile_expr(a.rule or PRESET_RULES[a.preset])
        rank = expr.compile_expr("roc(126)")
        for sym, b in series.items():
            ev = expr.Evaluator(b)
            if ev.last(rule):
                out["scan"].append({"symbol": sym, "close": round(b.close[-1], 4), "roc_6m_%": round(ev.last(rank) or 0, 2)})
            for h in patterns.scan(b, [x.strip() for x in a.patterns.split(",") if x.strip()]):
                if h["score"] >= a.min_score:
                    out["patterns"].append({"symbol": sym, "pattern": h["pattern"], "score": h["score"],
                                            "close": round(b.close[-1], 4), "pivot": h["pivot"], "stop": h["stop"],
                                            "to_pivot_%": round((h["pivot"] / b.close[-1] - 1) * 100, 2)})
        out["scan"].sort(key=lambda r: -r["roc_6m_%"])
        out["patterns"].sort(key=lambda r: -r["score"])
        out["scan_rule"] = a.rule or a.preset

    if a.report:
        secs = []
        for r in out["regimes"]:
            secs.append((f"Market: {r['index']}", f'<div class="card"><b>{report.esc(r["regime"])}</b> - suggested exposure '
                         f'{r["suggested_exposure_pct"]}% | {r["drawdown_from_52w_high_pct"]}% from high<br>'
                         + "<br>".join(report.esc(n) for n in r["notes"]) + "</div>"))
        rk = out["risk"]
        secs.append(("Risk", report.kpis([("Open trades", rk["open_trades"], ""), ("Open risk %", rk["open_risk_pct"], "pct"),
                                          ("Today P&L", rk["today_pnl"], "signed"), ("Losing streak", rk["losing_streak"], "")])))
        if positions:
            secs.append(("Open positions", report.table(positions, [(k, k) for k in ("symbol", "side", "qty", "entry", "stop", "last",
                                                                                    "open_pnl", "open_r", "to_stop_%", "alert")],
                                                        signed=("open_pnl", "open_r"))))
        if out["patterns"]:
            secs.append(("Live patterns", report.table(out["patterns"][:25], [(k, k) for k in ("symbol", "pattern", "score", "close",
                                                                                              "pivot", "stop", "to_pivot_%")])))
        if out["scan"]:
            secs.append((f"Screen: {out['scan_rule']}", report.table(out["scan"][:40], [("symbol", "symbol"), ("close", "close"),
                                                                                        ("roc_6m_%", "6m %")])))
        out["report"] = report.write(a.report, report.page("Trading brief", out["generated"], secs, DISCLAIMER))

    def md(o):
        lines = [f"# Trading brief - {o['generated']}", ""]
        for r in o["regimes"]:
            lines.append(f"**{r['index']}: {r['regime']}** (exposure {r['suggested_exposure_pct']}%, "
                         f"{r['drawdown_from_52w_high_pct']:+.1f}% from high)")
        rk = o["risk"]
        lines += ["", f"**Risk:** {rk['open_trades']} open, open risk {rk['open_risk_pct']}%, today P&L {rk['today_pnl']:,.2f}, "
                      f"losing streak {rk['losing_streak']}" + (" - KILL SWITCH ON" if rk["kill_switch"] else "")]
        if o["positions"]:
            lines += ["", "### Open positions", cli.md_table(o["positions"], ["id", "symbol", "side", "qty", "entry", "stop",
                                                                             "last", "open_pnl", "open_r", "to_stop_%", "alert"])]
        if o["patterns"]:
            lines += ["", "### Live patterns", cli.md_table(o["patterns"][:15], ["symbol", "pattern", "score", "close", "pivot",
                                                                                "stop", "to_pivot_%"])]
        if o.get("scan_rule"):
            lines += ["", f"### Screen: {o['scan_rule']} ({len(o['scan'])} matches)",
                      cli.md_table(o["scan"][:20], ["symbol", "close", "roc_6m_%"]) if o["scan"] else "none"]
        if o["errors"]:
            lines += ["", "Errors: " + "; ".join(f"{k}: {v[:80]}" for k, v in o["errors"].items())]
        if o.get("report"):
            lines.append(f"\nHTML: `{o['report']}`")
        lines.append("\n_Candidates and context only - every trade still goes through trading-plan and trading-risk._")
        return "\n".join(lines)

    cli.emit(out, a.json, md)


if __name__ == "__main__":
    cli.run(main)
