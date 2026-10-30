# Hashes and PRNGs

## Hash identification

```bash
hashid '<hash>'            # or: hash-identifier (interactive), both on PyPI/pacman
hashcat --example-hashes   # ground truth: format example per -m mode, searchable
john --list=formats        # all formats john knows
```

Manual tells: length in hex chars → 32 md5/ntlm, 40 sha1, 64 sha256, 128 sha512;
`$<id>$` prefix → crypt(3) family (`$6$` sha512crypt, `$y$` yescrypt);
base64ish 20/28/43 bytes → sha1/sha256 truncated; salt position matters for format.
Verify a guess: `echo -n test | sha256sum` vs the target when you have a known
plaintext.

## Cracking

```bash
sudo pacman -S hashcat john        # once, with user approval for sudo
# wordlist: rockyou is NOT in Arch repos — fetch once, keep in tools/:
mkdir -p tools && curl -L -o tools/rockyou.txt \
  https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
# system dictionary (smaller): /usr/share/dict/words via `sudo pacman -S words`

hashcat -m 1000 hash.txt tools/rockyou.txt          # 1000 = NTLM; see --example-hashes
hashcat -m 1000 --show hash.txt                     # cracked results
john --wordlist=tools/rockyou.txt --format=raw-sha256 hash.txt
# rules + masks:
hashcat -m 1000 hash.txt -r /usr/share/hashcat/rules/best64.rule tools/rockyou.txt
hashcat -m 1000 hash.txt -a 3 '?u?l?l?l?l?d?d?d?'   # mask attack
```

GPU needed for hashcat on real GPUs; john (CPU) is fine for rockyou-class attacks.

## CRC32

Linear over GF(2): `crc(a) ^ crc(b) ^ crc(c) ^ crc(d) == 0` when
`a^b^c^d == 0` (same-length strings). Consequences: forge a "checksum" by XOR-tuning a
modifiable field; `crc32(x ^ y)` relations make it zero-authentication. Python:
`zlib.crc32`. To hit a target CRC with free bytes: solve 4 free bytes via linear algebra
(brute last 4 bytes = 2^32 too slow; do GF(2) gaussian elimination or use the reverse-CRC
table technique).

## Custom hash → invert

Given a toy hash function in source:
1. Try direct inversion if each step is a bijection (XOR, S-box, rotate, add mod 2^n):
   run it backwards from the target.
2. Non-injective or branching → z3-solver:

```python
from z3 import BitVec, BitVecVal, Solver, sat
def sym_hash(x):            # mirror the challenge code, BitVec ops instead of int
    ...
x = BitVec('x', 32)
s = Solver(); s.add(sym_hash(x) == BitVecVal(target, 32))
if s.check() == sat: print(hex(s.model()[x].as_long()))
```

3. Differential: find input pairs whose hashes collide by solving
   `H(x) == H(x ^ delta)` with z3 — wins collision-style challenges ("find two
   transcripts with same hash").

## PRNG decision table

| Generator (seen in source) | State | Attack |
|---|---|---|
| Python `random` (any method) | MT19937, 19937 bits | recover 624 consecutive 32-bit outputs → `randcrack` predicts everything after (also `random.getrandbits`, `randrange` — note `getrandbits(32)` = one output; larger sizes concatenate) |
| `random.seed(time.time())` or similar | tiny seed space | brute the timestamp window (±hours at challenge time), regenerate, compare to observed outputs |
| `random.seed(<small int / player-controlled>)` | seed known or guessable | just re-run |
| LCG `next = (a·x + c) mod m`, params unknown | recover from outputs | z3 (below) or algebra: 6+ outputs → t = x_{n+1}-x_n, t2-t1, ... solve for m, a, c with gcd tricks |
| LCG with truncated output (only top k bits of each state) | truncated LCG | z3 with BitVecs over ≥ ~4-8 outputs; or lattice (Stern) — hard case, Sage |
| `java.util.Random` | 48-bit LCG, `seed = (seed ^ 0x5DEECE66D)`, `next() = (a·s+c) mod 2^48`, a=0x5DEECE66D, c=0xB; output = top 32 bits | 2 outputs → brute 16 low bits of state (2^16), verify; or z3. Note `nextInt(b)` truncates differently: top bits after mod — read the JDK spec in source |
| libc `rand()` (glibc, default) | TYPE_3 additive feedback LCG: state r[0..33], r[i] = r[i-3] + r[i-31] mod 2^32, output r[i] >> 1 | conceptual: recover 31 consecutive outputs → run recurrence forward/backward (outputs discard 1 bit → 2^k ambiguity per value; z3 or bit-by-bit). Rare in CTFs; usually the challenge uses MT or an LCG instead |
| numpy `np.random.default_rng` | PCG64 | cryptographically weak but no ready 1-liner; usually not the intended bug — check the seed instead |
| `os.urandom`, `secrets` | CSPRNG | not attackable; the bug is elsewhere |
| `random.choice`/`shuffle` on flag | MT19937 seeding the ordering | recover seed by brute (small event) or MT state from prior outputs |

## randcrack (MT19937)

```bash
uv pip install --python .venv/bin/python randcrack
```

```python
from randcrack import RandCrack
rc = RandCrack()
for x in outputs_624_unmasked_32bit:
    rc.submit(x)          # must be raw 32-bit outputs (getrandbits(32)), consecutive
rc.predict_getrandbits(32); rc.predict_randrange(0, 100)
# past values: recover state, then note MT is reversible — untemper to get state words
```

Leak surface: server prints 624+ "random tokens", or you can trigger
`getrandbits(32)` 624 times via reconnect if the seed is per-process-fixed. If fewer
than 624 outputs are available, the state is underdetermined — look for seed brute
instead.

## LCG recovery with z3

```python
from z3 import *
xs = [...]                      # consecutive outputs
m = BitVec('m', 64); a = BitVec('a', 64); c = BitVec('c', 64)
s = Solver()
for i in range(len(xs)-1):
    s.add((a*xs[i] + c) % m == xs[i+1])   # sketch; fix widths to match output range
print(s.check())
```

Caveat: modulo of a BitVec by an unknown BitVec is awkward; in practice fix `m` if
known (2^32, 2^31-1, a prime like 2^31-1) and solve for a, c, or use exact integer
algebra when full outputs are visible:
`t_i = x_{i+1} - x_i`; `a = t_{i+1} · inverse(t_i) mod m` (needs gcd(t_i, m) = 1);
`c = x_1 - a·x_0 mod m`; unknown m from `m = gcd(t_{i+1}·t_i ... differences of t-products)`.

## seed=time brute

```python
import time, random
observed = <first output you saw>
t0 = int(time.time())
for ts in range(t0 - 86400*2, t0 + 3600):
    r = random.Random(ts)
    if matches(r):            # reproduce the observed first draw
        print(ts); break
```

Record the challenge's start/stop time in notes.md — the window is around it.
