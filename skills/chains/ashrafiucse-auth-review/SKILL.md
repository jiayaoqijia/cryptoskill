---
name: auth-review
description: Reviews authentication and authorization in any codebase — login flows, password storage, session/cookie handling, JWT pitfalls, OAuth/OIDC misconfigurations, IDOR/broken access control, privilege escalation, and CSRF protection. Use when auditing how users log in, how permissions are enforced, or when reviewing auth-related code changes.
license: MIT
---

# Authentication & Authorization Review

## 1 — Map the auth architecture first

Find: login/register/password-reset endpoints, session middleware, role/permission checks, token creation/validation, OAuth client configs. Write a 3-line model: *who can authenticate how → what identity looks like → where authorization is enforced.* Broken access control is much easier to spot once you know the intended model.

## 2 — Authentication checks

### Password storage
```bash
rg -n -i "bcrypt|argon2|scrypt|pbkdf2|md5|sha1|sha256.*password|hashpw|crypt\("
```
- `bcrypt`/`argon2id`/`pbkdf2` with sane params (bcrypt cost ≥ 10, argon2id defaults or better) → OK
- MD5/SHA1/SHA-256 for passwords → **CRITICAL** (unsalted fast hash = instant crack)
- Plaintext or reversible encryption → **CRITICAL**

### Login mechanics
- User enumeration: login and password-reset responses differ for unknown vs wrong-password (timing or body) → MEDIUM
- No rate limiting / lockout on login, reset, and MFA endpoints → HIGH (note where it would live: middleware, API gateway, app code)
- Password reset: predictable token (timestamp, userid, `random.random()`), token reused or non-expiring, reset response leaks the token → HIGH/CRITICAL
- MFA present? Missing MFA on admin accounts → HIGH if roles exist

### JWT / tokens
```bash
rg -n "jwt\.(sign|decode|verify)|verify\(|algorithms|algorithm|none|HS256|RS256"
```
- `algorithm: "none"` accepted or `jwt.decode(token)` without algorithm pinning → **CRITICAL**
- Symmetric signing with weak/default secret (`secret`, `jwt-secret`, `changeme`) → CRITICAL
- No `exp` validation, or no `aud`/`iss` checks where multiple services share keys → HIGH
- Tokens in localStorage with XSS present elsewhere → MEDIUM (compounding)
- Session tokens: not rotated on login/privilege change → MEDIUM; long-lived non-revocable tokens → HIGH

## 3 — Authorization checks (IDOR & friends)

Find object access points, then check each for an ownership/scope test:
```bash
rg -n "req\.params\.id|findById\(|get\(|\.filter\(.*userId|user\.id|currentUser|req\.user"
```
- `Model.findById(req.params.id)` returned directly with no `where userId` / post-fetch ownership check → **IDOR**, HIGH (CRITICAL for sensitive objects: invoices, messages, PII)
- Admin routes: how are they guarded? Missing middleware → CRITICAL. Note *function-level* checks too (regular user hitting `/admin/*` handlers).
- Horizontal vs vertical: test reasoning for both — same-role users touching each other's data, and low-role → admin.
- Trusting client-side hints: `is_admin` from request body/cookie-in-JWT-without-verify, hidden-but-served admin UI → HIGH

## 4 — Session & CSRF

- Cookie flags on session/auth cookies: `HttpOnly` (missing + XSS present → HIGH), `Secure` (missing → HIGH if prod is HTTPS), `SameSite` (missing → MEDIUM)
- CSRF: state-changing endpoints protected by token/`SameSite=Strict`/`Origin` check? Both auth-cookie AND no CSRF defense → HIGH
- Logout invalidates server-side session? Not just client cookie clear → MEDIUM
- Session fixation: session ID regenerated after login → check

## 5 — OAuth/OIDC, if present

- `redirect_uri` validated exactly (not prefix/suffix match) → open redirect_uri = account takeover, CRITICAL
- `state` parameter present and verified → missing = CSRF/login CSRF, MEDIUM/HIGH
- Token in URL fragment vs query (query leaks via logs/referrers) → MEDIUM
- `id_token` validated: signature, `nonce`, `aud` → skipping any = CRITICAL

## Reporting

For each finding: severity, `file:line`, one-line exploit story ("authenticated user A reads user B's invoice by changing `?id=`"), and the concrete fix (ownership scope in query, middleware, flag). Group IDORs by endpoint pattern — they usually cluster.
