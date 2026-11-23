#!/usr/bin/env python3
"""Revenue-divergence screen: which top-N tickers are priced behind their own revenue.

Outputs revenue yield (rev30 * 12 / mcap), 30d/7d price change, P/F and the
growth-vs-price gap. Keyless: CoinPaprika (prices/mcap) + DefiLlama (revenue).

Usage:
    python3 revenue_divergence_screen.py [--top 100] [--min-rev 500000] [--min-mcap 2e8]

Why not CoinGecko first: the free tier rate-limits per IP (429) and the crons on
this box share it. CoinPaprika answers 1000 tickers in one call with rank, mcap
and 1h/24h/7d/30d changes already attached.

Why the joins look fussy: /overview/fees rows carry no `symbol` and
`gecko_id: null`, so a symbol/id join matches nothing and reads as "no protocol
has revenue". Build name -> symbol from /protocols instead.
"""
import argparse
import json
import statistics
import urllib.request

HDR = {"User-Agent": "Mozilla/5.0 hermes-screen"}


def get(url, retry=4):
    for i in range(retry):
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=50) as r:
                return json.loads(r.read().decode())
        except Exception:
            if i == retry - 1:
                raise
            import time
            time.sleep(3 + i * 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=100)
    ap.add_argument("--min-rev", type=float, default=500_000, help="rev30 floor, USD")
    ap.add_argument("--min-mcap", type=float, default=2e8)
    ap.add_argument("--out", default="revenue_divergence.json")
    a = ap.parse_args()

    tickers = get("https://api.coinpaprika.com/v1/tickers?limit=1000")
    protos = get("https://api.llama.fi/protocols")
    rev = get("https://api.llama.fi/overview/fees"
              "?dataType=dailyRevenue&excludeTotalDataChart=true"
              "&excludeTotalDataChartBreakdown=true")
    print(f"paprika {len(tickers)} | protocols {len(protos)} | revenue rows {len(rev.get('protocols', []))}")

    name2sym = {}
    for p in protos:
        n = (p.get("name") or "").lower().strip()
        s = (p.get("symbol") or "").strip().lower()
        if n and s:
            name2sym.setdefault(n, s)

    by_sym, by_name = {}, {}
    for c in tickers:
        if not c.get("rank"):
            continue
        by_sym.setdefault((c.get("symbol") or "").lower(), []).append(c)
        by_name.setdefault((c.get("name") or "").lower().strip(), []).append(c)

    rows, best = [], {}
    for p in rev.get("protocols", []):
        nm = (p.get("name") or "").lower().strip()
        sym = (p.get("symbol") or "").lower().strip() or name2sym.get(nm, "")
        cands = by_sym.get(sym) or by_name.get(nm)
        if not cands:
            continue
        c = min(cands, key=lambda x: x.get("rank") or 10 ** 6)
        if (c.get("rank") or 999) > a.top:
            continue
        q = (c.get("quotes", {}) or {}).get("USD", {}) or {}
        mcap = q.get("market_cap") or 0
        r30 = p.get("total30d") or 0
        if mcap < a.min_mcap or r30 < a.min_rev:
            continue
        row = {
            "rank": c["rank"], "sym": (c.get("symbol") or "").upper(), "name": c.get("name"),
            "mcap": mcap, "px": q.get("price"),
            "ch24": q.get("percent_change_24h"),
            "ch7": q.get("percent_change_7d"), "ch30": q.get("percent_change_30d"),
            "vol24": q.get("volume_24h") or 0,
            "rev30": r30,
            "rev_ch30": p.get("change_30dover30d") or 0,
            "rev_yield": r30 * 12 / mcap * 100,
            "p_f": mcap / (r30 * 12),
        }
        # same protocol can appear as several adapters with wildly different
        # totals (a 0.00% row next to the real 27% one) -> keep the largest rev30
        key = nm
        if key not in best or row["rev30"] > best[key]["rev30"]:
            best[key] = row

    rows = sorted(best.values(), key=lambda r: -r["rev_yield"])
    if not rows:
        raise SystemExit("join kosong: cek struktur /overview/fees (field symbol hilang?) "
                         "atau naikkan --min-rev")

    print(f"join {len(rows)} protokol")
    print("%-4s %-7s %-22s %9s %7s %7s %7s %6s %7s" %
          ("rk", "sym", "name", "mcap$M", "ch30%", "ch7%", "yield%", "P/F", "revCh"))
    for r in rows[:25]:
        print("%-4s %-7s %-22s %9.0f %7.1f %7.1f %7.2f %6.1f %7.1f" % (
            r["rank"], r["sym"], (r["name"] or "")[:22], r["mcap"] / 1e6,
            r["ch30"] or 0, r["ch7"] or 0, r["rev_yield"], r["p_f"], r["rev_ch30"] or 0))

    # gap = revenue growth minus price change: positive = price trailing the business
    for r in rows:
        r["gap"] = (r["rev_ch30"] or 0) - (r["ch30"] or 0)
    top_gap = sorted(rows, key=lambda r: -r["gap"])[:10]
    print("\n-- gap terbesar (revCh30 - ch30) --")
    for r in top_gap:
        print(f"{r['sym']:7s} gap {r['gap']:7.1f}  revCh {r['rev_ch30']:7.1f}  ch30 {r['ch30'] or 0:7.1f}  yield {r['rev_yield']:5.2f}%")

    json.dump(rows, open(a.out, "w"), indent=1)
    print("\nsaved", a.out)


if __name__ == "__main__":
    main()
