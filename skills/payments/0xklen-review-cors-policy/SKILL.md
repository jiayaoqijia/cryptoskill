---
name: review-cors-policy
description: Use when an API sets Access-Control-Allow-Origin and may expose data to other origins. Checks origin reflection, credentialed wildcards, and parsing bugs, then restricts to an allowlist.
---

# Review CORS policy

CORS is a browser-enforced relaxation of the same-origin policy; a wrong policy hands another site
read access to your users' data. The dangerous patterns are reflecting any origin and combining a
wildcard with credentials.

## Procedure

1. Observe the headers for a benign request and for a foreign origin:

       curl -sI -H 'Origin: https://evil.example' https://api.example.com/me | rg -i \
         '^access-control-allow-(origin|credentials|methods|headers)|^vary'

2. Check for origin reflection — the response echoing the request's `Origin`:

       if the `Access-Control-Allow-Origin` equals `https://evil.example`, the policy reflects; with
       `Access-Control-Allow-Credentials: true` this is a full data-exfiltration bug.

3. Confirm the wildcard trap: `Access-Control-Allow-Origin: *` together with
   `Access-Control-Allow-Credentials: true` is rejected by browsers, but a *reflected* origin is not
   — reflection with credentials is the real risk.

4. Inspect the origin-matching code for prefix/suffix mistakes:

       rg -n "Access-Control-Allow-Origin|allow_origin|add_cors|cors\(" src/

   Bugs to look for: `origin.startsWith("https://app.example.com")` (accepts
   `...example.com.evil.example`), `origin.endsWith("example.com")` (accepts
   `evil-example.com`), or a regex without anchors / with `.` unescaped.

5. Fix with a strict allowlist and echo only exact matches:

       ALLOWED = {"https://app.example.com", "https://admin.example.com"}
       if origin in ALLOWED:
           resp.headers["Access-Control-Allow-Origin"] = origin
           resp.headers["Access-Control-Allow-Credentials"] = "true"
           resp.headers["Vary"] = "Origin"           # cache correctness

6. Do not reflect for unauthenticated public APIs either; use `*` without credentials when data is
   genuinely public.

7. Keep the method/header allowlist tight (`GET,POST` not `*`), and only enable credentials if the
   endpoint actually needs cookies.

8. Test with a credentialed fetch from a foreign page and confirm the browser blocks the read.

## Pitfalls

- `null` origin (from sandboxed iframes and `file://`) is sometimes on the allowlist; it is
  attacker-controllable.
- Missing `Vary: Origin` lets a shared cache serve one origin's CORS response to another.
- A permissive CORS on a JSON API with cookie auth is equivalent to no same-origin policy.
- Wildcard subdomain patterns (`*.example.com`) include hosts you do not control if any subdomain is
  user-registered.
- Preflight (`OPTIONS`) handled by a different layer than the actual route can disagree on the
  policy.
- Reflections of the `Origin` header also break when it is absent; handle the null case explicitly.

## Verification

    for o in 'https://evil.example' 'null' 'https://app.example.com'; do \
      acao=$(curl -sI -H "Origin: $o" https://api.example.com/me | rg -i '^access-control-allow-origin' | tr -d '\r'); \
      echo "$o -> $acao"; \
    done

Pass: only the known app origin is echoed; `null` and `evil.example` get no
`Access-Control-Allow-Origin` (or a non-credentialed `*`). Report the observed policy, the matching
rule, and the origins now allowed.
