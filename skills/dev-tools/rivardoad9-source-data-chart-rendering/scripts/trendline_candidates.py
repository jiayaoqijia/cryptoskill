#!/usr/bin/env python3
"""Enumerate and validate candidate trendlines from REAL candles before drawing any of them.

Why this exists: on 2 Okt 2026 a trendline was drawn through a pivot that was not a meaningful
swing point. The rendered line fell 34% below spot, touched no high, and the user's reaction was
"trendline nya aneh" — the chart was wrong, not the market. Anchor choice is a claim; this script
makes you test it against the actual pivots first.

Usage:
    python3 trendline_candidates.py TNSRUSDT
    python3 trendline_candidates.py ETHUSDT --interval 4h --limit 500 --lookback 6 --window 180

Stdlib only. Data: Binance spot klines (real data, no key). Read-only.
Output per candidate pair:
    touch   how many pivot points the line passes within `--tol` (default 1.5%)
    below   pivots after anchor2 that sit under the line (a resistance line wants ALL of them)
    since   closes above (descending) / below (ascending) the line after anchor2, and the first date
    now     line value on the latest candle vs price, in %
    verdict VALID / BROKEN / REJECT
"""
import argparse
import datetime as dt
import json
import statistics
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=45))
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def klines(symbol, interval, limit):
    raw = get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}")
    bars = []
    for r in raw:
        bars.append({
            "day": int(r[0] // 86400000),
            "date": dt.datetime.utcfromtimestamp(r[0] / 1000).strftime("%Y-%m-%d"),
            "o": float(r[1]), "h": float(r[2]), "l": float(r[3]), "c": float(r[4]), "v": float(r[7]),
        })
    return bars


def pivots(bars, w, side):
    """Local swing points: high (side='h') or low (side='l'), `w` bars each side."""
    key = "h" if side == "h" else "l"
    cmp_ = (lambda a, b: a >= b) if side == "h" else (lambda a, b: a <= b)
    out = []
    for i in range(w, len(bars) - w):
        if all(cmp_(bars[i][key], bars[j][key]) for j in range(i - w, i + w + 1)):
            out.append(i)
    return out


def line_value(p1, p2, day):
    sl = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return p1[1] + sl * (day - p1[0])


def evaluate(bars, piv, side, w, tol, direction):
    """direction: 'down' = resistance (anchors descending), 'up' = support (anchors ascending)."""
    cur = bars[-1]["c"]
    today = bars[-1]["day"]
    key = "h" if side == "h" else "l"
    res = []
    for a in range(len(piv)):
        for z in range(a + 1, len(piv)):
            i1, i2 = piv[a], piv[z]
            p1, p2 = (bars[i1]["day"], bars[i1][key]), (bars[i2]["day"], bars[i2][key])
            if p2[0] - p1[0] < 5:
                continue
            desc = p2[1] < p1[1]
            if direction == "down" and not desc:
                continue
            if direction == "up" and desc:
                continue
            # how many other pivots sit on the line (within tol)
            touch = sum(1 for k in piv
                        if abs(bars[k][key] - line_value(p1, p2, bars[k]["day"])) <= tol * p1[1])
            after = [k for k in piv if bars[k]["day"] > p2[0]]
            if direction == "down":
                respect = sum(1 for k in after if bars[k][key] <= line_value(p1, p2, bars[k]["day"]) * (1 + tol))
            else:
                respect = sum(1 for k in after if bars[k][key] >= line_value(p1, p2, bars[k]["day"]) * (1 - tol))
            # closes on the breaking side after anchor2
            crosses = []
            for b in bars:
                if b["day"] <= p2[0]:
                    continue
                lv = line_value(p1, p2, b["day"])
                if (direction == "down" and b["c"] > lv) or (direction == "up" and b["c"] < lv):
                    crosses.append(b)
            now = line_value(p1, p2, today)
            gap = (cur / now - 1) * 100 if now else float("nan")
            near = abs(gap) <= 8
            if abs(gap) > 15 and not crosses:
                verdict = "REJECT (garis jauh dari harga — anchor bukan trendline hidup)"
            elif crosses and not near:
                verdict = "BROKEN (harga sudah lewat garis)"
            elif near:
                verdict = "VALID (harga nempel garis — belum tembus)"
            else:
                verdict = "lemah (harga di sisi sepatutnya, garis jauh)"
            res.append({
                "a1": f"{bars[i1]['date']} {p1[1]:.5f}", "a2": f"{bars[i2]['date']} {p2[1]:.5f}",
                "touch": touch, "respect": f"{respect}/{len(after)}",
                "since": crosses[0]["date"] if crosses else "-", "n_cross": len(crosses),
                "line_now": now, "gap_pct": gap, "verdict": verdict,
            })
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--limit", type=int, default=250)
    ap.add_argument("--window", type=int, default=180, help="hanya pakai candle N terakhir")
    ap.add_argument("--lookback", type=int, default=6, help="bar di kiri/kanan untuk pivot")
    ap.add_argument("--tol", type=float, default=0.015, help="toleransi sentuhan (fraksi harga)")
    ap.add_argument("--top", type=int, default=8)
    args = ap.parse_args()

    bars = klines(args.symbol.upper(), args.interval, args.limit)
    if len(bars) < 60:
        print("candle kurang — batal")
        return 1
    bars = bars[-args.window:]
    cur = bars[-1]["c"]
    today = bars[-1]["date"]
    print(f"{args.symbol.upper()} {args.interval} · {len(bars)} candle ({bars[0]['date']} → {today})")
    print(f"harga terakhir {cur:.6f}\n")

    for side, direction, label in (("h", "down", "RESISTANCE (trendline turun)"),
                                   ("l", "up", "SUPPORT (trendline naik)")):
        piv = pivots(bars, args.lookback, side)
        pts = ", ".join(f"{bars[i]['date']} {bars[i]['h' if side == 'h' else 'l']:.5f}" for i in piv[-10:])
        print(f"== {label} — pivot ({len(piv)}): {pts or '-'}")
        res = evaluate(bars, piv, side, args.lookback, args.tol, direction)
        # prioritaskan yang VALID/BROKEN, lalu sentuhan terbanyak
        rank = {"VALID": 0, "BROKEN": 1}
        res.sort(key=lambda r: (rank.get(r["verdict"].split()[0], 2), -r["touch"], abs(r["gap_pct"])))
        if not res:
            print("   (tidak ada pasangan anchor yang valid)\n")
            continue
        for r in res[:args.top]:
            print(f"   {r['a1']}  ->  {r['a2']} | touch {r['touch']} | pivot di sisi benar {r['respect']}"
                  f" | close tembus {r['n_cross']} (sejak {r['since']})"
                  f" | garis kini {r['line_now']:.5f} ({r['gap_pct']:+.1f}% vs harga)")
            print(f"        -> {r['verdict']}")
        print()

    print("ATURAN: garis hanya layak digambar kalau (a) menyentuh >= 2 pivot asli, (b) semua pivot")
    print("setelah anchor ke-2 ada di sisi yang benar, (c) harga terakhir DEKAT garis (bukan puluhan %")
    print("jauhnya). Selalu sebut di caption garis mana yang dipakai — beda anchor bisa berarti")
    print("'sudah tembus' vs 'belum tembus'. Sumber: Binance spot klines (data nyata).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
