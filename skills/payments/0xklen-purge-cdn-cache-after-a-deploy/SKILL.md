---
name: purge-cdn-cache-after-a-deploy
description: Use when new code is live but users still see old assets, or an API response is stale at the edge. Purge the CDN cache with the right granularity after a deploy and prove the origin's new content is served before declaring the release done.
---

# Purge the CDN cache after a deploy

A deploy that changes origin content does nothing for anyone behind a CDN until the edge cache is
invalidated. Either content-hash your filenames so you never need a purge, or purge precisely.

## Procedure

1. Confirm the stale object is actually cached, and read its age:
   ```bash
   curl -sI https://cdn.example.com/app.js | grep -iE 'age|cache-control|x-cache|etag'
   ```
   `Age:` greater than 0 means the edge served a cached copy; `X-Cache: Hit` (provider-specific) confirms it.
2. Prefer immutable, content-hashed assets so a new deploy is a new URL:
   ```nginx
   location /static/ {
     add_header Cache-Control "public, max-age=31536000, immutable";
   }
   ```
   `app.7f3a9c.js` needs no purge; only `index.html` does.
3. Purge narrowly. Invalidate the changed paths, not the whole zone:
   ```bash
   # Cloudflare
   curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE/purge_cache" \
     -H "Authorization: Bearer $CF_TOKEN" -H 'Content-Type: application/json' \
     -d '{"files":["https://cdn.example.com/index.html","https://cdn.example.com/styles.css"]}'
   ```
4. For a broad change, purge by tag or prefix rather than everything, and expect a cost/rate penalty for
   wildcard purges:
   ```bash
   aws cloudfront create-invalidation --distribution-id "$DIST" \
     --paths '/index.html' '/assets/*'
   ```
5. After the purge, verify the edge serves the new bytes — check the ETag or a version marker, not just
   the HTTP 200:
   ```bash
   curl -sI https://cdn.example.com/index.html | grep -iE 'etag|x-cache|age'
   curl -s  https://cdn.example.com/index.html | grep -o 'build-[0-9a-f]*' | head -1
   ```
6. Confirm invalidation completed (CloudFront invalidations are asynchronous):
   ```bash
   aws cloudfront get-invalidation --distribution-id "$DIST" --id "$INVALIDATION_ID" \
     --query 'Invalidation.Status'    # wait for "Completed"
   ```
7. Repeat the purge from a second edge location/region if the CDN is regional.

## Pitfalls

- Purging before the origin deploy has propagated serves the old content again and re-caches it.
- A wildcard purges everything and can cost money and hit provider rate limits; scope it.
- HTML cached with a long TTL is the classic bug — always keep `index.html` short-TTL or unhashed-purged.
- `Cache-Control: immutable` on a non-hashed URL traps clients with the old file for a year.
- Browsers cache too; a correct CDN purge still shows stale content until the client TTL expires.
- Purging through a different zone (www vs apex) leaves the other hostname stale.
- Verification by `curl` from your location may hit a warm edge; use `curl -H 'Pragma: no-cache'` or check the `Age` header.

## Verification

    curl -sI "https://cdn.example.com/index.html?cb=$(date +%s)" | grep -iE 'x-cache|age|etag'
    aws cloudfront get-invalidation --distribution-id "$DIST" --id "$INV" --query 'Invalidation.Status'

Pass means `Age` is 0 / `X-Cache: Miss` and the invalidation reports `Completed`. Report: "purged
/index.html + /assets/*, invalidation Completed, edge now serves build-9f2c1."
