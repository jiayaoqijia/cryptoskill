---
name: web-performance
domain: software-engineering/web-performance
trigger: "\"Improve LCP\", \"INP is poor\", \"fix layout shift\", \"pass Core Web Vitals\", \"the bundle is too big\", \"Lighthouse score dropped\", \"page loads slowly on mobile\"."
anti_trigger: "Server or API latency, profiling and load tests (subskills/performance.md); UI structure and state; browser functional tests."
scope: "Core Web Vitals targets, bundle and render cost, field vs lab data"
status: "seedling"
---

# Web Performance

## Standard

- **Core Web Vitals "good"**: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, at the 75th percentile of page loads, split by mobile and desktop (https://web.dev/articles/vitals, updated 31 Oct 2024; Google Search Central, updated 10 Dec 2025).
- **Poor bands**: LCP > 4.0 s, INP > 500 ms, CLS > 0.25.
- INP replaced FID on 12 March 2024.
- **Field vs lab**: field = real users (Chrome UX Report, RUM via `web-vitals`). Lab = Lighthouse, WebPageTest, DevTools on a set device.

## Decision rules

1. The target is field p75 in the good band for each metric, on mobile first.
2. Lab data finds causes; field data decides success. Never report a lab score as the outcome.
3. INP has no lab equivalent. Use Total Blocking Time in the lab as a proxy, then confirm in the field.
4. LCP fixes, in order: server response → render-blocking CSS and JS → hero resource discovery (preload, never lazy-load) → image size and format.
5. INP fixes: split long tasks (over 50 ms); yield to or move work off the main thread; cut hydration cost.
6. CLS fixes: dimensions or `aspect-ratio` on every image, video and embed; reserve space for late content; never insert above existing content; size-matched font fallbacks.
7. Bundle budget per route in CI. ⚠️ No standard number; set it from your baseline.
8. Every third-party script needs an owner and a measured cost; load it with `async`/`defer` or after interaction.

## Procedure

1. Get field data: CrUX (PageSpeed Insights or the CrUX API), or your RUM:
   ```js
   import { onLCP, onINP, onCLS } from 'web-vitals';
   [onLCP, onINP, onCLS].forEach(f => f(m => navigator.sendBeacon('/rum', JSON.stringify(m))));
   ```
2. Find the worst metric and the worst page template.
3. Reproduce in the lab on a throttled mobile profile:
   ```bash
   npx lighthouse https://example.com --preset=perf --form-factor=mobile --view
   ```
4. Diagnose in the DevTools Performance panel: LCP element and phases, long tasks, layout-shift sources.
5. Inspect bundles (`npx source-map-explorer dist/*.js`). Remove unused code; split by route; replace heavy dependencies.
6. Apply one fix. Re-run the lab test; record before and after.
7. Add Lighthouse CI with budgets:
   ```json
   { "ci": { "assert": { "assertions": {
     "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
     "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
     "total-blocking-time": ["warn", {"maxNumericValue": 200}] } } } }
   ```
 ⚠️ The TBT 200 ms line is a house proxy, not a CWV threshold.
8. Confirm field p75 after CrUX's rolling 28-day window or a week of RUM. ⚠️ Check the CrUX window in current docs.

## Anti-patterns

- Chasing Lighthouse 100 while field INP is poor.
- Lazy-loading the LCP image; images without dimensions.
- One bundle for every route.
- Testing only on a fast desktop.

## Done checklist

- [ ] Field p75 measured per metric, mobile and desktop.
- [ ] Worst metric diagnosed in the lab.
- [ ] Fix recorded with before and after numbers.
- [ ] Lighthouse CI budgets block regressions.
- [ ] Field p75 confirmed good.

## Sources

- https://web.dev/articles/vitals · https://developers.google.com/search/docs/appearance/core-web-vitals
- <https://web.dev/learn/performance>
- <https://sre.google>
