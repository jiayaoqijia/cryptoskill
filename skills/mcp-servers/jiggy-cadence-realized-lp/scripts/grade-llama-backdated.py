import json, gzip, urllib.request, statistics, os, time, datetime
from collections import Counter, defaultdict

UA = {"user-agent": "curl/8.5.0"}
CACHE = "/tmp/wbcache"
os.makedirs(CACHE, exist_ok=True)

def fetch(url, timeout=120, cache_key=None):
    if cache_key:
        p = os.path.join(CACHE, cache_key)
        if os.path.exists(p) and os.path.getsize(p) > 200:
            return open(p, "rb").read()
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    if cache_key:
        open(os.path.join(CACHE, cache_key), "wb").write(raw)
    return raw

print("=" * 70)
print("STEP 1 - full CDX inventory of archived /pools snapshots")
print("=" * 70)
cdx = json.loads(fetch(
    "http://web.archive.org/cdx/search/cdx?url=yields.llama.fi/pools&output=json&filter=statuscode:200",
    cache_key="cdx_full.json"))
hdr, rows = cdx[0], cdx[1:]
stamps = sorted({r[1] for r in rows})
print(f"  archived 200-OK captures: {len(rows)}  (distinct timestamps: {len(stamps)})")
print(f"  earliest: {stamps[0]}   latest: {stamps[-1]}")
by_year = Counter(s[:4] for s in stamps)
print("  by year:", dict(sorted(by_year.items())))

# Pick snapshots: >=35 days old (so a 30d outcome exists), spread out, one per ~45 days
def as_dt(s):
    return datetime.datetime.strptime(s, "%Y%m%d%H%M%S").replace(tzinfo=datetime.timezone.utc)

now = datetime.datetime.now(datetime.timezone.utc)
picked = []
for s in stamps:
    d = as_dt(s)
    if (now - d).days < 40:
        continue
    if picked and (d - as_dt(picked[-1])).days < 45:
        continue
    picked.append(s)
print(f"\n  selected {len(picked)} snapshots >=40d old, >=45d apart:")
for s in picked:
    print("   ", as_dt(s).date().isoformat())

print()
print("=" * 70)
print("STEP 2 - load each snapshot, collect its predictions")
print("=" * 70)
snaps = {}
for s in picked:
    try:
        raw = fetch(f"http://web.archive.org/web/{s}id_/https://yields.llama.fi/pools",
                    timeout=180, cache_key=f"pools_{s}.json")
        data = json.loads(raw).get("data", [])
    except Exception as e:
        print(f"  {s}: FETCH FAIL {type(e).__name__}")
        continue
    preds = {}
    for p in data:
        pr = p.get("predictions") or {}
        if not pr.get("predictedClass"):
            continue
        preds[p["pool"]] = {
            "cls": pr["predictedClass"], "prob": pr.get("predictedProbability"),
            "conf": pr.get("binnedConfidence"), "apy": p.get("apy"),
            "tvl": p.get("tvlUsd"), "project": p.get("project"),
            "chain": p.get("chain"), "symbol": p.get("symbol"),
        }
    snaps[s] = preds
    print(f"  {as_dt(s).date()}  pools={len(data):6d}  with predictions={len(preds):6d}")

# Choose pools to grade: high-TVL ones present in the most snapshots (bounded chart fetches)
score = defaultdict(float)
seen_in = Counter()
for s, preds in snaps.items():
    for pid, v in preds.items():
        if (v["tvl"] or 0) >= 1_000_000:
            seen_in[pid] += 1
            score[pid] += (v["tvl"] or 0) ** 0.5
target = [pid for pid, _ in sorted(score.items(), key=lambda kv: -kv[1]) if seen_in[pid] >= 2][:260]
print(f"\n  grading universe: {len(target)} pools (TVL>=$1M, present in >=2 snapshots)")

print()
print("=" * 70)
print("STEP 3 - pull each pool's ACTUAL apy history (ground truth)")
print("=" * 70)
hist = {}
fails = 0
for i, pid in enumerate(target):
    try:
        raw = fetch(f"https://yields.llama.fi/chart/{pid}", timeout=60, cache_key=f"chart_{pid}.json")
        rows_ = json.loads(raw).get("data", [])
        series = []
        for r in rows_:
            ts = r.get("timestamp")
            a = r.get("apy")
            if ts and a is not None:
                series.append((ts[:10], float(a)))
        if len(series) > 40:
            hist[pid] = series
    except Exception:
        fails += 1
    if (i + 1) % 60 == 0:
        print(f"    fetched {i+1}/{len(target)} (usable {len(hist)}, fail {fails})")
    time.sleep(0.05)
print(f"  usable apy histories: {len(hist)} / {len(target)}  (fetch failures {fails})")

def apy_on(series, target_date, tol_days=4):
    best, bestgap = None, 999
    for d, a in series:
        gap = abs((datetime.date.fromisoformat(d) - target_date).days)
        if gap < bestgap:
            best, bestgap = a, gap
    return best if bestgap <= tol_days else None

print()
print("=" * 70)
print("STEP 4 - GRADE: was each prediction right about apy direction 30d later?")
print("=" * 70)
HORIZON = 30
BANDS = [("strict  (0% band)", 0.0), ("mid     (5% band)", 0.05), ("loose  (10% band)", 0.10)]

graded = []
for s, preds in snaps.items():
    d0 = as_dt(s).date()
    d1 = d0 + datetime.timedelta(days=HORIZON)
    if (now.date() - d1).days < 0:
        continue
    for pid, v in preds.items():
        if pid not in hist:
            continue
        a0 = apy_on(hist[pid], d0)
        a1 = apy_on(hist[pid], d1)
        if a0 is None or a1 is None or a0 <= 0:
            continue
        graded.append({"snap": d0.isoformat(), "pid": pid, "cls": v["cls"], "conf": v["conf"],
                       "prob": v["prob"], "a0": a0, "a1": a1, "chg": (a1 - a0) / a0,
                       "project": v["project"], "symbol": v["symbol"], "tvl": v["tvl"]})
print(f"  graded prediction-instances: {len(graded)}")
if not graded:
    raise SystemExit("no gradeable instances")

print(f"  distinct snapshots: {len(set(g['snap'] for g in graded))}")
print(f"  distinct pools    : {len(set(g['pid'] for g in graded))}")
print(f"  class split       : {dict(Counter(g['cls'] for g in graded))}")

def grade(band):
    hits = tot = 0
    per_cls = defaultdict(lambda: [0, 0])
    for g in graded:
        if g["chg"] > band:
            actual = "Stable/Up"
        elif g["chg"] < -band:
            actual = "Down"
        else:
            actual = "Stable/Up"          # flat counts as stable -> matches "Stable/Up"
        ok = (g["cls"] == actual)
        hits += ok; tot += 1
        per_cls[g["cls"]][0] += ok; per_cls[g["cls"]][1] += 1
    return hits, tot, per_cls

print()
print("  ACCURACY (reported at 3 bands - a finding must survive the knob):")
print(f"  {'band':<20}{'n':>7}{'accuracy':>11}{'  Down acc':>12}{'  Up acc':>11}")
accs = []
for label, band in BANDS:
    hits, tot, per_cls = grade(band)
    acc = 100 * hits / tot
    accs.append(acc)
    dn = per_cls.get("Down", [0, 0]); up = per_cls.get("Stable/Up", [0, 0])
    dnacc = 100 * dn[0] / dn[1] if dn[1] else float("nan")
    upacc = 100 * up[0] / up[1] if up[1] else float("nan")
    print(f"  {label:<20}{tot:>7}{acc:>10.1f}%{dnacc:>11.1f}%{upacc:>10.1f}%")

print()
print("  BASELINES (the number that decides if the model has skill):")
_, tot, _ = grade(0.05)
maj = Counter()
for g in graded:
    maj["Stable/Up" if g["chg"] > 0.05 or abs(g["chg"]) <= 0.05 else "Down"] += 1
base = 100 * max(maj.values()) / sum(maj.values())
print(f"    always-guess-majority-class : {base:.1f}%   (majority = {maj.most_common(1)[0][0]})")
print(f"    model (5% band)             : {accs[1]:.1f}%")
print(f"    EDGE over always-guessing   : {accs[1]-base:+.1f} pts")

print()
print("  BY STATED CONFIDENCE (does higher confidence mean more accurate?):")
print(f"  {'binnedConfidence':<20}{'n':>7}{'accuracy':>11}")
for conf in sorted({g["conf"] for g in graded if g["conf"] is not None}):
    sub = [g for g in graded if g["conf"] == conf]
    hits = 0
    for g in sub:
        actual = "Down" if g["chg"] < -0.05 else "Stable/Up"
        hits += (g["cls"] == actual)
    print(f"  {conf:<20}{len(sub):>7}{100*hits/len(sub):>10.1f}%")

print()
print("  CANARY - can this harness detect a KNOWN-GOOD and KNOWN-BAD predictor?")
for name, fn in [("oracle (peeks at truth)", lambda g: "Down" if g["chg"] < -0.05 else "Stable/Up"),
                 ("inverted oracle       ", lambda g: "Stable/Up" if g["chg"] < -0.05 else "Down")]:
    hits = sum(1 for g in graded if fn(g) == ("Down" if g["chg"] < -0.05 else "Stable/Up"))
    print(f"    {name}: {100*hits/len(graded):5.1f}%")
print("    ^ oracle must be ~100% and inverted ~0% or the grader itself is broken")

out = {"gradedAt": now.isoformat(),
       "method": "Wayback-archived yields.llama.fi/pools snapshots -> DefiLlama's own live chart apy history 30d later",
       "snapshots": sorted(set(g["snap"] for g in graded)),
       "n": len(graded), "accuracyByBand": {l: a for (l, _), a in zip(BANDS, accs)},
       "majorityBaseline": base, "instances": graded[:4000]}
p = "/home/ubuntu/.openclaw/workspace/projects/ethonline2026-graph-agent/data/llama-grade-backdated.json"
json.dump(out, open(p, "w"), indent=2)
print(f"\n  wrote {p}")
