#!/usr/bin/env python3
"""Pre-trade risk gate: hard checks against your risk rules. PASS writes a short-lived approval
that trading-broker requires before submitting.

Examples
  python3 scripts/gate.py check --symbol AAPL --side long --entry 195 --stop 188 --target 212 --qty 70 --setup "VCP"
  python3 scripts/gate.py check --symbol AAPL --side long --entry 195 --stop 188 --target 212 --auto-size
  python3 scripts/gate.py check --plan 12                 # use a planned trade from the journal
  python3 scripts/gate.py status                          # risk dashboard: heat, daily P&L, streak, kill switch
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, config, gate, risk  # noqa: E402
from tradekit.journal import Journal  # noqa: E402

ICON = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}


def _equity_and_positions(override=None):
    try:
        from tradekit.brokers import get_broker
        br = get_broker()
        acct = br.account()
        pos = br.positions()
        return (override or float(acct["equity"])), pos, acct["broker"]
    except Exception:  # noqa: BLE001
        return (override or float(config.load()["account"]["equity"])), None, "config"


def md_check(r):
    out = [f"## Pre-trade gate: **{r['verdict']}** - {r['side'].upper()} {r['qty']:g} {r['symbol']} "
           f"@ {r['entry']} stop {r['stop']}" + (f" target {r['target']}" if r["target"] else ""), ""]
    out.append("| check | result | detail |\n|---|---|---|")
    for c in r["checks"]:
        out.append(f"| {c['check']} | {ICON[c['status']]} | {c['detail']} |")
    out.append("")
    if r.get("approval"):
        ap = r["approval"]
        out.append(f"Approval **{ap['approval_id']}** valid until {ap['expires']}. "
                   "trading-broker will require it for this exact symbol/side/qty/stop.")
    else:
        out.append("No approval issued. Fix the blocking checks (smaller size, better stop/target, or wait).")
    if r.get("sizing_note"):
        out.append(r["sizing_note"])
    return "\n".join(out)


def cmd_check(a):
    cfg = config.load()
    j = Journal()
    trade = {"symbol": a.symbol, "side": a.side, "entry": a.entry, "stop": a.stop, "target": a.target,
             "qty": a.qty, "setup": a.setup, "thesis": a.thesis}
    trade_id = None
    if a.plan:
        t = j.get(a.plan)
        if t["status"] != "planned":
            cli.fail(f"journal trade {a.plan} is {t['status']}, not planned")
        trade_id = t["id"]
        trade.update({"symbol": t["symbol"], "side": t["side"], "entry": t["plan_entry"], "stop": t["plan_stop"],
                      "target": t["plan_target"], "qty": a.qty or t["qty"], "setup": a.setup or t["setup"],
                      "thesis": a.thesis or t["thesis"]})
    for k in ("symbol", "entry", "stop"):
        if trade.get(k) in (None, ""):
            cli.fail(f"--{k} is required (or use --plan ID)")
    equity, positions, src = _equity_and_positions(a.equity)
    note = None
    if a.auto_size or not trade.get("qty"):
        sz = risk.position_size(equity, float(trade["entry"]), float(trade["stop"]),
                                float(cfg["risk"]["risk_per_trade_pct"]),
                                max_position_pct=cfg["risk"]["max_position_pct"], lot_size=a.lot,
                                fractional=a.fractional)
        trade["qty"] = sz["qty"]
        note = f"Auto-sized to {sz['qty']:g} units ({sz['actual_risk_pct']}% risk, bound by {sz['binding_constraint']})."
    r = gate.evaluate(trade, equity, j, cfg, positions)
    r["equity_source"] = src
    r["sizing_note"] = note
    if r["verdict"] != "FAIL":
        r["approval"] = gate.write_approval(r, trade_id)
        gate.audit("gate_pass", **{k: r[k] for k in ("symbol", "side", "qty", "entry", "stop", "target", "verdict")},
                   approval=r["approval"]["approval_id"])
    else:
        gate.audit("gate_fail", symbol=r["symbol"], blocking=r["blocking"])
    cli.emit(r, a.json, md_check)
    if r["verdict"] == "FAIL":
        sys.exit(3)


def cmd_status(a):
    cfg = config.load()
    lim = cfg["risk"]
    j = Journal()
    equity, positions, src = _equity_and_positions(a.equity)
    open_t = j.list(status="open")
    heat = sum(abs(t["entry_price"] - t["stop"]) * float(t["qty"]) for t in open_t
               if t["stop"] is not None and t["entry_price"] is not None and t["qty"])
    today = sum(t["pnl"] or 0 for t in j.closed_today())
    dd = gate.drawdown_from_peak(j, equity)
    st = {"equity": equity, "equity_source": src, "kill_switch": config.kill_switch_on(),
          "open_trades": len(open_t), "broker_positions": len(positions) if positions is not None else None,
          "open_risk": round(heat, 2), "open_risk_pct": round(heat / equity * 100, 2) if equity else None,
          "open_risk_limit_pct": lim["max_open_risk_pct"], "today_realized_pnl": round(today, 2),
          "daily_loss_limit_pct": lim["max_daily_loss_pct"], "consecutive_losses": j.consecutive_losses(),
          "loss_streak_limit": lim["max_consecutive_losses"],
          "drawdown_from_peak_pct": round(dd, 2) if dd is not None else None,
          "drawdown_limit_pct": lim["max_drawdown_pct"],
          "open_without_stop": [t["symbol"] for t in open_t if t["stop"] is None]}
    room = lim["max_open_risk_pct"] - (st["open_risk_pct"] or 0)
    st["risk_room_pct"] = round(room, 2)
    cli.emit(st, a.json, lambda s: "\n".join(filter(None, [
        f"## Risk status ({s['equity_source']} equity {s['equity']:,.2f})",
        f"- Kill switch: {'ON - trading halted' if s['kill_switch'] else 'off'}",
        f"- Open trades: {s['open_trades']}" + (f" (broker shows {s['broker_positions']} positions)" if s['broker_positions'] is not None else ""),
        f"- Open risk: {s['open_risk']:,.2f} = {s['open_risk_pct']}% of {s['open_risk_limit_pct']}% limit -> room {s['risk_room_pct']}%",
        f"- Today's realized P&L: {s['today_realized_pnl']:,.2f} (daily stop {s['daily_loss_limit_pct']}%)",
        f"- Losing streak: {s['consecutive_losses']} (pause at {s['loss_streak_limit']})",
        f"- Drawdown from journal peak: {s['drawdown_from_peak_pct']}% (limit {s['drawdown_limit_pct']}%)" if s['drawdown_from_peak_pct'] is not None else None,
        f"- WARNING: open trades without a stop: {', '.join(s['open_without_stop'])}" if s['open_without_stop'] else None,
    ])))


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--symbol")
    c.add_argument("--side", default="long", choices=["long", "short", "buy", "sell"])
    c.add_argument("--entry", type=float)
    c.add_argument("--stop", type=float)
    c.add_argument("--target", type=float)
    c.add_argument("--qty", type=float)
    c.add_argument("--auto-size", action="store_true")
    c.add_argument("--lot", type=float, default=1)
    c.add_argument("--fractional", action="store_true")
    c.add_argument("--setup", default="")
    c.add_argument("--thesis", default="")
    c.add_argument("--plan", type=int, help="journal id of a planned trade")
    c.add_argument("--equity", type=float)
    c.add_argument("--json", action="store_true")
    s = sub.add_parser("status")
    s.add_argument("--equity", type=float)
    s.add_argument("--json", action="store_true")
    a = p.parse_args()
    {"check": cmd_check, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    cli.run(main)
