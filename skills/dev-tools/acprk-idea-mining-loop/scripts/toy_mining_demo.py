#!/usr/bin/env python3
# TOY: not secure -- didactic walk-through of the idea-mining loop on a public textbook fact.
"""toy_mining_demo.py -- the 8-step idea-mining loop, end to end, on a toy problem.

Problem (Step 0, probe-able bottleneck): an SPN needs a *bijective* S-box.  For power permutations
F(x) = x^e over GF(2^n) (gcd(e, 2^n - 1) = 1), what is the differential uniformity
delta(F) = max_{a!=0,b} #{x : F(x+a) + F(x) = b}?  Lower is better (resistance to differential
cryptanalysis).  Baseline: the AES-style inverse map e = 2^n - 2.

The loop rediscovers a classical result (Gold exponents: delta(x^(2^k+1)) = 2^gcd(k,n)) and the
optimality bound delta >= 2, and it shows the two gates and the control experiment in action.
Everything here is public textbook material; the point is the *procedure*, not the result.

Run:  python3 toy_mining_demo.py            (n = 5..9, a few seconds)
      python3 toy_mining_demo.py --n 5 9    (range of field sizes)
      python3 toy_mining_demo.py --selftest
"""
from __future__ import annotations

import argparse
import math
import sys
from collections import Counter

# primitive polynomials (bit masks incl. x^n) for GF(2^n)
PRIM = {3: 0b1011, 4: 0b10011, 5: 0b100101, 6: 0b1000011, 7: 0b10000011,
        8: 0b100011101, 9: 0b1000010001, 10: 0b10000001001}


class GF2n:
    def __init__(self, n: int):
        self.n, self.q = n, 1 << n
        self.exp = [0] * (2 * self.q)
        self.log = [0] * self.q
        x = 1
        for i in range(self.q - 1):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & self.q:
                x ^= PRIM[n]
        for i in range(self.q - 1, 2 * self.q):
            self.exp[i] = self.exp[i - (self.q - 1)]

    def mul(self, a: int, b: int) -> int:           # generic multiply (used for re-verification)
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= PRIM[self.n]
        return r

    def power_table(self, e: int) -> list[int]:     # fast path via log tables
        m = self.q - 1
        return [0 if x == 0 else self.exp[(self.log[x] * e) % m] for x in range(self.q)] if e else [1] * self.q


def delta_power_fast(F: GF2n, e: int) -> int:
    """For power maps every row a != 0 of the DDT is a permutation of row a = 1."""
    T = F.power_table(e)
    return max(Counter(T[x ^ 1] ^ T[x] for x in range(F.q)).values())


def delta_generic(F: GF2n, e: int) -> int:
    """Independent re-verification: full DDT, square-and-multiply powering, no log tables."""
    def pw(x, k):
        r, b = 1, x
        while k:
            if k & 1:
                r = F.mul(r, b)
            b = F.mul(b, b)
            k >>= 1
        return r
    T = [pw(x, e) for x in range(F.q)]
    best = 0
    for a in range(1, F.q):
        best = max(best, max(Counter(T[x ^ a] ^ T[x] for x in range(F.q)).values()))
    return best


def cyclotomic_rep(e: int, n: int) -> int:
    m = (1 << n) - 1
    return min((e << i) % m for i in range(n)) if e % m else 0


def gold_k(e: int, n: int) -> int | None:
    """Return k if e is cyclotomic-equivalent to 2^k + 1 (1 <= k < n), else None."""
    rep = cyclotomic_rep(e, n)
    for k in range(1, n):
        if cyclotomic_rep((1 << k) + 1, n) == rep:
            return k
    return None


def loop(n_range, verbose=True) -> dict:
    say = print if verbose else (lambda *a, **k: None)
    summary = {}
    for n in n_range:
        F = GF2n(n)
        m = (1 << n) - 1
        say(f"\n=== GF(2^{n}) ===")
        # Step 1 (cheap probe): the baseline
        base = delta_power_fast(F, m - 1)
        say(f"Step 1  probe: delta(x^-1) = {base}   (baseline, inverse map)")
        # Gate 0 (security-bearing?): an S-box is a design object we are free to choose; the attack
        # model (differential cryptanalysis) is public -> not a hidden-structure trap. Proceed.
        # Step 2/Gate A: the "hidden fixed parameter" is the exponent e (textbooks show e = 3).
        # Step 3 sweep, one representative per cyclotomic class (cheap equivalence filter)
        reps = sorted({cyclotomic_rep(e, n) for e in range(1, m) if math.gcd(e, m) == 1} - {0, 1})
        table = {e: delta_power_fast(F, e) for e in reps}
        say(f"Step 3  swept {len(reps)} cyclotomic classes of permutation exponents (e ~ 1 excluded)")
        # Step 4: exact values re-verified by an independent code path (sample incl. all APN hits)
        apn = [e for e, d in table.items() if d == 2]
        if not apn:
            dmin = min(table.values())
            say(f"Gate B  delta distribution: {dict(sorted(Counter(table.values()).items()))}")
            say(f"Gate B  FAILED honestly: best power permutation has delta={dmin} = baseline {base}; "
                "no anomaly -> record the negative result, go back to Step 2 (free another parameter, "
                "e.g. leave the power-map family)")
            summary[n] = {"baseline": base, "apn": [], "h1": None, "residue": [], "controls": [],
                          "min_delta": dmin, "gate_b": False}
            continue
        sample = apn + reps[:: max(1, len(reps) // 6)]
        for e in sample:
            assert delta_generic(F, e) == table[e], f"fast/generic mismatch at e={e}"
        say(f"Step 4  re-verified {len(set(sample))} values with an independent generic DDT: OK")
        # Gate B: anomaly = values far below the typical delta
        dist = Counter(table.values())
        say(f"Gate B  delta distribution over classes: {dict(sorted(dist.items()))}")
        say(f"        anomalies (delta = 2, APN): exponents {apn}")
        # Step 5: algebraic hypothesis. Naive H0: 'Hamming weight 2 => APN'. Refined H1: Gold.
        hw2 = [e for e in reps if bin(e).count('1') == 2]  # surface feature shared by e = 3, 5, 9, ...
        h0_fail = [e for e in hw2 if table[e] != 2]
        gold_pred = {e: 1 << math.gcd(gold_k(e, n), n) for e in reps if gold_k(e, n)}
        h1_ok = all(table[e] == d for e, d in gold_pred.items())
        say(f"Step 5  H0 'HW(e)=2 => APN' fails on {h0_fail or 'nothing'};"
            f"  H1 'delta(x^(2^k+1)) = 2^gcd(k,n)' holds on all {len(gold_pred)} Gold classes: {h1_ok}")
        # Step 6: control experiment -- same surface feature (HW = 2), different algebra (gcd > 1)
        controls = [e for e in gold_pred if math.gcd(gold_k(e, n), n) > 1]
        if controls:
            e = controls[0]
            say(f"Step 6  control e={e} (=2^{gold_k(e, n)}+1 class, HW 2, gcd>1): delta={table[e]}"
                f" -> anomaly disappears, 'HW 2' was the naive explanation")
        else:
            say("Step 6  no Gold permutation with gcd(k,n)>1 for this n; the control must be run at another n "
                "(see n = 9: e = 2^3+1)")
        # Residue that H1 does not explain -> honest open list (Kasami, Welch, inverse ...)
        residue = [e for e in apn if e not in gold_pred]
        say(f"        APN classes NOT explained by H1 (next loop iteration): {residue or 'none'}")
        # Step 7: "real system" metric. In MPC/FHE-friendly ciphers the cost is the number of
        # NON-LINEAR multiplications; squaring is GF(2)-linear, so x^e costs HW(e) - 1 of them
        # (square-and-multiply). Report delta AND cost -- never only the ratio that looks good.
        best_e = min(table, key=lambda e: (table[e], bin(e).count("1"), e))
        cost = lambda e: bin(e).count("1") - 1
        say(f"Step 7  2-round trail bound (delta/2^n)^2: baseline x^-1 {(base / F.q) ** 2:.2e}, "
            f"best x^{best_e} {(table[best_e] / F.q) ** 2:.2e};  non-linear mults: {cost(m - 1)} vs "
            f"{cost(best_e)}")
        # Step 8: lower bound -- in characteristic 2, x and x+a solve the same equation -> delta >= 2
        say("Step 8  lower bound: delta >= 2 always (solutions come in pairs {x, x+a}); "
            f"APN exponents are optimal. Generalisation 2^gcd(k,n) verified for n={n}.")
        summary[n] = {"baseline": base, "apn": apn, "h1": h1_ok, "residue": residue,
                      "controls": controls, "min_delta": min(table.values()), "gate_b": True}
    return summary


def selftest() -> int:
    s = loop(range(5, 10), verbose=False)
    assert all(v["min_delta"] >= 2 for v in s.values())            # Step 8 bound
    assert s[6]["gate_b"] is False and s[6]["baseline"] == 4          # even n: no APN power permutation here
    assert s[5]["gate_b"] and s[7]["gate_b"] and s[9]["gate_b"] and s[5]["baseline"] == 2
    assert all(v["h1"] for v in s.values() if v["gate_b"])
    assert 9 in s[9]["controls"], s[9]["controls"]                     # 2^3+1 with gcd(3,9)=3 -> delta 8
    print("selftest: OK")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", nargs=2, type=int, default=[5, 9], metavar=("NMIN", "NMAX"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not (3 <= a.n[0] <= a.n[1] <= 10):
        ap.error("n must be within 3..10")
    loop(range(a.n[0], a.n[1] + 1))
