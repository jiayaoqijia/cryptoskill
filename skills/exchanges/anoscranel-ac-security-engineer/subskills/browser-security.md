---
name: browser-security
domain: security-hardening/browser-security
trigger: "Building or reviewing anything the browser executes: pages, scripts, cookies, CORS, security headers, CSRF protection for state-changing requests."
anti_trigger: "Server-side input and output rules (subskills/input-output.md); session token lifetime and storage (subskills/sessions-tokens.md)."
scope: "XSS, CSRF, CORS, CSP and security headers, cookies"
status: "seedling"
---

# Browser-Side Attacks

## Standard

- OWASP Cross-Site Scripting Prevention Cheat Sheet: context-aware output encoding (HTML body, attribute, JavaScript, URL and CSS are different encodings); ASVS V1.2.1 (L1).
- OWASP Content-Security-Policy Cheat Sheet: CSP is defence in depth for the XSS that slips through.
- OWASP Cross-Site Request Forgery Prevention Cheat Sheet: `SameSite` cookies plus a CSRF token (or double-submit) for state-changing requests.
- OWASP HTTP Headers Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet); MDN references for HSTS and cookies.
- ASVS 5.0 V3 Web Frontend Security (a new standalone chapter). CWE Top 25 2025: CWE-79 XSS #1, CWE-352 CSRF #3.

## Decision rules

1. Rely on framework auto-escaping (React, Vue, Angular); audit the residual sinks: `dangerouslySetInnerHTML`, `v-html`, `|safe`, `innerHTML`, `document.write`.
2. Set `SameSite=Lax` at minimum, `Strict` where possible; **never `SameSite=None` without `Secure`**.
3. Use the `__Host-` cookie name prefix where possible; keep `Domain` narrow.
4. CSP is the backstop, not the fix: it mitigates exploitation, it does not make XSS safe.
5. CORS: never `Access-Control-Allow-Origin: *` with credentials. Echo only an allow-listed origin — browsers reject wildcard-plus-credentials, but a reflected origin is not rejected.

## Procedure

1. Set the header baseline once at the edge or framework, not per route:

```http
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()
X-Frame-Options: DENY          # only where CSP frame-ancestors is unavailable
X-XSS-Protection: 0            # OWASP: do NOT set the legacy filter — it can create XSS
```

2. Audit every raw-HTML sink and DOM sink in the frontend; replace with framework-safe rendering.
3. Add a CSRF token to every state-changing form/fetch; verify server-side.
4. Configure the CORS origin allow-list explicitly, per environment.
5. Verify with an external header checker (securityheaders.com) and a browser console CSP report.

## Anti-patterns

- Setting `X-XSS-Protection: 1` — the legacy filter can itself create XSS (OWASP).
- A wildcard CORS origin with `Allow-Credentials: true`.
- Duplicating header logic per route, so one route silently misses it.
- Long HSTS `max-age` plus `preload` on a host with cert-automation gaps: a bad cert can lock users out until expiry. Start short and ramp.

## Done checklist

- [ ] Header baseline set once, at the edge.
- [ ] No raw-HTML sink renders untrusted data unescaped.
- [ ] CSRF token verified on every state-changing request.
- [ ] Cookies carry `Secure`, `HttpOnly`, `SameSite`, narrow `Domain`.
- [ ] CORS echoes only allow-listed origins; no wildcard with credentials.
- [ ] `X-XSS-Protection` is absent or `0`.

## Sources

- Primary: OWASP XSS Prevention, CSP, CSRF Prevention and HTTP Headers Cheat Sheets; OWASP ASVS 5.0 V1.2.1/V3; CWE Top 25 2025; MDN HSTS and Cookies.
- <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP>
