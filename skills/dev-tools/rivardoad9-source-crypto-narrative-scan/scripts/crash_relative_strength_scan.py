#!/usr/bin/env python3
"""Scan kekuatan relatif saat market turun: koin mana yang NAIHAN saat BTC merah.

Pertanyaan yang dijawab: "top coin yg performance paling well dan strong pas market crash,
kita bisa liat dari sini coin yg bener-bener kuat".

Jalanin:  python3 crash_relative_strength_scan.py [--min-vol 5000000] [--top 22]

Kenapa Binance ticker+klines dan bukan aggregator: satu panggilan /ticker/24hr = seluruh universe,
lalu klines 1d per kandidat memberi RS vs BTC + jarak ke high 30d + posisi EMA yang nggak ada di
snippet aggregator (dan snippet agregator sering basi/self-contradicting — lihat
`token-news-db-and-unlock-verification.md` §5).

Output: tabel ranked + daftar lolos filter inti + daftar "kelihatan kuat tapi bukan kekuatan".
Yang TIDAK dilakukan script ini: cek berita. Setiap nama di daftar SQUEEZE CHECK wajib lewat
`single-token-move-attribution.md` sebelum masuk laporan.
"""
import argparse
import datetime
import json
import time
import urllib.request

TZ = datetime.timezone(datetime.timedelta(hours=7))
UA = {"User-Agent": "Mozilla/5.0"}

STABLE = {"USDC", "FDUSD", "TUSD", "USDP", "DAI", "EUR", "AEUR", "USD1", "XUSD", "USDY",
          "BFUSD", "USDE", "USDJ", "PYUSD", "USDT", "BUSD", "USDS", "EURI", "RLUSD", "U"}


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
        except Exception:                                        # noqa: BLE001
            if i == tries - 1:
                return None
            time.sleep(1.2)


def is_junk(base):
    if base in STABLE:
        return True
    if base.startswith("WB"):                                    # WBTC/WBETH = wrapped, bukan koin
        return True
    return any(base.endswith(s) and len(base) > 3 for s in ("UP", "DOWN", "BULL", "BEAR"))


def ema(vals, n):
    a = 2 / (n + 1)
    e = vals[0]
    for x in vals[1:]:
        e = x * a + e * (1 - a)
    return e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-vol", type=float, default=5_000_000, help="ambang quoteVolume 24j USDT")
    ap.add_argument("--top", type=int, default=22, help="berapa baris ditampilkan")
    ap.add_argument("--save", default="/tmp/crash_scan/metrics.json")
    args = ap.parse_args()

    tickers = get("https://api.binance.com/api/v3/ticker/24hr")
    if not tickers:
        raise SystemExit("gagal tarik ticker (rate limit / jaringan)")

    universe = []
    for t in tickers:
        s = t["symbol"]
        if not s.endswith("USDT") or is_junk(s[:-4]):
            continue
        try:
            qv, pc, last = float(t["quoteVolume"]), float(t["priceChangePercent"]), float(t["lastPrice"])
        except (KeyError, ValueError):
            continue
        if qv >= args.min_vol and last > 0:
            universe.append((s[:-4], qv, pc, last))

    print(f"universe: {len(universe)} koin USDT likuid (> ${args.min_vol/1e6:.1f}M) · "
          f"{datetime.datetime.now(TZ).strftime('%d %b %H:%M WIB')}", flush=True)

    rows = []
    for i, (sym, qv, pc, last) in enumerate(universe, 1):
        k = get(f"https://api.binance.com/api/v3/klines?symbol={sym}USDT&interval=1d&limit=31")
        if not k or len(k) < 25:
            continue
        c = [float(x[4]) for x in k]
        hi = [float(x[2]) for x in k]
        lo = [float(x[3]) for x in k]
        vol = [float(x[7]) for x in k]
        high30 = max(hi[-30:])
        d = dict(sym=sym, price=last, vol24=qv / 1e6, chg24=pc,
                 chg7=(c[-1] / c[-8] - 1) * 100, chg30=(c[-1] / c[-25] - 1) * 100,
                 dist_high30=(c[-1] / high30 - 1) * 100,
                 dist_low30=(c[-1] / min(lo[-30:]) - 1) * 100,
                 above20=c[-1] > ema(c[-20:], 20), above50=c[-1] > ema(c, 50 if len(c) >= 50 else 31),
                 vol_exp=(sum(vol[-3:]) / 3) / (sum(vol[-30:]) / 30))
        rows.append(d)
        if i % 25 == 0:
            print(f"  ...{i}/{len(universe)}", flush=True)
        time.sleep(0.05)

    if args.save:
        try:
            json.dump(rows, open(args.save, "w"))
        except OSError:
            pass

    b = next((r for r in rows if r["sym"] == "BTC"), None)
    e = next((r for r in rows if r["sym"] == "ETH"), None)
    if not b:
        raise SystemExit("BTC nggak ada di universe — naikin --min-vol atau cek endpoint")
    print(f"\nBENCHMARK BTC {b['chg24']:+.2f}% 24j / {b['chg7']:+.2f}% 7d / {b['chg30']:+.2f}% 30d"
          + (f" · ETH {e['chg24']:+.2f}% / {e['chg7']:+.2f}% / {e['chg30']:+.2f}%" if e else ""))
    for r in rows:
        r["rs24"], r["rs7"], r["rs30"] = r["chg24"] - b["chg24"], r["chg7"] - b["chg7"], r["chg30"] - b["chg30"]
        r["score"] = (r["rs24"] * 1.2 + r["rs7"] + r["rs30"] * 0.35 + r["dist_high30"] * 0.5
                      + (4 if r["above20"] else 0) + (2 if r["above50"] else 0))
    rows.sort(key=lambda x: -x["score"])

    print(f"\n{'#':<4}{'coin':<8}{'harga':>12}{'24h%':>8}{'RS24':>7}{'7d%':>8}{'RS7':>7}"
          f"{'30d%':>8}{'drH30':>7}{'volx':>6}{'vol$M':>7}  EMA")
    for i, r in enumerate(rows[:args.top], 1):
        fl = ("A20" if r["above20"] else " - ") + ("A50" if r["above50"] else " - ")
        print(f"{i:<4}{r['sym']:<8}{r['price']:>12.6g}{r['chg24']:>8.2f}{r['rs24']:>7.2f}{r['chg7']:>8.2f}"
              f"{r['rs7']:>7.2f}{r['chg30']:>8.2f}{r['dist_high30']:>7.1f}{r['vol_exp']:>6.2f}"
              f"{r['vol24']:>7.0f}  {fl}")

    # Filter inti: 7d hijau (nahan selama drawdown), di atas EMA20 & 50, 24j nggak merah.
    core = [r for r in rows if r["chg7"] > 0 and r["above20"] and r["above50"] and r["chg24"] >= -1]
    core.sort(key=lambda x: -(x["chg7"] + x["chg24"] * 1.2 + x["chg30"] * 0.2))
    print(f"\n--- LOLOS FILTER INTI (7d hijau + di atas EMA20&50 + 24j >= -1%): "
          f"{len(core)} dari {len(rows)} ---")
    for r in core:
        print(f"  {r['sym']:<8}{r['price']:>12.6g}{r['chg24']:>8.2f}{r['chg7']:>8.2f}{r['chg30']:>8.2f}"
              f"{r['dist_high30']:>7.1f}{r['vol24']:>7.0f}")

    # Trap: lonjakan 1 hari di pasar tipis, atau pump yang sudah layu. WAJIB cek berita dulu.
    squeeze = [r for r in rows if r["chg24"] >= 40 or (r["vol_exp"] >= 2.5 and r["chg7"] >= 50)]
    faded = [r for r in rows if r["dist_high30"] <= -30 and r["chg30"] > 50]
    print("\n--- SQUEEZE CHECK (lonjakan ekstrem / vol meledak — cek berita, jangan dipuji) ---")
    for r in sorted(squeeze, key=lambda x: -x["chg24"]):
        print(f"  {r['sym']:<8}{r['chg24']:>8.2f}% 24j {r['chg7']:>8.2f}% 7d  volx {r['vol_exp']:>5.2f}  "
              f"vol24 ${r['vol24']:>5.0f}M  {'di atas EMA' if r['above20'] else 'di bawah EMA'}")
    print("--- PUMP LAYU (jauh dari high 30d walau 30d masih +) ---")
    for r in sorted(faded, key=lambda x: x["dist_high30"]):
        print(f"  {r['sym']:<8}30d {r['chg30']:>7.1f}%  tapi {r['dist_high30']:>6.1f}% dari high 30d  "
              f"volx {r['vol_exp']:.2f}")

    print("\nCatatan: 'volume naik' bukan sebab, itu gejala. Setiap nama di SQUEEZE CHECK harus lewat\n"
          "single-token-move-attribution.md (jam volume -> idiosinkratik vs sektor -> OI/funding -> "
          "berita bertanggal) sebelum masuk laporan.")


if __name__ == "__main__":
    main()
