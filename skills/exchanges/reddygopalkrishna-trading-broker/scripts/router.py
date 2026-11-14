#!/usr/bin/env python3
"""Order router with a two-step, human-confirmed flow. Paper broker by default.

  1. preview  -> validates, checks kill switch + gate approval, prints a CONFIRM CODE
  2. submit --confirm CODE   (only after the user explicitly approves that exact order)

Examples
  python3 scripts/router.py preview --symbol AAPL --side buy --qty 70 --type limit --limit-price 195 --stop-loss 188 --take-profit 212
  python3 scripts/router.py submit --confirm 7KQ2XD
  python3 scripts/router.py preview --symbol AAPL --side sell --qty 70 --type market --close      # exit a position
  python3 scripts/router.py account | positions | orders --open
  python3 scripts/router.py cancel P1a2b3c4d5
  python3 scripts/router.py process            # paper: fill resting orders, sync journal
  python3 scripts/router.py kill on --reason "stepping away"   |   kill off   |   kill status
  python3 scripts/router.py kill on --flatten  # paper: cancel orders + close everything
  python3 scripts/router.py preview --protect --symbol NSE:INFY --qty 10 --stop-price 1450   # Kite GTT stop
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

import datetime as dt  # noqa: E402
import json  # noqa: E402
import secrets  # noqa: E402
import string  # noqa: E402

from tradekit import cli, config, gate  # noqa: E402
from tradekit.brokers import BrokerError, get_broker  # noqa: E402
from tradekit.brokers.base import normalize_order  # noqa: E402
from tradekit.journal import Journal  # noqa: E402


def _code() -> str:
    alphabet = string.ascii_uppercase.replace("O", "").replace("I", "") + "23456789"
    return "".join(secrets.choice(alphabet) for _ in range(6))


def _broker_guard(broker):
    cfg = config.load()
    if broker.live and not cfg["broker"]["live_trading_enabled"]:
        cli.fail(f"broker '{broker.name}' sends REAL orders but live trading is disabled. "
                 "Use the paper broker, or enable with trading-setup: setup.py live on --i-understand-the-risks")


def cmd_preview(a):
    if config.kill_switch_on():
        cli.fail("KILL SWITCH is ON - no orders. Turn off with: router.py kill off (only if the user asks)")
    cfg = config.load()
    broker = get_broker(a.broker)
    _broker_guard(broker)
    if a.protect:
        if broker.name != "kite":
            cli.fail("--protect places a Kite GTT stop; paper orders carry stop_loss directly")
        if not (a.symbol and a.qty and a.stop_price):
            cli.fail("--protect needs --symbol --qty --stop-price")
        plan = broker.protect_plan(a.symbol, a.stop_price)  # fails here, before a confirm code, on a bad tick
        pending = {"kind": "protect", "symbol": a.symbol, "qty": int(a.qty), "stop": a.stop_price,
                   "limit": plan["limit"], "product": a.product or cfg["broker"].get("default_product") or "CNC"}
    else:
        order = {"symbol": a.symbol, "side": a.side, "qty": a.qty, "type": a.type or cfg["broker"]["default_order_type"],
                 "limit_price": a.limit_price, "stop_price": a.stop_price, "stop_loss": a.stop_loss,
                 "take_profit": a.take_profit, "product": a.product, "tag": a.tag}
        if order["type"] in ("limit",) and order["limit_price"] is None:
            cli.fail("limit order needs --limit-price (or use --type market)")
        o = normalize_order(order)
        approval = None
        if a.close:
            pos = next((p for p in broker.positions() if p["symbol"] == o["symbol"]), None)
            if not pos:
                cli.fail(f"--close: no open position in {o['symbol']}")
            if (pos["qty"] > 0 and o["side"] != "sell") or (pos["qty"] < 0 and o["side"] != "buy"):
                cli.fail("--close side must reduce the position (sell a long, buy back a short)")
            if o["qty"] > abs(pos["qty"]):
                cli.fail(f"--close qty {o['qty']} exceeds position {abs(pos['qty'])}")
        else:
            if o.get("stop_loss") is None:
                cli.fail("opening orders need --stop-loss (the gate approval is tied to it)")
            approval = gate.find_approval(o["symbol"], o["side"], o["qty"], o["stop_loss"])
            if not approval:
                cli.fail("no valid trading-risk approval for this exact symbol/side/qty/stop. "
                         f"Run: gate.py check --symbol {o['symbol']} --side {'long' if o['side'] == 'buy' else 'short'} "
                         f"--entry <price> --stop {o['stop_loss']} --qty {o['qty']:g} [--target ...]")
        ref = o.get("limit_price") or o.get("stop_price")
        if ref is None:
            try:
                from tradekit.data import get_provider
                ref = float(get_provider().quote(o["symbol"])["price"])
            except Exception:  # noqa: BLE001
                ref = None
        if broker.name == "kite":
            o["kite_params"] = broker.to_kite_params(order)
        elif hasattr(broker, "to_params"):
            broker.to_params(order)  # fail here, before a confirm code, on a bad symbol/product/price
        pending = {"kind": "close" if a.close else "open", "order": o,
                   "approval_id": approval["approval_id"] if approval else None,
                   "trade_id": approval.get("trade_id") if approval else None,
                   "setup": approval.get("setup", "") if approval else "",
                   "est_price": ref, "est_notional": round(ref * o["qty"], 2) if ref else None}
    code = _code()
    ttl = int(cfg["risk"].get("confirm_ttl_minutes", 10))
    pending.update({"code": code, "broker": broker.name, "live": broker.live,
                    "created": dt.datetime.now().isoformat(timespec="seconds"),
                    "expires": (dt.datetime.now() + dt.timedelta(minutes=ttl)).isoformat(timespec="seconds")})
    config.path("pending", code + ".json").write_text(json.dumps(pending, indent=2))
    gate.audit("preview", code=code, broker=broker.name, live=broker.live, pending=pending)
    cli.emit(pending, a.json, md_preview)


def md_preview(p):
    mode = "LIVE - REAL MONEY" if p["live"] else "PAPER (simulated)"
    out = [f"## Order preview [{mode}] via {p['broker']}", ""]
    if p["kind"] == "protect":
        out.append(f"GTT stop-loss: SELL {p['qty']} {p['symbol']} if price <= {p['stop']}"
                   + (f", limit {p['limit']}" if p.get("limit") is not None else "") + f" ({p['product']})")
    else:
        o = p["order"]
        px = o.get("limit_price") or o.get("stop_price") or "market"
        out.append(f"**{o['side'].upper()} {o['qty']:g} {o['symbol']}** {o['type']} @ {px}"
                   + (f" | stop-loss {o['stop_loss']}" if o.get("stop_loss") else "")
                   + (f" | take-profit {o['take_profit']}" if o.get("take_profit") else ""))
        if p.get("est_notional"):
            out.append(f"Estimated notional {p['est_notional']:,.2f} (ref price {p['est_price']})")
        out.append("Purpose: " + ("close/reduce existing position" if p["kind"] == "close"
                                  else f"open position (gate approval {p['approval_id']})"))
        if p["broker"] == "kite" and p["kind"] == "open" and o.get("stop_loss"):
            out.append("Note: Kite entry orders do not carry the stop. After the fill, place a protective "
                       "GTT with `preview --protect` or a stop order.")
        elif p["live"] and p["broker"] != "kite" and p["kind"] == "open" and o.get("stop_loss"):
            out.append(f"Note: {p['broker']} entry orders do not carry the stop. After the fill, place a protective "
                       "stop order (preview --type stop --stop-price ... --close).")
    out.append("")
    out.append(f"CONFIRM CODE: **{p['code']}** (expires {p['expires']})")
    out.append("Ask the user to confirm this exact order. Only after an explicit yes, run: "
               f"`router.py submit --confirm {p['code']}`")
    return "\n".join(out)


def _load_pending(code):
    f = config.path("pending", code.upper() + ".json")
    if not f.exists():
        cli.fail(f"no pending order with code {code} (expired, already submitted, or never previewed)")
    p = json.loads(f.read_text())
    if dt.datetime.fromisoformat(p["expires"]) < dt.datetime.now():
        f.unlink()
        cli.fail("confirm code expired - preview the order again")
    return p, f


def cmd_submit(a):
    if config.kill_switch_on():
        cli.fail("KILL SWITCH is ON - submission blocked")
    p, f = _load_pending(a.confirm)
    broker = get_broker(p["broker"])
    _broker_guard(broker)
    j = Journal()
    if p["kind"] == "protect":
        res = broker.protect(p["symbol"], p["qty"], p["stop"], p["product"])
        f.unlink()
        gate.audit("protect_submitted", result=res)
        cli.emit(res, a.json, lambda r: f"GTT stop placed: id {r['gtt_id']} trigger {r['trigger']} limit {r['limit']}")
        return
    o = p["order"]
    if p["kind"] == "open":
        appr = gate.find_approval(o["symbol"], o["side"], o["qty"], o["stop_loss"])
        if not appr:
            cli.fail("gate approval expired - re-run trading-risk, then preview again")
    order = {k: v for k, v in o.items() if k != "kite_params"}
    try:
        res = broker.place(order)
    except BrokerError as e:
        gate.audit("submit_failed", code=p["code"], error=str(e))
        cli.fail(f"broker rejected the order: {e}")
    f.unlink()
    gate.audit("submitted", code=p["code"], broker=broker.name, live=broker.live, result=res)
    journal_note = None
    filled = res.get("status") == "filled"
    px = res.get("avg_fill_price") or o.get("limit_price") or p.get("est_price")
    if p["kind"] == "open":
        gate.consume_approval(p["approval_id"])
        if filled or broker.live:
            t = j.open(p.get("trade_id"), symbol=o["symbol"], side="long" if o["side"] == "buy" else "short",
                       entry_price=float(px), qty=float(o["qty"]), stop=o.get("stop_loss"),
                       fees=float(res.get("fee") or 0), setup=p.get("setup", ""), account=broker.name,
                       broker_order_id=res.get("order_id"))
            journal_note = f"journal trade #{t['id']} opened" + ("" if filled else " (entry price = order price until filled)")
        else:
            journal_note = "order resting; journal entry is created when it fills (router.py process)"
            _remember_resting(res["order_id"], p)
    elif p["kind"] == "close" and (filled or broker.live):
        journal_note = _close_journal(j, o["symbol"], float(px), float(res.get("fee") or 0), "manual_close")
    res["journal"] = journal_note
    cli.emit(res, a.json, lambda r: "\n".join(filter(None, [
        f"## Submitted to {broker.name}{' (LIVE)' if broker.live else ' (paper)'}: order {r.get('order_id')} -> {r.get('status')}",
        f"Filled {r.get('filled_qty')} @ {r.get('avg_fill_price')} fee {r.get('fee')}" if r.get("status") == "filled" else None,
        r.get("journal"),
        "Live orders: verify the fill in your broker app." if broker.live else None,
    ])))


def _remember_resting(order_id, pending):
    f = config.path("paper", "resting.json")
    data = json.loads(f.read_text()) if f.exists() else {}
    data[order_id] = {"trade_id": pending.get("trade_id"), "order": pending["order"], "setup": pending.get("setup", "")}
    f.write_text(json.dumps(data, indent=2))


def _close_journal(j, symbol, price, fee, reason):
    open_t = [t for t in j.list(status="open") if t["symbol"] == symbol]
    if not open_t:
        return None
    t = j.close(open_t[0]["id"], price, fees=fee, reason=reason)
    return f"journal trade #{t['id']} closed: P&L {t['pnl']:,.2f} ({t['r_multiple']}R)" if t["r_multiple"] is not None \
        else f"journal trade #{t['id']} closed: P&L {t['pnl']:,.2f}"


def cmd_process(a):
    broker = get_broker(a.broker)
    if broker.name != "paper":
        cli.fail("process applies to the paper broker; live fills are handled by your broker")
    fills = broker.process()
    j = Journal()
    notes = []
    resting_f = config.path("paper", "resting.json")
    resting = json.loads(resting_f.read_text()) if resting_f.exists() else {}
    for fl in fills:
        tag = fl.get("tag")
        if fl["order_id"] in resting:
            info = resting.pop(fl["order_id"])
            o = info["order"]
            t = j.open(info.get("trade_id"), symbol=o["symbol"], side="long" if o["side"] == "buy" else "short",
                       entry_price=fl["avg_fill_price"], qty=fl["qty"], stop=o.get("stop_loss"),
                       fees=fl.get("fee") or 0, setup=info.get("setup", ""), account="paper",
                       broker_order_id=fl["order_id"])
            notes.append(f"entry filled {o['symbol']} @ {fl['avg_fill_price']} -> journal #{t['id']}")
        elif tag in ("stop_loss", "take_profit", "flatten"):
            n = _close_journal(j, fl["symbol"], fl["avg_fill_price"], fl.get("fee") or 0, tag)
            notes.append(f"{tag} filled {fl['symbol']} @ {fl['avg_fill_price']}" + (f" -> {n}" if n else ""))
    resting_f.write_text(json.dumps(resting, indent=2))
    gate.audit("process", fills=fills)
    cli.emit({"fills": fills, "journal": notes}, a.json,
             lambda r: "\n".join([f"Processed resting paper orders: {len(r['fills'])} fill(s)."] + [f"- {n}" for n in r["journal"]]))


def cmd_account(a):
    cli.emit(get_broker(a.broker).account(), a.json,
             lambda x: "\n".join(f"- {k}: {v:,.2f}" if isinstance(v, float) else f"- {k}: {v}" for k, v in x.items()))


def cmd_positions(a):
    pos = get_broker(a.broker).positions()
    cli.emit(pos, a.json, lambda x: cli.md_table(x, ["symbol", "qty", "avg_price", "last_price", "market_value", "unrealized_pnl"])
             if x else "No open positions.")


def cmd_orders(a):
    od = get_broker(a.broker).orders(open_only=a.open)
    cli.emit(od, a.json, lambda x: cli.md_table(x[-a.limit:], ["order_id", "symbol", "side", "qty", "type", "limit_price",
                                                             "stop_price", "status", "avg_fill_price", "tag"])
             if x else "No orders.")


def cmd_cancel(a):
    broker = get_broker(a.broker)
    _broker_guard(broker)
    res = broker.cancel(a.order_id)
    gate.audit("cancel", result=res)
    cli.emit(res, a.json, lambda r: f"Cancelled {r.get('order_id')}: {r.get('status')}")


def cmd_kill(a):
    if a.state == "status":
        on = config.kill_switch_on()
        print("KILL SWITCH ON - all submissions blocked" if on else "Kill switch off")
        return
    if a.state == "off":
        config.set_kill_switch(False)
        gate.audit("kill_off")
        print("Kill switch OFF. Orders can be previewed and submitted again.")
        return
    config.set_kill_switch(True, a.reason or "manual")
    gate.audit("kill_on", reason=a.reason, flatten=a.flatten)
    msg = ["KILL SWITCH ON - all new submissions blocked."]
    if a.flatten:
        broker = get_broker(a.broker)
        if broker.name == "paper":
            res = broker.close_all()
            j = Journal()
            for r in res:
                _close_journal(j, r["symbol"], r["avg_fill_price"], r.get("fee") or 0, "kill_switch")
            msg.append(f"Paper: cancelled open orders and closed {len(res)} position(s).")
        else:
            cancelled = 0
            for o in broker.orders(open_only=True):
                try:
                    broker.cancel(o["order_id"])
                    cancelled += 1
                except BrokerError:
                    pass
            pos = broker.positions()
            msg.append(f"Live: cancelled {cancelled} open order(s). {len(pos)} position(s) remain - close them in "
                       "your broker app or via preview --close (turn the kill switch off first).")
    print("\n".join(msg))


def main():
    p = cli.parser(__doc__)
    p.add_argument("--broker", choices=["paper", "kite", "fyers", "upstox", "dhan", "groww"], help="override config broker")
    sub = p.add_subparsers(dest="cmd", required=True)
    pv = sub.add_parser("preview")
    pv.add_argument("--symbol")
    pv.add_argument("--side", choices=["buy", "sell"])
    pv.add_argument("--qty", type=float)
    pv.add_argument("--type", choices=["market", "limit", "stop", "stop_limit"])
    pv.add_argument("--limit-price", type=float)
    pv.add_argument("--stop-price", type=float)
    pv.add_argument("--stop-loss", type=float, help="protective stop (required for opening orders)")
    pv.add_argument("--take-profit", type=float)
    pv.add_argument("--product", help="broker product, e.g. CNC / MIS / NRML (each adapter maps to its own names)")
    pv.add_argument("--tag")
    pv.add_argument("--close", action="store_true", help="this order reduces/closes an existing position")
    pv.add_argument("--protect", action="store_true", help="place a broker-side GTT stop for a holding (kite)")
    pv.add_argument("--json", action="store_true")
    sb = sub.add_parser("submit")
    sb.add_argument("--confirm", required=True)
    sb.add_argument("--json", action="store_true")
    for name in ("account", "positions"):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
    od = sub.add_parser("orders")
    od.add_argument("--open", action="store_true")
    od.add_argument("--limit", type=int, default=30)
    od.add_argument("--json", action="store_true")
    cn = sub.add_parser("cancel")
    cn.add_argument("order_id")
    cn.add_argument("--json", action="store_true")
    pr = sub.add_parser("process")
    pr.add_argument("--json", action="store_true")
    k = sub.add_parser("kill")
    k.add_argument("state", choices=["on", "off", "status"])
    k.add_argument("--reason")
    k.add_argument("--flatten", action="store_true")
    a = p.parse_args()
    {"preview": cmd_preview, "submit": cmd_submit, "process": cmd_process, "account": cmd_account,
     "positions": cmd_positions, "orders": cmd_orders, "cancel": cmd_cancel, "kill": cmd_kill}[a.cmd](a)


if __name__ == "__main__":
    cli.run(main)
