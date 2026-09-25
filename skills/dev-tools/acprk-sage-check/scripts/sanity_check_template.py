#!/usr/bin/env python3
"""sage-check template: exhaustive small-parameter checks of lemma statements.

Copy this file, replace STATEMENTS, and run:
    python3 sanity_check_template.py        (pure Python)
    sage -python sanity_check_template.py   (Sage available -> used for cross-checks)

Each statement is (ID, parameter iterator, hypothesis(params) -> bool,
conclusion(params) -> bool).  Output: one JSON line per statement.
Exit code 1 if any statement has a counterexample (so CI / agents notice).

Toy statements below are about roots of unity mod p -- replace them.
"""
from __future__ import annotations

import itertools
import json
import sys

try:  # guarded Sage import (SPEC: sage optional)
    from sage.all import GF, cyclotomic_polynomial  # type: ignore
    HAVE_SAGE = True
except Exception:  # pragma: no cover
    HAVE_SAGE = False


def primes(lo: int, hi: int):
    for n in range(max(2, lo), hi):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            yield n


def mult_order(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    k, x = 1, a
    while x != 1:
        x = x * a % p
        k += 1
    return k


def check(sid, params_iter, hypothesis, conclusion, max_cases=10 ** 7):
    cases = vacuous = 0
    for params in params_iter:
        if cases >= max_cases:
            break
        if not hypothesis(params):
            vacuous += 1
            continue
        cases += 1
        if not conclusion(params):
            return {"check": sid, "cases": cases, "passed": False, "counterexample": params}
    return {"check": sid, "cases": cases, "passed": cases > 0, "counterexample": None,
            "note": "VACUOUS: hypothesis never satisfied" if cases == 0 else f"{vacuous} param points excluded by hypothesis"}


# ---------------------------------------------------------------------------- statements
def s1_params():
    for p in primes(3, 400):
        for a in range(1, p):
            yield {"p": p, "a": a}


# S1 (true): a^2 = -1 mod p  =>  ord(a) = 4
S1 = ("S1: a^2=-1 mod p => ord_p(a)=4", s1_params(),
      lambda P: P["a"] ** 2 % P["p"] == P["p"] - 1,
      lambda P: mult_order(P["a"], P["p"]) == 4)

# S2 (true, iff): a square root of -1 exists mod odd p  <=>  p = 1 mod 4 ; test both directions
S2a = ("S2a: p=1 mod 4 => exists a, a^2=-1", ({"p": p} for p in primes(3, 2000)),
       lambda P: P["p"] % 4 == 1,
       lambda P: any(a * a % P["p"] == P["p"] - 1 for a in range(1, P["p"])))
S2b = ("S2b: exists a, a^2=-1 => p=1 mod 4", ({"p": p} for p in primes(3, 2000)),
       lambda P: any(a * a % P["p"] == P["p"] - 1 for a in range(1, P["p"])),
       lambda P: P["p"] % 4 == 1)

# S3 (FALSE, deliberately): "x -> a*x + y is injective on the box |x|,|y| <= B whenever 4B^2 < p".
# The correct sufficient condition is 2(|a|B + B) < p; this weaker one fails -> demonstrates counterexample output.
def s3_params():
    for p in primes(5, 60):
        roots = [a for a in range(1, p) if a * a % p == p - 1]
        for a in roots:
            for B in range(1, p):
                yield {"p": p, "a": a, "B": B}


def box_injective(P):
    p, a, B = P["p"], P["a"], P["B"]
    img = {(a * x + y) % p for x, y in itertools.product(range(-B, B + 1), repeat=2)}
    return len(img) == (2 * B + 1) ** 2


S3 = ("S3 (expected to FAIL): 4B^2 < p => box encoding injective", s3_params(),
      lambda P: 4 * P["B"] ** 2 < P["p"], box_injective)

STATEMENTS = [S1, S2a, S2b, S3]
EXPECTED_FAIL = {"S3 (expected to FAIL): 4B^2 < p => box encoding injective"}


def sage_crosscheck() -> dict | None:
    """Optional: cross-check S1 with Sage's own multiplicative order on a few primes."""
    if not HAVE_SAGE:
        return None
    ok = True
    for p in (5, 13, 17, 29):
        F = GF(p)
        for a in F:
            if a != 0 and a ** 2 == -1:
                ok &= (a.multiplicative_order() == 4)
        ok &= (cyclotomic_polynomial(4).change_ring(F).roots() != []) == (p % 4 == 1)
    return {"check": "sage-crosscheck S1/S2", "passed": bool(ok)}


def main() -> int:
    bad = 0
    for sid, it, hyp, concl in STATEMENTS:
        res = check(sid, it, hyp, concl)
        print(json.dumps(res))
        if not res["passed"] and sid not in EXPECTED_FAIL:
            bad += 1
        if sid in EXPECTED_FAIL and res["passed"]:
            print(json.dumps({"check": sid, "error": "expected a counterexample but found none"}))
            bad += 1
    sc = sage_crosscheck()
    if sc:
        print(json.dumps(sc))
        bad += 0 if sc["passed"] else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
