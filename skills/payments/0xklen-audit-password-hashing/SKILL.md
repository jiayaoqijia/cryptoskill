---
name: audit-password-hashing
description: Use when reviewing how user passwords are stored or verified. Checks for a memory-hard algorithm and cost factor, rules out fast hashes, and verifies comparison is constant-time.
---

# Audit password hashing

Passwords must be stored with a slow, salted, memory-hard function; anything fast enough to brute
force at scale (MD5, SHA-1, SHA-256, even with a salt) is inadequate. The parameters matter as much
as the algorithm name.

## Procedure

1. Find the hashing call and its algorithm:

       rg -n "md5|sha1|sha256|sha512|hashlib|bcrypt|argon2|scrypt|pbkdf2|password_hash|bcrypt\." src/ \
         | rg -i "pass|credential|secret"

2. Reject fast hashes outright. A salt stops rainbow tables but not per-password GPU brute force;
   SHA-256 at ~billions/sec falls in minutes.

3. Prefer, in order: Argon2id, scrypt, bcrypt. Check the cost parameter, not just the function:

   | Algo | Minimum sane setting (2024) |
   |---|---|
   | bcrypt | cost 12 (≈250 ms) |
   | Argon2id | m=19456 (19 MiB), t=2, p=1 |
   | scrypt | N=2^15, r=8, p=1 |
   | PBKDF2 | 600 000+ SHA-256 iterations (last resort) |

4. Confirm salts are per-password and random (they are embedded in bcrypt/argon2 strings). A single
   global salt or no salt is a finding.

5. Verify the comparison is constant-time. `==` on the digest leaks via timing; libraries expose a
   safe check:

       import bcrypt
       if bcrypt.checkpw(password.encode(), stored_hash): ...   # constant-time, parse-safe
       # Python hmac: hmac.compare_digest(a, b)

6. Handle algorithm migration: store the algorithm in the hash string and re-hash on next successful
   login when the cost is below target.

       if bcrypt.checkpw(pw, h) and bcrypt.cost(h) < 12:
           store(bcrypt.hashpw(pw, bcrypt.gensalt(12)))

7. Cap input length and normalise Unicode (NFC) before hashing; bcrypt truncates at 72 bytes, so
   pre-hash with SHA-256 if longer passwords must be supported.

## Pitfalls

- `hashlib.sha256(salt + password)` with a per-user salt is still a fast hash and is not acceptable.
- bcrypt cost 4-8 (test defaults) ships to production all the time; verify the real parameter.
- Peppers (an app-wide secret mixed in) help but do not replace a slow algorithm, and a rotated
  pepper invalidates every hash.
- Comparing hashes with `==` in Python/JS is a timing oracle.
- Silent truncation: two long passwords sharing the first 72 bytes collide under plain bcrypt.
- Re-hashing only on password change leaves the whole user base on the old parameter for years.

## Verification

    python3 -c "import bcrypt,sys; h=sys.argv[1].encode(); print('cost', bcrypt.cost(h))" '$HASH'
    rg -n "hashlib\.(md5|sha1|sha256)" src/ && echo "FAST HASH PRESENT" || echo "no fast hash"

Pass: every stored hash uses Argon2id/scrypt/bcrypt at or above the table's setting, no fast hash
appears in password code, and comparison is via the library's check function. Report the algorithm,
cost, salt source, and the migration path.
