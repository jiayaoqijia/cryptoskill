# Symmetric crypto — modes, oracles, MACs

Primitive-level bugs dominate: the AES/DES algorithm itself is fine; the mode, padding,
IV/nonce handling, or MAC construction is not. Find the `mode` in source before anything.

## Mode decision table

| Signal | Bug class | Attack |
|---|---|---|
| ECB + image/screenshot output | blocks visible | "ECB penguin": replace a PNG/bitmap body with ECB-encrypted (mostly) constant image; structure leaks through. Detect: repeated 16-byte ciphertext blocks for repetitive plaintext |
| ECB + prefix/suffix oracle (server encrypts `enc(user_input + secret)` or `enc(secret + user_input)`) | block alignment oracle | byte-at-a-time ECB decryption: brute the unknown byte by aligning blocks and comparing ciphertext blocks |
| CBC + controlled plaintext before an interesting field (role/price/ isAdmin) | bit-flipping | flip target bytes in the PREVIOUS ciphertext block: `C'_{i-1}[j] = C_{i-1}[j] ⊕ P_i[j] ⊕ want[j]`; corrupts P_{i-1}, fix or ignore if it's padding/IV region |
| CBC + IV prepended / IV = key / IV user-controlled | first-block manipulation | decrypt-then-inspect: IV acts as C_0; changing IV flips P_1 identically (no corruption elsewhere) |
| CBC/GCM + decrypts and reveals padding success/failure (error/timing differences) | padding oracle | full decryption without the key (below) |
| CTR/GCM nonce reused (two ciphertexts, same key+nonce) | keystream reuse | C1 ⊕ C2 = P1 ⊕ P2, crib-drag (classical.md); recover P1 from known P2 |
| CTR same nonce, attacker plaintext oracle | keystream known | KS = P_known ⊕ C; decrypt everything else under that nonce; GCM additionally loses all confidentiality AND the auth key (forbidden attack) |
| RC4 anywhere | bias/related-key | single-byte biases in initial keystream (first ~256 bytes); WEP-style IV reuse → same-stream XOR |
| single DES (8-byte blocks, key 64 bits) | brute force | `hashcat -m 15000` if a hash, or brute with `openssl` loop / DESchallenge-style; DES "weak keys" (0x010101.., 0xFEFEFE..) and semi-weak key pairs encrypt = decrypt — check key bytes if key partially known |
| custom AES-like toy cipher (S-box, few rounds) | weak structure | look for: missing key schedule (same subkey), linear S-box (affine over GF(2) → solve with z3), few rounds (statistical/differential by hand), ECB of a block cipher built from XORs (linear algebra over GF(2)) |

## CBC bit-flipping (exact mechanics)

Plaintext block i decrypts as `P_i = D(C_i) ⊕ C_{i-1}`. To make byte j of P_i equal
`want[j]`: set `C_{i-1}[j] ^= P_i[j] ^ want[j]` in the ciphertext you submit. The bytes
of P_{i-1} at the same positions become garbage — arrange the layout so that the
corrupted block is padding/irrelevant (put your target field in block 2+, corrupt block
1 whose plaintext nobody checks, or corrupt the IV to flip block 1: IV corruption is
silent).

## Padding oracle (PKCS#7) — padbuster logic

Server decrypts CBC and tells you (error code, timing) whether padding is valid.

For the last block: guess the last byte `g` (0..255); send a crafted 2-block message
`(R || C_last)` where `R` is random except `R[15] = S ^ 0x01` once you know how D(C)
byte relates. Standard loop, byte-by-byte from the end, maintaining pad value k:

```
R[15-k+1..15] = D(C)[16-k..15] ^ k    # set after those bytes are known
R[15-k]       = g ^ k                  # brute g until padding validates
D(C)[15-k]    = R[15-k] ^ k ... recover g then next byte
```

Practical: use `padbuster` (package `padbuster` on many distros; on Arch check AUR) or
script it in 30 lines with pwntools/requests. Detection: send the same ciphertext with
last byte of the previous block flipped both ways — differing responses = oracle.
Key insight: valid padding is indistinguishable-from-success only if the server also
leaks plaintext errors separately; capture the exact difference first.

## IV handling

- IV transmitted in the clear is normal — never a finding by itself.
- IV == key (common toy bug): recover key = P_1 ⊕ D(C_1)? Not directly; but with an
  encryption oracle you can often get D outputs and XOR out the key.
- IV reused across messages in CBC: identical first blocks leak equality; with chosen
  plaintexts this becomes encryption oracle abuse.
- Controllable IV + decrypt-then-MAC-check: bit-flip block 1 (see above).

## Nonce/keystream reuse

CTR mode is a stream cipher: `C = P ⊕ AES_K(nonce || counter)`. Nonce reuse under one
key = same keystream twice. Attack ladder:
1. C1 ⊕ C2 → P1 ⊕ P2 (no key needed).
2. Known plaintext (headers: `PNG`, `GET / HTTP`, `flag{`) → keystream fragment.
3. Crib-drag fragments back and forth until both sides read English (classical.md).
GCM: nonce reuse also yields the authentication subkey H (forbidden attack) → forgery.

## RC4

Key scheduling is fine for CTF purposes; the output has biases: byte 2 of the
keystream is 0 with probability ~2/256 (Mantin-Shamir); longer-term FLUKE biases exist.
If many messages under RC4 with random IVs, XOR the second keystream bytes and look at
the histogram. IV-prepended-to-key constructions (WEP) fall to the FMS attack class —
usually just a scripted XOR once enough (IV, C) pairs exist and P is known/partially
known.

## DES specifics

- Weak keys: `0x0101010101010101`, `0xFEFEFEFEFEFEFEFE`, `0xE0E0E0E0F1F1F1F1`,
  `0x1F1F1F1F0E0E0E0E` (each 8 bytes) — E_k(E_k(m)) = m, encryption = decryption.
- Semi-weak key pairs: encryption under one = decryption under the other.
- Key is 56 effective bits (8 parity bits) — brute-forceable. Unix descrypt hashes:
  `hashcat -m 1500 hash.txt rockyou.txt`. Raw DES with known plaintext/ciphertext pair:
  script the loop with pycryptodome (`from Crypto.Cipher import DES`); if only part of
  the key is unknown (parity/nibble hints), the search is tiny.

## MAC constructions

| Construction | Bug | Attack |
|---|---|---|
| `sha256(key ‖ msg)` | length extension | append `‖ admin=true`: `hashpumpy` (below) or manual Merkle-Damgård craft |
| `md5(key ‖ msg)`, sha1 same | same | hashpumpy supports md5/sha1/sha256 |
| raw `==` comparison of MAC | timing | not usually exploitable remotely; note it |
| truncated MAC | brute space shrinks | 32-bit MAC = 2^32 expected tries — feasible offline if oracle is local |
| HMAC | correct construction | do not attack HMAC itself; look at what is signed and replay/ordering |
| CRC32 as "MAC" | linear | see hash-prng.md; forge directly with CRC algebra |

Length extension with hashpumpy:

```bash
uv pip install --python .venv/bin/python hashpumpy   # may need a C compiler (gcc/base-devel)
.venv/bin/python -c "import hashpumpy; print(hashpumpy.hashpumpy.hashpumpy('sha256', b'<known-msg>', b'<digest-hex>', b'<append>', <keylen>))"
# returns (new_digest_hex, new_message) — new_message = msg + glue_padding + append
```

Manual fallback (no build tools): implement MD-length-extension in ~40 lines: sha256
state = first 8 words of digest, re-run compression over `append` with the original
block count, glue padding = 0x80 + zeros + 64-bit bit-length of (keylen + msglen).
Keylen is unknown → brute plausible lengths (8..64).
