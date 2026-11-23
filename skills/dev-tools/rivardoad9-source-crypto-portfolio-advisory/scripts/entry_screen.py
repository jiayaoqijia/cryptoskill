#!/usr/bin/env python3
"""Entry screen on liquid CEX pairs (Binance klines, stdlib only, no API key).

Two modes:

  python3 entry_screen.py --screen                 # mechanical pass: uptrend but not extended
  python3 entry_screen.py --inspect HBAR,XRP,ILV   # structure detail (high90 DATE, swings, volume trend)

MANDATORY: --screen is a first pass only. A mechanical RR > 1,5 has repeatedly been a false positive
(stale 90d high, or a blowoff high that was already rejected). ALWAYS run --inspect on the top names
before saying anything to the user. Rules + worked examples:
`references/entry-screen-liquid-majors.md`.

Filters used by --screen: price > EMA200, pos90 < 82, quoteVolume 24h > $8jt, vol7/30 > 1.05x.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://api.binance.com"

DEFAULT_UNIVERSE = [
    "BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "AVAX", "LINK", "DOT", "ATOM", "NEAR", "APT", "SUI",
    "ARB", "OP", "INJ", "TIA", "SEI", "FET", "RENDER", "TAO", "ONDO", "AAVE", "UNI", "LDO", "EIGEN",
    "ENA", "PENDLE", "JUP", "PYTH", "DOGE", "LTC", "TON", "ALGO", "HBAR", "ICP", "FIL", "GRT", "CRV",
    "SNX", "COMP", "MKR", "ZEC", "XLM", "ETC", "ILV", "IMX", "ALICE", "SAND", "MANA", "AXS", "GALA",
    "MAGIC", "ENJ", "SUPER", "TNSR", "GRAM", "BOME", "STONK",
]


def jget(url, tries=3, pause=4.0):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.load(r)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(pause * (i + 1))


def klines(symbol, limit=700):
    url = f"{BASE}/api/v3/klines?symbol={symbol}USDT&interval=1d&limit={limit}"
    return jget(url)


def rows(symbol, limit=700):
    """Daily bars as dicts with UTC dates (kline open time is ms)."""
    out = []
    for r in klines(symbol, limit):
        out.append({
            "d": dt.datetime.utcfromtimestamp(r[0] / 1000).strftime("%Y-%m-%d"),
            "o": float(r[1]), "h": float(r[2]), "l": float(r[3]), "c": float(r[4]), "v": float(r[7]),
        })
    return out


def ema(vals, period):
    a = 2.0 / (period + 1.0)
    out = [vals[0]]
    for x in vals[1:]:
        out.append(out[-1] + a * (x - out[-1]))
    return out


def metrics(symbol, ticker=None):
    b = rows(symbol)
    if len(b) < 210:
        return None
    C = [x["c"] for x in b]
    H = [x["h"] for x in b]
    L = [x["l"] for x in b]
    Q = [x["v"] for x in b]
    cur = C[-1]
    h90, l90 = max(H[-90:]), min(L[-90:])
    ma30 = statistics.mean(C[-30:])
    e200 = ema(C, 200)[-1]
    v7, v30 = statistics.mean(Q[-8:-1]), statistics.mean(Q[-31:-1])
    qv = (ticker or {}).get("qv") or 0.0
    up = (h90 / cur - 1) * 100
    dn = (1 - ma30 / cur) * 100
    return {
        "sym": symbol, "cur": cur, "qv_jt": qv / 1e6,
        "ch24": (ticker or {}).get("ch24", (cur / C[-2] - 1) * 100),
        "ch7": (cur / C[-8] - 1) * 100, "ch30": (cur / C[-31] - 1) * 100,
        "pos90": (cur - l90) / (h90 - l90) * 100 if h90 > l90 else 100.0,
        "up_high90": up, "dn_ma30": dn, "rr": up / dn if dn > 0.5 else float("inf"),
        "ma30": ma30, "e200": e200, "vs_e200": (cur / e200 - 1) * 100,
        "vol_ratio": v7 / v30 if v30 else 0.0, "high90": h90, "low90": l90,
    }


def tickers():
    return {r["symbol"][:-4]: {"qv": float(r["quoteVolume"]), "ch24": float(r["priceChangePercent"])}
            for r in jget(f"{BASE}/api/v3/ticker/24hr") if r["symbol"].endswith("USDT")}


def screen(universe):
    tk = tickers()
    ok = []
    for s in universe:
        if s not in tk:
            continue
        try:
            m = metrics(s, tk[s])
        except Exception as err:                                   # noqa: BLE001
            print(f"  ! {s}: {err}", file=sys.stderr)
            continue
        if m and m["vs_e200"] > 0 and m["pos90"] < 82 and m["qv_jt"] > 8 and m["vol_ratio"] > 1.05:
            ok.append(m)
    ok.sort(key=lambda r: -r["rr"])
    print("PASS: di atas EMA200, pos90 <82 (belum extended), likuid >$8jt, vol7/30 >1,05x")
    print("\n{:<7}{:>11}{:>7}{:>8}{:>7}{:>9}{:>8}{:>8}{:>9}{:>8}{:>7}".format(
        "SYM", "HARGA", "7d%", "30d%", "pos90", "vsE200", "toHigh", "toMA30", "vol24jt", "vol7/30", "RR"))
    for r in ok:
        print("{:<7}{:>11.6g}{:>7.1f}{:>8.1f}{:>7.1f}{:>8.1f}%{:>7.1f}%{:>7.1f}%{:>9.1f}{:>7.2f}x{:>7.2f}".format(
            r["sym"], r["cur"], r["ch7"], r["ch30"], r["pos90"], r["vs_e200"],
            r["up_high90"], r["dn_ma30"], r["qv_jt"], r["vol_ratio"], r["rr"]))
    print(f"\ntotal lolos: {len(ok)} dari {len(universe)}")
    print("!! JANGAN pakai RR mekanis apa adanya — jalankan --inspect dulu (high90 basi/blowoff = RR palsu)")
    return ok


def inspect(symbols):
    for s in symbols:
        b = rows(s)
        if len(b) < 30:
            print(f"\n=== {s}: data kurang ({len(b)} bar)")
            continue
        cur = b[-1]["c"]
        w = b[-90:]
        hi, lo = max(w, key=lambda x: x["h"]), min(w, key=lambda x: x["l"])
        print(f"\n=== {s} harga {cur} ===")
        print(f"  high90 {hi['h']} ({hi['d']})  <-- CEK TANGGAL: basi (>60 hari) = RR palsu, 1-2 hari = blowoff")
        print(f"  low90  {lo['l']} ({lo['d']})")
        print("  14 bar terakhir (close / high / low / vol$jt):")
        for x in b[-14:]:
            print(f"    {x['d']}  c {x['c']:<12.8g} h {x['h']:<12.8g} l {x['l']:<12.8g} vol ${x['v']/1e6:>8.2f}jt")
        sw_h, sw_l = [], []
        for i in range(5, len(b) - 5):
            if all(b[i]["h"] >= b[j]["h"] for j in range(i - 5, i + 6)):
                sw_h.append((b[i]["d"], round(b[i]["h"], 8)))
            if all(b[i]["l"] <= b[j]["l"] for j in range(i - 5, i + 6)):
                sw_l.append((b[i]["d"], round(b[i]["l"], 8)))
        print("  swing high 120d:", sw_h[-7:])
        print("  swing low  120d:", sw_l[-7:])
        v7 = statistics.mean([x["v"] for x in b[-8:-1]])
        v30 = statistics.mean([x["v"] for x in b[-31:-1]])
        print(f"  vol: 24j ${b[-1]['v']/1e6:.2f}jt | 7d avg ${v7/1e6:.2f}jt | 30d avg ${v30/1e6:.2f}jt"
              f" | rasio {v7/v30:.2f}x")
        # verdict bantu: spike ditolak atau flag?
        if len(b) >= 6:
            last6 = b[-6:]
            spike = max(last6, key=lambda x: x["h"])
            spk_avg = statistics.mean([x["v"] for x in b[-36:-6]]) or 1
            mult = spike["v"] / spk_avg
            drop = (spike["h"] - cur) / spike["h"] * 100
            hold = "HOLD di atas low spike (flag)" if cur > spike["l"] else "balik ke dalam body spike (gagal)"
            print(f"  spike terakhir: {spike['d']} high {spike['h']} vol {mult:.1f}x avg | dari high sekarang -{drop:.1f}% | {hold}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen", action="store_true", help="mechanical pass (default)")
    ap.add_argument("--inspect", help="comma-separated symbols → structure detail")
    ap.add_argument("--universe", help="comma-separated symbols to screen (default: built-in ~60)")
    a = ap.parse_args()
    if a.inspect:
        inspect([s.strip().upper() for s in a.inspect.split(",") if s.strip()])
    else:
        uni = [s.strip().upper() for s in a.universe.split(",")] if a.universe else DEFAULT_UNIVERSE
        screen(uni)


if __name__ == "__main__":
    main()
