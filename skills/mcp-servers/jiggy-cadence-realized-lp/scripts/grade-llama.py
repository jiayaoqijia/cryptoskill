import json, sys, urllib.request, statistics, datetime

KEY = sys.argv[1]
UNI = "https://gateway.thegraph.com/api/" + KEY + "/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

def gq(query, timeout=120):
    req = urllib.request.Request(UNI, data=json.dumps({"query": query}).encode(),
                                 headers={"content-type": "application/json", "user-agent": "curl/8.5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def get(u, t=60):
    req = urllib.request.Request(u, headers={"user-agent": "curl/8.5.0"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return json.loads(r.read())

def il_pct(r):
    if r is None or r <= 0: return None
    return (2 * (r ** 0.5) / (1 + r) - 1) * 100

print("=" * 66)
print("STEP 1 — CAN we grade past predictions at all?")
print("=" * 66)
# Their /pools is a live snapshot. /chart/<id> is the only history endpoint.
pid = "fc9f488e-8183-416f-a61e-4e5c571d4395"
chart = get("https://yields.llama.fi/chart/" + pid)["data"]
keys = sorted(chart[-1].keys())
has_pred = any("predict" in k.lower() or "confidence" in k.lower() for k in keys)
print("  chart history rows      :", len(chart))
print("  chart row fields        :", keys)
print("  historical predictions? :", has_pred)
print()
print("  VERDICT: predictions are a LIVE SNAPSHOT ONLY. There is no public archive")
print("  of what DefiLlama predicted on any past date, so a retrospective hit-rate")
print("  CANNOT be computed. Anyone claiming one is reconstructing, not grading.")

print()
print("=" * 66)
print("STEP 2 — the test that IS possible today: what do they predict ABOUT?")
print("=" * 66)
print("  predictedClass forecasts the direction of `apy`.")
print("  `apy` for uniswap-v3 pools = apyBase = FEE yield. No price term.")
print("  So: even a PERFECT apy-direction call says nothing about LP outcome")
print("  unless apy direction actually tracks realized return. Test that ceiling.")
print()

d = gq('''{ pools(first: 150, orderBy: volumeUSD, orderDirection: desc,
        where: { totalValueLockedUSD_gt: "1000000" }) {
    id token0 { symbol } token1 { symbol }
    poolDayData(first: 180, orderBy: date, orderDirection: desc) {
        date volumeUSD feesUSD tvlUSD token0Price
    }
} }''')
pools = d.get("data", {}).get("pools", [])
STABLES = {"USDC","USDT","DAI","FRAX","LUSD","TUSD","USDS","USDE","GUSD","BUSD","PYUSD","USDP","crvUSD"}

rows = []
for p in pools:
    days = p.get("poolDayData") or []
    if len(days) < 120: continue
    s0, s1 = p["token0"]["symbol"], p["token1"]["symbol"]
    if s0 in STABLES and s1 in STABLES: continue
    days = list(reversed(days))
    prices_all = [float(x["token0Price"] or 0) for x in days if float(x["token0Price"] or 0) > 0]
    if len(prices_all) < 5: continue
    if prices_all[-1] / max(prices_all) < 0.05: continue   # collapse filter
    for t in range(7, len(days) - 30, 15):
        origin, horizon, trailing = days[t], days[t:t+30], days[t-7:t]
        tvl0 = float(origin["tvlUSD"] or 0)
        vol7 = sum(float(x["volumeUSD"] or 0) for x in trailing)
        active = sum(1 for x in trailing if float(x["feesUSD"] or 0) > 0)
        if tvl0 < 250_000 or vol7 < 50_000 or active < 6: continue
        p0 = float(origin["token0Price"] or 0); p1 = float(horizon[-1]["token0Price"] or 0)
        if p0 <= 0 or p1 <= 0: continue
        ratio = p1 / p0
        if not (0.01 < ratio < 100): continue
        il = il_pct(ratio)
        if il is None: continue
        # apy at origin (fee-only, annualized) and apy at horizon end
        apy0 = (float(origin["feesUSD"] or 0) / tvl0) * 365 * 100
        tvlN = float(horizon[-1]["tvlUSD"] or 0)
        if tvlN <= 0: continue
        apyN = (float(horizon[-1]["feesUSD"] or 0) / tvlN) * 365 * 100
        fees = sum(float(x["feesUSD"] or 0) for x in horizon)
        realized = ((fees / tvl0) * 100 + il) / 30 * 365
        rows.append({"pair": f"{s0}/{s1}", "apy0": apy0, "apyN": apyN,
                     "apy_up": apyN > apy0, "realized": realized, "profit": realized > 0})

n = len(rows)
print(f"  forecast windows built from Graph history: {n}")
if n:
    apy_up   = [r for r in rows if r["apy_up"]]
    apy_down = [r for r in rows if not r["apy_up"]]
    def wr(g): return 100 * sum(1 for r in g if r["profit"]) / len(g) if g else float("nan")
    print()
    print("  If you had PERFECT foresight of DefiLlama's target variable (apy direction):")
    print(f"    apy went UP   (n={len(apy_up):4d}) -> LP actually profited {wr(apy_up):5.1f}% of the time")
    print(f"    apy went DOWN (n={len(apy_down):4d}) -> LP actually profited {wr(apy_down):5.1f}% of the time")
    print(f"    base rate     (n={n:4d}) -> LP profited {wr(rows):5.1f}% of the time")
    edge = wr(apy_up) - wr(apy_down)
    print(f"    EDGE from a perfect apy-direction call: {edge:+.1f} percentage points")

    # correlation between apy change and realized return
    dapy = [r["apyN"] - r["apy0"] for r in rows]
    real = [r["realized"] for r in rows]
    m1, m2 = statistics.mean(dapy), statistics.mean(real)
    cov = sum((a - m1) * (b - m2) for a, b in zip(dapy, real)) / n
    s1_, s2_ = statistics.pstdev(dapy), statistics.pstdev(real)
    corr = cov / (s1_ * s2_) if s1_ and s2_ else float("nan")
    print(f"    corr(apy change, realized return) = {corr:+.3f}")

print()
print("=" * 66)
print("STEP 3 — start the clock: snapshot today's predictions so they CAN be graded")
print("=" * 66)
pools_ll = get("https://yields.llama.fi/pools")["data"]
snap = [{"pool": p["pool"], "project": p["project"], "chain": p["chain"], "symbol": p["symbol"],
         "tvlUsd": p["tvlUsd"], "apy": p["apy"], "apyBase": p.get("apyBase"),
         "predictedClass": p["predictions"]["predictedClass"],
         "predictedProbability": p["predictions"]["predictedProbability"],
         "binnedConfidence": p["predictions"]["binnedConfidence"]}
        for p in pools_ll if p.get("predictions", {}).get("predictedClass")]
out = {"snapshotAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "source": "https://yields.llama.fi/pools",
       "note": "DefiLlama publishes no prediction archive. This snapshot is the t0 needed to grade them forward.",
       "count": len(snap), "predictions": snap}
path = "/home/ubuntu/.openclaw/workspace/projects/ethonline2026-graph-agent/data/llama-predictions-t0.json"
with open(path, "w") as f: json.dump(out, f, indent=2)
print(f"  snapshotted {len(snap)} live predictions -> data/llama-predictions-t0.json")
from collections import Counter
print("  class split:", Counter(s["predictedClass"] for s in snap).most_common())
uni_ = [s for s in snap if s["project"] == "uniswap-v3" and s["chain"] == "Ethereum"]
print(f"  uniswap-v3 ethereum (gradeable against our Graph instrument): {len(uni_)}")
