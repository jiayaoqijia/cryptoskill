#!/usr/bin/env python3
"""Kartu rencana posisi (READ-ONLY): state spot+futures, trim, opsi sizing short, invalidation.

Contoh:
  python3 position_plan_card.py --trim TAO --sl 2635 --tp1 2503 --tp2 2440 \
      --sizes "0.10:5,0.15:5,0.20:5" --btc-zone 81500,80100

Kredensial dari ~/.hermes/.env (BINANCE_API_KEY / BINANCE_SECRET_KEY).
TIDAK pernah naruh order — output cuma angka biar user yang klik di app.
Detail endpoint + pitfall: cex-portfolio-monitoring/references/binance-futures-readonly.md
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

WIB = timezone(timedelta(hours=7))
SPOT = "https://api.binance.com"
FUT = "https://fapi.binance.com"
ENVF = os.path.expanduser("~/.hermes/.env")
HOLD = ("TAO", "SUI", "BOME", "SOL", "WLD", "ONDO", "VIRTUAL", "ETH", "BTC")


def load_keys(path=ENVF):
    k = s = None
    for ln in open(path):
        ln = ln.strip()
        if ln.startswith("BINANCE_API_KEY="):
            k = ln.split("=", 1)[1].strip()
        elif ln.startswith("BINANCE_SECRET_KEY="):
            s = ln.split("=", 1)[1].strip()
    if not k or not s:
        sys.exit("kredensial Binance gak ada di " + path)
    return k, s


def call(base, path, key=None, secret=None, params=None, signed=False):
    p = dict(params or {})
    if signed:
        p["timestamp"] = int(time.time() * 1000)
        p["recvWindow"] = 5000
    qs = urllib.parse.urlencode(p)
    if signed:
        qs += "&signature=" + hmac.new(secret.encode(), qs.encode(), hashlib.sha256).hexdigest()
    hdrs = {"X-MBX-APIKEY": key} if key else {}          # jangan kirim header None
    req = urllib.request.Request(base + path + ("?" + qs if qs else ""), headers=hdrs)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())


def price(sym):
    return float(call(SPOT, "/api/v3/ticker/price", params={"symbol": sym})["price"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", default="ETHUSDT", help="simbol futures yang di-short")
    ap.add_argument("--trim", default="TAO", help="aset spot yang ditrim")
    ap.add_argument("--trim-target", type=float, default=0.20)
    ap.add_argument("--sl", type=float, required=True, help="stop loss (harga)")
    ap.add_argument("--tp1", type=float, default=None)
    ap.add_argument("--tp2", type=float, default=None)
    ap.add_argument("--risk", type=float, default=0.03, help="budget risiko fraksi equity")
    ap.add_argument("--sizes", default="0.10:5,0.15:5,0.20:5", help="qty:lev,qty:lev")
    ap.add_argument("--btc-zone", default="", help="level BTC, pisah koma (opsional)")
    ap.add_argument("--beta", type=float, default=1.22, help="beta alt vs BTC")
    a = ap.parse_args()

    key, secret = load_keys()
    now = datetime.now(WIB)

    acct = call(SPOT, "/api/v3/account", key, secret, signed=True)
    bal = {b["asset"]: float(b["free"]) + float(b["locked"])
           for b in acct["balances"] if float(b["free"]) + float(b["locked"]) > 0}
    usdt = bal.get("USDT", 0.0)
    alt = {}
    for h in HOLD:
        if bal.get(h, 0) > 0:
            try:
                alt[h] = bal[h] * price(h + "USDT")
            except Exception:
                pass

    fbal = call(FUT, "/fapi/v2/balance", key, secret, signed=True)
    fw = next((float(x["balance"]) for x in fbal if x["asset"] == "USDT"), 0.0)
    favail = next((float(x["availableBalance"]) for x in fbal if x["asset"] == "USDT"), 0.0)

    prem = call(FUT, "/fapi/v1/premiumIndex", params={"symbol": a.short})
    mark = float(prem["markPrice"])
    funding = float(prem["lastFundingRate"])

    brr = call(FUT, "/fapi/v1/leverageBracket", key, secret,
               params={"symbol": a.short}, signed=True)
    brs = brr[0]["brackets"] if isinstance(brr, list) and brr else []
    mmr = float(brs[0]["maintMarginRatio"]) if brs else 0.004

    positions = [p for p in call(FUT, "/fapi/v2/positionRisk", key, secret, signed=True)
                 if abs(float(p.get("positionAmt", 0))) > 0]

    equity = usdt + sum(alt.values()) + fw
    print(f"# KARTU RENCANA POSISI · {now:%d %b %Y %H:%M} WIB")
    print(f"\nEQUITY ${equity:,.2f} = kas spot ${usdt:,.2f} ({usdt / equity * 100:.1f}%)"
          f" + alt ${sum(alt.values()):,.2f} + dompet futures ${fw:,.2f} (available ${favail:,.2f})")
    for h, v in sorted(alt.items(), key=lambda x: -x[1]):
        print(f"   {h:<7} {bal[h]:>13,.4f} = ${v:>8,.2f}  ({v / equity * 100:>5.1f}%)")

    print("\n--- POSISI FUTURES SEKARANG ---")
    if not positions:
        print("   (kosong)")
    for p in positions:
        amt = float(p["positionAmt"])
        notional = abs(amt) * float(p["markPrice"])
        mode = "isolated" if p.get("isolated") else "CROSS"
        print(f"   {p['symbol']} {amt:+.4f} · entry {float(p['entryPrice']):,.2f}"
              f" · mark {float(p['markPrice']):,.2f} · ${notional:,.2f} · {p['leverage']}x {mode}"
              f" · liq {float(p['liquidationPrice']):,.2f} · uPnL {float(p['unRealizedProfit']):+,.2f}")
        if mode == "CROSS":
            print(f"      ! CROSS: liq dihitung dari SELURUH dompet futures (${fw:,.2f}) —"
                  f" jarak liq {(float(p['liquidationPrice']) / float(p['markPrice']) - 1) * 100:+.1f}%")

    print(f"\n--- LANGKAH 1 · rapidikan buku: trim {a.trim} ---")
    tv = alt.get(a.trim, 0.0)
    tgt = equity * a.trim_target
    trim = max(0.0, tv - tgt)
    if trim > 1:
        tpx = bal[a.trim] and (tv / bal[a.trim]) or 0
        print(f"   {a.trim} ${tv:,.2f} ({tv / equity * 100:.1f}%) -> target {a.trim_target * 100:.0f}%")
        print(f"   JUAL {trim / tpx:,.4f} {a.trim} (~${trim:,.2f}) -> kas jadi ${usdt + trim:,.2f}"
              f" ({(usdt + trim) / equity * 100:.1f}%)")
    else:
        print(f"   {a.trim} udah di bawah target ({tv / equity * 100:.1f}%) — nggak perlu trim")

    print(f"\n--- LANGKAH 2 · bentuk short {a.short} ---")
    risk_eth = a.sl - mark
    fund_yr = funding * 3 * 365 * 100
    print(f"   mark {mark:,.2f} · funding {funding * 100:+.4f}%/8j ({fund_yr:+.1f}%/thn)")
    print(f"   SL {a.sl:,.2f} ({risk_eth / mark * 100:+.2f}%)"
          + (f" · TP1 {a.tp1:,.2f} (-{(mark - a.tp1) / mark * 100:.2f}%)" if a.tp1 else "")
          + (f" · TP2 {a.tp2:,.2f} (-{(mark - a.tp2) / mark * 100:.2f}%)" if a.tp2 else ""))
    budget = equity * a.risk
    theo = budget / risk_eth if risk_eth > 0 else 0.0
    print(f"   budget risiko ${budget:,.2f} ({a.risk * 100:.0f}% equity) -> ukuran teoretis"
          f" {theo:.3f} ({theo * mark:,.2f} notional, margin @3x ${theo * mark / 3:,.2f})")
    print("   opsi (isolated; liq estimasi):")
    for item in a.sizes.split(","):
        qty_s, lev_s = item.split(":")
        qty, lev = float(qty_s), float(lev_s)
        notional = qty * mark
        margin = notional / lev
        liq = mark * (1 + 1 / lev - mmr)
        rk = qty * risk_eth
        t1 = qty * (mark - a.tp1) if a.tp1 else 0.0
        t2 = qty * (mark - a.tp2) if a.tp2 else 0.0
        print(f"      {qty:>5.2f} · ${notional:>8,.0f} · margin ${margin:>7,.2f} @{lev:.0f}x"
              f" · liq {liq:>9,.0f} · risiko ${rk:>7,.2f} · TP1 +${t1:>6,.2f} · TP2 +${t2:>6,.2f}")

    if a.btc_zone:
        btc = price("BTCUSDT")
        print("\n--- LANGKAH 3 · zona beli (kalau tesis kena) ---")
        for s in a.btc_zone.split(","):
            lvl = float(s)
            mv = 1 - lvl / btc
            print(f"   BTC {lvl:,.0f} ({-mv * 100:+.1f}%) -> {a.short[:-4]} setara"
                  f" ~{mark * (1 - mv * a.beta):,.2f}")

    print("\n--- INVALIDATION (tesis batal kalau) ---")
    print("   • tulis level close harian/4H yang membatalkan, sebelum entry")
    print("   • SL harus selalu LEBIH DEKAT dari harga liq — SL duluan, bukan liq")
    print("   • satu ide satu stop; kalau kena SL keluar, jangan rata-rata bawah")
    print("   • agent READ-ONLY: angka ini buat user klik, verifikasi setelahnya dari trade history")


if __name__ == "__main__":
    main()
