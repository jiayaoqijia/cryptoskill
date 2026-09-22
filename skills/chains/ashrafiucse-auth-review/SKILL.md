---
name: auth-review
description: Reviews authentication and authorization in any codebase — login flows, password storage, session/cookie handling, JWT pitfalls, OAuth/OIDC misconfigurations, IDOR/broken access control, privilege escalation, CSRF protection, route census for unguarded endpoints, trusted-header identity spoofing, check-then-act race conditions (TOCTOU), and WebSocket/SSE authorization. Use when auditing how users log in, how permissions are enforced, how internal services trust each other, or when reviewing auth-related code changes.
license: MIT
---

# Authentication & Authorization Review

## 1 — Map the auth architecture first

Find: login/register/password-reset endpoints, session middleware, role/permission checks, token creation/validation, OAuth client configs. Write a 3-line model: *who can authenticate how → what identity looks like → where authorization is enforced.* Broken access control is much easier to spot once you know the intended model.

### Route census (enumerate, don't guess)

Pattern greps find what they look for; a census finds what nobody remembered. Enumerate EVERY route, then check each one:

```bash
rg -n "app\.(get|post|put|patch|delete|all|use)\("            # Express/Koa
rg -n "@app\.route\(|@\w+\.route\(|add_url_rule"              # Flask
rg -n "path\(|re_path\(" */urls.py                             # Django
rg -n "^\s*(get|post|patch|put|delete) |resources " config/routes.rb  # Rails
rg -n "@(Get|Post|Put|Patch|Delete|Request)Mapping"             # Spring
rg -n "Route::(get|post|any|resource|apiResource)" routes/     # Laravel
rg -n "@(app|router)\.(get|post|put|delete|patch)"             # FastAPI
```

Build a table `route → auth middleware → ownership check` and fill it by reading each handler. Every row with **neither** is a finding (Critical for admin/state-changing, High otherwise). Census-only catches:
- routes registered BEFORE the auth middleware (order bugs — `app.use(auth)` must precede every guarded route)
- the one handler missing `@login_required` / `authorize` / `auth:sanctum` in an otherwise-guarded file
- non-HTTP surfaces that are routes in disguise: queue consumers, cron/background job handlers, webhook receivers, GraphQL resolvers (see `../graphql-security/SKILL.md`), event subscribers, RPC/message handlers — census them with the same table
- dispatch-style apps (`?action=` → switch) — enumerate the switch arms, not the single URL

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
- **Algorithm confusion** (RS256 → HS256): `jwt.verify(token, PUBLIC_KEY, {algorithms: ['HS256', ...]})` — attacker signs with the public key as HMAC secret → **CRITICAL**. Pin asymmetric algorithms only when the key is public; never pass a public key where the library accepts it for HMAC.
```bash
rg -n "algorithms.*HS256|verify\(.*public|createPublicKey|jwt\.RSAPublicKey" 
```
- **JWKS `kid` injection**: token-controlled `kid`/`alg`/`jku`/`x5u` header flowing into paths, queries, or fetches (`'./keys/' + header.kid`, `jwks_url + kid`) → path traversal / attacker-controlled key material → **Critical**. Trust `kid` for lookup only against a fixed key set.
```bash
rg -n "header\.kid|\bkid\b.*\+|jku|x5u" 
```
- **PKCE**: public clients (SPA/mobile/desktop — anything that can't hold a secret) using auth-code flow without `code_challenge`/`code_verifier` → code interception, HIGH. Server-side confidential clients may omit it (note, not a finding).
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

### Mass assignment (generic)

The framework skills cover Laravel/Django/Rails fillable semantics; the generic version bites every ORM:
```bash
rg -n "\.create\(\s*req\.body|\.update\(\s*req\.body|Object\.assign\(\s*\w+\s*,\s*req\.body|new \w+\(\s*req\.body|findOneAndUpdate\(\s*\w+,\s*req\.body|bulkCreate\(\s*req\.body"
```
Request body spread into create/update without an allowlist → attacker sets `role`, `isAdmin`, `userId`, `credits`, `price`, `email` (account takeover via email change). Report **High** — Critical when the model has role/permission fields. Safe: explicit field destructuring/pick, schema-level allowlist (`$fillable`, `fields`), validators configured to strip unknown keys (default `validate`/zod `.strict()` — not passthrough). Also check filter/map "sanitizers" that only check types: an allowLIST of keys, not of types, is what counts.

### Trusted-header authorization (identity spoofing)
```bash
rg -n -i "req\.headers\[\s*['\"]x-|request\.headers\.get\(|getHeader\(\s*\"X-|headers\[\s*'X-|x-forwarded-for|x-forwarded-user|x-real-ip|HTTP_X_"
```
Using `X-User-Id` / `X-Email` / `X-Admin` / `X-Forwarded-For` as the **identity or authz input** means anyone who can reach the service directly is any user → **CRITICAL**. Valid only when BOTH hold: (1) an edge proxy/gateway strips these headers from inbound traffic, and (2) the app is not directly reachable (check NodePort/LoadBalancer services, ingress annotations, port exposure in compose). Microservice meshes are the classic miss: service B trusts `X-User-Id` "because only service A calls us" — but anything on the cluster network can. Headers used only for logging (`X-Request-Id`) are fine — trace the value into an authz decision before flagging.

### Check-then-act races (TOCTOU)
Look for state checks followed by a **separate** write:
```bash
rg -n "if\s*\(.*\b(used|redeemed|approved|active|enabled|stock|balance|remaining)\b|\.findOne\(.*\)\.then|SELECT.*\b(balance|stock|used)\b.*FROM|\.save\(\)"
```
- Single-use coupons/tokens/reset links: `if (t.used) reject; ... t.used = true` → parallel replay wins every time → **High** (Critical for payments/refunds/webhooks). Fix: atomic conditional write — `findOneAndUpdate({code, used:false}, {$set:{used:true}})`, `UPDATE ... SET used=1 WHERE code=? AND used=0` checking rows affected.
- Balance/stock read-modify-write: `user.balance -= amt; user.save()` → double-spend under concurrency. Fix: `UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?`.
- Webhooks/event handlers without idempotency keys or event-id dedup → replayable. Report as one grouped finding with every affected flow listed.

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

## 6 — Realtime channels (WebSocket / SSE)

```bash
rg -n "io\.on\(|socket\.on\(|new WebSocket|WebSocketServer|@MessageMapping|@SubscribeMapping|STOMP|EventSource|ActionCable|cable\.|channel\.subscribe"
```

- **Handshake auth**: no `io.use(authMiddleware)` / token check on connect → **CRITICAL** (any client connects as anyone)
- **Subscription authz**: `socket.join('room:' + id)` / channel subscribe without ownership check → IDOR over sockets, **High** — same rule as REST IDOR, different transport
- **Message handlers are routes**: every `socket.on('cmd', ...)` doing a state change needs authz; grep the handler bodies exactly like controllers
- `io.origins('*')` / missing origin check on a credentialed socket → Medium (cross-site WebSocket hijacking)
- SSE (`EventSource` endpoints) are plain GETs — same authz as any other route

## Reporting

For each finding: severity, `file:line`, one-line exploit story ("authenticated user A reads user B's invoice by changing `?id=`"), and the concrete fix (ownership scope in query, middleware, flag). Group IDORs by endpoint pattern — they usually cluster.
