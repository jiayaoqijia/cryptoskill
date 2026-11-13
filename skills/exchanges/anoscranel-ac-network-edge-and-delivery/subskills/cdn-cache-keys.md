---
name: cdn-cache-keys
domain: software-engineering/cdn-cache-keys
trigger: "Working out what a CDN key includes and why it serves what it serves."
anti_trigger: "Not for application-internal caches, and not for browser cache choice."
scope: "What the key includes, what vary means, and why keys drift."
status: seedling
---

# CDN cache keys

## Standard

A CDN decides whether two requests are the same request by comparing their cache keys. The key is built from configurable parts of the request — path and query usually, sometimes selected headers or cookies — and anything not in the key is invisible to the cache even if the origin varies its response by it. The classic failure follows directly: the origin respects a header the key omits, one user's answer is cached for everyone, and the wrong user's page appears to another.

The key's other property is its cost. A key that includes everything defeats sharing; a key that includes too little collides responses. Compression and other variations add silent dimensions, and the debugging discipline is to reconstruct the key for a specific request, compare it against what was cached, and reason about collisions — rather than assuming the CDN is clever, which it documented itself as not being.

Primary source: <https://developer.mozilla.org/en-US/docs/Web/HTTP>.

## Decision rules

- Record the exact scheme for every route class: what the key includes and what it omits.
- Record what the origin varies by for each route, and align the key or disable caching on any mismatch.
- Record the vary-behaviour the CDN supports; vary on many headers fragments the cache.
- Treat request headers absent from the key as invisible to caching decisions.
- Purge authority and the runbook must be recorded together with the key documentation.
- Record the response headers the CDN is permitted to alter or normalise while serving.

## Procedure

1. Document the key scheme for each cacheable route class.
2. List the headers that influence the origin response for those routes.
3. Compare each such header against the key and record the mismatches.
4. Record what can and cannot be purged, and by whom.
5. Test worst cases directly: purge an object, vary a controlling header, and observe.
6. Record the scheme and the tests that verified it.

## Anti-patterns

- Caching a response the origin varies by an omitted header.
- Varying on high-entropy headers, fragmenting everything.
- Debugging by turning off the cache instead of reconstructing the key.
- An origin header leaking a set-cookie through a shared cache.
- Purging as a substitute for correct expiration.

## Done checklist

- [ ] Key scheme per route class recorded.
- [ ] Origin vary headers listed.
- [ ] Mismatches resolved or caching disabled there.
- [ ] Purge authority and runbook recorded.
- [ ] Purge and vary tested directly.
- [ ] Scheme documented with the verification method.

## Sources

- HTTP caching semantics: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching>
- RFC 9111, HTTP caching including Vary: <https://www.rfc-editor.org/rfc/rfc9111>
- Set-Cookie interactions with shared caches: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie>
