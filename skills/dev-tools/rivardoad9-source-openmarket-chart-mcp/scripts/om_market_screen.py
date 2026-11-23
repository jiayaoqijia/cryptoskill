#!/usr/bin/env python3
"""Metrics + level sheet for a list of perps from OpenMarket, for intraday plan writing.

Run it with the venv that carries mcp 2.0 (see SKILL.md section 3):
    <V>/bin/python3 om_market_screen.py NEARUSDT HYPEUSDT ADAUSDT

Pulls 15m candles for the last 5 days per symbol, caches them under ./bars/<SYMBOL>.json
so a rerun costs no data weight, tolerates the free plan's 429 (`{"error": "rate_limited"}`)
by sleeping and retrying, then prints one row of measurements plus two candidate plans per
symbol (shelf breakout and EMA20 retest) with risk percent and where the 2R target lands
relative to the 24h and 5-day high. It measures; the pick and the wording are the agent's job.
"""
import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from om_call import load_token, URL  # sibling bridge: stored token + refresh

import httpx2
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

EXCHANGE = "BINANCE_FUTURES"
CACHE = "bars"
LOOKBACK = "5d"
INTERVAL = "FIFTEEN_MINUTES"


def ema(vals, n):
    k = 2.0 / (n + 1)
    e = vals[0]
    for v in vals[1:]:
        e = v * k + e * (1 - k)
    return e


def wilder(values, n=14):
    a = sum(values[:n]) / n
    out = [a]
    for v in values[n:]:
        a = (a * (n - 1) + v) / n
        out.append(a)
    return out


def rsi(closes, n=14):
    gains = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    losses = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    ag, al = wilder(gains, n)[-1], wilder(losses, n)[-1]
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)


async def fetch(session, sym, tries=4):
    """Cached points call. Returns {sym, columns, rows} or None."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{sym}.json")
    if os.path.exists(path):
        return json.load(open(path))
    for attempt in range(tries):
        res = await session.call_tool("points", {
            "type": "TRADE_SIDE_AGNOSTIC_AGG", "exchanges": [EXCHANGE],
            "rawSymbol": sym, "interval": INTERVAL, "lookback": LOOKBACK})
        txt = next((c.text for c in (res.content or []) if getattr(c, "type", None) == "text"), None)
        data = json.loads(txt) if txt else {}
        if "series" in data:
            ser = data["series"][0]
            rec = {"sym": sym, "columns": ser["columns"], "rows": ser["rows"]}
            json.dump(rec, open(path, "w"))
            return rec
        wait = 7 * (attempt + 1)
        print(f"  ! {sym}: {str(data)[:110]} — sleep {wait}s", file=sys.stderr)
        time.sleep(wait)
    return None


def sheet(rec):
    rows = rec["rows"]
    o, h, l, c, v = ([r[i] for r in rows] for i in (1, 2, 3, 4, 5))
    tr = [max(rows[i][2] - rows[i][3], abs(rows[i][2] - rows[i - 1][4]),
              abs(rows[i][3] - rows[i - 1][4])) for i in range(1, len(rows))]
    atr = wilder(tr, 14)[-1]
    last = c[-1]
    return dict(
        sym=rec["sym"], last=last, atr=atr, atrpct=atr / last * 100,
        e20=ema(c[-200:], 20), e50=ema(c[-200:], 50), e200=ema(c[-300:], 200),
        rsi=rsi(c[-200:]), chg24=(last / c[-97] - 1) * 100, chg6=(last / c[-25] - 1) * 100,
        hi12=max(h[-12:]), lo12=min(l[-12:]), hi24=max(h[-96:]), lo24=min(l[-96:]),
        hi5=max(h), lo5=min(l),
        volr=(sum(v[-24:]) / 24) / (sum(v[-120:-24]) / 96) if sum(v[-120:-24]) else 0.0,
        pos24=(last - min(l[-96:])) / (max(h[-96:]) - min(l[-96:]) or 1) * 100,
        bars=len(rows))


def plan(m):
    a, last = m["atr"], m["last"]
    entry_b = m["hi12"] + 0.10 * a
    stop_b = m["lo12"] - 0.25 * a
    risk_b = entry_b - stop_b
    entry_r = m["e20"]
    stop_r = entry_r - 1.0 * a
    risk_r = entry_r - stop_r
    if risk_b > 0:
        print(f"    LONG breakout  entry {entry_b:.6g}  stop {stop_b:.6g}  risk {risk_b / entry_b * 100:.2f}%"
              f"  target {entry_b + 2 * risk_b:.6g}  vs hi24 {(entry_b + 2 * risk_b) / m['hi24'] - 1:+.2%}"
              f"  vs hi5 {(entry_b + 2 * risk_b) / m['hi5'] - 1:+.2%}")
    print(f"    LONG EMA20     entry {entry_r:.6g}  stop {stop_r:.6g}  risk {risk_r / entry_r * 100:.2f}%"
          f"  target {entry_r + 2 * risk_r:.6g}  vs hi24 {(entry_r + 2 * risk_r) / m['hi24'] - 1:+.2%}")


async def main(symbols):
    token = load_token()
    async with httpx2.AsyncClient(headers={"Authorization": f"Bearer {token}"}, timeout=120) as http:
        async with streamable_http_client(URL, http_client=http) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                print(f"{'sym':>13} {'last':>11} {'chg24%':>7} {'chg6%':>6} {'rsi':>5} {'atr%':>5}"
                      f" {'volR':>5} {'pos24':>6} {'>E20':>5} {'>E50':>5} {'>E200':>5}")
                for sym in symbols:
                    rec = await fetch(s, sym)
                    if not rec or len(rec["rows"]) < 300:
                        print(f"{sym:>13}  no data")
                        continue
                    m = sheet(rec)
                    print(f"{m['sym']:>13} {m['last']:>11.6g} {m['chg24']:>7.2f} {m['chg6']:>6.2f}"
                          f" {m['rsi']:>5.1f} {m['atrpct']:>5.2f} {m['volr']:>5.2f} {m['pos24']:>6.1f}"
                          f" {str(m['last'] > m['e20']):>5} {str(m['last'] > m['e50']):>5} {str(m['last'] > m['e200']):>5}")
                    print(f"      EMA20 {m['e20']:.6g}  EMA50 {m['e50']:.6g}  EMA200 {m['e200']:.6g}"
                          f"  hi24 {m['hi24']:.6g}  lo24 {m['lo24']:.6g}  hi5 {m['hi5']:.6g}  lo5 {m['lo5']:.6g}")
                    plan(m)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit("usage: om_market_screen.py SYMBOL [SYMBOL ...]  (e.g. NEARUSDT HYPEUSDT ADAUSDT)")
    asyncio.run(main(args))
