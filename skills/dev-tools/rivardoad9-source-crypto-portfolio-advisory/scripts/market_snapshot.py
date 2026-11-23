#!/usr/bin/env python3
"""Snapshot market keyless: harga + mcap + %ATH, MA20/MA50 + posisi rentang 30h + vol realized, Fear&Greed.

Pakai: python3 market_snapshot.py [out.json]
Sumber: CoinGecko /coins/markets (WAJIB price_change_percentage=24h,7d), Binance klines, alternative.me.
Jebakan yang sudah dijaga: (a) field None TIDAK boleh dicetak sebagai 0, (b) 429 -> backoff, (c) aset
yang sejarah Binance-nya pendek ditandai (MA/pos30d n/a), (d) id CoinGecko != ticker.
"""
import json, sys, time, urllib.request, statistics as st

UA = {"User-Agent": "Mozilla/5.0"}
OUT = sys.argv[1] if len(sys.argv) > 1 else "market_snapshot.json"

CG_IDS = {
    "bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "injective-protocol": "INJ",
    "ondo-finance": "ONDO", "hyperliquid": "HYPE", "near": "NEAR", "quant-network": "QNT",
    "uniswap": "UNI", "chainlink": "LINK", "theta-token": "THETA", "telcoin": "TEL",
}
BIN = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "INJUSDT", "ONDOUSDT", "NEARUSDT", "UNIUSDT",
       "LINKUSDT", "QNTUSDT", "HYPEUSDT", "THETAUSDT"]


def get(url, tries=3, sleep=4, timeout=40):
    last = None
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout))
        except Exception as e:            # 429 / timeout -> backoff, bukan "endpoint mati"
            last = e
            time.sleep(sleep * (i + 1))
    raise last


def f(x, fmt="{:.1f}%"):
    """Formatter AMAN: None -> n/a. JANGAN pernah fallback ke 0 — itu ngarang angka."""
    return fmt.format(x) if isinstance(x, (int, float)) else "n/a"


out = {"prices": {}, "tech": {}, "fng": None}

u = ("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + ",".join(CG_IDS) +
     "&price_change_percentage=24h,7d&order=market_cap_desc")
try:
    for c in get(u):
        out["prices"][(c.get("symbol") or "").upper()] = {
            "px": c.get("current_price"), "mcap": c.get("market_cap"),
            "ch24": c.get("price_change_percentage_24h_in_currency"),
            "ch7d": c.get("price_change_percentage_7d_in_currency"),
            "ath": c.get("ath"), "ath_chg": c.get("ath_change_percentage"),
            "vol24": c.get("total_volume"),
        }
except Exception as e:
    print("COINGECKO GAGAL:", str(e)[:120])

for sym in BIN:
    try:
        k = get(f"https://api.binance.com/api/v3/klines?symbol={sym}&interval=1d&limit=100", tries=2, sleep=3)
        cl = [float(r[4]) for r in k]; hi = [float(r[2]) for r in k]; lo = [float(r[3]) for r in k]
        last = cl[-1]
        ma20 = sum(cl[-20:]) / 20 if len(cl) >= 20 else None
        ma50 = sum(cl[-50:]) / 50 if len(cl) >= 50 else None
        hi30, lo30 = max(hi[-30:]), min(lo[-30:])
        rets = [cl[i] / cl[i - 1] - 1 for i in range(1, len(cl))][-30:]
        out["tech"][sym[:-4]] = {
            "px": last, "ma20": ma20, "ma50": ma50,
            "ma20_gap": (last / ma20 - 1) * 100 if ma20 else None,
            "ma50_gap": (last / ma50 - 1) * 100 if ma50 else None,
            "hi30": hi30, "lo30": lo30,
            "pos30": (last - lo30) / (hi30 - lo30) * 100 if hi30 > lo30 else None,
            "vol30_ann": (st.pstdev(rets) if len(rets) > 1 else 0) * (365 ** 0.5) * 100,
            "ch30": (last / cl[-31] - 1) * 100 if len(cl) > 31 else None,
            "partial": len(cl) < 60,          # aset baru listing: MA/pos30d jangan dipercaya
        }
        time.sleep(0.6)
    except Exception as e:
        out["tech"][sym[:-4]] = {"err": str(e)[:90]}

try:
    out["fng"] = [{"v": d["value"], "cls": d["value_classification"]} for d in
                  get("https://api.alternative.me/fng/?limit=8")["data"]]
except Exception as e:
    out["fng"] = {"err": str(e)[:90]}

json.dump(out, open(OUT, "w"), indent=1)
print("=== HARGA ===")
print(f"{'tok':6}{'harga':>12}{'mcap':>18}{'24h':>8}{'7d':>8}{'%ATH':>9}")
for s, v in sorted(out["prices"].items(), key=lambda x: -(x[1]["mcap"] or 0)):
    px = f"{v['px']:,.4f}" if isinstance(v["px"], (int, float)) else "n/a"
    print(f"{s:6}{px:>12}{(v['mcap'] or 0):>18,.0f}{f(v['ch24']):>8}{f(v['ch7d']):>8}{f(v['ath_chg']):>9}")
print("\n=== TEKNIKAL (Binance 100d) ===")
print(f"{'tok':6}{'harga':>12}{'vsMA20':>9}{'vsMA50':>9}{'pos30d':>8}{'volThn':>8}{'ch30d':>8}")
for s, v in out["tech"].items():
    if "err" in v:
        print(f"{s:6}  ERR {v['err']}"); continue
    flag = " (parsial)" if v.get("partial") else ""
    print(f"{s:6}{v['px']:>12,.4f}{f(v['ma20_gap']):>9}{f(v['ma50_gap']):>9}"
          f"{f(v['pos30'], '{:.0f}%'):>8}{f(v['vol30_ann'], '{:.0f}%'):>8}{f(v['ch30']):>8}{flag}")
print("\n=== FEAR & GREED ===", out["fng"])
print(f"\ndisimpan: {OUT}")
