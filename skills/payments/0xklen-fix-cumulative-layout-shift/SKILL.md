---
name: fix-cumulative-layout-shift
description: Use when content jumps while the page loads and CLS is over 0.1. Reserves space for images, fonts, ads and embeds, and verifies with layout-shift observers.
---

# Fix Cumulative Layout Shift

CLS is shift distance times the fraction of the viewport moved. Every un-sized box is a future jump, and users notice it as a misclick more than a metric.

## Procedure

1. Attribute the shifts before fixing. Log each one with its sources:

       new PerformanceObserver(list => {
         for (const e of list.getEntries()) {
           if (!e.hadRecentInput) console.log(e.value, e.sources?.map(s => s.node));
         }
       }).observe({type: 'layout-shift', buffered: true});

2. Give every `<img>` explicit `width` and `height` attributes; the browser derives the aspect ratio and reserves the box.
3. For responsive media without intrinsic size, set the ratio in CSS:

       .thumb { aspect-ratio: 16 / 9; width: 100%; height: auto; }

4. Reserve the font swap window: use `font-display: optional` or `size-adjust` on a `@font-face` metric override so the fallback matches the web font's metrics.
5. Budget fixed-height containers for ads, cookie banners and third-party embeds before they load; a late-injecting iframe is a classic 0.2 shift.
6. Animate only `transform` and `opacity`; a shift-free animation is compositor-only.
7. Re-check on a cold cache and a throttled connection, where late resources expose shifts a warm load hides.

## Pitfalls

- Setting `height: auto` on an image with `width`/`height` attributes plus a CSS rule that overrides the ratio, reverting to a jump.
- Injected banners/notices that push content down; overlay them or reserve the space from first paint.
- Skeleton loaders whose final content has a different height than the placeholder.
- `window.scrollY`-triggered sticky headers toggling `position` and shifting the whole document.
- Ignoring `hadRecentInput` and counting shifts the user caused by clicking, which do not count toward CLS.

## Verification

    npx lighthouse https://shop.example.com --only-categories=performance --preset=desktop --view --chrome-flags="--headless"

CLS in the report must be under 0.1 on desktop and mobile. Report the observed total and the top contributing source node.
