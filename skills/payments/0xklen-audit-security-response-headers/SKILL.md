---
name: audit-security-response-headers
description: Use when reviewing what browser-side protections a web app declares. Checks CSP, HSTS, X-Content-Type-Options, Referrer-Policy, frame-ancestors, and permissions policy on live responses.
---

# Audit security response headers

Response headers move protection into the browser: they stop MIME sniffing, framing, downgrade to
HTTP, and — via a good CSP — most script injection. They are cheap to add and easy to get subtly
wrong, so they are observed from a live response, never from a documentation page.

## Procedure

1. Fetch headers from the real origin, following redirects to see what the final page returns:

       curl -sI https://app.example.com/ | tee /tmp/headers.txt
       curl -s -D - -o /dev/null -X GET https://app.example.com/ | rg -i '^(strict-transport|content-security|x-content|x-frame|referrer|permissions-policy)'

2. Check each one against its job:

   | Header | Target value | Stops |
   |---|---|---|
   | `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | downgrade/SSLstrip |
   | `Content-Security-Policy` | `default-src 'self'; object-src 'none'; base-uri 'none'` | XSS, injection |
   | `X-Content-Type-Options` | `nosniff` | MIME sniffing |
   | `Referrer-Policy` | `strict-origin-when-cross-origin` or `no-referrer` | URL leak |
   | `frame-ancestors` (in CSP) | `'none'` | clickjacking |
   | `Permissions-Policy` | deny unused features | feature abuse |

3. For CSP, hunt the escape hatches: `'unsafe-inline'`, `'unsafe-eval'`, `data:` in `script-src`,
   and wildcard hosts. A nonce or hash beats `unsafe-inline`.

       rg -i "unsafe-inline|unsafe-eval|script-src[^;]*\*" /tmp/headers.txt

4. Prefer `frame-ancestors` in CSP over the legacy `X-Frame-Options`; ship `X-Frame-Options: DENY`
   too if you must support old browsers.

5. Deploy CSP in report-only first (`Content-Security-Policy-Report-Only`) with a `report-uri`/
   `report-to`, watch for violations, then enforce.

6. Verify HSTS is only sent over HTTPS and that you are not relying on it before the first visit
   (the very first request is still plaintext; preload closes that gap).

## Pitfalls

- `max-age=0` (a common copy-paste) disables HSTS while looking present.
- CSP with `'unsafe-inline'` in `script-src` is nearly useless as XSS defence.
- Setting CSP via a meta tag ignores `frame-ancestors` — that directive must be a header.
- Headers on the app but not on static/CDN responses leave assets unprotected.
- `X-XSS-Protection` is deprecated; do not rely on it or the legacy auditor.
- A wildcard `default-src *` mid-string can override an earlier restrictive directive by sourcing
  flow; read the whole policy, not the first token.

## Verification

    curl -sI https://app.example.com/ | tr -d '\r' | rg -i \
      'strict-transport-security|content-security-policy|x-content-type-options|referrer-policy'

Pass: HSTS has `max-age` >= 31536000, CSP lacks `unsafe-inline`/`unsafe-eval`, and `nosniff` and a
referrer policy are present. Report each header's value and every weak directive found.
