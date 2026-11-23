#!/usr/bin/env python3
"""Beta koin vs BTC dari seri harian CoinGecko (stdlib saja, keyless).

Kenapa ada: check #5 di `references/holdings-thesis-verification.md` minta angka beta/vol buat
sizing, tapi 90d series CoinGecko gampang kena 429 dan hitungannya harus konsisten antar koin.
Script ini: 1 request per koin, dedupe ke 1 titik/hari, log-return, beta = cov(a,btc)/var(btc).

Pakai:
    python3 beta_vs_btc.py ondo-finance virtual-protocol          # id CoinGecko
    python3 beta_vs_btc.py --days 180 ondo-finance bittensor

Catatan:
- BTC-nya otomatis di-fetch sekali, dipakai bareng semua koin (hemat request).
- `--twap` tidak ada; `market_chart` balikin harga spot per ~5 menit → di-dedupe ke hari terakhir
  per tanggal UTC. Cukup buat beta/vol harian; JANGAN dipakai buat entry level presisi.
- Kalau kena 429 di semua retry: turunkan ke `/coins/markets?ids=a,b,c` (bulk, jauh lebih tahan 429)
  atau pakai Binance klines — lihat `references/data-source-fallback-ladder.md`.
"""
import json
import math
import statistics
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"}
BASE = "https://api.coingecko.com/api/v3"


def get(url, tries=5, wait=15):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=35))
        except Exception as e:  # 429 / transient
            last = e
            if i < tries - 1:
                time.sleep(wait)
    raise last


def daily_series(cid, days):
    """1 titik per hari UTC (harga terakhir hari itu) dari market_chart."""
    data = get("%s/coins/%s/market_chart?vs_currency=usd&days=%d" % (BASE, cid, days))["prices"]
    out, last_day = [], None
    for ts, px in data:
        day = ts // 86400000
        if day != last_day:
            out.append(float(px))
            last_day = day
        else:
            out[-1] = float(px)  # titik terakhir hari itu menang
    return out


def stats(px, btc):
    n = min(len(px), len(btc)) - 1
    if n < 35:
        return None
    px, btc = px[-n - 1:], btc[-n - 1:]
    ra = [math.log(px[i] / px[i - 1]) for i in range(1, len(px)) if px[i - 1] > 0]
    rb = [math.log(btc[i] / btc[i - 1]) for i in range(1, len(btc)) if btc[i - 1] > 0]
    m = min(len(ra), len(rb))
    ra, rb = ra[-m:], rb[-m:]
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    cov = sum((rb[i] - mb) * (ra[i] - ma) for i in range(m)) / (m - 1)
    var = statistics.pvariance(rb)
    beta = cov / var if var else float("nan")
    corr = cov / (statistics.pstdev(rb) * statistics.pstdev(ra)) if var else float("nan")
    return {
        "n": m,
        "beta": beta,
        "corr": corr,
        "vol": 100 * statistics.pstdev(ra),
        "btc_vol": 100 * statistics.pstdev(rb),
        "ma20": statistics.mean(px[-20:]),
        "ma50": statistics.mean(px[-50:]) if len(px) >= 50 else statistics.mean(px),
        "last": px[-1],
        "lo30": min(px[-30:]),
        "hi30": max(px[-30:]),
        "d30": 100 * (px[-1] / px[-31] - 1) if len(px) > 31 else float("nan"),
    }


def main(argv):
    days = 180
    if "--days" in argv:
        i = argv.index("--days")
        days = int(argv[i + 1])
        del argv[i:i + 2]
    ids = argv[1:] or ["ondo-finance"]
    btc = daily_series("bitcoin", days)
    print("BTC: %d titik harian | terakhir $%.0f | vol harian %.1f%%" % (
        len(btc), btc[-1],
        100 * statistics.pstdev([math.log(btc[i] / btc[i - 1]) for i in range(1, len(btc)) if btc[i - 1] > 0])))
    for cid in ids:
        try:
            s = stats(daily_series(cid, days), btc)
        except Exception as e:
            print("%-22s GAGAL: %s (coba /coins/markets bulk atau Binance klines)" % (cid, e))
            continue
        if not s:
            print("%-22s data kurang (%d titik) — lewati" % (cid, s and s["n"] or 0))
            continue
        print("\n%-22s beta %.2f | korelasi %.2f | vol harian %.1f%% (BTC %.1f%%)" % (
            cid, s["beta"], s["corr"], s["vol"], s["btc_vol"]))
        print("   180h: %d hari | harga $%.4f | MA20 $%.4f | MA50 $%.4f" % (
            s["n"], s["last"], s["ma20"], s["ma50"]))
        print("   range 30h $%.4f-$%.4f | 30 hari %+.0f%% | BTC -30%% → koin ini ≈ %+.0f%% (beta-based)" % (
            s["lo30"], s["hi30"], s["d30"], 100 * (math.exp(s["beta"] * math.log(0.7)) - 1)))


if __name__ == "__main__":
    main(sys.argv)
