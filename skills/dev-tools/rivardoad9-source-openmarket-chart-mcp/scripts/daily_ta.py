#!/usr/bin/env python3
"""Daily/weekly TA that OpenMarket's free plan refuses (tier_forbidden past a 167h window).

Pulls the venue's public klines REST directly (no auth, no rate-limit plan) and prints the
indicator stack a chart question needs: EMA stack, Wilder RSI14, StochRSI(5,3,3), ATR14 in
price AND percent of price, range position, volume ratio, swing highs/lows, last candles.

Usage:
  python3 daily_ta.py PUMPUSDT
  python3 daily_ta.py PUMPUSDT --spot --interval 1d --limit 400
  python3 daily_ta.py NEARUSDT,HYPEUSDT,WLDUSDT

Stdlib only (urllib) - the system python has no numpy/pandas and needs none.
"""
import argparse
import datetime
import json
import urllib.request

FAPI = "https://fapi.binance.com/fapi/v1/klines?symbol={s}&interval={i}&limit={n}"
SAPI = "https://api.binance.com/api/v3/klines?symbol={s}&interval={i}&limit={n}"


def fetch(symbol, interval, limit, spot):
    url = (SAPI if spot else FAPI).format(s=symbol, i=interval, n=limit)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = json.loads(r.read().decode())
    if not isinstance(raw, list) or not raw:
        raise RuntimeError(f"{symbol}: no klines returned")
    # row = [openTime, o, h, l, c, volume, closeTime, quoteVolume, trades, ...]
    return {
        "t": [int(k[0]) // 1000 for k in raw],
        "o": [float(k[1]) for k in raw],
        "h": [float(k[2]) for k in raw],
        "l": [float(k[3]) for k in raw],
        "c": [float(k[4]) for k in raw],
        "qv": [float(k[7]) for k in raw],  # quote (USD) turnover
    }


def day(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d")


def ema(x, n):
    k = 2 / (n + 1)
    e = sum(x[:n]) / n
    for p in x[n:]:
        e = p * k + e * (1 - k)
    return e


def rsi_series(x, n=14):
    """Wilder RSI, returned aligned to x with the first n entries None."""
    if len(x) <= n:
        return [None] * len(x)
    g = [max(x[i] - x[i - 1], 0) for i in range(1, len(x))]
    l = [max(x[i - 1] - x[i], 0) for i in range(1, len(x))]
    ag, al = sum(g[:n]) / n, sum(l[:n]) / n
    out = [None] * n + [100.0 if al == 0 else 100 - 100 / (1 + ag / al)]
    for i in range(n, len(g)):
        ag = (ag * (n - 1) + g[i]) / n
        al = (al * (n - 1) + l[i]) / n
        out.append(100.0 if al == 0 else 100 - 100 / (1 + ag / al))
    return out


def stoch_rsi(x, rp=5, kp=3, dp=3):
    """StochRSI(rp,kp,dp) - the 5 3 3 preset most mobile apps show."""
    r = rsi_series(x)
    ks = []
    for i in range(len(r)):
        if r[i] is None or i < rp - 1:
            continue
        w = r[i - rp + 1:i + 1]
        if any(v is None for v in w):
            continue
        lo, hi = min(w), max(w)
        ks.append(50.0 if hi == lo else (r[i] - lo) / (hi - lo) * 100)
    if len(ks) < kp + dp:
        return None, None
    sk = [sum(ks[i - kp + 1:i + 1]) / kp for i in range(kp - 1, len(ks))]
    sd = [sum(sk[i - dp + 1:i + 1]) / dp for i in range(dp - 1, len(sk))]
    return sk[-1], sd[-1]


def atr14(b):
    h, l, c = b["h"], b["l"], b["c"]
    if len(c) < 15:
        return None
    tr = [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])) for i in range(1, len(c))]
    a = sum(tr[:14]) / 14
    for v in tr[14:]:
        a = (a * 13 + v) / 14
    return a


def report(symbol, b):
    c, h, l, qv = b["c"], b["h"], b["l"], b["qv"]
    last = c[-1]
    print(f"### {symbol}  bar terakhir {day(b['t'][-1])}  close {last:g}  (bar berjalan: H {h[-1]:g} / L {l[-1]:g})")
    periods = (13, 21, 33, 50, 100, 200)
    if len(c) >= max(periods):
        E = {n: ema(c, n) for n in periods}
        print("EMA      " + "  ".join(f"{n} {E[n]:.6g}" for n in periods))
        stack = all(E[a] > E[n] for a, n in zip(periods, periods[1:]))
        print("stack    " + ("BULLISH (13>21>33>50>100>200)" if stack else "tidak urut bullish"))
        print("posisi   " + "  ".join(f"{n}:{'ATAS' if last > E[n] else 'bawah'}" for n in periods)
              + f"   jarak ke EMA200 {(last / E[200] - 1) * 100:+.1f}%")
        print("pitfall  kalau harga DI BAWAH EMA13 tapi di atas EMA21/33, itu pullback di tren naik, bukan long signal.")
    else:
        print(f"EMA      butuh {max(periods)} bar, cuma ada {len(c)}")
    r = rsi_series(c)
    if r[-1] is not None:
        hist = "  ".join(f"{d}h lalu {r[-1 - d]:.0f}" for d in (3, 7) if len(r) > d and r[-1 - d] is not None)
        print(f"RSI14    {r[-1]:.1f}   ({hist})")
    k, d = stoch_rsi(c)
    if k is not None:
        print(f"StochRSI 5,3,3  K {k:.1f}  D {d:.1f}" + ("   <- oversold" if k < 20 else "   <- overbought" if k > 80 else ""))
    a = atr14(b)
    if a:
        print(f"ATR14    {a:.6g}  = {a / last * 100:.2f}% dari harga")
        print(f"         stop 1xATR di bawah close = {last - a:.6g}; stop 0,5xATR = {last - a / 2:.6g}")
        print("pitfall  stop yang lebih pendek dari 1xATR hampir pasti kesapu goyangan biasa, bukan karena analisanya salah.")
    for n in (7, 14, 30, 60, 90, 180):
        if len(c) > n:
            print(f"chg {n:>3}d  {(last / c[-1 - n] - 1) * 100:+.1f}%")
    for n in (20, 30, 60, 90, 180, 365):
        if len(h) >= n:
            hi, lo = max(h[-n:]), min(l[-n:])
            pos = 0 if hi == lo else (last - lo) / (hi - lo) * 100
            print(f"range {n:>3}d  high {hi:.6g}  low {lo:.6g}  posisi {pos:.0f}% dari range")
    if len(qv) >= 31:
        avg = sum(qv[-30:-1]) / 29
        if avg:
            print(f"volume   24j ${qv[-1] / 1e6:.2f}jt  rata2 30d ${avg / 1e6:.1f}jt  rasio {qv[-1] / avg:.2f}x"
                  "   (bar berjalan belum penuh - rasio rendah itu normal)")
    hs, ls = [], []
    for i in range(2, len(h) - 2):
        if h[i] == max(h[i - 2:i + 3]):
            hs.append((day(b["t"][i]), h[i]))
        if l[i] == min(l[i - 2:i + 3]):
            ls.append((day(b["t"][i]), l[i]))
    if hs:
        print("swing high  " + "  ".join(f"{d}:{v:.6g}" for d, v in hs[-6:]))
    if ls:
        print("swing low   " + "  ".join(f"{d}:{v:.6g}" for d, v in ls[-6:]))
    print("candle terakhir (tgl O H L C):")
    for i in range(-10, 0):
        print(f"   {day(b['t'][i])}  {b['o'][i]:.6g} {h[i]:.6g} {l[i]:.6g} {c[i]:.6g}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("symbol", help="venue-raw symbol, atau beberapa dipisah koma (PUMPUSDT,NEARUSDT)")
    p.add_argument("--interval", default="1d")
    p.add_argument("--limit", type=int, default=400, help="max 1500")
    p.add_argument("--spot", action="store_true", help="pakai api.binance.com (spot), default fapi (USDT-M futures)")
    a = p.parse_args()
    for i, s in enumerate(a.symbol.split(",")):
        s = s.strip().upper()
        if not s:
            continue
        if i:
            print()
        try:
            report(s, fetch(s, a.interval, min(a.limit, 1500), a.spot))
        except Exception as e:
            print(f"### {s}  GAGAL: {e}")


if __name__ == "__main__":
    main()
