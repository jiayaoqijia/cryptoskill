---
name: debug-cors-preflight-failures
description: Use when a browser blocks a cross-origin request with a CORS error while curl and the server succeed. Reproduce the OPTIONS preflight, read the Access-Control-* headers, and fix the exact header the browser is missing rather than disabling the policy.
---

# Debug CORS preflight failures

The browser rejects a response the server is sending, because a required `Access-Control-*` header is
missing or does not match the request. curl never enforces CORS, so it always "works" and misleads you.

## Procedure

1. Reproduce the preflight the browser actually sends — the `OPTIONS` request with the origin and the
   method it intends to use:
   ```bash
   curl -si -X OPTIONS https://api.example.com/v1/items \
     -H 'Origin: https://app.example.com' \
     -H 'Access-Control-Request-Method: PUT' \
     -H 'Access-Control-Request-Headers: content-type,authorization'
   ```
2. Check the response for the three headers the browser needs:
   ```
   Access-Control-Allow-Origin: https://app.example.com
   Access-Control-Allow-Methods: PUT, POST, GET
   Access-Control-Allow-Headers: content-type, authorization
   ```
   A missing `Allow-Methods` that lists `PUT`, or an `Allow-Headers` that omits `authorization`, is
   the failure.
3. Confirm the status is `2xx` — a `405`/`404` on the OPTIONS route means the framework rejected the
   preflight before CORS middleware ran.
4. If credentials are used, verify the exact pair (both required):
   ```
   Access-Control-Allow-Credentials: true
   Access-Control-Allow-Origin: https://app.example.com   # must NOT be "*"
   ```
   `Allow-Origin: *` with credentials is rejected outright by the spec.
5. Confirm the real request's headers too; a preflight that passes can still fail if the actual
   response omits `Allow-Origin`:
   ```bash
   curl -si -X PUT https://api.example.com/v1/items \
     -H 'Origin: https://app.example.com' -H 'Content-Type: application/json' -d '{}' \
     | grep -i '^access-control'
   ```
6. For a wildcard subdomain requirement, echo the request Origin from an allowlist and add `Vary: Origin`
   so caches do not serve one origin's headers to another:
   ```nginx
   add_header Vary Origin always;
   ```
7. Cache preflight responses with `Access-Control-Max-Age` to cut the extra round trip:
   ```
   Access-Control-Max-Age: 600
   ```

## Pitfalls

- Testing with curl `-H 'Origin: ...'` without the `OPTIONS`+`Access-Control-Request-Method` pair does not exercise preflight logic.
- `Allow-Origin: *` cannot be combined with `Allow-Credentials: true`; browsers reject it silently.
- A proxy stripping `Access-Control-*` headers on the way out undoes a correct app config.
- CORS must be set on the *response to the preflight* and the actual request, not only one.
- `Allow-Methods` omitting `OPTIONS` or the app returning `405` to preflight breaks everything.
- A redirect (301 to a canonical host) on the preflight is followed by some browsers and fails on others.
- Without `Vary: Origin`, a shared CDN cache can return one origin's CORS headers to a different origin.

## Verification

    curl -si -X OPTIONS https://api.example.com/v1/items \
      -H 'Origin: https://app.example.com' \
      -H 'Access-Control-Request-Method: PUT' \
      -H 'Access-Control-Request-Headers: authorization' | grep -i '^access-control'

Pass means the preflight returns `200` with `Allow-Origin` echoing the origin (or the allowlisted
value), `Allow-Methods` including `PUT`, and `Allow-Headers` including `authorization`. Report those
exact headers.
