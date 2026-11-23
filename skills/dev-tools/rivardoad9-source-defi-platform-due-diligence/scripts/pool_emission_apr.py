#!/usr/bin/env python3
"""Per-pool emission-APR probe for ve(3,3) / MetaDEX LP products.

Why this exists: on these DEXes the LP reward is a native-token EMISSION (fees go to veTOKEN
lockers), so the number that decides the verdict is computed, not displayed:
`epochEmissionUSD / poolTVL x periodsPerYear`, with period = one WEEK (x52, never x365).

Usage:
    python3 pool_emission_apr.py https://app.usenest.xyz/api/blaze/liquidity-pools [--weeks 1] [--top 20]

Rules learned the hard way (see references/nest-hyperevm-lp-2026-09.md for the worked case):
  * field names differ per protocol -> we try several aliases and REPORT what matched;
  * numeric fields are unit-scaled, not percentages (Nest `fee: 102400` == 0.102%) -> verify one
    known pool against the UI/docs before trusting the fee column;
  * pools with zero emissions must be surfaced: "no votes = no emissions" means an unvoted pool
    pays LPs nothing that epoch, and 34 of Nest's 70 pools were in that state;
  * read the reward field's OWNER. `curEpochEmissionRewardsUSD` is the LP side; swap fees on a
    MetaDEX belong to lockers and are a separate (0-for-LP) line;
  * cross-check against an independent source (DefiLlama `/summary/fees/<slug>`, third-party
    dashboard). A dashboard "APY" may be the fee APR that LPs do not receive -- resolve the layer,
    never average the two numbers.

Exit codes: 0 ok, 2 fetch/parse problem (treat unmapped fields as a coverage gap, not a verdict).
"""
import argparse
import json
import sys
import urllib.request

TVL_KEYS = ("tvlUSD", "tvlUsd", "tvl_usd", "tvl", "liquidityUSD")
VOL_KEYS = ("24hVolume", "volumeUSD", "volume_24h", "volume24h", "volumeUSD24h")
EMIT_KEYS = (
    "curEpochEmissionRewardsUSD", "epochEmissionRewardsUSD", "emissionRewardsUSD",
    "emissionsUSD", "rewardUSD", "gaugeRewardsUSD",
)
FEE_KEYS = ("fee", "feeTier", "feeRate")


def first(d, keys):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k], k
    return None, None


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def pair_name(p):
    for a, b in (("token0", "token1"), ("baseToken", "quoteToken")):
        try:
            def sym(t):
                return (t.get("basetoken") or t).get("symbol") or "?"
            return f"{sym(p[a])}/{sym(p[b])}"
        except Exception:
            continue
    return p.get("pair") or p.get("symbol") or p.get("id", "?")[:10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("api_url")
    ap.add_argument("--weeks", type=float, default=1.0, help="weeks per reward period (epoch=1)")
    ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()

    try:
        with urllib.request.urlopen(a.api_url, timeout=30) as r:
            data = json.load(r)
    except Exception as e:  # noqa: BLE001 - report, don't crash the DD session
        print(f"FETCH FAILED: {e}\n(coverage gap, not a verdict)")
        return 2

    pools = data if isinstance(data, list) else (data.get("data") or data.get("pools") or [])
    if not pools:
        print("no pools found in payload; keys seen:", list(data)[:20] if isinstance(data, dict) else type(data))
        return 2

    rows, seen = [], set()
    for p in pools:
        tvl, tk = first(p, TVL_KEYS)
        vol, _ = first(p, VOL_KEYS)
        em, ek = first(p, EMIT_KEYS)
        fee, _ = first(p, FEE_KEYS)
        for s in (tk, ek, "fee=" + str(fee)):
            seen.add(s)
        rows.append(dict(pair=pair_name(p), tvl=num(tvl), vol=num(vol), em=num(em), fee=num(fee)))
    rows.sort(key=lambda r: r["tvl"], reverse=True)

    periods = 52.0 / a.weeks
    print(f"matched fields -> tvl:{tk} volume:{first(pools[0], VOL_KEYS)[1]} emissions:{ek}")
    print(f"{'pool':22}{'TVL$':>13}{'vol24h$':>13}{'epochEmis$':>12}{'emisAPY%':>10}{'vol/TVL':>9}")
    for r in rows[: a.top]:
        apr = (r["em"] / r["tvl"] * periods * 100) if r["tvl"] else 0.0
        vtl = (r["vol"] / r["tvl"]) if r["tvl"] else 0.0
        print(f"{r['pair'][:21]:22}{r['tvl']:>13,.0f}{r['vol']:>13,.0f}{r['em']:>12,.0f}{apr:>10,.1f}{vtl:>9.2f}")

    tot = sum(r["tvl"] for r in rows)
    em_tot = sum(r["em"] for r in rows)
    zero = sum(1 for r in rows if r["em"] <= 0)
    print(f"\ntotal TVL ${tot:,.0f} | pools {len(rows)} | with emissions {len(rows)-zero} | ZERO-emission pools {zero}")
    if tot and em_tot:
        print(f"emissions ${em_tot:,.0f}/period  ->  top pool {rows[0]['pair']}: "
              f"{(rows[0]['em']/rows[0]['tvl']*periods*100 if rows[0]['tvl'] else 0):,.1f}% APR")
        print("DILUTION CHECK: annualised emissions as % of token mcap, and "
              "'one period of emissions / (24h token volume x 1 day)' -- quote both.")
        print(f"  user $250 in top pool -> pool share {250/rows[0]['tvl']*100:.5f}% -> "
              f"${rows[0]['em']*(250/rows[0]['tvl'])*periods:,.2f}/yr at CURRENT token price")
        print("  restate that APR at the 30d-AVERAGE token price before rating the product.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
