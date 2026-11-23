#!/usr/bin/env python3
"""Screen top-120 CoinGecko: ruang (%ATH), ekstensi (30h/7h), FLOAT (circ/total), likuiditas (vol/mcap).

Dipakai buat: (a) nolak kandidat secara kuantitatif (mis. QNT 30h +340% -> EV negatif),
(b) nempel float sebagai KOLOM (HYPE circ 23% / XPL 45% / TAO 54% / ONDO 49% = kelemahan
struktural yang nggak kelihatan kalau cuma lihat harga), (c) cari kandidat sleeve baru.

Satu panggilan API = seluruh tabel pembanding. Simpan JSON-nya biar bisa dipakai ulang tanpa hit ulang.

Jalanin:  python3 market_screen.py [path_cache.json]
"""
import json
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
CACHE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/market120.json"

URL = ("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
       "&per_page=120&page=1&sparkline=false&price_change_percentage=7d,30d")
# CATATAN: price_change_percentage WAJIB -> tanpa itu field 7d/30d None dan tabel lu ngarang "0,0%".


def get(url, tries=4, wait=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception as e:                                    # noqa: BLE001
            if i == tries - 1:
                raise
            print(f"  (retry {i + 1}: {str(e)[:50]})", file=sys.stderr)
            time.sleep(wait)                                      # 429 = tunggu, bukan endpoint mati


def main():
    try:
        data = json.load(open(CACHE))
    except Exception:                                             # noqa: BLE001
        data = get(URL)
        json.dump(data, open(CACHE, "w"))
    print(f"cache {CACHE} · {len(data)} koin\n")

    rows = []
    for c in data:
        mc, px = c.get("market_cap"), c.get("current_price")
        if not mc or not px:
            continue
        circ, tot = c.get("circulating_supply") or 0, c.get("total_supply") or 0
        rows.append(dict(
            rk=c["market_cap_rank"], sym=c["symbol"].upper(), px=px, mc=mc / 1e6,
            ath=c.get("ath_change_percentage") or 0,
            d7=c.get("price_change_percentage_7d_in_currency") or 0,
            d30=c.get("price_change_percentage_30d_in_currency") or 0,
            f=(circ / tot * 100) if tot else 100.0,
            vm=(c.get("total_volume") or 0) / mc * 100,
            fdv=(px * tot / 1e6) if tot else mc / 1e6,
        ))

    print(f"{'#':>4} {'sym':7}{'harga':>12}{'mcap $jt':>11}{'dariATH':>9}{'30h':>8}{'7h':>8}"
          f"{'circ%':>7}{'vol/mc':>8}{'FDV $jt':>10}")
    for r in sorted(rows, key=lambda x: x["rk"]):
        print(f"{r['rk']:>4} {r['sym']:7}{r['px']:>12,.4f}{r['mc']:>11,.0f}{r['ath']:>8.1f}%"
              f"{r['d30']:>7.1f}%{r['d7']:>7.1f}%{r['f']:>6.0f}%{r['vm']:>7.1f}%{r['fdv']:>10,.0f}")

    print("\n--- Kandidat: 30h moderat (<60%) + ruang (%ATH ≤ -60%) + float tinggi (circ ≥75%) ---")
    for r in sorted(rows, key=lambda x: x["ath"]):
        if r["d30"] < 60 and r["ath"] <= -60 and r["f"] >= 75 and 1000 <= r["mc"] <= 100_000:
            print(f"  {r['sym']:7} mcap ${r['mc']:>8,.0f}jt  {r['ath']:>6.1f}% ATH  30h {r['d30']:>5.1f}%  "
                  f"circ {r['f']:>3.0f}%  vol/mc {r['vm']:>5.1f}%")

    print("\n--- Bahaya float: kandidat kuat tapi circ <60% (overhang, bukan price discovery) ---")
    for r in sorted(rows, key=lambda x: x["f"]):
        if r["f"] < 60 and r["mc"] >= 300:
            print(f"  {r['sym']:7} circ {r['f']:>3.0f}%  FDV ${r['fdv']:>8,.0f}jt vs mcap ${r['mc']:>8,.0f}jt  "
                  f"{r['ath']:>6.1f}% ATH  30h {r['d30']:>5.1f}%")


if __name__ == "__main__":
    main()
