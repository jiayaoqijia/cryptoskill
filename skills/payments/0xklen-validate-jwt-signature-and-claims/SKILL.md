---
name: validate-jwt-signature-and-claims
description: Use when a service trusts a JWT for identity or authorization. Checks signature verification, rejects alg=none and algorithm confusion, validates exp/aud/iss, and pins the key source.
---

# Validate JWT signature and claims

A JWT is only as trustworthy as its signature check. The classic bugs are accepting `alg: none`,
accepting any algorithm the token names, and parsing without verifying). Even a valid signature
proves nothing about audience or expiry unless those claims are checked too.

## Procedure

1. Find where tokens are verified, and confirm the library call actually verifies:

       rg -n "jwt\.(decode|verify)|jsonwebtoken|jose|PyJWT|jwt\.Parse" src/

   In PyJWT, `jwt.decode(token, key)` verifies; `jwt.decode(token, options={"verify_signature": False})`
   and a bare `jwt.get_unverified_claims` do not.

2. Pin the expected algorithm on the verify call; never let the token choose it:

       # Python / PyJWT — explicit algorithms list
       jwt.decode(token, key, algorithms=["RS256"], audience="api", issuer="https://auth.example.com")
       # Node / jsonwebtoken
       jwt.verify(token, publicKey, { algorithms: ["RS256"], audience: "api", issuer: "..." });

   An empty or missing `algorithms` list permits `none` and HS/RS confusion.

3. Reject `alg: none` explicitly and reject a symmetric verify when you expect asymmetric: if the
   token is signed `HS256` with your *public* key as the HMAC secret, an attacker who has the public
   key can forge tokens. Fix by fixing the algorithm, not by trusting the header.

4. Validate every relevant claim: `exp` (not expired), `nbf` (not premature), `iat`, `aud` (this
   service, not another), `iss` (the expected issuer), and any `azp`.

5. Fetch keys from the issuer's JWKS over HTTPS and pin/refresh them; do not accept a `jku` or `x5u`
   header pointing at an attacker-controlled URL, and validate `kid` against the known set.

6. Keep access-token lifetimes short (minutes) and pair with a checked refresh flow; verify the
   signature on every request rather than caching "valid" forever.

7. Test with three degenerate tokens: `alg:none`, RS256→HS256 re-signed with the public key, and an
   expired token. Each must be rejected.

       alg=none token:  eyJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbiJ9.
       python3 -c "import jwt; print(jwt.decode(open('/tmp/t.txt').read(), 'pub', algorithms=['HS256','RS256']))"

## Pitfalls

- `jwt.decode(token, verify=False)` / `options={'verify_signature': False}` disables the only check
  that matters.
- Libraries that default to "any algorithm" are the root of alg-confusion CVEs; pass the list.
- Checking `exp` in seconds vs milliseconds fails silently; know the unit.
- `aud` is often omitted from validation, so a token minted for one service works on another.
- `kid` path traversal (`../../dev/null`) can force an empty key if the verifier reads files.
- Base64url padding differences can make a round-trip comparison miss a tampered payload.

## Verification

    python3 - <<'PY'
    import jwt
    for name, tok in [("none","eyJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbiJ9.")]:
        try:
            jwt.decode(tok, "k", algorithms=["RS256"], options={"verify_signature": True})
            print(name, "ACCEPTED  <-- BUG")
        except jwt.InvalidTokenError as e:
            print(name, "rejected:", type(e).__name__)
    PY

Pass: the `none` and confusion tokens are rejected and the decode call names an explicit algorithm
list plus audience and issuer. Report the verify call, its algorithm pin, and the claims checked.
