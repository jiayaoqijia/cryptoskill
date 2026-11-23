#!/usr/bin/env python3
"""Pre-event binary decision matrix: HOLD vs TRIM-TO-CAP vs EXIT-THESIS-DEAD vs CUT-ALL.

Answers "cut all position or biarin aja" with four priced options across macro scenarios,
instead of voting on a direction. Stdlib only (json/urllib/argparse) — runs on plain python3.

Worked case: 7 Okt 2026, ~$1,3k alt book, a few hours before FOMC minutes (01:00 WIB).
Key line it produced: after cut-all you need +8,9% to get back to cost; holding needs +8,7%.

Usage:
  python3 cut_or_hold_scenarios.py
  python3 cut_or_hold_scenarios.py --dead ONDO,WLD,BOME      # thesis-dead assets -> exit fully
  python3 cut_or_hold_scenarios.py --cap 0.12 --beta 2.4     # user's cap % + book beta vs BTC
  python3 cut_or_hold_scenarios.py --scenarios -5,-8,-1.36,0,3,5
"""
import argparse
import json
import os
import urllib.request

SPOT = "https://api.binance.com/api/v3/ticker/price?symbol={}USDT"
FEE, SPREAD = 0.001, 0.0005  # Binance spot taker ~0,1% + ~0,05% spread


def price(sym, fallback):
    """Live price, falling back to the snapshot price so the script never dies mid-answer."""
    try:
        req = urllib.request.Request(SPOT.format(sym), headers={"User-Agent": "curl/8"})
        return float(json.load(urllib.request.urlopen(req, timeout=15))["price"])
    except Exception:
        return fallback


def load(path):
    d = json.load(open(os.path.expanduser(path)))
    rows = d.get("rows") or d.get("holdings") or []
    book, cost_basis = [], 0.0
    for r in rows:
        sym = r["asset"]
        qty = float(r.get("qty") or r.get("amount") or 0)
        px = 1.0 if sym == "USDT" else price(sym, float(r.get("price") or 0))
        val = qty * px
        pnl = float(r.get("pnl_pct") or 0)
        cost = val / (1 + pnl / 100) if pnl > -100 else val
        cost_basis += cost
        book.append(dict(sym=sym, qty=qty, px=px, val=val, pnl=pnl, cost=cost))
    return book, cost_basis, d.get("wib") or d.get("ts")


def realized(chunks):
    """Realized loss for sold chunks [(usd_sold, pnl_pct)] — proportional to avg cost."""
    return sum(-(u - u / (1 + p / 100)) for u, p in chunks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="~/.hermes/data/binance_porto.json")
    ap.add_argument("--cap", type=float, default=0.12, help="per-position cap as a fraction")
    ap.add_argument("--beta", type=float, default=2.4, help="book beta vs BTC (measure it, don't guess)")
    ap.add_argument("--dead", default="", help="comma list of thesis-dead assets to exit fully")
    ap.add_argument("--scenarios", default="-5,-8,-1.36,0,3,5", help="BTC %% moves, comma separated")
    a = ap.parse_args()
    dead = {s.strip().upper() for s in a.dead.split(",") if s.strip()}

    book, cost_basis, stamp = load(a.file)
    total = sum(b["val"] for b in book)
    usdt = sum(b["val"] for b in book if b["sym"] == "USDT")
    alt = total - usdt
    cap = total * a.cap
    print(f"snapshot {stamp}")
    print(f"BOOK ${total:,.2f} | modal ${cost_basis:,.2f} | unrealized ${total - cost_basis:+,.2f} "
          f"({(total - cost_basis) / cost_basis * 100:+.1f}%) | USDT ${usdt:,.2f} ({usdt / total * 100:.1f}%) "
          f"| ALT ${alt:,.2f} | cap {a.cap:.0%} = ${cap:,.2f}\n")

    print("=== posisi vs cap (sisa yang harus dijual) ===")
    over = {}
    for b in sorted(book, key=lambda x: -x["val"]):
        if b["sym"] == "USDT":
            continue
        o = b["val"] - cap
        if o > 0:
            over[b["sym"]] = o
            note = f"OVER ${o:,.2f} -> jual {o / b['px']:,.4f} unit, sisa {cap / b['px']:,.4f} = {a.cap:.0%}"
        else:
            note = f"dalam cap (kurang ${-o:,.2f})"
        print(f"  {b['sym']:8} ${b['val']:>9,.2f} ({b['val'] / total * 100:>5.1f}%) "
              f"pnl {b['pnl']:>7.2f}%  {note}")

    pnl = {b["sym"]: b["pnl"] for b in book}
    trim_chunks = [(v, pnl[k]) for k, v in over.items()]
    dead_chunks = [(b["val"], b["pnl"]) for b in book if b["sym"] in dead and b["sym"] != "USDT"]

    trim_usd = sum(u for u, _ in trim_chunks)
    dead_usd = sum(u for u, _ in dead_chunks) + trim_usd
    cash = lambda u: u * (1 - FEE - SPREAD)

    print("\n=== opsi (angka rupiah-dollar, bukan opini) ===")
    opts = {}
    opts["HOLD"] = (usdt, alt, 0.0, 0.0)
    opts["TRIM-TO-CAP"] = (usdt + cash(trim_usd), alt - trim_usd, trim_usd, realized(trim_chunks))
    # exit-thesis-dead = full exit of those + trim of the rest to cap
    dead_only = [(b["val"], b["pnl"]) for b in book if b["sym"] in dead and b["sym"] != "USDT"]
    keep_alt = alt - sum(u for u, _ in dead_only) - trim_usd
    opts["EXIT-DEAD+TRIM"] = (usdt + cash(dead_usd), max(keep_alt, 0.0), dead_usd,
                              realized(dead_chunks))
    opts["CUT-ALL"] = (usdt + cash(alt), 0.0, alt, realized([(b["val"], b["pnl"]) for b in book if b["sym"] != "USDT"]))

    for name, (cash_v, alt_v, sold, real) in opts.items():
        print(f"  {name:16} USDT ${cash_v:>9,.2f} ({cash_v / total * 100:>5.1f}%) | ALT ${alt_v:>9,.2f} "
              f"| jual ${sold:>8,.2f} | biaya ${sold * (FEE + SPREAD):>6,.2f} | realized ${real:>8,.2f}")

    print("\n=== recovery math (ini yang biasanya mengakhiri panik) ===")
    for name, (cash_v, alt_v, _, _) in opts.items():
        if cash_v <= 0:
            continue
        print(f"  setelah {name:16} modal ${cost_basis:,.2f} butuh +{(cost_basis / (cash_v + alt_v) - 1) * 100:5.1f}% "
              f"buat balik ke modal")

    moves = [float(x) for x in a.scenarios.split(",") if x.strip()]
    print(f"\n=== matriks skenario (book = {a.beta:g}x move BTC) ===")
    head = "".join(f"{n:>15}" for n in opts)
    print(f"  {'BTC move':>22}{head}")
    for mv in moves:
        bm = mv * a.beta / 100
        line = f"  {mv:>+7.2f}% -> book {bm * 100:>+6.2f}%"
        for name, (cash_v, alt_v, _, _) in opts.items():
            line += f"{cash_v + alt_v * (1 + bm):>15,.0f}"
        print(line)
    print("\n  Baca: kalau kolom CUT-ALL dan HOLD hampir simetris di dua ujung, cut-all itu TARUHAN ARAH, "
          "bukan perlindungan modal. Opsi tengah menang di dua tail -> itu yang direkomendasikan.")


if __name__ == "__main__":
    main()
