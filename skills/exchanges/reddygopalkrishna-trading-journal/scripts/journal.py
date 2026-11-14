#!/usr/bin/env python3
"""Trade journal (SQLite) - plan, open, close, annotate, list, import and export trades.

Examples
  python3 scripts/journal.py plan --symbol AAPL --side long --entry 195 --stop 188 --target 212 --qty 70 --setup VCP --thesis "..."
  python3 scripts/journal.py open --id 3 --price 195.4 --qty 70                 # fill a planned trade
  python3 scripts/journal.py open --symbol MSFT --side long --price 410 --qty 20 --stop 398 --setup pullback
  python3 scripts/journal.py close --id 3 --price 209.8 --reason target --fees 2.5
  python3 scripts/journal.py note --id 3 --text "moved stop to breakeven" --grade A --tags discipline,patience
  python3 scripts/journal.py list --status open
  python3 scripts/journal.py show --id 3
  python3 scripts/journal.py import --file broker_trades.csv
  python3 scripts/journal.py export --file trades.csv
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, config  # noqa: E402
from tradekit.journal import Journal  # noqa: E402

LIST_COLS = ["id", "symbol", "side", "status", "setup", "qty", "entry_price", "stop", "exit_price", "pnl", "r_multiple",
             "entry_time", "exit_time"]


def _tags(s):
    return [t.strip() for t in (s or "").split(",") if t.strip()]


def show(t):
    out = [f"## Trade #{t['id']}: {t['side'].upper()} {t['symbol']} - {t['status']}"]
    for k in ("setup", "thesis", "account", "plan_entry", "plan_stop", "plan_target", "qty", "entry_price", "entry_time",
              "stop", "exit_price", "exit_time", "exit_reason", "fees", "pnl", "r_multiple", "hold_days", "mae", "mfe",
              "grade", "tags", "broker_order_id"):
        v = t.get(k)
        if v not in (None, "", []):
            out.append(f"- {k}: {', '.join(v) if isinstance(v, list) else v}")
    if t.get("notes"):
        out.append("\nNotes:\n" + t["notes"])
    return "\n".join(out)


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("plan")
    for k in ("symbol", "side"):
        pl.add_argument(f"--{k}", required=True)
    pl.add_argument("--entry", type=float, required=True)
    pl.add_argument("--stop", type=float, required=True)
    pl.add_argument("--target", type=float)
    pl.add_argument("--qty", type=float)
    pl.add_argument("--setup", default="")
    pl.add_argument("--thesis", default="")
    pl.add_argument("--tags")
    op = sub.add_parser("open")
    op.add_argument("--id", type=int, help="planned trade id")
    op.add_argument("--symbol")
    op.add_argument("--side")
    op.add_argument("--price", type=float, required=True)
    op.add_argument("--qty", type=float, required=True)
    op.add_argument("--stop", type=float)
    op.add_argument("--time", help="ISO time, default now")
    op.add_argument("--fees", type=float, default=0.0)
    op.add_argument("--setup", default="")
    op.add_argument("--account")
    op.add_argument("--tags")
    cl = sub.add_parser("close")
    cl.add_argument("--id", type=int, required=True)
    cl.add_argument("--price", type=float, required=True)
    cl.add_argument("--time")
    cl.add_argument("--fees", type=float, default=0.0)
    cl.add_argument("--reason", default="")
    cl.add_argument("--mae", type=float, help="max adverse excursion (price units per share)")
    cl.add_argument("--mfe", type=float, help="max favourable excursion")
    nt = sub.add_parser("note")
    nt.add_argument("--id", type=int, required=True)
    nt.add_argument("--text", required=True)
    nt.add_argument("--grade", help="A-F process grade (how well you followed the plan, not the P&L)")
    nt.add_argument("--tags")
    up = sub.add_parser("update")
    up.add_argument("--id", type=int, required=True)
    up.add_argument("--stop", type=float)
    up.add_argument("--target", type=float)
    up.add_argument("--setup")
    cn = sub.add_parser("cancel")
    cn.add_argument("--id", type=int, required=True)
    cn.add_argument("--reason", default="")
    ls = sub.add_parser("list")
    ls.add_argument("--status", choices=["planned", "open", "closed", "cancelled"])
    ls.add_argument("--symbol")
    ls.add_argument("--setup")
    ls.add_argument("--since")
    ls.add_argument("--limit", type=int, default=50)
    sh = sub.add_parser("show")
    sh.add_argument("--id", type=int, required=True)
    im = sub.add_parser("import")
    im.add_argument("--file", required=True)
    im.add_argument("--account", default="imported")
    ex = sub.add_parser("export")
    ex.add_argument("--file")
    for s in (pl, op, cl, nt, up, cn, ls, sh, im, ex):
        s.add_argument("--json", action="store_true")
    a = p.parse_args()
    j = Journal()
    acct = config.load()["broker"]["name"]

    if a.cmd == "plan":
        t = j.plan(a.symbol, a.side, a.entry, a.stop, a.target, a.qty, a.setup, a.thesis, _tags(a.tags), acct)
        cli.emit(t, a.json, lambda t: f"Planned trade #{t['id']}: {t['side']} {t['symbol']} entry {t['plan_entry']} "
                                      f"stop {t['plan_stop']} target {t['plan_target']}")
    elif a.cmd == "open":
        t = j.open(a.id, symbol=a.symbol, side=a.side, entry_price=a.price, qty=a.qty, stop=a.stop,
                   entry_time=a.time, fees=a.fees, setup=a.setup, account=a.account or acct, tags=_tags(a.tags))
        cli.emit(t, a.json, lambda t: f"Opened trade #{t['id']}: {t['side']} {t['qty']:g} {t['symbol']} @ {t['entry_price']}"
                                      + ("" if t["stop"] is not None else "  WARNING: no stop recorded"))
    elif a.cmd == "close":
        t = j.close(a.id, a.price, a.time, a.fees, a.reason, a.mae, a.mfe)
        cli.emit(t, a.json, lambda t: f"Closed trade #{t['id']} {t['symbol']}: P&L {t['pnl']:,.2f}"
                                      + (f" ({t['r_multiple']:+.2f}R)" if t["r_multiple"] is not None else "")
                                      + " - add a note on what you learned (journal.py note).")
    elif a.cmd == "note":
        t = j.note(a.id, a.text, a.grade, _tags(a.tags))
        cli.emit(t, a.json, show)
    elif a.cmd == "update":
        ch = {}
        if a.stop is not None:
            ch["stop"] = a.stop
        if a.target is not None:
            ch["plan_target"] = a.target
        if a.setup:
            ch["setup"] = a.setup
        t = j.update(a.id, **ch)
        cli.emit(t, a.json, show)
    elif a.cmd == "cancel":
        t = j.cancel(a.id, a.reason)
        cli.emit(t, a.json, lambda t: f"Cancelled planned trade #{t['id']}")
    elif a.cmd == "list":
        rows = j.list(a.status, a.symbol, a.since, a.setup)[-a.limit:]
        cli.emit(rows, a.json, lambda r: cli.md_table(r, LIST_COLS) if r else "Journal is empty for that filter.")
    elif a.cmd == "show":
        cli.emit(j.get(a.id), a.json, show)
    elif a.cmd == "import":
        n = j.import_csv(open(a.file).read(), a.account)
        cli.emit({"imported": n}, a.json, lambda r: f"Imported {r['imported']} trades.")
    elif a.cmd == "export":
        text = j.export_csv()
        if a.file:
            open(a.file, "w").write(text)
            print(f"Exported to {os.path.abspath(a.file)}")
        else:
            print(text)


if __name__ == "__main__":
    cli.run(main)
