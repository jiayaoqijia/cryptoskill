#!/usr/bin/env python3
"""Crash / systemic-shock relative-strength screen (Binance spot, keyless).

Answers: "selama crash, ticker mana yang benar-benar kuat, dan mana yang cuma
belum jatuh?" and separately "nama yang kemarin gw sebut masih unggul nggak?".

Usage:
  python3 crash_relative_strength.py                 # screen top-70 liquid pairs
  python3 crash_relative_strength.py --vol 30 --top 40
  python3 crash_relative_strength.py --watch LINK UNI TAO SUI HYPE

Columns per symbol:
  r24   = 24h %
  r7    = 7d %   (close vs close 7 candles back)
  crash = % from the OPEN of the crash-day candle to now (the shock window;
          bump --crash-offset when the shock day is not yesterday)
  dd10  = distance from the 10d high (how much it gave back at all)
  pos30 = where price sits inside the 30d range (0 = 30d low, 100 = 30d high)
  vsBTC = r7 minus BTC r7 -> the relative-strength ranking key
  e20/e50 = 4h EMA20/EMA50 stretch in % (positive = extended above the mean)

Reading rules (see references/drawdown-and-trim-decisions.md §5):
  * rank by vsBTC, but only names with real liquidity are candidates
  * e20 > +5% means the move is already made: quote a limit at EMA20, not market
  * a name can leave the leaderboard in one session -- always re-run, never
    repeat last session's pick from memory
"""
from __future__ import annotations

import argparse
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://api.binance.com"
STABLE = {"USDT", "USDC", "FDUSD", "TUSD", "DAI", "BUSD", "USDP", "EUR", "TRY",
          "BRL", "ARS", "AEUR", "XUSD", "USD1", "RLUSD", "RWUSD"}
LEV = ("UP", "DOWN", "BULL", "BEAR")


def get(url: str, timeout: int = 20):
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-screen"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def klines(symbol: str, interval: str, limit: int):
    d = get(f"{BASE}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}")
    return ([float(x[4]) for x in d], [float(x[1]) for x in d],
            [float(x[2]) for x in d], [float(x[3]) for x in d])


def ema(vals: list[float], n: int) -> float:
    k = 2 / (n + 1)
    e = vals[0]
    for v in vals[1:]:
        e = v * k + e * (1 - k)
    return e


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", type=float, default=15, help="min 24h quote volume, $M")
    ap.add_argument("--top", type=int, default=70, help="how many liquid pairs to keep")
    ap.add_argument("--crash-offset", type=int, default=2,
                    help="index of the shock day's candle (2 = yesterday)")
    ap.add_argument("--watch", nargs="*", default=[], help="extra tickers to always print")
    a = ap.parse_args()

    tick = get(f"{BASE}/api/v3/ticker/24hr")
    rows = []
    for t in tick:
        s = t["symbol"]
        if not s.endswith("USDT"):
            continue
        base = s[:-4]
        if base in STABLE or base.endswith(LEV):
            continue
        qv = float(t["quoteVolume"])
        if qv < a.vol * 1e6:
            continue
        rows.append((s, base, float(t["lastPrice"]), float(t["priceChangePercent"]), qv))
    rows.sort(key=lambda r: -r[4])
    rows = rows[: a.top]
    for w in a.watch:
        s = w.upper() + "USDT"
        if all(r[0] != s for r in rows):
            try:
                t = get(f"{BASE}/api/v3/ticker/24hr?symbol={s}")
                rows.append((s, w.upper(), float(t["lastPrice"]),
                             float(t["priceChangePercent"]), float(t["quoteVolume"])))
            except Exception:
                pass

    def one(sym: str):
        try:
            c, o, h, lo = klines(sym, "1d", 32)
            c4, _, _, _ = klines(sym, "4h", 90)
            return sym, (c, o, h, lo, c4)
        except Exception:
            return sym, None

    with ThreadPoolExecutor(max_workers=12) as ex:
        data = dict(ex.map(one, [r[0] for r in rows]))

    bc, bo, _, _ = klines("BTCUSDT", "1d", 32)
    btc7 = bc[-1] / bc[-8] - 1
    btc_crash = bc[-1] / bo[-a.crash_offset] - 1

    out = []
    for sym, base, px, chg, qv in rows:
        d = data.get(sym)
        if not d or len(d[0]) < 10:
            continue
        c, o, h, lo, c4 = d
        r7 = c[-1] / c[-8] - 1
        crash = c[-1] / o[-a.crash_offset] - 1
        dd10 = c[-1] / max(h[-10:]) - 1
        span = max(h[-30:]) - min(lo[-30:])
        pos30 = (c[-1] - min(lo[-30:])) / span * 100 if span else 0.0
        e20 = (c[-1] / ema(c4[-40:], 20) - 1) * 100
        e50 = (c[-1] / ema(c4[-100:], 50) - 1) * 100
        out.append(dict(base=base, px=px, r24=chg, r7=r7 * 100, crash=crash * 100,
                        dd10=dd10 * 100, pos30=pos30, vs= (r7 - btc7) * 100,
                        e20=e20, e50=e50, vol=qv / 1e6))

    print(f"BTC 7d {btc7*100:+.2f}%  |  crash window {btc_crash*100:+.2f}%")
    print("\n== relative strength (r7 - BTC r7), top 12")
    print(f"{'sym':9}{'px':>12}{'24h':>8}{'7d':>8}{'crash':>8}{'dd10':>7}{'pos30':>7}{'e20':>7}{'vol$M':>8}")
    for r in sorted(out, key=lambda x: -x["vs"])[:12]:
        print(f"{r['base']:9}{r['px']:>12.6g}{r['r24']:>8.2f}{r['r7']:>8.2f}{r['crash']:>8.2f}"
              f"{r['dd10']:>7.1f}{r['pos30']:>7.0f}{r['e20']:>7.1f}{r['vol']:>8.0f}")
    print("\n== held up best inside the shock window, top 10")
    for r in sorted(out, key=lambda x: -x["crash"])[:10]:
        print(f"{r['base']:9}{r['px']:>12.6g}{r['r24']:>8.2f}{r['r7']:>8.2f}{r['crash']:>8.2f}"
              f"{r['dd10']:>7.1f}{r['pos30']:>7.0f}{r['e20']:>7.1f}")
    if a.watch:
        print("\n== watchlist")
        for r in out:
            if r["base"] in {w.upper() for w in a.watch}:
                print(f"{r['base']:9}{r['px']:>12.6g}{r['r24']:>8.2f}{r['r7']:>8.2f}{r['crash']:>8.2f}"
                      f"{r['dd10']:>7.1f}{r['pos30']:>7.0f}{r['e20']:>7.1f}{r['e50']:>7.1f}")


if __name__ == "__main__":
    main()
