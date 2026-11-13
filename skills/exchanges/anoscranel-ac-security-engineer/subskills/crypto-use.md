---
name: crypto-use
domain: security-hardening/crypto-use
trigger: "Choosing or reviewing cryptographic primitives: password hashing, encryption, TLS, key handling, and post-quantum readiness."
anti_trigger: "Storing and rotating credentials and API keys (subskills/secrets.md); JWT validation mechanics (subskills/sessions-tokens.md)."
scope: "Pick vetted primitives, TLS, key handling, PQC readiness"
status: "seedling"
---

# Cryptographic Use

## Standard

- OWASP Cryptographic Storage Cheat Sheet: use OS, framework or cloud key storage (HSM, KMS, Key Vault) rather than inventing key handling.
- Hashing, encryption and encoding are different jobs: hashing (SHA-256/3, BLAKE) is one-way integrity — never for passwords; encryption (AEAD) gives confidentiality plus integrity; encoding (Base64, hex) gives no security.
- Authenticated encryption only: AES-GCM (NIST-preferred, hardware-accelerated) or ChaCha20-Poly1305 (RFC 8439). Unauthenticated AES-CBC/CTR lets attackers tamper undetected.
- NIST FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA) are final since 2024-08-13; NIST IR 8547 (initial public draft, 2024-11) deprecates 112-bit classical algorithms (RSA-2048, P-256) after 2030 and disallows them after 2035.
- OWASP Password Storage Cheat Sheet for KDF parameters (Argon2id m=19456 KiB, t=2, p=1; scrypt N=2^17, r=8, p=1; bcrypt ≥10; PBKDF2-HMAC-SHA-256 ≥600,000 only under FIPS-140).
- Nonce discipline: Bock et al., USENIX WOOT '16, found 184 HTTPS servers repeating GCM nonces and >70,000 using random nonces — never reuse a (key, nonce) pair.

## Decision rules

1. Never roll your own. Use vetted libraries: libsodium/NaCl, OpenSSL/BoringSSL, Go's `crypto`, Python `cryptography`, `age`.
2. Passwords need a slow, memory-hard KDF, not a general hash.
3. Nonce discipline: 96-bit nonce, random-per-message or a strictly-increasing counter; rotate the key before the counter wraps.
4. Prefer TLS 1.3; keep TLS 1.2 with strong ciphers as fallback; disable 1.0/1.1.
5. Crypto-agility: isolate every crypto call behind one interface so the algorithm can be swapped without touching business logic — the hedge against the PQC timeline.
6. Managed KMS with envelope encryption (data key under a key-encryption key in an HSM) for data at rest; a solo never handles the root key.
7. FIPS-validated modules only where a requirement demands them.

## Procedure

1. Inventory every crypto call: hashing, encryption, signing, random generation, TLS configuration.
2. Replace any home-grown primitive or mode with a library AEAD; set the nonce rule.
3. Confirm password hashing uses an approved KDF with benchmarked parameters (subskills/authentication.md).
4. Configure TLS 1.2/1.3 at the edge; enable HSTS with a short `max-age` first, then ramp.
5. Route data-at-rest encryption through managed KMS envelope encryption; never store the root key.
6. Record where RSA/ECC are used; prefer hybrid PQC key exchange when the TLS stack supports it; keep each call behind the interface.
7. Record the crypto decisions in an ADR; the PQC migration path is a design decision.

## Anti-patterns

- Base64 or ROT-n presented as "encryption".
- Unauthenticated CBC/CTR modes.
- Reusing a nonce, or a random nonce at scale without a rotation bound.
- Custom padding, custom key schedules, "our own hash".
- Treating a signed JWT as confidential — signed, not encrypted.

## Done checklist

- [ ] Every crypto call inventoried; none hand-rolled.
- [ ] AEAD everywhere; nonce rule documented and enforced.
- [ ] Password hashing uses an approved KDF with benchmarked parameters.
- [ ] TLS 1.2/1.3 only; 1.0/1.1 disabled; HSTS ramped safely.
- [ ] Data-at-rest encryption via managed KMS envelope encryption.
- [ ] RSA/ECC usages recorded; hybrid PQC preferred where available.
- [ ] Crypto interfaces isolate algorithm choice.

## Sources

- Primary: OWASP Cryptographic Storage and Password Storage Cheat Sheets; RFC 8439; Bock et al. WOOT '16; NIST FIPS 203/204/205 (2024-08-13); NIST IR 8547 (2024-11); NSA CNSA 2.0 (2025-05-30).
- <https://csrc.nist.gov/pubs/fips/203/final>
- <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>
