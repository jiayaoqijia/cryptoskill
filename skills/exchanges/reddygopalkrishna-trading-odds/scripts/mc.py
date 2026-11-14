#!/usr/bin/env python3
"""Monte Carlo: (1) system-level equity/drawdown ranges from R-multiples, (2) setup-level odds of target before stop.

Examples
  python3 scripts/mc.py setup AAPL --entry 195 --stop 188 --target 212 --horizon 20
  python3 scripts/mc.py setup BTC-USD --entry 64000 --stop 61000 --target 70000 --interval 1h --period 1mo --horizon 48
  python3 scripts/mc.py trades --journal --risk-pct 1 --trades 100
  python3 scripts/mc.py trades --csv trades.csv --risk-pct 0.5 --report mc.html     # trading-backtest --trades-csv output
  python3 scripts/mc.py trades --r "2.1,-1,-1,0.4,3,-1,-0.6,1.8,-1,2.5" --trades 200
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

import csv  # noqa: E402

from tradekit import DISCLAIMER, cli, data, montecarlo, report  # noqa: E402


def cmd_setup(a):
    b = data.load_bars(a.symbol, a.csv, a.interval, a.period, a.provider, min_bars=30)
    entry = a.entry if a.entry is not None else b.close[-1]
    r = montecarlo.simulate_setup(b, entry, a.stop, a.target, a.horizon, a.sims, a.lookback, a.block, a.seed)
    r["symbol"] = b.symbol
    cli.emit(r, a.json, lambda x: "\n".join([
        f"## {x['symbol']} {x['setup']['side']} setup: {x['verdict']}",
        f"Entry {x['setup']['entry']} / stop {x['setup']['stop']} / target {x['setup']['target']} "
        f"(R:R {x['setup']['reward_risk']}), horizon {x['setup']['horizon_bars']} bars, {x['n_sims']:,} sims",
        "",
        f"- Target first: **{x['prob_target_first_pct']}%** | stop first: **{x['prob_stop_first_pct']}%** | "
        f"neither: {x['prob_neither_pct']}%",
        f"- Breakeven win rate for this R:R: {x['breakeven_win_rate_pct']}%",
        f"- Expected R: **{x['expected_r']}** | R percentiles 5/50/95: {x['r_percentiles'][5]} / "
        f"{x['r_percentiles'][50]} / {x['r_percentiles'][95]}",
        f"- Median bars to target {x['median_bars_to_target']}, to stop {x['median_bars_to_stop']}",
        f"- History: {x['history']['bars_used']} bars ({x['history']['from']} to {x['history']['to']}), "
        f"block bootstrap of {x['history']['block']}",
        "",
        "_Resamples this symbol's own recent price behaviour. It has no knowledge of news, earnings or "
        "regime change - a simulation of the past, not a forecast._",
    ]))


def _load_rs(a):
    if a.r:
        return [float(x) for x in a.r.split(",") if x.strip()]
    if a.csv:
        rs = []
        with open(a.csv) as fh:
            for row in csv.DictReader(fh):
                v = row.get("r_multiple") or row.get("R") or row.get("r")
                if v not in (None, ""):
                    rs.append(float(v))
        return rs
    if a.journal:
        from tradekit.journal import Journal
        return [t["r_multiple"] for t in Journal().list(status="closed", setup=a.setup) if t["r_multiple"] is not None]
    cli.fail("give --r LIST, --csv FILE (r_multiple column) or --journal")


def cmd_trades(a):
    rs = _load_rs(a)
    r = montecarlo.simulate_trades(rs, a.risk_pct, a.trades, a.sims, a.equity, a.ruin, seed=a.seed,
                                   compounding=not a.no_compound)
    if a.report:
        paths = r["sample_paths"]
        series = [(f"path {i + 1}", [(str(k), v) for k, v in enumerate(pth)], "var(--acc)") for i, pth in enumerate(paths[:25])]
        k = report.kpis([("Median return", r["final_return_pct"][50], "signedpct"),
                         ("5th pct return", r["final_return_pct"][5], "signedpct"),
                         ("95th pct return", r["final_return_pct"][95], "signedpct"),
                         ("Median max DD", r["max_drawdown_pct"][50], "signedpct"),
                         ("95th pct max DD", r["max_drawdown_pct"][95], "signedpct"),
                         ("P(loss)", r["prob_loss_pct"], "pct"), ("Risk of ruin", r["risk_of_ruin_pct"], "pct")])
        chart = report.line_chart(series).replace('stroke-width="1.8"', 'stroke-width="1" stroke-opacity=".45"')
        r["report"] = report.write(a.report, report.page(
            "Monte Carlo: trade resampling", f"{r['inputs']['n_sims']:,} sims x {r['inputs']['n_trades']} trades at "
            f"{a.risk_pct}% risk, sampled from {r['inputs']['trades_sampled_from']} trades",
            [("", k), ("Sample equity paths", f'<div class="card">{chart}</div>')], DISCLAIMER))
    out = dict(r)
    out.pop("sample_paths", None)
    cli.emit(out, a.json, lambda x: "\n".join(filter(None, [
        f"## Monte Carlo: {x['inputs']['n_sims']:,} sequences of {x['inputs']['n_trades']} trades at {a.risk_pct}% risk",
        f"Sampled from {x['inputs']['trades_sampled_from']} trades: win rate {x['inputs']['win_rate_pct']}%, "
        f"avg {x['inputs']['avg_r']}R",
        "",
        "| percentile | final return % | max drawdown % |\n|---|---|---|",
        *[f"| {p}th | {x['final_return_pct'][p]} | {x['max_drawdown_pct'][p]} |" for p in (5, 25, 50, 75, 95)],
        "",
        f"- Probability of ending at a loss: {x['prob_loss_pct']}%",
        "- Probability of a drawdown " + ", ".join(f"{k}: {v}%" for k, v in x["prob_drawdown_pct"].items()),
        f"- Risk of ruin ({x['ruin_definition']}): {x['risk_of_ruin_pct']}%",
        f"- Worst losing streak: median {x['worst_losing_streak'][50]:.0f}, 95th pct {x['worst_losing_streak'][95]:.0f}",
        f"\nReport: `{x['report']}`" if x.get("report") else None,
        "\n_Assumes future trades look like past trades, independently. Real edges decay; treat the 95th "
        "percentile drawdown as a planning minimum, not a worst case._",
    ])))


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup")
    s.add_argument("symbol", nargs="?")
    s.add_argument("--entry", type=float, help="default last close")
    s.add_argument("--stop", type=float, required=True)
    s.add_argument("--target", type=float, required=True)
    s.add_argument("--horizon", type=int, default=20, help="bars to simulate")
    s.add_argument("--lookback", type=int, default=250)
    s.add_argument("--block", type=int, default=5)
    s.add_argument("--sims", type=int, default=10000)
    s.add_argument("--seed", type=int, default=7)
    data.add_data_args(s, period="2y")
    s.add_argument("--json", action="store_true")
    t = sub.add_parser("trades")
    t.add_argument("--r", help="comma list of R-multiples")
    t.add_argument("--csv", help="CSV with an r_multiple column")
    t.add_argument("--journal", action="store_true", help="use closed trades from the journal")
    t.add_argument("--setup", help="with --journal, only this setup")
    t.add_argument("--risk-pct", type=float, default=1.0)
    t.add_argument("--trades", type=int, help="trades per sequence (default = sample size)")
    t.add_argument("--sims", type=int, default=10000)
    t.add_argument("--equity", type=float, default=100000.0)
    t.add_argument("--ruin", type=float, default=50.0, help="drawdown %% that counts as ruin")
    t.add_argument("--no-compound", action="store_true")
    t.add_argument("--seed", type=int, default=7)
    t.add_argument("--report")
    t.add_argument("--json", action="store_true")
    a = p.parse_args()
    {"setup": cmd_setup, "trades": cmd_trades}[a.cmd](a)


if __name__ == "__main__":
    cli.run(main)
