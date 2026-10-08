---
name: lazy-load-offscreen-media
description: Use when offscreen images and iframes still load on first paint. Applies native loading=lazy, decoding=async and an IntersectionObserver fallback.
---

# Lazy Load Offscreen Media

Most pages ship images for content the user will never scroll to. Deferring them frees bandwidth and main-thread decode time for the region actually on screen.

## Procedure

1. List images that load but sit below the fold, from the Lighthouse payload:

       npx lighthouse https://shop.example.com --only-audits=offscreen-images --output=json | jq '.audits."offscreen-images".details.items[].url'

2. Add native lazy loading to everything except the LCP element:

       <img src="/p/1.jpg" width="800" height="600" loading="lazy" decoding="async" alt="...">

3. Keep the hero eager with `fetchpriority="high"`; lazy-loading the LCP image delays it by a scroll event that never happens.
4. Lazy-load iframes the same way — `loading="lazy"` on `<iframe>` is widely supported and cheap.
5. For carousels and masonry layouts whose children are offscreen but already in JS, gate the source swap on visibility:

       const io = new IntersectionObserver((es) => es.forEach(e => {
         if (e.isIntersecting) { e.target.src = e.target.dataset.src; io.unobserve(e.target); }
       }), {rootMargin: '200px'});

6. Give every lazy image `width`/`height` or `aspect-ratio` so deferring the bytes does not create a shift.

## Pitfalls

- Lazy-loading the hero image, which pushes LCP out to a scroll or intersection tick and usually makes it worse.
- A too-large `rootMargin` that preloads everything, defeating the point; 200-400 px of lead is enough.
- Lazy-loading images that are in the initial viewport because a JS layout shifts them down later.
- Forgetting dimensions on deferred images, trading a byte win for a CLS regression.
- Using a JS lazy-loader that runs after paint, so the browser's eager preload scanner has already fetched the images.

## Verification

    npx lighthouse https://shop.example.com --only-audits=offscreen-images --quiet --output=json | jq '.audits."offscreen-images".score'

A score of 1.0 means no offscreen media is loading eagerly. Report the wasted bytes reclaimed and confirm the LCP image is still eager.
