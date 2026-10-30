#!/usr/bin/env python3
"""rsacheck.py — quick triage of RSA moduli and parameter sets.

Given one or more n values (decimal or 0x-prefixed hex, as args or one per line in
files via --files), reports per-n:
  - bit length, hex form
  - prime check (sympy if available, Miller-Rabin fallback otherwise)
  - perfect square
  - small factors up to --small-limit (default 10^6)
  - divisibility by the first few hundred small primes (same loop, reported separately)
  - Fermat close-prime check with bounded rounds
  - factordb.com status/factor query (network) unless --offline
Given multiple n: pairwise GCD to find shared primes.

Only stdlib is required; sympy is imported lazily and absence degrades output.
"""
import argparse
import json
import math
import re
import sys
import urllib.request
from math import gcd, isqrt

SMALL_PRIMES = []


def _sieve(limit):
    out = []
    s = bytearray([1]) * (limit + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if s[i]:
            s[i * i :: i] = bytearray(len(s[i * i :: i]))
    for i in range(limit + 1):
        if s[i]:
            out.append(i)
    return out


def parse_int(s):
    s = s.strip()
    if not s:
        return None
    try:
        if s.lower().startswith("0x"):
            return int(s, 16)
        return int(s, 10)
    except ValueError:
        return None


def is_prime(n):
    """sympy.isprime if available; else deterministic Miller-Rabin for n < 3.3e24."""
    try:
        from sympy import isprime

        return bool(isprime(n))
    except Exception:
        pass
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    # valid witnesses for n < 3,317,044,064,679,887,385,961,981
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def small_factors(n, limit):
    """Return list of (small) prime factors found by trial division up to limit."""
    found = []
    if n <= 1:
        return found
    m = n
    for p in SMALL_PRIMES:
        if p > limit:
            break
        if m % p == 0:
            found.append(p)
            while m % p == 0:
                m //= p
    return found


def fermat(n, rounds):
    """Fermat factorization; returns (p, q) or None."""
    if n % 2 == 0:
        return (2, n // 2)
    a = isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(rounds):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return (a - b, a + b)
        a += 1
    return None


def factordb(n):
    """Query factordb.com. Returns dict from its JSON API or raises."""
    url = "https://factordb.com/api?query=" + str(n)
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read().decode())


def check(n, small_limit, fermat_rounds, offline):
    print(f"n = {n}")
    print(f"  bits      : {n.bit_length()}")
    print(f"  hex       : {hex(n)}")
    r = isqrt(n)
    if r * r == n:
        print(f"  PERFECT SQUARE: n = {r}^2")
        fac = small_factors(r, small_limit)
        print(f"  sqrt small factors: {fac if fac else 'none (prime-ish)'}")
    prime = is_prime(n)
    print(f"  prime     : {prime}")
    if prime:
        print("  -> n is prime: textbook RSA broken; phi = n-1")
        return
    fac = small_factors(n, small_limit)
    if fac:
        m = n
        for p in fac:
            while m % p == 0:
                m //= p
        print(f"  small factors (<= {small_limit}): {fac}")
        print(f"  cofactor  : {m} ({m.bit_length()} bits)"
              + ("" if m > 1 else "  <- fully factored!"))
    else:
        print(f"  small factors: none up to {small_limit}")
    if not fac:
        res = fermat(n, fermat_rounds)
        if res:
            print(f"  FERMAT HIT: p = {res[0]}  q = {res[1]}")
        else:
            print(f"  fermat    : no hit in {fermat_rounds} rounds (p,q not close)")
        if not offline:
            try:
                d = factordb(n)
                print(f"  factordb  : status={d.get('status')} "
                      f"factors={d.get('factors')}")
            except Exception as e:
                print(f"  factordb  : query failed ({e}); use --offline to skip")
    print()


def main():
    global SMALL_PRIMES
    ap = argparse.ArgumentParser(
        description="RSA modulus triage: size, primality, small factors, "
        "Fermat close primes, factordb lookup, pairwise gcd.")
    ap.add_argument("n", nargs="*", help="moduli, decimal or 0x hex")
    ap.add_argument("--files", nargs="+", default=[],
                    help="files containing one n per line (comments with # ok)")
    ap.add_argument("--small-limit", type=int, default=10**6,
                    help="trial-division bound (default 1e6)")
    ap.add_argument("--fermat-rounds", type=int, default=10**5,
                    help="Fermat rounds per n (default 1e5)")
    ap.add_argument("--offline", action="store_true",
                    help="skip the factordb.com network query")
    args = ap.parse_args()

    SMALL_PRIMES = _sieve(max(args.small_limit, 1000))

    vals = []
    for s in args.n:
        v = parse_int(s)
        if v is None:
            sys.exit(f"cannot parse value: {s}")
        vals.append(v)
    for f in args.files:
        try:
            fh = open(f)
        except OSError as e:
            sys.exit(f"cannot open {f}: {e}")
        with fh:
            for line in fh:
                line = re.sub(r"#.*", "", line).strip()
                if not line:
                    continue
                v = parse_int(line)
                if v is None:
                    sys.exit(f"cannot parse line in {f}: {line!r}")
                vals.append(v)

    if not vals:
        ap.print_help()
        return

    for n in vals:
        check(n, args.small_limit, args.fermat_rounds, args.offline)

    if len(vals) > 1:
        print("pairwise gcd:")
        hit = False
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                g = gcd(vals[i], vals[j])
                if g > 1:
                    hit = True
                    print(f"  n[{i}] and n[{j}] share factor: {g}")
        if not hit:
            print("  no shared factors")


if __name__ == "__main__":
    main()
