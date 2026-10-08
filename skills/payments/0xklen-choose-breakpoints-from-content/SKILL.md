---
name: choose-breakpoints-from-content
description: Use when picking responsive breakpoints. Derives them from where the layout actually breaks, not from named device widths, and prefers intrinsic layout over a grid of media queries.
---

# Choose breakpoints from content

"You need a tablet breakpoint at 768 px" is a device list, not a reason. Breakpoints should fall where the content stops fitting, which you find by shrinking the window until it breaks.

## Procedure

1. Build the layout mobile-first with `min-width` queries so the base styles apply at the smallest size and enhancements add up.
2. Drag the viewport from 320 px to 1600 px and mark every width where something looks wrong: a line of text stretches past ~75 characters, cards squeeze below a readable width, a nav wraps two rows. Those widths are the breakpoints.
3. Round each to a nearby round number (e.g. 736 → 720) and give it a name tied to content, not hardware:
       /* stacking → two column */  @media (min-width: 40rem)  { ... }
       /* two → three column */     @media (min-width: 64rem)  { ... }
4. Prefer intrinsic layouts that need no query: `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr))` reflows on its own; add a query only when the self-reflowing grid fails.
5. Use container queries for components that live in different-width slots, so a card adapts to its container rather than the viewport:
       .card-wrap { container-type: inline-size; }
       @container (min-width: 24rem) { .card { flex-direction: row; } }
6. Keep the number of breakpoints small — three to five for most products. Each one multiplies the states a designer must check.
7. Express breakpoints as custom media or Sass variables so the numbers agree between CSS and JS:
       $bp-md: 64rem;   // 1024px
8. Verify at the extremes: 320 px (small phone), 1024 px, and a 200% zoom at 1280 px, which must reflow rather than scroll horizontally.

## Pitfalls

- A fixed `min-width: 768px` chosen because it is "the iPad", leaving a phone in landscape stranded in the desktop layout.
- Breakpoints in px while spacing uses rem; a zoomed browser crosses the px query at a different visual size than the rem ones.
- `@media (max-width: ...)` crossed with `min-width` queries producing overlapping rules and specificity wars.
- Only two extremes (mobile and desktop) with nothing between 480 px and 1280 px, so tablets get the desktop layout squeezed.
- Forgetting `overflow-x`, which lets one over-wide child scroll the whole page horizontally at 320 px.

## Verification

    # No horizontal scroll at the narrowest supported width:
    npx playwright screenshot --viewport-size=320,800 --full-page http://localhost:3000 /tmp/320.png
    node -e "console.log(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth))"

`scrollWidth <= innerWidth` at 320 px (and at 200% zoom) means no horizontal overflow. Report the breakpoint values, why each exists, and the widths where the layout was most fragile.
