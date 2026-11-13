#!/usr/bin/env python3
"""route_score.py: blind routing-eval scorer (subskills/routing-eval.md).

Stdlib only, no network,
no file writes. Pre-register it: record its sha256 in the run log BEFORE the
sealed router runs.

Usage: route_score.py ROUTES_MD LABELS_MD [--need GROUP=N ...] [--min-pct P]

Inputs:
  ROUTES_MD  the first table whose header is exactly
             | id | rsi_first | first | second | confidence | index_enough |
  LABELS_MD  rows | Txx | skill | expected | alternates |  (any count >= 1)

Rules:
  top-1 hit = `first` equals `expected` or is in `alternates`.
  Negatives (expected none) hit iff first is none; a bare '-' in `first`
  also counts as none (no leaf chosen). An empty `first` cell is an input error.
  Groups = each skill's content rows, plus `negatives`.
  Bars: --need GROUP=N sets an absolute top-1 bar for that group. A group
  without --need gets ceil(P% x n) for content (P = --min-pct, default 80)
  and ceil(75% x n) for negatives. Every group present in the labels is
  scored; a --need group absent from the labels is an input error.
  top-2 (first or second accepted) is reported, never counted toward PASS.
  A labelled id missing from the routes counts as a miss and is flagged.
  Duplicate ids (routes or labels) = input error.

Exit: 0 PASS, 1 FAIL, 2 input error.
"""
import math
import re
import sys

HDR = ["id", "rsi_first", "first", "second", "confidence", "index_enough"]
NEG_PCT = 75.0


def die(msg):
    print("input error:", msg)
    sys.exit(2)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def norm(x):
    x = x.strip().strip("`*").strip().lower()
    if x in ("", "-", "n/a", "na"):
        return "-"
    if x in ("none", "no leaf", "no-leaf", "(none)"):
        return "none"
    x = re.split(r"[\s(]", x)[0].strip("`*")
    x = x.split("/")[-1]
    return x if x.endswith(".md") else x + ".md"


def read_routes(path):
    out, on = {}, False
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not on:
            on = s.startswith("|") and [c.lower().strip("`* ") for c in cells(s)] == HDR
            continue
        if not s.startswith("|"):
            break
        c = cells(s)
        if all(re.fullmatch(r":?-+:?", x) for x in c if x):
            continue
        if len(c) < 6:
            die(f"short row: {s}")
        tid = c[0].strip("`* ")
        if not c[2].strip("`* "):
            die(f"empty first cell for {tid}")
        if tid in out:
            die(f"duplicate id {tid}")
        out[tid] = c
    if not out:
        die("routes table header not found")
    return out


def read_labels(path):
    """Labels come from the FIRST table whose header is exactly
    | id | skill | expected | alternates |. Any later `| Tnn |` table (alternate
    reasons, coverage notes) is prose, not labels, and must be ignored.
    """
    out, seen, on = {}, {}, False
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not on:
            on = (s.startswith("|") and [c.lower().strip("`* ") for c in cells(s)] ==
                  ["id", "skill", "expected", "alternates"])
            continue
        if not s.startswith("|"):
            break
        c = cells(s)
        if all(re.fullmatch(r":?-+:?", x) for x in c if x):
            continue
        if len(c) < 4:
            die(f"short label row: {s}")
        if c[0] in out:
            die(f"duplicate label id {c[0]}")
        exp = norm(c[2])
        if exp != "none" and seen.setdefault(exp, c[1]) != c[1]:
            die(f"leaf {exp} is expected under two skills; routes cannot tell them apart")
        alts = {norm(a) for a in re.split(r"[,;\s]+", c[3]) if norm(a) not in ("-", ".md")}
        out[c[0]] = (c[1], exp, alts)
    if not out:
        die("no label table found (need a header | id | skill | expected | alternates |)")
    return out


def parse_args(argv):
    pos, need, pct = [], {}, 80.0
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--need", "--min-pct"):
            if i + 1 >= len(argv):
                die(f"{a} needs a value")
            v = argv[i + 1]
            i += 2
        elif a.startswith("--need=") or a.startswith("--min-pct="):
            a, v = a.split("=", 1)
            i += 1
        elif a.startswith("--"):
            die(f"unknown flag {a}")
        else:
            pos.append(a)
            i += 1
            continue
        if a == "--need":
            m = re.fullmatch(r"([^=\s]+)=(\d+)", v)
            if not m:
                die(f"--need wants GROUP=N, got {v!r}")
            need[m.group(1)] = int(m.group(2))
        else:
            try:
                pct = float(v)
            except ValueError:
                die(f"--min-pct wants a number, got {v!r}")
            if not 80 <= pct <= 100:
                die("--min-pct must be in [80, 100]; bars only tighten")
    if len(pos) != 2:
        print(__doc__)
        sys.exit(2)
    return pos[0], pos[1], need, pct


def main():
    routes_p, labels_p, need, pct = parse_args(sys.argv[1:])
    R, L = read_routes(routes_p), read_labels(labels_p)
    known = {"negatives" if exp == "none" else skill for skill, exp, _ in L.values()}
    unknown = sorted(set(need) - known)
    if unknown:
        die(f"--need names group(s) not in labels: {unknown}; groups are {sorted(known)}")
    tally, conf = {}, {}
    print("| id | skill | expected | accepted alternates | first | second | top-1 | top-2 | confidence |")
    print("|---|---|---|---|---|---|---|---|---|")
    for tid in sorted(L):
        skill, exp, alts = L[tid]
        ok = {exp} | alts
        grp = "negatives" if exp == "none" else skill
        r = R.get(tid)
        if r:
            first, second, cf = norm(r[2]), norm(r[3]), r[4].strip("`* ").lower()
            if first == "-":
                first = "none"
        else:
            first, second, cf = "MISSING", "-", "-"
        t1 = first in ok
        t2 = t1 or second in ok
        a = tally.setdefault(grp, [0, 0, 0]); a[0] += 1; a[1] += t1; a[2] += t2
        b = conf.setdefault(cf, [0, 0]); b[0] += 1; b[1] += t1
        print(f"| {tid} | {skill} | {exp} | {', '.join(sorted(alts)) or '-'} | {first} | {second} | "
              f"{'HIT' if t1 else 'miss'} | {'HIT' if t2 else 'miss'} | {cf} |")
    small = [g for g, v in tally.items() if v[0] < 3]
    if small:
        print(f"\nflag: groups with < 3 rows (typo in skill column?): {small}")
    missing = sorted(set(L) - set(R))
    if missing:
        print(f"\nflag: labelled ids missing from routes (scored as miss): {missing}")
    extra = sorted(set(R) - set(L))
    if extra:
        print(f"\nflag: route ids with no label (ignored): {extra}")
    print("\n| group | top-1 | top-2 | threshold | verdict |\n|---|---|---|---|---|")
    ok_all = True
    groups = sorted(g for g in tally if g != "negatives") + (["negatives"] if "negatives" in tally else [])
    for g in groups:
        tot, h1, h2 = tally[g]
        if g in need:
            n, src = need[g], "need"
            if n < math.ceil((NEG_PCT if g == "negatives" else 80.0) / 100.0 * tot - 1e-9):
                die(f"--need {g}={n} is below the default bar; bars only tighten")
        else:
            p = NEG_PCT if g == "negatives" else pct
            n, src = math.ceil(p / 100.0 * tot - 1e-9), f"{p:g}%"
        v = h1 >= n
        ok_all &= v
        print(f"| {g} | {h1} of {tot} | {h2} of {tot} | >= {n} ({src}) | {'PASS' if v else 'FAIL'} |")
    if "negatives" not in tally:
        print("\nflag: no negatives in labels (routing-eval.md wants >= 4)")
    print("\nconfidence calibration (top-1 hits / rows): " + ", ".join(f"{k} {v[1]} of {v[0]}" for k, v in sorted(conf.items())))
    rsi = sum(1 for r in R.values() if r[1].strip("`* ").lower().startswith("y"))
    ie = sum(1 for r in R.values() if r[5].strip("`* ").lower().startswith("y"))
    print(f"rsi_first=yes: {rsi} of {len(R)}; index_enough=yes: {ie} of {len(R)}")
    print(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'}")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
