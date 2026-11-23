#!/usr/bin/env python3
"""Scan pool Solana (GeckoTerminal, keyless) -> tabel coverage = vol24/TVL sebagai proxy fee/TVL.

Pakai: python3 solana_pool_scan.py
Kenapa GeckoTerminal: endpoint Meteora datapi (`dlmm-api.meteora.ag/pair/*`, `amm-v2.meteora.ag/pools`)
balas 404 sejak skema-nya pindah. GeckoTerminal cukup buat screening kasar; detail bin/range tetap dari UI.

Baca hasilnya dengan mata skeptis:
  cov 20-90x dengan TVL $300k+  = pool yang masih hidup (kandidat LP)
  cov 200-300x+ dengan TVL kecil = SPIKE token baru, bukan "pool terbaik"
Selalu cek trend volume DEX (DefiLlama change_7d) sebelum naikin size: volume turun = fee bakal nyusut.
"""
import json, urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
MIN_TVL, MIN_VOL = 30_000, 10_000


def get(u, timeout=40):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=timeout).read())


rows = []
for label, u in [
    ("trending", "https://api.geckoterminal.com/api/v2/networks/solana/trending_pools?page=1"),
    ("top_vol", "https://api.geckoterminal.com/api/v2/networks/solana/pools?sort=h24_volume_usd_desc&page=1"),
]:
    try:
        for p in get(u).get("data", []):
            a = p["attributes"]
            tvl = a.get("reserve_in_usd")
            v24 = (a.get("volume_usd") or {}).get("h24")
            try:
                tvl, v24 = float(tvl), float(v24)
            except (TypeError, ValueError):
                continue                      # skip kalau field kosong — jangan anggap 0
            if tvl < MIN_TVL or v24 < MIN_VOL:
                continue
            rows.append({"src": label, "name": a.get("name") or "?", "tvl": tvl, "v24": v24,
                         "cov": v24 / tvl, "v6": float((a.get("volume_usd") or {}).get("h6") or 0),
                         "ch24": (a.get("price_change_percentage") or {}).get("h24"),
                         "fee": a.get("pool_fee") or a.get("fee_tier"), "addr": a.get("address")})
    except Exception as e:
        print(f"GAGAL {label}: {str(e)[:110]}")   # 429 page 2+ itu normal; 2 halaman cukup

seen, uniq = set(), []
for r in sorted(rows, key=lambda x: -x["cov"]):
    if r["name"] in seen:
        continue
    seen.add(r["name"]); uniq.append(r)

print(f"pool dlm band (TVL>${MIN_TVL:,}, vol24>${MIN_VOL:,}): {len(uniq)} dari {len(rows)} baris")
print(f"{'cov':>7}{'fee/TVL/hr':>11}{'6j':>7}  {'pool':<26}{'TVL':>11}{'vol24':>12}{'ch24':>8}  fee")
for r in uniq[:15]:
    ch = r["ch24"] if isinstance(r["ch24"], (int, float)) else 0
    print(f"{r['cov']:>6.1f}x{r['cov']*100/24:>10.2f}%{r['v6']/r['tvl']*100:>6.1f}%  {r['name'][:26]:<26}"
          f"{r['tvl']:>11,.0f}{r['v24']:>12,.0f}{ch:>7.1f}%  {str(r['fee'])[:10]}")
json.dump(uniq, open("solana_pools.json", "w"), indent=1)
print("\ncatatan: imbal hasil nyata = fee - IL - gas; pool cov tinggi tapi token lagi dump = jebakan.")
print("simpan: solana_pools.json")
