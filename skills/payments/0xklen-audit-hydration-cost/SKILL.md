---
name: audit-hydration-cost
description: Use when server-rendered HTML is fast but the page stays unresponsive. Measures hydration main-thread cost and moves to islands or partial hydration.
---

# Audit Hydration Cost

SSR paints fast and then spends a second re-executing the same tree to attach handlers. Until hydration finishes, the page looks ready but ignores taps — the worst kind of slow.

## Procedure

1. Measure the gap between first paint and interactivity: record with 4x CPU throttling and read the timestamp of the last long task after load.
2. Sum hydration script self-time in the bottom-up view; a heavy component library re-parsing on the client is the usual suspect.
3. Budget the JS that hydrates: if the client bundle re-ships every component's code, the server render was cosmetic.
4. Move to islands — hydrate only interactive regions, leaving marketing copy and layout as static HTML:

       <!-- Astro island: only the cart hydrates -->
       <Cart client:visible />
       <article>{staticProse}</article>

5. For a React app, render the tree on the server but defer below-the-fold widgets with `client:idle` or `client:visible`.
6. Confirm the win by re-measuring Time to Interactive / INP under the same throttling; a static page with one island should hydrate in tens of milliseconds.
7. Keep server-only work server-side: date formatting, markdown rendering and i18n should not reappear in the client bundle after the split.
8. Record the hydration budget in the build: a route whose client JS exceeds the budget should fail CI, not ship and be noticed by users.

## Pitfalls

- Hydrating a component that never changes; static JSX should not ship a client bundle at all.
- Using `client:load` on everything, which is a synonym for the full-hydration problem you were fixing.
- A `useEffect` that fires a data fetch immediately on hydration, doubling requests the server render already made.
- Measuring TTI on an unthrottled desktop, where hydration finishes before the first frame and looks free.
- Hydration mismatches from rendering a random value or date on both sides, forcing a full client re-render.

## Verification

    npx lighthouse https://shop.example.com --preset=perf --form-factor=mobile --only-audits=total-blocking-time,bootup-time --output=json | jq '.audits."bootup-time".details.items'

Bootup time and TBT after the island split must fall well below the pre-change run. Report the hydrated component count before and after.
