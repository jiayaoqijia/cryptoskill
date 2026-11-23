#!/usr/bin/env python3
"""Matematika buku porto: beta buku, HHI, alpha vs BTC, likuiditas — dari Binance, keyless.

Kenapa ada: `beta_vs_btc.py` ngasih beta/vol PER koin (CoinGecko). Yang dipakai buat mutusin
komposisi itu angka BUKU (bobot × beta, HHI, nama efektif, terjemahan "kalau BTC -20%"), plus
fakta eksekusi per koin (posisi vs EMA20d/50d, alpha 7h/30h, likuiditas 24 jam). Semua dari
Binance klines + ticker → nggak kena 429 CoinGecko dan konsisten sama venue eksekusi user.

Pakai:
    python3 book_risk_composition.py --live                       # bobot porto asli (binance_porto.py)
    python3 book_risk_composition.py SOL=40 SUI=30 TAO=30         # skenario komposisi
    python3 book_risk_composition.py --live SOL=40 SUI=30 TAO=30  # dua-duanya, biar kelihatan deltanya
    python3 book_risk_composition.py --live SOL=35 SUI=25 TAO=25 USDT=15 --json

Catatan penting:
- `interval=1d` baris TERAKHIR = candle yang masih jalan. Script ini selalu drop baris terakhir
  → semua metrik cuma pakai candle yang SUDAH tutup (07:00 WIB).
- Timestamp baris klines = waktu OPEN, bukan close. Candle harian open 00:00 UTC = 07:00 WIB.
- Beta = cov(ret_koin, ret_BTC)/var(ret_BTC) atas 60 candle tutup terakhir (return sederhana).
- HHI = Σ bobot² → nama efektif = 1/HHI. USDT/kas dihitung beta 0 (ikut di HHI, bukan di beta).
- Likuiditas = quoteVolume 24 jam Binance; ini yang nentuin slippage, bukan market cap.
"""
from __future__ import annotations

import json
import os
import statistics
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"}
BIN = "https://api.binance.com/api/v3"
BETA_N = 60
CASH = ("USDT", "USDC", "FDUSD", "BUSD")


def get(url, tries=4, wait=6):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
        except Exception as e:  # transient / rate limit
            last = e
            if i < tries - 1:
                import time
                time.sleep(wait)
    raise last


def closed_closes(sym, n=120):
    """Close harian yang SUDAH tutup (baris terakhir = candle jalan → dibuang)."""
    rows = get(f"{BIN}/klines?symbol={sym}USDT&interval=1d&limit={n + 1}")
    return [float(x[4]) for x in rows[:-1]], [int(x[0]) for x in rows[:-1]]


def ema(vals, p):
    k = 2 / (p + 1)
    e = vals[0]
    for v in vals[1:]:
        e = v * k + e * (1 - k)
    return e


def ret(cl, n):
    return (cl[-1] / cl[-1 - n] - 1) * 100 if len(cl) > n else float("nan")


def beta_vs(ra, rb):
    m = min(len(ra), len(rb))
    ra, rb = ra[-m:], rb[-m:]
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    cov = sum((rb[i] - mb) * (ra[i] - ma) for i in range(m)) / m
    var = sum((x - mb) ** 2 for x in rb) / m
    return cov / var if var else float("nan")


def metrics(sym, btc_cl):
    cl, _ = closed_closes(sym)
    rs = [cl[i] / cl[i - 1] - 1 for i in range(len(cl) - BETA_N, len(cl))]
    rb = [btc_cl[i] / btc_cl[i - 1] - 1 for i in range(len(btc_cl) - BETA_N, len(btc_cl))]
    b7, b30 = ret(btc_cl, 7), ret(btc_cl, 30)
    r7, r30 = ret(cl, 7), ret(cl, 30)
    t = get(f"{BIN}/ticker/24hr?symbol={sym}USDT")
    hi90 = max(cl[-90:])
    return {
        "px": cl[-1],
        "r7": r7, "a7": r7 - b7,
        "r30": r30, "a30": r30 - b30,
        "beta": beta_vs(rs, rb),
        "vol": statistics.pstdev(rs) * (365 ** 0.5) * 100,
        "e20": ema(cl[-20:], 20), "e50": ema(cl[-50:], 50),
        "dd90": (cl[-1] / hi90 - 1) * 100,
        "liq": float(t["quoteVolume"]),
    }


def parse_weights(args):
    w = {}
    for a in args:
        if "=" not in a:
            continue
        k, v = a.split("=", 1)
        k = k.upper().replace("USDT", "") or "USDT"
        if k in ("", "CASH"):
            k = "USDT"
        w[k] = float(v.rstrip("%")) / 100
    s = sum(w.values())
    if s <= 0:
        raise SystemExit("bobot kosong — contoh: SOL=40 SUI=30 TAO=30")
    if abs(s - 1) > 0.02:
        print(f"⚠️  bobot total {s * 100:.1f}% (bukan 100%) — dinormalkan")
        w = {k: v / s for k, v in w.items()}
    return w


def live_weights():
    import importlib.util
    p = os.path.expanduser("~/.hermes/scripts/binance_porto.py")
    spec = importlib.util.spec_from_file_location("bp", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    d = m.build()
    tot = float(d["total_usd"])
    return {r["asset"]: r["usd"] / tot for r in d["rows"] if r["usd"] > 0}, tot


def analyse(name, w, M):
    b = sum(w[s] * M[s]["beta"] for s in w if s not in CASH and s in M)
    hhi = sum(v * v for v in w.values())
    print(f"\n--- {name}")
    print("    " + " · ".join(f"{s} {v * 100:.0f}%" for s, v in sorted(w.items(), key=lambda x: -x[1])))
    print(f"    beta buku {b:.2f} (kas = beta 0) · HHI {hhi:.2f} → {1 / hhi:.1f} nama efektif")
    print(f"    kalau BTC -20% → sleeve ini ≈ {-20 * b:+.0f}%")
    return b, hhi


def main(argv):
    args = argv[1:]
    want_live = "--live" in args
    as_json = "--json" in args
    scen = [a for a in args if "=" in a and not a.startswith("--")]
    if not want_live and not scen:
        raise SystemExit(__doc__)

    btc_cl, _ = closed_closes("BTC")
    coins = sorted({a.split("=")[0].upper().replace("USDT", "") for a in scen} |
                   (set(live_weights()[0].keys()) if want_live else set()))
    coins = [c for c in coins if c not in CASH]
    M = {}
    for c in coins:
        try:
            M[c] = metrics(c, btc_cl)
        except Exception as e:
            print(f"⚠️  {c}: gagal ambil data ({e}) — dilewati")

    print(f"=== METRIK LIVE (candle harian tutup terakhir 07:00 WIB) ===")
    for c in coins:
        if c not in M:
            continue
        m = M[c]
        print(f"{c:5s} ${m['px']:>10,.4f} | 7h {m['r7']:+6.2f}% a7 {m['a7']:+6.2f}pp | 30h {m['r30']:+7.2f}% "
              f"a30 {m['a30']:+7.2f}pp | β {m['beta']:4.2f} | vol {m['vol']:5.0f}% | dari high90 {m['dd90']:+6.1f}% | "
              f"{'ATAS' if m['px'] > m['e20'] else 'BAWAH'} EMA20d · "
              f"{'ATAS' if m['px'] > m['e50'] else 'BAWAH'} EMA50d | liq ${m['liq'] / 1e6:,.1f}M")

    out = {"metrics": M, "books": {}}
    if want_live:
        w, tot = live_weights()
        print(f"\n=== BUKU (bobot porto live, total ${tot:,.2f}) ===")
        b, h = analyse("SEKARANG (live)", w, M)
        out["books"]["live"] = {"weights": w, "beta": b, "hhi": h, "total": tot}
    if scen:
        w = parse_weights(scen)
        b, h = analyse("SKENARIO TARGET", w, M)
        out["books"]["target"] = {"weights": w, "beta": b, "hhi": h}
    if as_json:
        print(json.dumps(out, indent=2, default=float))
    print("\nCatatan: beta tinggi + 0% BTC/kas = nggak ada bantalan. Bantalan sejati di crypto itu BTC "
          "(β 1,00) atau kas (β 0) — ETH (β ~1,2) bukan bantalan.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except SystemExit:
        raise
    except Exception as e:
        print(f"⚠️  book_risk_composition gagal — {e}")
        sys.exit(1)
