#!/usr/bin/env python3
"""Performance analytics and coaching from your journal (or any trades CSV).

Examples
  python3 scripts/review.py                                  # all closed trades in the journal
  python3 scripts/review.py --since 2026-01-01 --report review.html
  python3 scripts/review.py --setup VCP
  python3 scripts/review.py --csv trades.csv                 # e.g. trading-backtest --trades-csv output
  python3 scripts/review.py --period week                    # this week's digest
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

import csv  # noqa: E402
import datetime as dt  # noqa: E402
import statistics  # noqa: E402

from tradekit import DISCLAIMER, cli, config, metrics, report  # noqa: E402
from tradekit.journal import Journal  # noqa: E402


def load_trades(a):
    if a.csv:
        rows = []
        with open(a.csv) as fh:
            for r in csv.DictReader(fh):
                t = dict(r)
                for k in ("pnl", "r_multiple", "qty", "entry_price", "exit_price", "bars_held", "hold_days"):
                    if t.get(k) not in (None, ""):
                        try:
                            t[k] = float(t[k])
                        except ValueError:
                            t[k] = None
                    else:
                        t[k] = None
                t.setdefault("exit_time", t.get("exit_date"))
                t.setdefault("entry_time", t.get("entry_date"))
                t.setdefault("setup", t.get("setup") or "")
                rows.append(t)
        return rows
    since = a.since
    if a.period:
        today = dt.date.today()
        start = {"week": today - dt.timedelta(days=today.weekday()), "month": today.replace(day=1),
                 "quarter": today.replace(month=(today.month - 1) // 3 * 3 + 1, day=1),
                 "year": today.replace(month=1, day=1)}[a.period]
        since = start.isoformat()
    return Journal().list(status="closed", since=since, setup=a.setup, account=a.account)


def group(trades, key_fn, min_n=1):
    g = {}
    for t in trades:
        g.setdefault(key_fn(t) or "(none)", []).append(t)
    rows = []
    for k, ts in g.items():
        if len(ts) < min_n:
            continue
        st = metrics.trade_stats(ts)
        rows.append({"group": k, "trades": st["trades"], "win_rate_%": st["win_rate_pct"], "net_pnl": st["net_pnl"],
                     "avg_r": st.get("avg_r"), "total_r": st.get("total_r"), "profit_factor": st.get("profit_factor")})
    return sorted(rows, key=lambda r: -(r["net_pnl"] or 0))


def insights(trades, st, by_setup, cfg):
    tips = []
    n = st["trades"]
    if n < 20:
        tips.append(f"Only {n} closed trades - patterns below are tentative. Keep journaling; 50+ trades makes this meaningful.")
    if st.get("expectancy", 0) < 0:
        tips.append("Negative expectancy: the current approach loses money on average. Cut size to the minimum "
                    "and review which setups are dragging (table below) before trading more.")
    losses_r = [t["r_multiple"] for t in trades if t.get("r_multiple") is not None and t["r_multiple"] < 0]
    if losses_r:
        avg_l = statistics.fmean(losses_r)
        big = sum(1 for r in losses_r if r < -1.25)
        if avg_l < -1.15 or big >= max(2, len(losses_r) * 0.2):
            tips.append(f"Losses average {avg_l:.2f}R and {big} losses exceeded -1.25R: stops are being moved, ignored "
                        "or gapped through. Use broker-side stops and honour the plan.")
    if st.get("avg_hold_losers") and st.get("avg_hold_winners") and st["avg_hold_losers"] > 1.5 * st["avg_hold_winners"]:
        tips.append(f"Losers are held {st['avg_hold_losers']:.1f} vs winners {st['avg_hold_winners']:.1f} (days/bars) - "
                    "classic 'cut winners, ride losers'. Consider time stops and letting winners trail.")
    if st.get("win_rate_pct", 0) >= 55 and (st.get("payoff_ratio") or 0) < 1:
        tips.append("High win rate but small winners (payoff < 1): profits may be taken too early. Test trailing stops "
                    "or a 2R minimum target on half the position.")
    if st.get("win_rate_pct", 100) < 35 and (st.get("payoff_ratio") or 0) < 2:
        tips.append("Low win rate without large winners: entries may be early/late or setups too loose. "
                    "Tighten setup criteria (fewer, better trades).")
    named = [r for r in by_setup if r["group"] != "(none)"]
    good = [r for r in named if r["trades"] >= 5 and (r["avg_r"] or 0) > 0] if len(named) > 1 else []
    bad = [r for r in named if r["trades"] >= 5 and (r["avg_r"] or 0) < 0] if len(named) > 1 else []
    if not named:
        tips.append("No setup names recorded. Tag every trade with a setup so you can see which ones actually make money.")
    if good:
        b = max(good, key=lambda r: r["total_r"] or 0)
        tips.append(f"Best setup: **{b['group']}** ({b['trades']} trades, {b['avg_r']}R avg). Consider allocating more of your risk here.")
    if bad:
        w = min(bad, key=lambda r: r["total_r"] or 0)
        tips.append(f"Worst setup: **{w['group']}** ({w['trades']} trades, {w['avg_r']}R avg). Pause it or redefine it.")
    if st.get("max_consecutive_losses", 0) >= cfg["risk"]["max_consecutive_losses"]:
        tips.append(f"Max losing streak {st['max_consecutive_losses']} reached your pause limit - check whether you kept "
                    "trading through it (revenge trading shows up as larger size after losses).")
    graded = [t for t in trades if t.get("grade") and t.get("r_multiple") is not None]
    if len(graded) >= 6:
        by_g = {}
        for t in graded:
            by_g.setdefault(t["grade"][0].upper(), []).append(t["r_multiple"])
        txt = ", ".join(f"{g}: {statistics.fmean(v):+.2f}R ({len(v)})" for g, v in sorted(by_g.items()))
        tips.append(f"Average R by process grade - {txt}. If A-grade trades beat the rest, discipline is your edge.")
    no_stop = sum(1 for t in trades if t.get("r_multiple") is None)
    if no_stop and not all(t.get("r_multiple") is None for t in trades):
        tips.append(f"{no_stop} trades have no planned stop recorded, so their R is unknown. Always log the stop.")
    pnl_by_sym = {}
    for t in trades:
        pnl_by_sym[t["symbol"]] = pnl_by_sym.get(t["symbol"], 0) + (t["pnl"] or 0)
    total_profit = sum(v for v in pnl_by_sym.values() if v > 0)
    if total_profit > 0:
        top = max(pnl_by_sym, key=pnl_by_sym.get)
        if pnl_by_sym[top] > 0.5 * total_profit and len(pnl_by_sym) > 3:
            tips.append(f"{top} produced over half of all gross profit - results depend on one name; don't mistake luck for edge.")
    return tips


def main():
    p = cli.parser(__doc__)
    p.add_argument("--csv", help="trades CSV instead of the journal")
    p.add_argument("--since")
    p.add_argument("--period", choices=["week", "month", "quarter", "year"])
    p.add_argument("--setup")
    p.add_argument("--account")
    p.add_argument("--report", help="write an HTML report")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    cfg = config.load()
    trades = [t for t in load_trades(a) if t.get("pnl") is not None]
    if not trades:
        cli.fail("no closed trades found (journal empty for this filter?)")
    trades.sort(key=lambda t: str(t.get("exit_time") or ""))
    st = metrics.trade_stats(trades)
    by_setup = group(trades, lambda t: t.get("setup"))
    by_side = group(trades, lambda t: t.get("side"))
    by_symbol = group(trades, lambda t: t.get("symbol"))
    by_dow = group(trades, lambda t: dt.date.fromisoformat(str(t["entry_time"])[:10]).strftime("%a")
                   if t.get("entry_time") else None)
    by_month = group(trades, lambda t: str(t.get("exit_time") or "")[:7])
    equity = cfg["account"]["equity"]
    start_eq = equity - sum(t["pnl"] for t in trades) if not a.csv else equity
    curve, eq = [], start_eq
    for t in trades:
        eq += t["pnl"]
        curve.append((str(t.get("exit_time") or "")[:10], eq))
    dd = metrics.max_drawdown([start_eq] + [v for _, v in curve])
    res = {"trades": len(trades), "stats": st, "max_drawdown": dd, "by_setup": by_setup, "by_side": by_side,
           "by_symbol": by_symbol[:15], "by_weekday": by_dow, "by_month": sorted(by_month, key=lambda r: r["group"]),
           "insights": insights(trades, st, by_setup, cfg),
           "period": {"from": str(trades[0].get("exit_time"))[:10], "to": str(trades[-1].get("exit_time"))[:10]}}
    if a.report:
        rs = [t["r_multiple"] for t in trades if t.get("r_multiple") is not None]
        k = report.kpis([("Net P&L", st["net_pnl"], "signed"), ("Trades", st["trades"], ""),
                         ("Win rate", st["win_rate_pct"], "pct"), ("Profit factor", st.get("profit_factor"), ""),
                         ("Avg R", st.get("avg_r"), "signed"), ("Total R", st.get("total_r"), "signed"),
                         ("Expectancy", st["expectancy"], "signed"), ("Max DD", dd["max_drawdown_pct"], "signedpct"),
                         ("SQN", st.get("sqn"), ""), ("Max loss streak", st["max_consecutive_losses"], "")])
        cols = [("group", "Group"), ("trades", "Trades"), ("win_rate_%", "Win %"), ("net_pnl", "Net P&L"),
                ("avg_r", "Avg R"), ("total_r", "Total R"), ("profit_factor", "PF")]
        sections = [("", k), ("Equity (closed trades)", f'<div class="card">{report.line_chart([("Equity", curve, "var(--acc)")])}</div>')]
        if rs:
            sections.append(("R-multiples", f'<div class="card">{report.histogram_chart(metrics.histogram(rs, 14))}</div>'))
        sections.append(("Coaching", "".join(f'<div class="warn">{report.esc(i.replace("**", ""))}</div>' for i in res["insights"])))
        for title, rows in (("By setup", by_setup), ("By side", by_side), ("By month", res["by_month"]),
                            ("By weekday", by_dow), ("Top symbols", res["by_symbol"])):
            sections.append((title, report.table(rows, cols, signed=("net_pnl", "avg_r", "total_r"))))
        res["report"] = report.write(a.report, report.page("Performance review", f"{res['period']['from']} to "
                                                           f"{res['period']['to']} | {len(trades)} trades", sections, DISCLAIMER))

    def md(r):
        s = r["stats"]
        out = [f"## Performance review: {r['trades']} trades ({r['period']['from']} to {r['period']['to']})", "",
               f"Net P&L **{s['net_pnl']:,.2f}** | win rate {s['win_rate_pct']}% | profit factor {s.get('profit_factor')} | "
               f"payoff {s.get('payoff_ratio')} | expectancy {s['expectancy']:,.2f}/trade",
               f"Avg R {s.get('avg_r')} | total R {s.get('total_r')} | SQN {s.get('sqn')} | max drawdown "
               f"{r['max_drawdown']['max_drawdown_pct']}% | streaks W{s['max_consecutive_wins']}/L{s['max_consecutive_losses']}"
               + (f" | hold winners {s.get('avg_hold_winners')} vs losers {s.get('avg_hold_losers')}" if s.get("avg_hold") else ""),
               "", "### Coaching"]
        out += [f"- {i}" for i in r["insights"]] or ["- Nothing stands out yet."]
        cols = ["group", "trades", "win_rate_%", "net_pnl", "avg_r", "total_r", "profit_factor"]
        out += ["", "### By setup", cli.md_table(r["by_setup"], cols)]
        if len(r["by_side"]) > 1:
            out += ["", "### By side", cli.md_table(r["by_side"], cols)]
        out += ["", "### By month", cli.md_table(r["by_month"], cols)]
        if r.get("report"):
            out.append(f"\nHTML report: `{r['report']}`")
        return "\n".join(out)

    cli.emit(res, a.json, md)


if __name__ == "__main__":
    cli.run(main)
