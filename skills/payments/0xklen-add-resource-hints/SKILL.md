---
name: add-resource-hints
description: Use when discovered-late resources delay LCP. Adds preconnect, preload, fetchpriority and prefetch hints to the right URLs and no others.
---

# Add Resource Hints

The preload scanner ends at the first blocking resource; anything it cannot see costs a full round trip of discovery latency. Hints buy that back, but only for the handful of URLs on the critical path.

## Procedure

1. Read the request waterfall and circle the resources that start more than ~200 ms after the document. Those are the hint candidates.
2. Warm the connection for third-party origins used on the critical path:

       <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
       <link rel="dns-prefetch" href="https://cdn.shop.example.com">

3. Preload the true LCP element and its font, with `as` matching so the response is not fetched twice:

       <link rel="preload" as="image" href="/hero.avif" fetchpriority="high">
       <link rel="preload" as="font" type="font/woff2" href="/f/inter.woff2" crossorigin>

4. Mark the hero with `fetchpriority="high"` and demote below-the-fold media to `fetchpriority="low"` rather than hinting more URLs.
5. Use `rel="prefetch"` only for the next likely navigation (e.g. a product the user is hovering), never for the current page.
6. Confirm each preload is used within ~3 s of load; DevTools warns "preloaded but not used" for hints the page never consumes.

## Pitfalls

- Preloading resources the page never uses; the browser logs a console warning and you have stolen bandwidth from the real LCP.
- Preloading an image without `as="image"`, which triggers a duplicate fetch because the request is not matched to the resource.
- Preconnecting to ten origins "just in case"; each open socket costs CPU and memory on the phone.
- Preloading a font without `crossorigin`, which fetches it twice due to CORS mode mismatch.
- Assuming hints fix a slow origin; preconnect hides the handshake, not a 600 ms server response.

## Verification

    curl -s https://shop.example.com/ | grep -oE '<link rel="(preconnect|preload|prefetch|dns-prefetch)"[^>]*>'

Every hinted URL must appear in the network waterfall before first paint, and none may be flagged unused in the DevTools console. Report the hints added and their resource.
