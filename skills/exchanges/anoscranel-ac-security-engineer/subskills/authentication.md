---
name: authentication
domain: security-hardening/authentication
trigger: "Building or reviewing how users prove identity: password storage, MFA, passkeys, account recovery and anti-enumeration."
anti_trigger: "Keeping the authenticated state over time — sessions and tokens (subskills/sessions-tokens.md); what an authenticated user may do (subskills/authorization.md)."
scope: "Passwords (hashing), MFA, passkeys, recovery, per 800-63B-4"
status: "seedling"
---

# Authentication

## Standard

- OWASP Password Storage Cheat Sheet: **Argon2id** with `m≥19456 KiB (19 MiB), t=2, p=1` (alternatives 46 MiB t=1 or 12 MiB t=3); scrypt `N=2^17, r=8, p=1`; legacy bcrypt work factor ≥10 (72-byte limit); PBKDF2-HMAC-SHA-256 ≥600,000 iterations only where FIPS-140 is required. Unique random salt per password (https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).
- NIST SP 800-63B-4, **final July 2025** (CSRC history 07/31/25; announced 2025-08-01): verifiers SHALL blocklist the secret, SHALL allow ≥64 characters, SHALL NOT impose composition rules, SHALL NOT require periodic rotation. AAL2 offers a phishing-resistant option; AAL3 uses a phishing-resistant authenticator with a non-exportable key (https://csrc.nist.gov/pubs/sp/800/63/b/4/final).
- OWASP Multifactor Authentication Cheat Sheet names push-fatigue, reverse-proxy phishing, SIM swap, device-binding bypass and downgrade attacks.
- OWASP Passkey Security Cheat Sheet and Forgot Password Cheat Sheet (reset tokens long, stored securely, single-use, expiring; identical responses whether or not the account exists).

## Decision rules

1. Order the factors: passkey/hardware key > TOTP > number-matching push > SMS. SMS is fallback only — phone-number takeover defeats it.
2. Use the framework's auth library or a managed provider; confirm its defaults meet the cheat-sheet parameters. Hand-rolled hashing is an anti-pattern.
3. A pepper is optional defence in depth stored outside the database; skip it unless you already run a secrets vault (subskills/secrets.md).
4. Recovery is the bypass of your strongest factor: single-use expiring links, never reflected in the page, rate-limited.
5. Return one neutral message on login, registration and reset — "email already registered" on signup is enumeration.

## Procedure

1. Check the library's password-hash parameters against the cheat sheet; benchmark on your own hardware.
2. Load a breach-corpus blocklist (or the provider's) for password checks.
3. Offer passkeys (WebAuthn) through a maintained library; never validate ceremony fields by hand.
4. Build recovery: generate a long random token, store it hashed, single-use, expiring; deliver by link or `HttpOnly` cookie token; rate-limit.
5. Make login, registration and reset responses identical in content and timing for existing and non-existing accounts.
6. Test with two accounts: a real one and a random one; the responses must be indistinguishable.

## Anti-patterns

- MD5/SHA-1 for passwords — fast general hashes, cheap on GPUs.
- Forced composition rules or scheduled rotation (SP 800-63B-4 forbids both).
- SMS as the primary MFA method.
- Enumerating accounts via signup, reset or login timing.
- Implementing WebAuthn ceremony validation yourself instead of using a maintained server library.

## Done checklist

- [ ] Hash parameters verified against the OWASP cheat sheet.
- [ ] Blocklist, ≥64-char allowance, no composition rules, no forced rotation.
- [ ] Phishing-resistant factor offered (AAL2) where users can adopt it.
- [ ] Recovery tokens single-use, hashed, expiring, rate-limited.
- [ ] Anti-enumeration verified with the two-account test.
- [ ] Passkey ceremony handled by a maintained library.

## Sources

- Primary: OWASP Password Storage, MFA, Passkey Security and Forgot Password Cheat Sheets; NIST SP 800-63B-4.
- <https://pages.nist.gov/800-63-3/sp800-63b.html>
- <https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html>
