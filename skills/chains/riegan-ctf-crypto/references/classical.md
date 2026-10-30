# Classical ciphers and encodings

Triage order: strip whitespace, measure length and alphabet, try decodings first,
ciphers second. Ciphertext that keeps its language's letter frequency is substitution
or transposition; flat or shuffled frequency with byte-alphabet is XOR/stream.

## Encoding vs cipher decision table

| Observation | Guess | Test |
|---|---|---|
| `[A-Za-z0-9+/]+={0,2}`, length % 4 == 0 | base64 | `base64 -d` yields printable / known header |
| base64 alphabet but `-` and `_` | base64url | replace `-`→`+`, `_`→`/`, pad, decode |
| `A-Z2-7` with `=` padding | base32 | decode; note it cannot encode lowercase |
| `0-9A-F` (or af) pairs, even length | hex | `xxd -r -p` |
| `123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz` (no `0OIl`) | base58 (Bitcoin) | decode (CyberChef "From Base58") |
| chars `!`–`u`, starts `;<=>?` often | ascii85 (btoa/boh); `<~` wrapper = Adobe | CyberChef "From Ascii85" |
| `\uXXXX` / `%41` / `&#65;` | unicode/url/html entity | CyberChef or python `codecs`/`unquote` |
| dots and dashes | morse | table below |
| only 2 symbols (0/1, A/B, case) in groups of 5 | bacon (A/B) or binary | bacon groups of 5 → letters |
| `JK` etc. = ROT13 of real words | rot13/caesar | try all 25 shifts |
| letters only, preserves frequency peaks | substitution / atbash / affine | atbash & affine are instant; else quipqiup |
| flat-ish frequency, repeated blocks | transposition | anagramming; columnar |
| bytes, no structure, similar lengths XORed | XOR key | `scripts/xorfind.py` |

Layered encodings (base64 of hex of base64...) are common: decode until readable, then
stop. CyberChef "Magic" operation brute-forces up to N layers for you.

## Offline CyberChef

```bash
git clone -b gh-pages --depth 1 https://github.com/gchq/CyberChef.git tools/cyberchef
# open tools/cyberchef/CyberChef_v*.html directly in a browser; fully client-side
```

The gh-pages branch carries the prebuilt single-file release. Everything runs locally
in the page — use this instead of online tools whenever the data is event-sensitive.
(Install once; never paste flags/secrets into random web tools.)

## Single-key ciphers

| Cipher | Recognition | Break |
|---|---|---|
| ROT13 / Caesar | English-like after shift | brute 25 shifts, score with letter frequency |
| Atbash | A↔Z mapping | instant: `chr(219-ord(c))` for lowercase... apply once and read |
| Affine `y=ax+b mod 26` | 2 params, gcd(a,26)=1 | brute a in {1,3,5,7,9,11,15,17,19,21,23,25}, b in 0..25 |
| Rail fence | letters intact, jumbled order | brute rail counts 2..len, read zigzag |
| Columnar transposition | repeated short blocks; word fragments | brute key lengths; anagram columns (try common key words) |
| Bacon | 2 symbols, length % 5 == 0 | map 5-group binary (AAAAA=a) — watch variant 24/26-letter tables |
| Morse | `.` `-` `/` separators | standard table; separator chars vary (`/`, space) |
| Tap code | pairs of small numbers/taps 1-5 | 5x5 Polybius square (C/K merged) |
| Book/running-key cipher | plaintext-like keystream needed | find the book/text; look for hints (title, author, provided file); crib "the"/flag prefix at many offsets |

Frequency analysis approach (any monoalphabetic): count letters, match the English
profile `ETAOINSHRDLCUMWFGYPBVKJXQZ`; the top peak is usually e/t; `'` and `-` survive
substitution and anchor word shapes. Quadgram scoring beats single-letter counts —
implement once or let quipqiup do it.

## Substitution → word patterns

1. Compute word patterns: `pattern(w) = positions of repeated letters`, e.g.
   `ABBA`, `ABCDC`. `pattern("hello") = ABCDE`, `pattern("all") = ABB`.
2. Look up candidate English words with identical patterns for the longest ciphertext
   words; intersect constraints.
3. Automated: https://quipqiup.com (non-secret data only) — paste ciphertext, it solves
   monoalphabetic substitution by hill-climbing on quadgrams.

## Vigenere

Index of coincidence (IC), per candidate period `t`: split ciphertext into `t` cosets
(positions ≡ i mod t); IC of a coset ≈ 0.066 for English when `t` is the true period,
≈ 0.038 (random) otherwise.

```python
def ic(s):
    from collections import Counter
    n = len(s)
    if n < 2: return 0
    f = Counter(s)
    return sum(v*(v-1) for v in f.values()) / (n*(n-1))
```

Kasiski examination: find repeated substrings of length ≥ 3; distances between repeats
are multiples of the key length → gcd of distances narrows it. Then solve each coset as
Caesar (best frequency fit) or, better, pair columns against each other: the shift
between coset i and j is (k_i − k_j), found by correlating — recovers the whole key up
to one unknown letter.

## XOR

| Case | Method |
|---|---|
| single-byte key | brute 256, score printability + English frequency (`scripts/xorfind.py blob`) |
| repeating key, known length | per-column frequency solve (`scripts/xorfind.py --keylen N blob`) |
| repeating key, unknown length | Hamming-distance keysize test (normalized edit distance of adjacent blocks, keys 2..64) then per-column solve |
| known plaintext prefix (e.g. `flag{`) | XOR crib against ciphertext at each offset to expose keystream fragments; a repeating key shorter than the crib is recovered outright |
| two ciphertexts, same keystream (nonce reuse, many-time-pad) | C1 ⊕ C2 = P1 ⊕ P2; crib-drag: slide a likely word (the, flag, HTTP headers) through C1⊕C2 — where the XOR looks like English in both, you've recovered plaintext at that offset; extend recursively |

Crib-dragging is manual but fast: keystream reuse means every recovered byte of P1
gives the matching byte of P2 at the same offset (and vice versa).

```bash
.venv/bin/python skills/ctf-crypto/scripts/xorfind.py dist/blob              # single-byte
.venv/bin/python skills/ctf-crypto/scripts/xorfind.py dist/blob --keylen 7   # repeating key
.venv/bin/python skills/ctf-crypto/scripts/xorfind.py dist/blob --crib 'flag{'
.venv/bin/python skills/ctf-crypto/scripts/xorfind.py dist/blob --key-prefix 'flag{'
```

## Other classics worth knowing

- **Playfair / Bifid / ADFGVX**: digraph ciphers; look for even-length letters-only
  text and digram frequency; solvers exist online (non-secret only).
- **Enigma**: if the challenge says so; use an Enigma simulator library (`pip install
  py-enigma`) with known rotor settings from the challenge.
- **Binary/brainfuck/JSFuck/esoteric**: dispatch to `ctf-misc`, not crypto.
