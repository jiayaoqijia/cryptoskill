---
name: enforce-csrf-protection
description: Use when a state-changing endpoint may accept a forged cross-site request. Confirms which mutation routes lack a token or SameSite defence, adds synchronizer tokens, and tests with a foreign Origin.
---

# Enforce CSRF protection

Cross-site request forgery makes the victim's browser send an authenticated request the user never
intended. Cookie-based sessions are the risk: the browser attaches the cookie automatically, so the
server must demand a second, unguessable proof that the request originated from your own page.

## Procedure

1. List the state-changing routes: POST, PUT, PATCH, DELETE, and any GET that mutates.

       rg -n "\.(post|put|patch|delete)\(|methods=\[.*'(POST|PUT|PATCH|DELETE)'" src/ | tee /tmp/mutating.txt

2. For each, check which defence is present:

   - a per-session synchronizer token validated server-side, or
   - `SameSite=Lax`/`Strict` on the session cookie, or
   - a double-submit cookie compared constant-time, or
   - an `Origin`/`Referer` check against an allowlist.

   A route with none of these is exposed.

3. Add the synchronizer token. The token must be tied to the session and compared in constant time:

       # Flask-WTF style
       @app.before_request
       def csrf_protect():
           if request.method in ("POST","PUT","PATCH","DELETE"):
               token = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
               if not secrets.compare_digest(token or "", session.get("csrf", "")):
                   abort(403)

4. For JSON APIs that skip tokens, require a custom header (`X-Requested-With`) *and* an `Origin`
   allowlist — a cross-site form cannot set arbitrary headers, but keep both checks.

5. Ensure `SameSite` is not `None` without `Secure`; treat `SameSite` as defence in depth, not the
   only control (older browsers and some flows ignore it).

6. Exempt only genuinely public, unauthenticated, idempotent routes, and justify each exemption.

7. Test: send a valid request with a foreign `Origin` and no token and expect 403.

       curl -s -X POST https://app.example.com/api/transfer \
         -H 'Origin: https://evil.example' -H 'Cookie: sid=<victim>' \
         -d 'to=attacker&amount=100' -o /dev/null -w '%{http_code}\n'

## Pitfalls

- Validating the token but not binding it to the session lets an attacker reuse their own token
  against a victim.
- A `GET` route that mutates bypasses token forms entirely; move it to `POST`.
- Checking `Referer` only when present: a request with no `Referer` must fail closed.
- Substring or prefix matches on `Origin` (`startsWith("https://app.example.com")`) admit
  `https://app.example.com.evil.com`.
- CORS does not prevent CSRF: simple cross-site requests skip preflight.
- Double-submit without signing is bypassable if an attacker can set cookies (subdomain takeover).

## Verification

    for m in POST PUT PATCH DELETE; do \
      code=$(curl -s -X $m https://app.example.com/api/profile \
        -H 'Origin: https://evil.example' -H "Cookie: sid=$VICTIM" -o /dev/null -w '%{http_code}'); \
      echo "$m $code"; \
    done

Pass: every mutating verb returns 403 or 419 without a valid token, and the legitimate same-origin
request still succeeds. Report the routes checked, the defence chosen per route, and any justified
exemptions.
