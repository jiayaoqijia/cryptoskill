#!/usr/bin/env python3
"""Price alerts for any market: levels, stops, targets, % moves, the opening bell, "flat by close".

Each alert rings once. `check` fetches only the symbols in your rules, works out each exchange's
session from the data (NYSE, NSE, LSE ... no holiday tables), and prints what rang. Run it on a
schedule (/loop 5m, or a scheduled task) while you trade. An alert is information, never an order.

Examples
  python3 scripts/alerts.py add --symbol RELIANCE.NS --above 1400
  python3 scripts/alerts.py add --symbol AAPL --below 340 --note "under the 50-day"
  python3 scripts/alerts.py add --symbol TSLA --stop 358.32 --side long
  python3 scripts/alerts.py add --symbol INFY.NS --pct 3
  python3 scripts/alerts.py add --symbol NIFTYBEES.NS --open            # NSE opening bell
  python3 scripts/alerts.py add --symbol AAPL --close 5                 # 5 minutes before NYSE closes
  python3 scripts/alerts.py add --from-journal                          # stop + target of every open trade
  python3 scripts/alerts.py check                                       # exit 0 = something rang
  python3 scripts/alerts.py clock RELIANCE.NS AAPL                      # is the exchange open?
  python3 scripts/alerts.py list | remove ID | reset [ID]
"""

import datetime as dt
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import alerts as A, cli, data, session  # noqa: E402
from tradekit.journal import Journal  # noqa: E402


def quote_for(sym, a):
    q = data.live_quote(sym, a.provider, a.offline)
    b = q.pop("bars")
    now = session.now_local(b, a.now)
    st = session.market_status(b, now)
    q.update(session=st.get("session"), status=st["status"], now=now)
    return q


def notify(title, text):
    """Optional desktop notification (macOS / Linux). Never required."""
    try:
        if shutil.which("osascript"):
            esc = lambda x: x.replace("\\", "\\\\").replace('"', '\\"')  # noqa: E731
            subprocess.run(["osascript", "-e", f'display notification "{esc(text)}" with title "{esc(title)}"'],
                           timeout=5, capture_output=True)
        elif shutil.which("notify-send"):
            subprocess.run(["notify-send", title, text], timeout=5, capture_output=True)
    except (OSError, subprocess.SubprocessError):
        pass


def cmd_add(a):
    added = []
    if a.from_journal:
        trades = Journal().list(status="open")
        for r in A.from_trades(trades, A.load_rules()):
            added.append(A.add(r))
        if not trades:
            cli.fail("no open trades in the journal")
    else:
        kinds = [k for k in ("above", "below", "stop", "target") if getattr(a, k) is not None]
        rule = {"symbol": a.symbol, "note": a.note, "date": a.date, "rearm": True if a.rearm else None}
        if kinds:
            for k in kinds:
                added.append(A.add({**rule, "type": k, "price": getattr(a, k),
                                    "side": a.side if k in ("stop", "target") else None}))
        elif a.pct:
            added.append(A.add({**rule, "type": "pct", "pct": a.pct, "direction": a.direction}))
        elif a.at:
            added.append(A.add({**rule, "type": "time", "at": a.at, "label": a.label}))
        elif a.open:
            added.append(A.add({**rule, "type": "open"}))
        elif a.close is not None:
            added.append(A.add({**rule, "type": "close", "minutes": a.close}))
        else:
            cli.fail("say what to watch: --above/--below/--stop/--target PRICE, --pct N, --at HH:MM, --open, "
                     "--close MIN or --from-journal")
    cli.emit({"added": added}, a.json, lambda o: "\n".join(
        f"Added {r['id']}: {describe(r)}" for r in o["added"]) or "Nothing new to add.")


def describe(r):
    t = r["type"]
    sym = r.get("symbol") or ""
    if t in ("above", "below"):
        s = f"{sym} at or {t} {r['price']:g}"
    elif t in ("stop", "target"):
        s = f"{sym} {t} {r['price']:g} ({r.get('side', 'long')})"
    elif t == "pct":
        s = f"{sym} moves {r['pct']:g}% {r.get('direction', 'any')} from the previous close"
    elif t == "time":
        s = f"{r['at']} {'on ' + sym + chr(39) + 's exchange clock' if sym else 'local clock'}" + (f" - {r['label']}" if r.get("label") else "")
    elif t == "open":
        s = f"{sym}'s exchange opens"
    else:
        s = f"{r.get('minutes', 5)} min before {sym}'s exchange closes"
    if r.get("date"):
        s += f", on {r['date']} only"
    if r.get("rearm"):
        s += ", re-arms"
    return s + (f" ({r['note']})" if r.get("note") and t not in ("stop", "target") else "")


def cmd_check(a):
    rules = A.load_rules()
    if not rules:
        cli.fail("no alerts set: add one with alerts.py add ...")
    st = A.load_state()
    rang_now, errors, quotes = [], {}, {}
    syms = sorted({r["symbol"] for r in rules if r.get("symbol")})
    for s in syms:
        try:
            quotes[s] = quote_for(s, a)
        except Exception as e:  # noqa: BLE001 - one bad symbol must not stop the rest
            errors[s] = str(e)
    for r in rules:
        q = quotes.get(r.get("symbol")) if r.get("symbol") else None
        if r.get("symbol") and q is None:
            continue
        now = q["now"] if q else (a.now or dt.datetime.now().strftime("%Y-%m-%dT%H:%M"))
        A.rearm(r, q, st["rang"])
        msg = A.evaluate(r, q, now.replace(" ", "T"), st["rang"])
        if msg:
            st["rang"][r["id"]] = now
            rang_now.append({"id": r["id"], "message": msg, "at": now})
    if not a.dry_run:
        A.save_state(st)
    out = {"rang": rang_now, "watched": len(rules), "errors": errors,
           "quotes": {s: {k: q[k] for k in ("price", "previous_close", "status", "now", "exchange", "currency")}
                      for s, q in quotes.items()}}
    if a.notify:
        for x in rang_now:
            notify("trading-skills alert", x["message"])

    def md(o):
        lines = [f"ALERT {x['message']}  [{x['id']}]" for x in o["rang"]]
        if not lines:
            prices = ", ".join(f"{s} {q['price']:,.2f} ({q['status']})" for s, q in o["quotes"].items())
            lines.append(f"Nothing rang. {o['watched']} alert(s) watched. {prices}")
        for s, e in o["errors"].items():
            lines.append(f"could not price {s}: {e}")
        lines.append("Free quotes are delayed and can lag; a price can pass a level between two checks. "
                     "An alert is not an order: with a bracket or GTT order, the broker does the stopping.")
        return "\n".join(lines)
    cli.emit(out, a.json, md)
    sys.exit(0 if rang_now else 1)


def cmd_clock(a):
    out = []
    for s in a.symbols:
        try:
            q = quote_for(s, a)
            out.append({"symbol": s, "exchange": q["exchange"], "timezone": q["timezone"], "now": q["now"],
                        "status": q["status"], "session": q["session"]})
        except Exception as e:  # noqa: BLE001
            out.append({"symbol": s, "error": str(e)})

    def md(rows):
        lines = []
        for r in rows:
            if r.get("error"):
                lines.append(f"{r['symbol']}: {r['error']}")
                continue
            sess = r["session"]
            span = f" (session {sess['open']}-{sess['close']})" if sess and sess.get("close") else ""
            lines.append(f"{r['symbol']} on {r['exchange']}: {r['status'].upper()} at {r['now'][11:16]} "
                         f"{r['timezone']}{span}")
        return "\n".join(lines)
    cli.emit(out, a.json, md)


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    ad = sub.add_parser("add")
    ad.add_argument("--symbol")
    for k in ("above", "below", "stop", "target"):
        ad.add_argument(f"--{k}", type=float)
    ad.add_argument("--side", default="long", choices=["long", "short"], help="for --stop/--target")
    ad.add_argument("--pct", type=float, help="move from the previous close, in %%")
    ad.add_argument("--direction", default="any", choices=["up", "down", "any"])
    ad.add_argument("--at", help="HH:MM on the symbol's exchange clock")
    ad.add_argument("--label")
    ad.add_argument("--open", action="store_true", help="the symbol's exchange opens")
    ad.add_argument("--close", type=int, metavar="MIN", help="MIN minutes before the exchange closes")
    ad.add_argument("--from-journal", action="store_true", help="stop and target of every open trade")
    ad.add_argument("--date", help="watch on this date only (YYYY-MM-DD)")
    ad.add_argument("--rearm", action="store_true", help="ring again after the price goes back across")
    ad.add_argument("--note")
    ad.add_argument("--json", action="store_true")
    ck = sub.add_parser("check")
    ck.add_argument("--notify", action="store_true", help="also show a desktop notification")
    ck.add_argument("--dry-run", action="store_true", help="do not remember what rang")
    cl = sub.add_parser("clock")
    cl.add_argument("symbols", nargs="+")
    for sp in (ck, cl):
        sp.add_argument("--provider", choices=["yahoo", "csv", "kite"])
        sp.add_argument("--offline", help="folder of saved charts (tests, replays)")
        sp.add_argument("--now", help="pin the exchange-local clock, 'YYYY-MM-DD HH:MM'")
        sp.add_argument("--json", action="store_true")
    ls = sub.add_parser("list")
    ls.add_argument("--json", action="store_true")
    rm = sub.add_parser("remove")
    rm.add_argument("id")
    rs = sub.add_parser("reset")
    rs.add_argument("id", nargs="?")
    a = p.parse_args()
    if a.cmd == "add":
        cmd_add(a)
    elif a.cmd == "check":
        cmd_check(a)
    elif a.cmd == "clock":
        cmd_clock(a)
    elif a.cmd == "list":
        rules, st = A.load_rules(), A.load_state()
        cli.emit({"rules": rules, "rang": st["rang"]}, a.json, lambda o: "\n".join(
            f"{r['id']}: {describe(r)}" + (f"  (rang {o['rang'][r['id']]})" if r["id"] in o["rang"] else "")
            for r in o["rules"]) or "No alerts set.")
    elif a.cmd == "remove":
        print("removed" if A.remove(a.id) else f"no alert {a.id}")
    elif a.cmd == "reset":
        print(f"re-armed {A.reset(a.id)} alert(s)")


if __name__ == "__main__":
    cli.run(main)
