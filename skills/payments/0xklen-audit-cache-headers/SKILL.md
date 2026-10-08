---
name: audit-cache-headers
description: Use when repeat visits still download unchanged assets. Audits Cache-Control, validators and hashed filenames across static and HTML responses.
---

# Audit Cache Headers

Cache headers decide whether a returning visitor waits on the network at all. A missing `immutable` on a hashed asset costs every repeat visit a revalidation round trip.

## Procedure

1. Dump the headers for a hashed asset and for the HTML entry point:

       curl -sI https://shop.example.com/assets/app.9f2c1a.js | grep -iE 'cache-control|etag|last-modified|vary'
       curl -sI https://shop.example.com/ | grep -iE 'cache-control|etag|vary'

2. For content-addressed files, the target is `Cache-Control: public, max-age=31536000, immutable`. The filename hash is the cache key; the URL changes when the bytes change.
3. For HTML, the target is `Cache-Control: no-cache` (revalidate, do not store blindly) so a deploy is visible on the next navigation.
4. Confirm a validator exists when the URL is not hashed: a stable `ETag` lets a 304 replace the body transfer.
5. Check `Vary` on negotiated responses — `Vary: Accept-Encoding` at minimum, plus `Vary: Accept` when you serve AVIF/WebP by content negotiation.
6. Verify the CDN does not strip or rewrite your origin header:

       curl -sI https://cdn.shop.example.com/app.9f2c1a.js | grep -i 'x-cache\|age\|cache-control'

7. Walk the deploy path: after a release, an old hashed URL should still 200 from cache, and the new HTML must reference the new hash.

## Pitfalls

- Setting `max-age=31536000` on a filename that does not contain a hash; the fix for a bug can never reach the client.
- Caching HTML for a year, so users see the previous deploy until they hard-refresh.
- `Cache-Control: no-store` on assets that never change; every visit refetches them.
- Trusting `ETag` values that change on every request (some servers emit a timestamp-based tag), which disables 304s entirely.
- Forgetting `immutable`, so browsers still issue a conditional request on reload within the max-age window.

## Verification

    curl -sI https://shop.example.com/assets/app.9f2c1a.js | grep -i cache-control

The asset must return `max-age=31536000, immutable`; the HTML must return `no-cache`. Report both header lines and the URL each came from.
