# RSA attack decision table

Keyed on what leaked beyond the bare `n, e, c`. Always run the cheap screens first:
`scripts/rsacheck.py` reports bit length, primality, perfect square, small factors,
Fermat-close primes, and queries factordb.com (network, `--offline` to skip).

| You have / observe | Attack | Tool/command | Notes |
|---|---|---|---|
| `n, e, c` only, n ≤ ~256 bits (composite) | direct factor | `sympy.factorint(n)`; factordb.com; `msieve`/`yafu` for hard ones | anything ≤ 100 bits factors in seconds; 512-bit semiprime is a multi-hour+ CADO-NFS job — if the challenge intends it, n is small or already in factordb |
| n already factored somewhere | factordb lookup | open https://factordb.com, paste n; `rsacheck.py` shows the status | status "FF" = fully factored |
| small factor exists | trial division / RsaCtfTool | `rsacheck.py` (to 10^6) then `sympy.ntheory.factor_.smoothness`/ecm | p-1 smooth: Pollard p-1 via `sympy` or gmpy2 loop; Pollard rho for ~64-bit factors |
| p ≈ q (Fermat) | Fermat factorization | `rsacheck.py` (bounded); explicit loop below | works when `abs(p-q) < ~n^0.25`; try 10^5–10^7 rounds |
| ROCA-vulnerable n (Infineon) | ROCA detect + attack | detection: github.com/crocs-mit/roca (detect.py); attack included there and in RsaCtfTool's attack set | vulnerable n is generated from a fixed set of small primes; detection is instant, factorization needs Coppersmith (Sage) |
| e small (3, 5, 7) + m^e < n | integer e-th root | `gmpy2.iroot(c, e)` | no padding, message tiny; check exact root, else m^e > n was reduced |
| e=3, m^3 slightly > n, or m high bits known | Coppersmith stereotyped message | Sage `small_roots` (see math-tools.md) | needs short unknown part of m (< n^(1/e)) |
| e=3 and ≥ 3 recipients, same m, no padding | Hastad broadcast | CRT the c_i mod n_i, then cube root | linear padding variants also work (Coppersmith), plain CRT for no padding |
| e large (~n) | Wiener attack | pure-python continued fractions (code in `references/math-tools.md`) | works when d < (1/3)·n^(1/4) |
| e large, Wiener failed | Boneh-Durfee | Sage implementation (e.g. defund's boneh_durfee.py) | extends to d < n^0.292; lattice attack, not guaranteed |
| `dp` or `dq` leaked | dp leak → factor n | standard algorithm (below) | recovers p, then d |
| same n, two different e (gcd(e1,e2)=1) | common modulus | `m = pow(c1, a, n)·pow(c2, b, n)` with `a·e1 + b·e2 = 1` (gcdext; a or b negative → invert mod n) | no factoring needed |
| many ciphertexts/files with different n | pairwise gcd | `rsacheck.py n1 n2 n3 ...` or files with `--files` | shared prime reuse across users |
| two messages related: m2 = a·m1 + b | Franklin-Reiter related-message | polynomial GCD over Z_n — Sage: `gcd(x^e - c1, (a·x+b)^e - c2)` over `Zmod(n)`, root is m1 | classic e=3 short-pad setup (b = 2^k padding) |
| m^e < n but root not exact | m^e wrapped once | search small multiples: iroot(c + k·n, e) for k = 0..few hundred | |
| e = 1 | identity | `m = c mod n` | check for e=1 before anything else |
| high bits of p known | Coppersmith factoring | Sage `small_roots` on f(x) = x + p_high over Z_n | unknown low part < n^0.25 |
| small d known to be tiny (< 2^40) | brute d | loop d, check `pow(pow(2,e,n), d, n) == 2` | |
| c ≡ m, c == n-1, c tiny | sanity checks | read m directly; c = 0 → m = 0 | check `pow(m, e, n) == c` after |
| key file (PEM/DER) | extract | `openssl rsa -in key.pem -text -noout`; `openssl rsa -in key.pub -pubin -text -noout` | look at e size, primes present, dp/dq |

Recoveries after factoring: `d = pow(e, -1, (p-1)*(q-1))` (Python 3.8+) or
`d = gmpy2.invert(e, (p-1)*(q-1))`, then `m = pow(c, d, n)`,
`bytes.fromhex(hex(m)[2:]).decode()` (strip leading zeros: `hex(m)[2:]` then zfill to
even length).

## dp leak → factor n (sketch, dp = d mod (p-1))

Given (n, e, dp): for each k in 1..e: phi_candidate = (e·dp - 1)/k must be an integer;
then p = ... — the standard route: e·dp = 1 + k·(p-1) for some 1 ≤ k < e. For each k,
p = (e·dp - 1)/k + 1; if p > 1 and n % p == 0, done. (Works because k is small when e
is small; iterate k until n % p == 0.)

## Fermat factorization loop

```python
from math import isqrt
def fermat(n, rounds=10**6):
    a = isqrt(n)
    if a*a < n: a += 1
    for _ in range(rounds):
        b2 = a*a - n
        b = isqrt(b2)
        if b*b == b2:
            return a-b, a+b
        a += 1
    return None
```

## RsaCtfTool

Automated try-everything; good when the leak type is unclear.

```bash
# install into the shared venv (from GitHub, not on PyPI under this name):
uv pip install --python .venv/bin/python git+https://github.com/RsaCtfTool/RsaCtfTool
# its CLI entrypoint also wants some attack deps; if imports fail, clone and read README:
git clone https://github.com/RsaCtfTool/RsaCtfTool tools/RsaCtfTool

# usage (network-free attacks are tried first):
.venv/bin/rsactftool -n <n> -e <e> --uncipher <c> --attack all
# with a private-key file or dp leak, pass what you have: --keyfile, --dp
```

Honesty note: the exact flag set changes between versions; run
`.venv/bin/rsactftool --help` and read the attack list rather than trusting this page
for rarely-used flags. The `--attack all` / `-n -e --uncipher` form above is stable.

## Sage / Coppersmith preconditions

Coppersmith finds small roots: `f(x)` degree d over Z_n has a root < n^(1/d) (Lattice/
LLL-based, `small_roots` in Sage with `epsilon` slack). Needs SageMath — heavyweight:

```bash
sudo pacman -S sagemath      # multi-GB pull; do this before the event, not during
```

Alternatives: https://sagecell.sagemath.org for non-secret values (paste only public
parameters, never a flag or a key you intend to keep), or pure-python LLL-based
Coppersmith implementations (e.g. defund's coppersmith.py — small roots with Sage-only
`small_roots` replaced by an LLL you supply via fpylll; for toy sizes a sympy/brute
search may suffice). What genuinely needs Sage: polynomial GCD over Z_n
(Franklin-Reiter), Coppersmith, Boneh-Durfee, generic lattices.
