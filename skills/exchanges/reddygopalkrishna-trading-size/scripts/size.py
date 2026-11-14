#!/usr/bin/env python3
"""Position sizing calculator (pure math, no data needed).

Examples
  python3 scripts/size.py risk --equity 50000 --entry 120 --stop 114 --risk-pct 1
  python3 scripts/size.py risk --equity 50000 --entry 120 --stop 114 --risk-amount 400 --max-position-pct 20
  python3 scripts/size.py risk --equity 2000000 --entry 22500 --stop 22350 --lot 50 --multiplier 1 --margin-pct 12
  python3 scripts/size.py risk --equity 10000 --entry 64000 --stop 61000 --fractional --lot 0.0001
  python3 scripts/size.py table --equity 50000 --entry 120 --stop 114
  python3 scripts/size.py kelly --win-rate 0.45 --payoff 2.2
  python3 scripts/size.py vol --equity 100000 --price 50 --annual-vol 35 --target-vol 10
  python3 scripts/size.py ruin --win-rate 0.45 --payoff 2 --risk-pct 1 --ruin-pct 30
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, config, risk  # noqa: E402


def _equity(a):
    if a.equity is not None:
        return a.equity
    return float(config.load()["account"]["equity"])


def cmd_risk(a):
    eq = _equity(a)
    pct = a.risk_pct
    if a.risk_amount is not None:
        pct = a.risk_amount / eq * 100
    if pct is None:
        pct = float(config.load()["risk"]["risk_per_trade_pct"])
    r = risk.position_size(eq, a.entry, a.stop, pct, lot_size=a.lot, multiplier=a.multiplier,
                           max_position_pct=a.max_position_pct, cash=a.cash, fractional=a.fractional,
                           fee_per_unit=a.fee_per_unit, margin_pct=a.margin_pct)
    r["equity"] = eq
    r["risk_pct_requested"] = round(pct, 4)
    if a.target:
        r["target"] = a.target
        r["reward_risk"] = risk.reward_risk(a.entry, a.stop, a.target)
        r["potential_profit"] = round(abs(a.target - a.entry) * r["qty"] * a.multiplier, 2)
    cli.emit(r, a.json, lambda x: "\n".join(filter(None, [
        f"## {x['side'].upper()} size: **{x['qty']:g}** units" + (f" ({x['lots']:g} lots)" if x.get("lots") else ""),
        f"Entry {x['entry']} / stop {x['stop']} -> risk per unit {x['risk_per_unit']}",
        f"Risk {x['actual_risk']:,.2f} = {x['actual_risk_pct']}% of {x['equity']:,.2f} (budget {x['risk_budget']:,.2f})",
        f"Notional {x['notional']:,.2f} ({x['position_pct']}% of equity), capital required {x['capital_required']:,.2f}",
        f"Binding constraint: {x['binding_constraint']}",
        f"Reward:risk {x['reward_risk']} -> potential profit {x['potential_profit']:,.2f}" if x.get("target") else None,
        f"Note: {x['note']}" if x.get("note") else None,
    ])))


def cmd_table(a):
    eq = _equity(a)
    rows = []
    for pct in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0):
        r = risk.position_size(eq, a.entry, a.stop, pct, lot_size=a.lot, multiplier=a.multiplier,
                               fractional=a.fractional, margin_pct=a.margin_pct)
        rows.append({"risk_%": pct, "qty": r["qty"], "risk": r["actual_risk"], "notional": r["notional"],
                     "position_%": r["position_pct"], "losses_to_-20%": round(20 / pct)})
    cli.emit(rows, a.json, lambda x: f"## Size table (equity {eq:,.0f}, entry {a.entry}, stop {a.stop})\n\n"
             + cli.md_table(x, list(x[0].keys())) +
             "\n\n`losses_to_-20%` = consecutive full losses before a 20% drawdown.")


def cmd_kelly(a):
    f = risk.kelly(a.win_rate, a.payoff)
    out = {"win_rate": a.win_rate, "payoff": a.payoff, "kelly_fraction_pct": round(f * 100, 2),
           "half_kelly_pct": round(f * 50, 2), "quarter_kelly_pct": round(f * 25, 2),
           "expectancy_r": round(a.win_rate * a.payoff - (1 - a.win_rate), 4)}
    cli.emit(out, a.json, lambda x: (
        f"## Kelly: {x['kelly_fraction_pct']}% (half {x['half_kelly_pct']}%, quarter {x['quarter_kelly_pct']}%)\n"
        f"Expectancy {x['expectancy_r']}R per trade.\n\n"
        "Kelly here is the fraction of equity to RISK per trade. It assumes your win rate and payoff are exact - "
        "they never are. Most traders cap risk far below Kelly (quarter-Kelly or a flat 0.5-1%)."
        if x["kelly_fraction_pct"] > 0 else "## No edge: Kelly is 0%. Do not size up a negative-expectancy system."))


def cmd_vol(a):
    r = risk.volatility_size(_equity(a), a.price, a.annual_vol, a.target_vol, a.lot, a.fractional)
    cli.emit(r, a.json, lambda x: f"## Volatility-target size: {x['qty']:g} units "
             f"({x['weight_pct']}% weight, notional {x['notional']:,.2f}) for {a.target_vol}% annual vol contribution")


def cmd_ruin(a):
    p = risk.risk_of_ruin(a.win_rate, a.payoff, a.risk_pct, a.ruin_pct)
    cli.emit({"risk_of_ruin": p, "ruin_pct": a.ruin_pct}, a.json,
             lambda x: f"## Risk of a {a.ruin_pct}% drawdown: ~{x['risk_of_ruin'] * 100:.2f}% (closed-form approximation)\n"
                       "For path-based estimates from your own trades use trading-odds.")


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("risk", "table"):
        s = sub.add_parser(name)
        s.add_argument("--equity", type=float)
        s.add_argument("--entry", type=float, required=True)
        s.add_argument("--stop", type=float, required=True)
        s.add_argument("--lot", type=float, default=1)
        s.add_argument("--multiplier", type=float, default=1.0)
        s.add_argument("--margin-pct", type=float, default=100.0)
        s.add_argument("--fractional", action="store_true")
        s.add_argument("--json", action="store_true")
        if name == "risk":
            s.add_argument("--risk-pct", type=float)
            s.add_argument("--risk-amount", type=float)
            s.add_argument("--max-position-pct", type=float)
            s.add_argument("--cash", type=float)
            s.add_argument("--fee-per-unit", type=float, default=0.0)
            s.add_argument("--target", type=float)
    k = sub.add_parser("kelly")
    k.add_argument("--win-rate", type=float, required=True, help="0-1")
    k.add_argument("--payoff", type=float, required=True, help="avg win / avg loss")
    k.add_argument("--json", action="store_true")
    v = sub.add_parser("vol")
    v.add_argument("--equity", type=float)
    v.add_argument("--price", type=float, required=True)
    v.add_argument("--annual-vol", type=float, required=True, help="annualized volatility %%")
    v.add_argument("--target-vol", type=float, default=10.0)
    v.add_argument("--lot", type=float, default=1)
    v.add_argument("--fractional", action="store_true")
    v.add_argument("--json", action="store_true")
    r = sub.add_parser("ruin")
    r.add_argument("--win-rate", type=float, required=True)
    r.add_argument("--payoff", type=float, required=True)
    r.add_argument("--risk-pct", type=float, required=True)
    r.add_argument("--ruin-pct", type=float, default=50.0)
    r.add_argument("--json", action="store_true")
    a = p.parse_args()
    {"risk": cmd_risk, "table": cmd_table, "kelly": cmd_kelly, "vol": cmd_vol, "ruin": cmd_ruin}[a.cmd](a)


if __name__ == "__main__":
    cli.run(main)
