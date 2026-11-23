#!/usr/bin/env python3
"""Screen Meteora DLMM pools against the LP band and price a ticket.

Usage:
    python3 meteora_lp_scan.py 500                  # coverage for a $500 position
    python3 meteora_lp_scan.py 400 --pages 12 --top 20
    python3 meteora_lp_scan.py 500 --json           # machine-readable
    python3 meteora_lp_scan.py 500 --sol-price 124.11

Read-only: HTTP GETs only, signs nothing, no credentials.

Why this exists:
  DefiLlama `yields` omits most DLMM memecoin pools, so the pool table at dlmm.datapi.meteora.ag is the
  only source for fee/TVL in this band. Two traps that cost time: a bare urllib request gets HTTP 403
  (needs a User-Agent header), and sort_by/sort_key/order params return an EMPTY data list, so we
  paginate and sort client-side.

Decision rule (see references/lp-position-economics-2026-09.md):
  fee_24h_you_earn = pool_fee24h * (size / pool_tvl)
  round_trip_cost  = gas(0.008 SOL) + exit_slippage(2%) * size
  coverage         = fee_24h_you_earn / round_trip_cost      -> want >= 2.5
"""

import argparse
import json
import sys
import time
import urllib.request

API = "https://dlmm.datapi.meteora.ag/pools?page_size=100&page="
HDR = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
GAS_SOL = 0.008
EXIT_SLIPPAGE = 0.02
MIN_COVERAGE = 2.5


def num(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def fetch_pages(pages):
    pools = []
    for p in range(1, pages + 1):
        try:
            req = urllib.request.Request(API + str(p), headers=HDR)
            with urllib.request.urlopen(req, timeout=30) as resp:
                rows = json.load(resp).get("data", [])
        except Exception as exc:  # noqa: BLE001 - report and stop paging
            print(f"page {p} failed: {exc}", file=sys.stderr)
            break
        if not rows:
            break
        pools.extend(rows)
    return pools


def age_days(created):
    try:
        t = float(created)
    except (TypeError, ValueError):
        return 0.0
    if t > 1e12:  # milliseconds
        t /= 1000.0
    return (time.time() - t) / 86400.0


def rows_for(pools, min_tvl, max_tvl, min_vol, min_age):
    out = []
    for r in pools:
        tvl = num(r.get("tvl"))
        fees = r.get("fees") or {}
        vol = r.get("volume") or {}
        fee24 = num(fees.get("24h")) if isinstance(fees, dict) else 0.0
        vol24 = num(vol.get("24h")) if isinstance(vol, dict) else 0.0
        age = age_days(r.get("created_at"))
        if not (min_tvl <= tvl <= max_tvl) or vol24 < min_vol or age < min_age:
            continue
        tx = r.get("token_x") or {}
        ty = r.get("token_y") or {}
        out.append(
            {
                "pool": r.get("name"),
                "address": r.get("address"),
                "tvl": tvl,
                "fee24h": fee24,
                "fee_tvl_pct": (fee24 / tvl * 100) if tvl else 0.0,
                "vol24h": vol24,
                "turnover": (vol24 / tvl) if tvl else 0.0,
                "age_days": age,
                "token_x": {"symbol": tx.get("symbol"), "address": tx.get("address")},
                "token_y": {"symbol": ty.get("symbol"), "address": ty.get("address")},
            }
        )
    out.sort(key=lambda r: -r["fee_tvl_pct"])
    return out


def main():
    ap = argparse.ArgumentParser(description="Meteora DLMM LP screening + coverage")
    ap.add_argument("size", type=float, help="position size in USD")
    ap.add_argument("--pages", type=int, default=8, help="pages of 100 pools to fetch (default 8)")
    ap.add_argument("--min-tvl", type=float, default=50_000, help="band floor (engine: 50k)")
    ap.add_argument("--max-tvl", type=float, default=500_000, help="band ceiling (engine: 500k)")
    ap.add_argument("--min-vol", type=float, default=10_000, help="min 24h volume (engine: 10k)")
    ap.add_argument("--min-age", type=float, default=2.0, help="min pool age in days (engine: 48h)")
    ap.add_argument("--sol-price", type=float, default=124.11, help="SOL price for gas costing")
    ap.add_argument("--top", type=int, default=15, help="rows to print")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args()

    pools = fetch_pages(args.pages)
    band = rows_for(pools, args.min_tvl, args.max_tvl, args.min_vol, args.min_age)
    rt = GAS_SOL * args.sol_price + EXIT_SLIPPAGE * args.size

    for r in band:
        r["fee_earned_24h"] = r["fee24h"] * (args.size / r["tvl"]) if r["tvl"] else 0.0
        r["round_trip_cost"] = rt
        r["coverage"] = (r["fee_earned_24h"] / rt) if rt else 0.0
        r["clears_bar"] = r["coverage"] >= MIN_COVERAGE

    if args.json:
        print(json.dumps({"sampled": len(pools), "band": len(band),
                          "size": args.size, "round_trip_cost": rt, "pools": band}, indent=2))
        return

    need = MIN_COVERAGE * rt
    print(f"sampled {len(pools)} pools | band {len(band)} | size ${args.size:,.0f}")
    print(f"round-trip cost ${rt:,.2f} | need fee24h >= ${need:,.2f} "
          f"-> fee/TVL >= {need / args.size * 100:.2f}%")
    print(f"clearing {MIN_COVERAGE}x: {sum(1 for r in band if r['clears_bar'])} of {len(band)}\n")
    print(f"{'pool':22}{'TVL$':>10}{'fee/TVL%':>9}{'fee24h$':>10}{'vol24h$':>11}"
          f"{'age(d)':>7}{'turn':>6}{'coverage':>9}")
    for r in band[: args.top]:
        print(f"{str(r['pool'])[:21]:22}{r['tvl']:>10,.0f}{r['fee_tvl_pct']:>9.2f}"
              f"{r['fee24h']:>10,.0f}{r['vol24h']:>11,.0f}{r['age_days']:>7.1f}"
              f"{r['turnover']:>6.1f}{r['coverage']:>8.1f}x")
    print("\nreminders: cross-check top-10 holders + mint/freeze via `gmgn-cli token security`; "
          "keep the ticket <=1-2% of pool TVL; re-pull right before entering (data goes stale in hours).")


if __name__ == "__main__":
    main()
