#!/usr/bin/env python3
"""Scoreboard PERFORMANCE per tema narasi -> /tmp/narr_perf.json + tabel teks.

Bedanya sama narr_audit.py: ini performa TIAP TEMA (r1/r3/r7/r14/r30 + alpha vs BTC,
beta/resid, breadth, volratio), bukan audit akurasi screener.

Impor modul detektor (narrative_rotation_early.py) supaya bucket tema SATU sumber —
jangan tulis definisi tema kedua di sini.

Pakai: python3 narr_perf.py [hari]   (default 120)
Dump /tmp/narr_perf.json dikonsumsi ~/.hermes/scripts/diag/make_narr_perf_chart.py.
Kunci `btc` harus BERNama (r7, bukan int 7) — chart script baca D['btc']['r7'].
"""
import importlib.util
import json
import os
import sys

S = os.path.expanduser("~/.hermes/scripts/narrative_rotation_early.py")
spec = importlib.util.spec_from_file_location("nre", S)
nre = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nre)

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 120
hist = json.load(open(os.path.join(nre.DATA, "narr_hist_cache.json")))
ts, M, out = nre.build(hist, DAYS)
i = len(ts) - 1
btc = M.get("BTC", {})


def btc_r(w):
    a, b = btc.get(ts[i - w]), btc.get(ts[i])
    if not a or not b or a[0] <= 0:
        return None
    return b[0] / a[0] - 1


def sym_r(sym, w):
    a, b = M.get(sym, {}).get(ts[i - w]), M.get(sym, {}).get(ts[i])
    if not a or not b or a[0] <= 0:
        return None
    return b[0] / a[0] - 1


def beta60(ret, w=60):
    xs, ys = [], []
    for j in range(max(1, i - w + 1), i + 1):
        r = ret[j]
        b, b0 = btc.get(ts[j]), btc.get(ts[j - 1])
        if r is None or not b or not b0 or b0[0] <= 0:
            continue
        xs.append(b[0] / b0[0] - 1)
        ys.append(r)
    if len(xs) < 20:
        return None
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    var = sum((x - mx) ** 2 for x in xs) / (len(xs) - 1)
    if not var:
        return None
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)
    return cov / var


def breadth(mem, w):
    up = n = 0
    for s in mem:
        r = sym_r(s, w)
        if r is None:
            continue
        n += 1
        if r > 0:
            up += 1
    return (up / n) if n else None


def volratio(vv, short=7, long=30):
    sv = [x for x in vv[max(0, i - long + 1):i + 1] if x]
    if len(sv) < 10:
        return None
    s7 = sum(sv[-short:]) / min(short, len(sv))
    s30 = sum(sv) / len(sv)
    return (s7 / s30) if s30 else None


B = {w: btc_r(w) for w in (1, 3, 7, 14, 30)}
rows = []
for th, td in out.items():
    ret, mem = td["ret"], td["members"]
    r = {w: nre.cum(ret, i, w) for w in (1, 3, 7, 14, 30)}
    if r[1] is None or r[3] is None:
        continue
    b = beta60(ret)
    exp7 = (b * B[7]) if (b is not None and B[7] is not None) else None
    members = [(s, sym_r(s, 7), sym_r(s, 1)) for s in mem]
    members7 = [m for m in members if m[1] is not None]
    members7.sort(key=lambda x: -x[1])
    m1 = [m for m in members if m[2] is not None]
    m1.sort(key=lambda x: -x[2])
    rows.append({
        "th": th, "n": len(mem),
        "r1": r[1], "r3": r[3], "r7": r[7], "r14": r[14], "r30": r[30],
        "a1": (r[1] - B[1]) if B[1] is not None else None,
        "a3": (r[3] - B[3]) if B[3] is not None else None,
        "a7": (r[7] - B[7]) if (r[7] is not None and B[7] is not None) else None,
        "a30": (r[30] - B[30]) if (r[30] is not None and B[30] is not None) else None,
        "beta60": b, "exp7": exp7,
        "resid7": (r[7] - exp7) if (r[7] is not None and exp7 is not None) else None,
        "breadth1": breadth(mem, 1), "breadth7": breadth(mem, 7),
        "volratio7": volratio(td["vol"]),
        "top3": [(m[0], m[1]) for m in members7[:3]],
        "bot3": [(m[0], m[1]) for m in members7[-3:]][::-1],
        "best24": (m1[0][0], m1[0][2]) if m1 else None,
        "worst24": (m1[-1][0], m1[-1][2]) if m1 else None,
    })

ms = lambda x: "  n/a" if x is None else f"{x*100:+7.2f}%"
rows.sort(key=lambda x: -(x["r7"] if x["r7"] is not None else -9))

print(f"KALENDER: candle terakhir={ts[i]}  sebelumnya={ts[i-1]}  ({len(ts)} hari, base {DAYS})")
print(f"BTC: 24j {ms(B[1])} · 3d {ms(B[3])} · 7d {ms(B[7])} · 14d {ms(B[14])} · 30d {ms(B[30])}")
print(f"{'tema':<12}{'r1':>9}{'r3':>9}{'r7':>9}{'r14':>9}{'r30':>9}{'a7':>9}{'beta':>7}{'resid7':>9}{'brd7':>7}{'vol7':>7}")
for x in rows:
    bb = "  n/a" if x["beta60"] is None else f"{x['beta60']:7.2f}"
    bd = "  n/a" if x["breadth7"] is None else f"{x['breadth7']*100:6.0f}%"
    vr = "  n/a" if x["volratio7"] is None else f"{x['volratio7']:6.2f}x"
    print(f"{x['th']:<12}{ms(x['r1'])}{ms(x['r3'])}{ms(x['r7'])}{ms(x['r14'])}{ms(x['r30'])}"
          f"{ms(x['a7'])}{bb}{ms(x['resid7'])}{bd}{vr}")

print("\nANGGOTA (r7 terbaik / terburuk):")
for x in rows:
    t = ", ".join(f"{s} {v*100:+.1f}%" for s, v in x["top3"])
    b = ", ".join(f"{s} {v*100:+.1f}%" for s, v in x["bot3"])
    print(f"  {x['th']:<12} top: {t}")
    print(f"  {'':<12} bot: {b}")

n_beat = sum(1 for x in rows if (x["a7"] or 0) > 0)
n_struct = sum(1 for x in rows if (x["resid7"] is not None and x["resid7"] < -0.01 and (x["volratio7"] or 1) < 0.95))
print(f"\nRINGKAS: {len(rows)} tema · {n_beat} ngalahin BTC 7d · {n_struct} struktural (resid<0 & volume keluar)")

json.dump({"ts_last": ts[i], "ts_prev": ts[i - 1], "days": len(ts),
           "btc": {f"r{w}": B[w] for w in B}, "rows": rows},
          open("/tmp/narr_perf.json", "w"), indent=1)
print("dump: /tmp/narr_perf.json")
