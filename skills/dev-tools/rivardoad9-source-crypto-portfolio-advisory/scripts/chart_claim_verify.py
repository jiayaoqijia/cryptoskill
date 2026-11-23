#!/usr/bin/env python3
"""Verify a user's TradingView chart claims against live Binance data (keyless).

Usage:
    python3 chart_claim_verify.py [SYMBOL ...]
    python3 chart_claim_verify.py                 # defaults to the book below

Prints, per symbol: live price + 24h change, weekly & daily 200/50-EMA position,
52w range position, % bounce off the 52w low, Stoch(5,3,3) on both timeframes,
the last 4 bars as % moves, the structure-break test (weekly close vs the high of
the previous 11 weeks), and the all-time high + drawdown from it (incl. the wkh
of BTC as the "most proven asset" benchmark).

Keyless: api.binance.com only, no credentials. Companion reference:
references/user-chart-claim-verification.md
"""
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

B = "https://api.binance.com/api/v3"
WIB = timezone(timedelta(hours=7))
DEFAULT = ["ONDOUSDT", "TAOUSDT", "WLDUSDT", "VIRTUALUSDT", "BOMEUSDT", "BTCUSDT", "ETHUSDT"]
EXTRA = ["BTCUSDT"]


def get(path):
    with urllib.request.urlopen(B + path, timeout=20) as r:
        return json.load(r)


def klines(sym, itv, limit=400):
    return get(f"/klines?symbol={sym}&interval={itv}&limit={limit}")


def ema(vals, n):
    k = 2 / (n + 1)
    e = vals[0]
    out = [e]
    for v in vals[1:]:
        e = v * k + e * (1 - k)
        out.append(e)
    return out


def stoch(cl, hi, lo, n=5, ks=3, ds=3):
    kv = []
    for i in range(len(cl)):
        if i < n - 1:
            kv.append(None)
            continue
        hh, ll = max(hi[i - n + 1:i + 1]), min(lo[i - n + 1:i + 1])
        kv.append(50.0 if hh == ll else (cl[i] - ll) / (hh - ll) * 100)
    kv = [x for x in kv if x is not None]
    sma = lambda a, p: [sum(a[i - p + 1:i + 1]) / p for i in range(p - 1, len(a))]
    kk = sma(kv, ks)
    return kk[-1], sma(kk, ds)[-1]


def fmt(n):
    if n >= 1000:
        return f"{n:,.0f}"
    if n >= 1:
        return f"{n:,.2f}"
    return f"{n:,.4f}"


def main():
    syms = sys.argv[1:] or DEFAULT
    for s in EXTRA:
        if s not in syms:
            syms.append(s)
    t = {x["symbol"]: x for x in get("/ticker/24hr?symbols=" + json.dumps(syms).replace(" ", ""))}

    print("=== ATH vs sekarang (sejak listing) ===")
    for s in syms:
        try:
            k = klines(s, "1w", 500)
            ath_bar = max(k, key=lambda x: float(x[2]))
            ath = float(ath_bar[2])
            ath_t = datetime.fromtimestamp(ath_bar[0] / 1000, WIB).strftime("%d %b %Y")
            last = float(t[s]["lastPrice"])
            print(f"  {s:12} ATH {fmt(ath):>12} ({ath_t})  now {fmt(last):>10}  = {(last/ath-1)*100:+.1f}% dari ATH")
        except Exception as e:
            print(f"  {s:12} GAGAL: {e}")

    for s in syms:
        tick = t[s]
        last = float(tick["lastPrice"])
        print(f"\n{'='*64}\n{s}  LIVE {fmt(last)}  24h {float(tick['priceChangePercent']):+.2f}%"
              f"  range {fmt(float(tick['lowPrice']))}-{fmt(float(tick['highPrice']))}")
        for itv, label in (("1w", "WEEKLY"), ("1d", "DAILY")):
            k = klines(s, itv, 400)
            cl = [float(x[4]) for x in k]
            hi = [float(x[2]) for x in k]
            lo = [float(x[3]) for x in k]
            e200, e50 = ema(cl, 200)[-1], ema(cl, 50)[-1]
            kk, dd = stoch(cl, hi, lo)
            h52, l52 = max(hi[-52:]), min(lo[-52:])
            rng = (last - l52) / (h52 - l52) * 100 if h52 > l52 else 0
            print(f"  {label}: 200EMA {fmt(e200)} ({'DI ATAS' if last > e200 else 'DI BAWAH'}"
                  f" {(last/e200-1)*100:+.1f}%) | 50EMA {fmt(e50)}"
                  f" | 52{label[0]} hi {fmt(h52)} / lo {fmt(l52)} -> {rng:.0f}% range"
                  f" | bounce {(last/l52-1)*100:+.1f}% | Stoch {kk:.2f}/{dd:.2f}")
            print("        4 bar terakhir: " + " | ".join(
                datetime.fromtimestamp(x[0] / 1000, WIB).strftime("%d%b") +
                f" {(float(x[4])/float(x[1])-1)*100:+.1f}%" for x in k[-4:]))
        k = klines(s, "1w", 400)
        if len(k) > 12:
            prior = max(float(x[2]) for x in k[-12:-1])
            status = "SUDAH break struktur" if last > prior else "BELUM break struktur"
            print(f"        struktur: close {fmt(last)} vs high 11 minggu sebelumnya {fmt(prior)} -> {status}")


if __name__ == "__main__":
    main()
