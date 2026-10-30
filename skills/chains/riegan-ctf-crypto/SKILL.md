---
name: ctf-crypto
description: Use when a challenge involves cryptography: RSA (n, e, c given; p, q, d, dp leaks; Wiener, Hastad, Coppersmith, lattices), ECC/ECDSA, AES/DES modes (ECB penguin, CBC bit-flip, padding oracle, CTR/GCM nonce reuse), hashes (crack, length extension, CRC32), PRNG prediction (MT19937, LCG, seed=time), XOR or classical ciphers (Caesar, Vigenere, substitution, base64/hex encodings), or math tooling (gmpy2, sympy, Sage, z3, RsaCtfTool, CyberChef).
---

# CTF crypto — triage, attack tables, math tooling

Workspace rules, remote gate, flag logging: see sibling skill `ctf`. All local analysis
here is offline-safe; nothing in this skill needs the network unless explicitly noted
(factordb.com query, online Sage cell — see guardrails below).

## Triage — identify the primitive (first 5 minutes)

1. Write down in `notes.md` every parameter the statement/source gives you
   (`n, e, c, p, q, d, dp, dq, phi, g, h, key, IV, nonce, mode, hash, seed, curve`).
   Missing parameters are the puzzle — note which are absent.
2. Classify the primitive:

| What you see | Primitive | Read |
|---|---|---|
| Letter soup, symbols, `...=` padding, dots/dashes | encoding or classical cipher | `references/classical.md` |
| Big integers `n e c` (often 0x or 1024+ bits), `openssl rsa` files | RSA | `references/rsa.md` |
| Points on a curve, `y^2 = x^3 + ax + b`, ECDSA/DSA sigs + nonces | ECC / lattice | `references/math-tools.md` |
| `AES/DES/RC4`, modes `ECB/CBC/CTR/GCM`, an oracle service | symmetric crypto | `references/symmetric.md` |
| Hash to invert/crack, `sha256(key||msg)`, CRC32, custom hash func | hashes | `references/hash-prng.md` |
| `random.*`, `rand()`, LCG constants, "guess my number" | PRNG | `references/hash-prng.md` |
| Huge knapsack sums, Merkle-Hellman, "biased nonce", "short pad" | lattice problem | `references/math-tools.md` |

3. Run the quick screens:

```bash
python3 skills/ctf-crypto/scripts/rsacheck.py <n>     # RSA params triage (stdlib)
python3 skills/ctf-crypto/scripts/xorfind.py dist/blob # XOR/encoding triage (stdlib)
file dist/* ; xxd dist/* | head        # key files? PEM? raw bytes?
openssl rsa -in key.pem -text -noout   # if any PEM/DER key is present
```

4. Encodings vs encryption: try decode layers first (base64 → hex → rot13). If the
   decoded blob is still high-entropy bytes with no structure, it is ciphered or XORed.
   Use a local CyberChef (see `references/classical.md`) — never paste event secrets
   into random online tools.

5. Nothing recognizable? Read the challenge source. Crypto challenges almost always
   ship the algorithm; the bug is in a parameter or a mode, not the primitive.

## Playbook — expert flow

1. Extract every constant into `notes.md` (dec + hex + bit length).
2. Pick the attack table for the primitive (RSA table in `references/rsa.md` is keyed
   on leaked material: match what you have, not what looks fun).
3. Prefer the cheapest attack that fits the preconditions; escalate only on failure.
   Record each failed attack in `notes.md` — RSA trial-and-error otherwise loops.
4. Verify a recovered secret against the challenge: re-encrypt/re-sign and compare, or
   check `d*e ≡ 1 (mod φ)`, or decrypt to a string matching the flag regex.
5. Interactive oracles (padding, prefix-suffix, broadcast): script them with pwntools;
   remote connections need the user gate from `ctf`.

Attack quick-index (details + commands in the reference files):

| Attack family | Precondition | Where |
|---|---|---|
| Classical / XOR / encodings | human-readable ciphertext | `references/classical.md` |
| RSA: factordb, Fermat, small e root, Hastad, Wiener, common modulus, dp leak, Coppersmith, related messages | any `n e c` set | `references/rsa.md` |
| ECB/CBC/CTR/GCM mode abuse, padding oracle, length extension | block cipher + oracle | `references/symmetric.md`, `references/hash-prng.md` |
| MT19937 / LCG / seed brute | any PRNG output | `references/hash-prng.md` |
| LLL: knapsack, HNP/biased nonces, Wiener fallback | lattice-shaped integers | `references/math-tools.md` |

## References

- `references/classical.md` — encodings vs ciphers decision table, frequency analysis,
  Vigenere (IC + Kasiski), substitution via quipqiup, transposition, XOR incl.
  crib-dragging; offline CyberChef setup.
- `references/rsa.md` — attack decision table keyed on leaked material; RsaCtfTool and
  Sage install notes.
- `references/symmetric.md` — block cipher modes, bit-flipping, padding oracle,
  nonce reuse, RC4/DES legacy, MAC length extension.
- `references/hash-prng.md` — hash identification and cracking, CRC32 linearity,
  custom-hash inversion with z3, MT19937/LCG/Java PRNG prediction.
- `references/math-tools.md` — gmpy2/sympy idioms, Sage availability matrix, lattice
  starter (LLL, knapsack, HNP), pure-python Wiener.

## Scripts in this skill

| Script | Purpose |
|---|---|
| `scripts/rsacheck.py` | n triage: bit length, primality, small factors, Fermat close primes, factordb lookup, pairwise gcd |
| `scripts/xorfind.py` | single/multi-byte XOR solver, crib search, known-prefix keystream recovery |

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| `gmpy2`, `sympy`, `pycryptodome` | already in `.venv` (`scripts/setup.sh`) | big-int math, factoring, AES/DES primitives |
| `scripts/rsacheck.py`, `scripts/xorfind.py` | included (this skill) | RSA triage, XOR solving |
| RsaCtfTool | clone https://github.com/RsaCtfTool/RsaCtfTool + `uv pip install --python .venv/bin/python git+https://github.com/RsaCtfTool/RsaCtfTool` | automated RSA attack try-all (`rsactftool -n <n> -e <e> --uncipher <c> --attack all`) |
| CyberChef (offline) | `git clone -b gh-pages --depth 1 https://github.com/gchq/CyberChef.git tools/cyberchef`, open `CyberChef_v*.html` locally | local encode/decode/magic ops, no data leaves the box |
| quipqiup | offline not available; use https://quipqiup.com only for non-secret puzzles, or word-pattern solver in `references/classical.md` | substitution solving |
| hashcat / john | `sudo pacman -S hashcat john` | hash cracking (GPU / CPU) |
| `hashpumpy` | `uv pip install --python .venv/bin/python hashpumpy` (may need build tools; manual fallback in `references/symmetric.md`) | SHA length extension |
| `randcrack` | `uv pip install --python .venv/bin/python randcrack` | MT19937 state recovery + prediction |
| `z3-solver` | `uv pip install --python .venv/bin/python z3-solver` | constraint solving: LCG params, custom hash inversion |
| SageMath (optional, huge) | `sudo pacman -S sagemath` (multi-GB) or https://sagecell.sagemath.org for non-secret values | polynomial GCD, Coppersmith, LLL |
| fpylll (if avoiding Sage) | try `sudo pacman -S python-fpylll`; if absent, `uv pip install --python .venv/bin/python fpylll` often fails to build → prefer Sage | LLL without Sage |
| factordb.com | browse https://factordb.com | check if n is already factored |
