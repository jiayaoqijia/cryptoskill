#!/usr/bin/env python3
"""Backtest a rule-based strategy on one or many symbols, with costs, stops, targets and an HTML report.

Examples
  python3 scripts/backtest.py --spec assets/strategies/rsi2-pullback.json --universe AAPL,MSFT,NVDA
  python3 scripts/backtest.py --entry "cross_above(ema(20), ema(50))" --exit "cross_below(ema(20), ema(50))" \
      --stop atr:3 --start 2010-01-01 --report sma_cross.html SPY
  python3 scripts/backtest.py --spec my.json --universe list.txt --set n=10 --set mult=2.5 --oos-start 2021-01-01
  python3 scripts/backtest.py --spec my.json --csv-dir ./data --universe A,B,C --json
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

import json  # noqa: E402
import re  # noqa: E402

from tradekit import DISCLAIMER, backtest, cli, config, data, metrics, report  # noqa: E402
from tradekit.frame import Bars  # noqa: E402


def parse_level(s):
    if s is None:
        return None
    s = str(s).strip()
    low = s.lower()
    if low in ("none", "off"):
        return {"type": "none"}
    if low.startswith("atr:"):
        return {"type": "atr", "mult": float(low[4:]), "n": 14}
    if low.startswith("pct:"):
        return {"type": "pct", "value": float(low[4:])}
    if low.startswith("r:"):
        return {"type": "r", "value": float(low[2:])}
    return {"type": "expr", "value": s}


def substitute(spec, params):
    def sub(v):
        if isinstance(v, str):
            return re.sub(r"\{(\w+)\}", lambda m: str(params.get(m.group(1), m.group(0))), v)
        if isinstance(v, dict):
            return {k: sub(x) for k, x in v.items()}
        if isinstance(v, list):
            return [sub(x) for x in v]
        return v
    return sub(spec)


def build_spec(a):
    spec = {}
    if a.spec:
        spec = json.loads(open(a.spec).read())
    for key in ("entry", "exit", "name", "side", "rank_by"):
        v = getattr(a, key, None)
        if v:
            spec[key] = v
    if a.stop:
        spec["stop"] = parse_level(a.stop)
    if a.target:
        spec["target"] = parse_level(a.target) if a.target.lower() not in ("none", "off") else None
    if a.trail:
        spec["trail"] = parse_level(a.trail)
    if a.max_bars:
        spec["max_bars"] = a.max_bars
    if a.max_positions:
        spec["max_positions"] = a.max_positions
    if a.risk_pct:
        spec["sizing"] = {"type": "risk", "risk_pct": a.risk_pct}
    if a.capital:
        spec["initial_capital"] = a.capital
    if a.oos_start:
        spec["oos_start"] = a.oos_start
    if "costs" not in spec:
        spec["costs"] = dict(config.load()["costs"])
    params = dict(spec.get("params", {}))
    for kv in a.set or []:
        k, _, v = kv.partition("=")
        params[k.strip()] = v.strip()
    spec = substitute(spec, params)
    spec["params"] = params
    return spec


def load_universe(a, spec):
    syms = data.load_universe(a.universe, a.symbols)
    if not syms and spec.get("universe"):
        u = spec["universe"]
        syms = data.load_universe(",".join(u) if isinstance(u, list) else u)
    return syms


def html_report(res, path):
    m = res["metrics"]
    eq = [(d, v) for d, v in res["equity"]]
    series = [("Strategy", eq, "var(--acc)")]
    bm = res.get("benchmark") or {}
    if bm.get("equity"):
        series.append((f"Buy & hold {bm['symbol']}", [(d, v) for d, v in bm["equity"]], "var(--muted)"))
    dd = metrics.drawdown_series([v for _, v in eq])
    rs = [t["r_multiple"] for t in res["trades"] if t["r_multiple"] is not None]
    k = report.kpis([
        ("Total return", m.get("total_return_pct"), "signedpct"), ("CAGR", m.get("cagr_pct"), "signedpct"),
        ("Max drawdown", m.get("max_drawdown_pct"), "signedpct"), ("Sharpe", m.get("sharpe"), ""),
        ("Sortino", m.get("sortino"), ""), ("Trades", m.get("trades"), ""),
        ("Win rate", m.get("win_rate_pct"), "pct"), ("Profit factor", m.get("profit_factor"), ""),
        ("Avg R", m.get("avg_r"), "signed"), ("Expectancy", m.get("expectancy"), "signed"),
        ("Exposure", m.get("exposure_pct"), "pct"),
        ("Benchmark", bm.get("total_return_pct"), "signedpct"),
    ])
    sections = [("", k), ("Equity", f'<div class="card">{report.line_chart(series)}</div>'),
                ("Drawdown", f'<div class="card">{report.area_chart(list(zip([d for d, _ in eq], dd)))}</div>')]
    if rs:
        sections.append(("R-multiple distribution", f'<div class="card">{report.histogram_chart(metrics.histogram(rs, 16))}</div>'))
    for label in ("in_sample", "out_of_sample"):
        if res.get(label) and "total_return_pct" in res[label]:
            s = res[label]
            sections.append((label.replace("_", " ").title(), report.kpis([
                ("Return", s.get("total_return_pct"), "signedpct"), ("CAGR", s.get("cagr_pct"), "signedpct"),
                ("Max DD", s.get("max_drawdown_pct"), "signedpct"), ("Sharpe", s.get("sharpe"), ""),
                ("Trades", s.get("trades"), ""), ("Avg R", s.get("avg_r"), "signed")])))
    if res["warnings"]:
        sections.append(("Caveats", "".join(f'<div class="warn">{report.esc(w)}</div>' for w in res["warnings"])))
    cols = [("symbol", "Symbol"), ("entry_date", "Entry"), ("entry_price", "Price"), ("exit_date", "Exit"),
            ("exit_price", "Price"), ("qty", "Qty"), ("pnl", "P&L"), ("r_multiple", "R"), ("bars_held", "Bars"),
            ("exit_reason", "Reason")]
    sections.append((f"Trades (last 200 of {len(res['trades'])})",
                     report.table(list(reversed(res["trades"]))[:200], cols, signed=("pnl", "r_multiple"))))
    spec = {k: v for k, v in res["spec"].items() if k not in ("costs",)}
    sections.append(("Strategy spec", f'<div class="card"><pre>{report.esc(json.dumps(spec, indent=2))}</pre></div>'))
    sub = f"{', '.join(res['symbols'][:12])}{'...' if len(res['symbols']) > 12 else ''} | {m.get('start')} to {m.get('end')}"
    return report.write(path, report.page(f"Backtest: {res['name']}", sub, sections, DISCLAIMER))


def md(res):
    m = res["metrics"]
    bm = res.get("benchmark") or {}
    out = [f"## Backtest: {res['name']} - {len(res['symbols'])} symbol(s), {m.get('start')} to {m.get('end')}", ""]
    rows = [
        ("Total return", f"{m.get('total_return_pct')}%", f"{bm.get('total_return_pct')}% ({bm.get('symbol')})" if bm else "-"),
        ("CAGR", f"{m.get('cagr_pct')}%", f"{bm.get('cagr_pct')}%" if bm.get("cagr_pct") is not None else "-"),
        ("Max drawdown", f"{m.get('max_drawdown_pct')}%", f"{bm.get('max_drawdown_pct')}%" if bm.get("max_drawdown_pct") is not None else "-"),
        ("Sharpe / Sortino", f"{m.get('sharpe')} / {m.get('sortino')}", str(bm.get("sharpe", "-"))),
    ]
    out.append("| metric | strategy | benchmark |\n|---|---|---|")
    out += [f"| {a} | {b} | {c} |" for a, b, c in rows]
    out.append("")
    out.append(f"Trades {m.get('trades')} | win rate {m.get('win_rate_pct')}% | profit factor {m.get('profit_factor')} | "
               f"avg R {m.get('avg_r')} | expectancy {m.get('expectancy')} | avg hold {m.get('avg_hold')} bars | "
               f"exposure {m.get('exposure_pct')}% | max losing streak {m.get('max_consecutive_losses')}")
    for label in ("in_sample", "out_of_sample"):
        s = res.get(label)
        if s and "total_return_pct" in s:
            out.append(f"- **{label.replace('_', '-')}**: return {s['total_return_pct']}%, CAGR {s.get('cagr_pct')}%, "
                       f"max DD {s['max_drawdown_pct']}%, Sharpe {s.get('sharpe')}, trades {s.get('trades')}, avg R {s.get('avg_r')}")
    reasons = {}
    for t in res["trades"]:
        reasons[t["exit_reason"]] = reasons.get(t["exit_reason"], 0) + 1
    if reasons:
        out.append("Exit reasons: " + ", ".join(f"{k} {v}" for k, v in sorted(reasons.items(), key=lambda x: -x[1])))
    if res.get("report"):
        out.append(f"\nHTML report: `{res['report']}`")
    if res.get("trades_csv"):
        out.append(f"Trades CSV: `{res['trades_csv']}`")
    if res.get("errors"):
        out.append("Data errors: " + "; ".join(f"{k}: {v}" for k, v in res["errors"].items()))
    out.append("\n**Caveats:**")
    out += [f"- {w}" for w in res["warnings"]]
    return "\n".join(out)


def main():
    p = cli.parser(__doc__)
    p.add_argument("symbols", nargs="*")
    p.add_argument("--universe")
    p.add_argument("--spec", help="strategy JSON file")
    p.add_argument("--name")
    p.add_argument("--entry")
    p.add_argument("--exit")
    p.add_argument("--side", choices=["long", "short"])
    p.add_argument("--stop", help="atr:M | pct:N | none | RULE")
    p.add_argument("--target", help="r:M | pct:N | none | RULE")
    p.add_argument("--trail", help="atr:M | pct:N")
    p.add_argument("--max-bars", type=int)
    p.add_argument("--max-positions", type=int)
    p.add_argument("--risk-pct", type=float)
    p.add_argument("--rank-by")
    p.add_argument("--capital", type=float)
    p.add_argument("--oos-start", help="date starting the out-of-sample period")
    p.add_argument("--set", action="append", help="param=value substituted into {param} placeholders")
    p.add_argument("--start", default=None)
    p.add_argument("--end", default=None)
    p.add_argument("--period", default="10y", choices=data.PERIODS)
    p.add_argument("--interval", default="1d", choices=data.INTERVALS)
    p.add_argument("--provider", choices=["yahoo", "csv", "kite"])
    p.add_argument("--csv-dir", help="folder of SYMBOL.csv files (overrides provider)")
    p.add_argument("--benchmark", help="benchmark symbol (default config account.benchmark)")
    p.add_argument("--report", help="write an HTML report here")
    p.add_argument("--trades-csv", help="write trades to CSV")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    spec = build_spec(a)
    if not spec.get("entry"):
        cli.fail("strategy needs an entry rule: --entry RULE or --spec FILE")
    syms = load_universe(a, spec)
    if not syms:
        cli.fail("no symbols: pass symbols, --universe, or a 'universe' in the spec")
    errors = {}
    if a.csv_dir:
        series = {}
        for s in syms:
            f = os.path.join(a.csv_dir, s.replace(":", "_").replace("/", "_") + ".csv")
            try:
                series[s] = Bars.from_csv(f, symbol=s, interval=a.interval)
                series[s].meta.setdefault("adjusted", True)
            except Exception as e:  # noqa: BLE001
                errors[s] = str(e)
        if a.start:
            series = {k: v.since(a.start) for k, v in series.items()}
        if a.end:
            series = {k: v.until(a.end) for k, v in series.items()}
    else:
        series, errors = data.get_many(syms, a.interval, a.period, a.provider, start=a.start, end=a.end)
    if not series:
        cli.fail("no data loaded: " + "; ".join(f"{k}: {v}" for k, v in errors.items()))
    bm_sym = a.benchmark or spec.get("benchmark") or config.load()["account"].get("benchmark")
    bm = None
    if bm_sym and not a.csv_dir:
        try:
            first = min(b.date[0] for b in series.values())
            bm = data.get_bars(bm_sym, a.interval, a.period, start=a.start or first[:10], end=a.end, provider=a.provider)
        except Exception as e:  # noqa: BLE001
            errors[f"benchmark {bm_sym}"] = str(e)
    res = backtest.run(spec, series, bm)
    res["errors"] = errors
    if a.report:
        res["report"] = html_report(res, a.report)
    if a.trades_csv:
        import csv
        with open(a.trades_csv, "w", newline="") as fh:
            if res["trades"]:
                w = csv.DictWriter(fh, fieldnames=list(res["trades"][0].keys()))
                w.writeheader()
                w.writerows(res["trades"])
        res["trades_csv"] = os.path.abspath(a.trades_csv)
    if a.json:
        out = dict(res)
        if len(out["equity"]) > 600:
            step = len(out["equity"]) // 500 + 1
            out["equity"] = out["equity"][::step] + [out["equity"][-1]]
        if out.get("benchmark", {}).get("equity"):
            out["benchmark"] = {k: v for k, v in out["benchmark"].items() if k != "equity"}
        print(cli.dump(out))
    else:
        print(md(res))


if __name__ == "__main__":
    cli.run(main)
