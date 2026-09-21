---
name: crypto-review
description: Finds cryptographic weaknesses in code — weak ciphers (DES, RC4, ECB mode), weak hashes (MD5, SHA-1) used for security purposes, hardcoded keys/IVs/salts, predictable randomness (Math.random, random, time-based tokens), disabled certificate verification, and undersized key lengths. Use when auditing anything involving encryption, hashing, tokens, certificates, or random number generation.
license: MIT
---

# Cryptography Review

## 1 — Quick sweep

```bash
rg -n -i "md5|sha1|des\b|rc4|ecb|cbc\(|blowfish|math\.random\(\)|random\.random\(\)|srand\(|new date\(\)\.gettime\(\)|nanoid\(|uuid\.v1\("
rg -n -i "rejectunauthorized\s*:\s*false|insecureskipverify\s*:\s*true|verify\s*=\s*false|ssl_verify|checkhostname|node_tls_reject_unauthorized"
rg -n -i "aes\.|createcipheriv|crypto\.randombytes|secrets\.|urandom|crypto/rand|rand\.read"
rg -n -i "(key|iv|salt|secret|passphrase)\s*[:=]\s*[\"'][a-z0-9]{8,}[\"']"
```

## 2 — Judge each hit by purpose

Context decides severity. The same MD5 is noise in a cache key and CRITICAL in a password hash.

| Purpose | Weak (flag) | Strong (OK) |
|---|---|---|
| Password storage | MD5/SHA1/SHA-256, unsalted | bcrypt, argon2id, scrypt, pbkdf2(≥100k iters) |
| Integrity/MAC | MD5, SHA-1, homemade "XOR obfuscation" | HMAC-SHA256+; AES-GCM/ChaCha20-Poly1305 for AEAD |
| Encryption at rest | ECB mode, static IV, DES/RC4, key==password | AES-256-GCM / ChaCha20-Poly1305, random IV per message, authenticated |
| Tokens/secrets/IDs | `Math.random()`, `random.random()`, timestamp-based, `uuid.v1()` | CSPRNG: `crypto.randomBytes`, `secrets`, `/dev/urandom`, `uuid.v4` (v5 for names) |
| TLS | `rejectUnauthorized: false`, `InsecureSkipVerify`, `NODE_TLS_REJECT_UNAUTHORIZED=0` in prod code | verification on + pinned CAs |

## 3 — Deep checks

- **Static vs per-message IVs**: `createCipheriv('aes-256-cbc', key, FIXED_IV)` or IV derived from deterministic data → HIGH (breaks semantic security; CBC+fixed IV leaks prefixes)
- **Hardcoded keys**: any literal key/PEM in source → CRITICAL (see `../secrets-detection/SKILL.md`); keys should come from env/secret manager, and rotate-by-commit means history keeps them
- **Key derivation**: password used directly as AES key instead of KDF (PBKDF2/HKDF/scrypt) → HIGH
- **Nonce reuse contexts**: counters resetting per restart, random nonces >2^32 messages (GCM) — flag as note, usually theoretical
- **Comparisons**: token/password hash compared with `==` instead of constant-time (`timingSafeEqual`, `hmac.compare_digest`) → LOW/MEDIUM (timing oracle)
- **Length**: RSA < 2048, ECC < 256, HMAC-SHA1 legacy — MEDIUM hygiene
- **Custom crypto**: any hand-rolled cipher/XOR/"custom encoding" protecting real data → HIGH by default (rate as if broken)

## 4 — Reporting

Per finding: purpose ("password hashing"), current construction, why it fails (one sentence), the drop-in replacement with correct usage example (e.g. `crypto.createCipheriv('aes-256-gcm', key, crypto.randomBytes(12))`), and severity per the table. Note positives: libsodium/argon2/CSPRNG usage done right.
