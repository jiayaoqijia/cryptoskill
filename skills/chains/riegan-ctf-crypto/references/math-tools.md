# Math tooling — gmpy2, sympy, Sage, lattices

## gmpy2 idioms (in .venv)

```python
import gmpy2
gmpy2.iroot(c, 3)                 # (root, exact_bool) — integer e-th root
gmpy2.invert(e, phi)              # d = e^-1 mod phi  (raises if not invertible → gcd>1 → shared factor!)
gmpy2.gcdext(a, b)                # (g, x, y) with a*x + b*y == g — common-modulus & CRT setup
gmpy2.is_prime(n)                 # Miller-Rabin, probabilistic
gmpy2.next_prime(n)
# stdlib equivalents when gmpy2 absent: pow(e, -1, phi), pow(a,-1,m), pow(c, d, n)
pow(2, e, n); pow(c, d, n)        # python pow with 3 args is fine at CTF sizes
```

## sympy (in .venv)

```python
from sympy import factorint, nextprime, isprime, discrete_log, sqrt_mod, nthroot_mod
factorint(n)              # trial/pollard rho+pm1; ok to ~10^20-ish general, more if smooth
nextprime(p)
discrete_log(p, y, g)     # DLP: g^x = y mod p; needs smooth p-1 (Pohlig-Hellman inside)
sqrt_mod(a, p)            # Tonelli-Shanks
nthroot_mod(c, e, p, all_roots=True)   # e-th roots mod prime p — small-e RSA mod p
```

Honest limits: `factorint` is Pollard-class — useless on real 1024-bit semiprimes;
`discrete_log` needs favorable group order. Both are exactly right for challenge-sized
parameters.

## Sage availability matrix

| Task | Pure python (venv) | Sage required |
|---|---|---|
| big-int arithmetic, RSA textbook ops | gmpy2 | no |
| trial/pollard factoring | sympy | no |
| polynomial GCD over Z_n (Franklin-Reiter) | no | yes (`Zmod(n)` PolynomialRing, `gcd`) |
| Coppersmith small roots | toy cases only | yes (`f.small_roots(X=…, epsilon=…)` on `PolynomialRing(Zmod(n), 'x')`) |
| Boneh-Durfee, generic lattices/LWE/HNP | fpylll hand-rolled | strongly prefer Sage |
| elliptic curve DLP / Weil pairing | tiny curves brute | yes (`EllipticCurve`, `discrete_log`) |

Install (heavyweight — do before the event): `sudo pacman -S sagemath` (multi-GB).
Non-secret values only on https://sagecell.sagemath.org. fpylll without Sage:
try `sudo pacman -S python-fpylll` (name may differ; check `pacman -Ss fpylll`),
else `uv pip install --python .venv/bin/python fpylll` — frequently fails to build
from source on Arch; the pragmatic answer is Sage. `olvm` is not an LLL substitute.

## Lattice starter

Problem is lattice-shaped when you can write integer unknowns related by small
linear combinations. LLL finds short vectors in a lattice basis you construct.

Canonical constructions (build matrix, run LLL, read row entries as the unknowns):

| Problem | Lattice | Outcome |
|---|---|---|
| Merkle-Hellman knapsack (superincreasing private, public `b_i = a·w_i mod q`, ciphertext `S = sum x_i b_i`) | classic Shamir attack / low-density subset-sum lattice | recovers the transform, then solve the easy superincreasing knapsack |
| Hidden Number Problem (ECDSA/DSA with biased nonces: k = high bits known + small `r_low`) | rows: diag(N) + known-high-bit column, S-values column | LLL → recover k lows → recover d = (s·k - H(m)) · r^-1 mod n |
| biased nonce, top bits leak (l = ~4+ bits per signature, ~tens of sigs) | HNP as above; see also `github.com/maple3142/GPThack`-style writeup code | private key from signatures |
| short-pad Coppersmith (e=3, random 2·l/3-bit pads) | Franklin-Reiter via poly GCD is simpler; Coppersmith lattice also works | message recovery |
| Wiener with d slightly too big | Boneh-Durfee lattice (Sage) | extends to n^0.292 |

HNP setup recipe (DSA, nonce k_i = k_hi·2^t + x_i with x_i < 2^t unknown, t small):

```
s_i · k_i ≡ H(m_i) + r_i · d  (mod n)
→ x_i ≡ s_i^-1 (H_i + r_i d) - s_i^-1·s_i·k_hi·2^t   ... eliminate d by differencing
   pairs i>0 against i=0 → 2 unknowns per equation small (x_i, x_0 and d) → lattice
```

The standard blog formulation (Boneh-Venkatesan) builds a matrix with 1/2^t scaling on
the x_i, 1/n on the differences, plus a d row; Sage:

```python
M = Matrix(ZZ, ...)      # n+2 x n+2: diag knowns, columns for s_i^-1 r_i, H terms
M.LLL()                  # shortest vector → (x_1, ..., x_m, d·scale, ...)
```

Recover d, verify with a signature check.

## Wiener attack in pure python (d < (1/3)·n^(1/4))

```python
from math import isqrt

def cont_frac(a, b):
    while b:
        q = a // b
        yield q
        a, b = b, a - q*b

def convergents(cf):
    n0, d0, n1, d1 = 0, 1, 1, 0
    for q in cf:
        n0, n1 = n1, q*n1 + n0
        d0, d1 = d1, q*d1 + d0
        yield n1, d1

def wiener(e, n):
    for k, d in convergents(cont_frac(e, n)):
        if k == 0:
            continue
        # candidate phi; must factor as (p-1)(q-1) of this n
        phi = (e*d - 1) // k
        if (e*d - 1) % k:
            continue
        # x^2 - (n - phi + 1)x + n = 0 has integer roots p, q
        s = n - phi + 1
        disc = s*s - 4*n
        if disc < 0:
            continue
        r = isqrt(disc)
        if r*r == disc and (s + r) % 2 == 0:
            p = (s + r) // 2
            q = (s - r) // 2
            if p*q == n:
                return d, p, q
    return None
```

Test on construction: generate p, q random primes, d a 256-bit odd < n^(1/4)/3,
e = inverse(d, phi). Boneh-Durfee covers d up to n^0.292 — Sage
implementation (defund's `boneh_durfee.py` gist) when Wiener fails.

## ECC quick notes (delegated mostly here since no separate ECC file)

| Setup | Attack |
|---|---|
| small curve order (< 2^40ish) | brute/BSGS DLP: `sage: E.discrete_log(P, Q)` or baby-step giant-step in python |
| smooth order | Pohlig-Hellman (`sympy.discrete_log` on the group if prime-order factors) |
| singular curve (cusp/node: discriminant 0, e.g. a2=a3 form breaks) | map to multiplicative/additive group, DLP easy (pohlig/abs: `y^2 = x^3` → (x/y) dlog mod p) |
| same nonce k reused in two ECDSA sigs | k = (h1-h2)·(s1-s2)^-1 mod n → d = (s1·k - h1)·r^-1 mod n |
| attacker-chosen generator point / invalid curve | invalid-curve attack: twist order small → recover k mod small order, CRT |
| Smart's attack / additive transfer for anomalous curves (order == p) | Sage `Smart`-style lift: p-adic elliptic logarithm, few lines |

ECDSA/DSA nonce relations, Montgomery ladders with missing checks, `secp256k1` —
parameterize: always extract (curve params, G, n_order, Q_public, (r, s), h(m)).
