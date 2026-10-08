---
name: harden-session-cookie-attributes
description: Use when reviewing how an application stores and transmits a login session. Inspects cookie flags, fixes missing Secure/HttpOnly/SameSite and no-rotation bugs, and verifies with curl.
---

# Harden session cookie attributes

A session cookie is a bearer token: whoever holds it is the user. The flags on that cookie are the
only thing stopping script access, network sniffing, and cross-site replay, so they are checked
individually rather than assumed from framework defaults.

## Procedure

1. Observe the actual `Set-Cookie` on login rather than reading config:

       curl -si -X POST https://app.example.com/login \
         -d 'user=demo&pass=demo' | rg -i '^set-cookie:'

2. Check each attribute against its job:

   | Attribute | Required | Rejects |
   |---|---|---|
   | `HttpOnly` | yes | JS read via XSS |
   | `Secure` | yes | plaintext transport |
   | `SameSite=Lax` or `Strict` | yes | cross-site CSRF replay |
   | `Path=/` | scoped | over-broad scope leak |
   | `Domain` | omitted (host-only) | subdomain injection |
   | `Max-Age`/`Expires` | bounded | immortal sessions |

3. Prefer the `__Host-` prefix, which the browser only accepts with `Secure`, `Path=/`, and no
   `Domain`:

       Set-Cookie: __Host-sid=<token>; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=86400

4. Rotate the session id on every privilege change — login, password change, and role elevation —
   to close session fixation:

       # after successful auth
       request.session.cycle_key()          # Django
       # or regenerate the id before writing the cookie

5. Set an idle timeout (e.g. 30 min) and an absolute cap (e.g. 12 h) and enforce both server-side.

6. Invalidate server-side on logout, not just by clearing the cookie client-side; a stolen copy
   must stop working.

7. Never store session ids in `localStorage`; that is JavaScript-readable and defeats `HttpOnly`.

## Pitfalls

- `SameSite=None` silently requires `Secure`; without it browsers drop the cookie entirely.
- A `Domain=.example.com` cookie is sent to every subdomain, so one XSS on an old host takes the
  session.
- Clearing a cookie on logout without deleting the server record leaves a valid token.
- Session id in the URL (for "shareable" links) leaks via Referer and logs.
- Frameworks default `SameSite` differently across versions — verify, do not assume.
- Rolling `Max-Age` on every request makes the idle timeout moot unless the absolute cap is kept.

## Verification

    curl -si https://app.example.com/login -d 'user=demo&pass=demo' \
      | rg -i '^set-cookie:' | rg -q 'HttpOnly' && rg -q 'Secure' && echo OK || echo MISSING-FLAG
    # session-fixation check: id before login must differ from id after
    test "$(curl -s .../login -c - | awk '/sid/{print $7}')" != "$(pre_login_id)" && echo ROTATED

Pass: the cookie carries `Secure`, `HttpOnly`, and `SameSite`, uses the `__Host-` prefix or omits
`Domain`, and the id changes across login. Report each attribute observed and the rotation result.
