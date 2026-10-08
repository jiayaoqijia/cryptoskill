---
name: replace-spinners-with-skeletons
description: Use when a loading state is a bare spinner or indefinite text. Builds a skeleton that mirrors the coming layout, times out to an error, and avoids the layout shift a spinner-to-content swap causes.
---

# Replace spinners with content skeletons

A centred spinner tells the user nothing about what is coming and then jumps when content of a different size arrives. A skeleton that traces the real layout makes the wait feel shorter and pins the box.

## Procedure

1. Use a skeleton when the shape of the result is known (a list, a card grid, a profile header). Keep the spinner for genuinely unknown or short (< 400 ms) operations.
2. Reserve the exact space of the loaded content. A skeleton row 44 px tall must load into a 44 px row; if the real row is 48 px, you have created the shift the skeleton was meant to kill.
3. Render 3–5 skeleton rows — enough to fill the viewport, not so many that a short list looks broken. Mirror the real item count when it is known from a prior render or a cached total.
4. Shimmer with a transform or opacity animation only, never `background-position` on a large element, which repaints and can jank on low-end devices:
       .skeleton { background: linear-gradient(90deg,#eee,#f5f5f5,#eee); background-size:200% 100%;
                   animation: shimmer 1.4s linear infinite; }
       @media (prefers-reduced-motion: reduce) { .skeleton { animation: none; background:#eee; } }
5. Announce loading to assistive tech; a pile of empty divs is silent:
       <div role="status" aria-live="polite" aria-busy="true"><span class="sr-only">Loading projects…</span></div>
6. Guard against the skeleton outliving the request: after ~8–10 s, replace it with an error state that offers Retry, so a hung fetch never shimmers forever.
7. Avoid a flash for fast responses — if data lands in under ~200 ms, show nothing (do not mount the skeleton for a single frame); a short debounce prevents the flicker.
8. Keep one skeleton component and vary only its row shape, so the shimmer timing is identical across the app.

## Pitfalls

- Skeleton blocks of the wrong height, so the shift is larger than a spinner-to-content swap would have been.
- A skeleton with no accessible name, so a screen-reader user hears silence and assumes the page is done.
- Shimmering forever when the request fails, because only the success branch clears `isLoading`.
- Skeletons on a page whose content is a single line of text, adding a fake box that then collapses.

## Verification

    # Force a slow response and measure layout shift around the swap:
    #   intercept the API, delay 2000ms, load the page
    npx lighthouse http://localhost:3000 --only-categories=performance --output=json | \
      node -e "let d='';process.stdin.on('data',c=>d+=c).on('end',()=>console.log('CLS',JSON.parse(d).audits['cumulative-layout-shift'].numericValue))"
    # Count skeleton rows vs a real render at a known page size:
    grep -c "Skeleton" src/components/ProjectsList.tsx

CLS for the swap should be ≈ 0, the skeleton row height equal to the real row height, and the skeleton replaced by an error after the timeout. Report the skeleton count and the observed shift.
