#!/usr/bin/env python3
"""Entry timer: watch a setup bar by bar and say the moment it triggers. Any market, long or short.

Opening-range breakout (orb): the high and low of the first N minutes of the session (15 by default).
The entry is the first CLOSED bar after that whose close is above the range high (long) or below
the range low (short). Level: the same, against a price you give (a 20-day high, a pattern pivot).
A wick through the level never counts, and nothing is ever bought: it hands off to trading-plan.

Examples
  python3 scripts/entry.py check RELIANCE.NS                     # NSE, 15-min opening range, 5-min bars
  python3 scripts/entry.py check AAPL --side short
  python3 scripts/entry.py check NVDA --setup level --level 151.20 --min-volume-x 1.5
  python3 scripts/entry.py watch TCS.NS --until 14:30             # one line per closed bar, stops on trigger
  python3 scripts/entry.py watchlist --watchlist ~/my_list.txt    # check every symbol once
  python3 scripts/entry.py check AAPL --offline saved/ --now "2026-11-13 10:15"   # replay a past session
"""

import datetime as dt
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vendor"))

from tradekit import cli, config, data, session  # noqa: E402


def evaluate(sym, a, now_override=None, bars=None):
    b = bars or data.fresh_bars(sym, a.interval, "5d" if a.interval in ("5m", "15m", "30m", "60m") else "1d",
                                a.provider, a.offline)
    now = session.now_local(b, now_override or a.now)
    cfg = config.load()
    last_min = int(config.get_key(cfg, "risk.no_entries_last_minutes", 30) if a.last_minutes is None else a.last_minutes)
    res = session.entry_check(b, now, a.setup, a.side, a.level, a.or_minutes, a.min_volume_x, last_min, a.interval)
    rng = res.get("opening_range")
    if res["status"] == "triggered":
        long = a.side == "long"
        stops = {}
        if rng:
            stops["range_mid"] = round((rng["high"] + rng["low"]) / 2, 2)
            stops["range_far_side"] = round(rng["low"] if long else rng["high"], 2)
        res["stop_ideas"] = stops
        stop_arg = f" --stop {stops['range_mid']}" if stops else " --stop atr:1.5"
        res["next"] = (f"Set the stop and target BEFORE anything is bought: trading-plan "
                       f"`plan.py {sym} --side {a.side} --entry {res['price']}{stop_arg} --target r:2 --save "
                       f"--setup \"{'opening-range breakout' if a.setup == 'orb' else 'level break'}\"`")
    return res, b


def md_one(r):
    lines = []
    sess = r.get("session") or {}
    head = f"{r['symbol']}  {r['now'].replace('T', ' ')} {r.get('timezone') or ''}  {r['setup']} {r['side']} on {r['interval']} bars"
    if sess.get("close"):
        head += f"  (session {sess['open']}-{sess['close']})"
    lines.append(head)
    rng = r.get("opening_range")
    if rng:
        lines.append(f"Opening range {rng['from']}-{rng['to']}: high {rng['high']:,.2f}, low {rng['low']:,.2f} ({rng['bars']} bars).")
    lines.append(r.get("message", r["status"]))
    if r.get("stop_ideas"):
        s = r["stop_ideas"]
        lines.append(f"Stop ideas: range midpoint {s['range_mid']:,.2f}, far side of the range {s['range_far_side']:,.2f}.")
    if r.get("next"):
        lines.append("Next: " + r["next"])
    return "\n".join(lines)


def save(res):
    config.path("state", "entry.json").write_text(json.dumps(res, indent=2, default=str) + "\n")


def cmd_check(a):
    res, _ = evaluate(a.symbol, a)
    if a.save or res["status"] == "triggered":
        save(res)
    cli.emit(res, a.json, md_one)
    sys.exit(0 if res["status"] == "triggered" else 1)


def cmd_watch(a):
    """Re-check after each bar closes. With --offline/--now it replays the day on a simulated clock."""
    step = session.interval_minutes(a.interval)
    replay = bool(a.offline or a.now)
    bars = data.fresh_bars(a.symbol, a.interval, "5d", a.provider, a.offline) if replay else None
    clock_now = session.now_local(bars, a.now) if replay else None
    deadline = time.time() + a.max_minutes * 60
    last_msg = None
    while True:
        res, b = evaluate(a.symbol, a, clock_now, bars)
        msg = (res["status"], res.get("message"))
        if msg != last_msg:
            line = f"{res['now'][11:16]}  {res.get('message', res['status'])}"
            print(json.dumps(res, default=str) if a.json else line, flush=True)
            last_msg = msg
        if res["status"] == "triggered":
            save(res)
            if not a.json:
                print("\n".join(x for x in md_one(res).split("\n")[1:] if x != res.get("message")))
            sys.exit(0)
        if res["status"] in ("expired", "closed", "no-data") and (res["status"] != "no-data" or replay):
            sys.exit(1)
        if a.until and res["now"][11:16] >= a.until:
            print(f"Stopped at {a.until} without a trigger.")
            sys.exit(1)
        if replay:
            t = dt.datetime.strptime(res["now"], "%Y-%m-%dT%H:%M") + dt.timedelta(minutes=step)
            t -= dt.timedelta(minutes=t.minute % step)
            clock_now = t.strftime("%Y-%m-%dT%H:%M")
            continue
        if time.time() > deadline:
            print("Stopped: --max-minutes reached.")
            sys.exit(1)
        # wake just after the next bar closes, plus a little for the data source to catch up
        now = dt.datetime.now()
        secs = (step - now.minute % step) * 60 - now.second + a.grace
        time.sleep(max(15, secs))


def cmd_watchlist(a):
    syms = data.load_universe(a.watchlist, a.symbols)
    if not syms:
        cli.fail("give symbols or --watchlist FILE")
    rows = []
    for s in syms:
        try:
            res, _ = evaluate(s, a)
        except Exception as e:  # noqa: BLE001
            res = {"symbol": s, "status": "error", "message": str(e)}
        rows.append(res)
    order = {"triggered": 0, "waiting": 1, "forming": 2, "not-open": 3, "expired": 4}
    rows.sort(key=lambda r: (order.get(r["status"], 9), r.get("distance_pct") or 0))

    def md(rs):
        out = [f"{r['symbol']:14} {r['status'].upper():10} {r.get('message', '')}" for r in rs]
        out.append("Triggered is information, not an order: plan it with trading-plan, check it with trading-risk.")
        return "\n".join(out)
    cli.emit(rows, a.json, md)
    sys.exit(0 if any(r["status"] == "triggered" for r in rows) else 1)


def main():
    p = cli.parser(__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("symbol")
    c.add_argument("--save", action="store_true", help="write state/entry.json even when not triggered")
    w = sub.add_parser("watch")
    w.add_argument("symbol")
    w.add_argument("--until", help="stop at HH:MM exchange time")
    w.add_argument("--max-minutes", type=float, default=420)
    w.add_argument("--grace", type=int, default=20, help="seconds to wait after a bar closes")
    wl = sub.add_parser("watchlist")
    wl.add_argument("symbols", nargs="*")
    wl.add_argument("--watchlist")
    for sp in (c, w, wl):
        sp.add_argument("--setup", default="orb", choices=["orb", "level"])
        sp.add_argument("--side", default="long", choices=["long", "short"])
        sp.add_argument("--level", type=float, help="price for --setup level")
        sp.add_argument("--or-minutes", type=int, default=15, help="opening range length (minutes)")
        sp.add_argument("--interval", default="5m", choices=["1m", "2m", "5m", "15m"])
        sp.add_argument("--min-volume-x", type=float, help="trigger bar volume >= X times the range's average bar")
        sp.add_argument("--last-minutes", type=int, help="no new entries this close to the close (default 30)")
        sp.add_argument("--provider", choices=["yahoo", "csv", "kite"])
        sp.add_argument("--offline", help="saved chart file or folder (replays, tests)")
        sp.add_argument("--now", help="pin the exchange-local clock, 'YYYY-MM-DD HH:MM'")
        sp.add_argument("--json", action="store_true")
    a = p.parse_args()
    {"check": cmd_check, "watch": cmd_watch, "watchlist": cmd_watchlist}[a.cmd](a)


if __name__ == "__main__":
    cli.run(main)
