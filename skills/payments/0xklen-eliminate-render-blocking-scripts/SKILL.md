---
name: eliminate-render-blocking-scripts
description: Use when first paint waits on JavaScript. Finds parser-blocking tags in the head and rewrites them as defer, async or modules.
---

# Eliminate Render-Blocking Scripts

A classic `<script>` in the head stops the parser dead: no HTML after it is rendered until it downloads and executes. Moving it off the critical path is often a half-second of LCP for free.

## Procedure

1. List every script tag that ships in the initial response:

       curl -s https://shop.example.com/ | grep -oE '<script[^>]*>' | head -50

2. Classify each: `defer` runs after parsing in document order; `async` runs whenever it arrives; `type="module"` is deferred by default. Only scripts that write to `document` before parse need to stay synchronous, and almost none do.
3. Rewrite parser-blocking tags:

       <script src="/analytics.js" defer></script>
       <script src="/cart.js" type="module"></script>

4. Check for `document.write` calls injected by third parties; those forbid defer and are the genuine blockers. Load them behind a consent/interaction gate instead.
5. Measure coverage to confirm what the critical path actually executes:

       # DevTools: Cmd+Shift+P -> "Coverage" -> record a reload, sort by unused bytes

6. Re-test the initial HTML for remaining tags without `defer`/`async`/`type=module`; the grep should return zero matches for your own bundles.

## Pitfalls

- Deferring a script that another synchronous script assumes already ran, breaking load order silently.
- Marking a script `async` when it depends on the DOM being parsed; `async` can run before the body exists.
- Leaving an inline configuration script that `document.write`s the loader for a tag manager; that single tag blocks everything after it.
- Assuming `defer` helps a script that is already at the end of `<body>`; the win there is zero and the diff is noise.
- Forgetting that deferred scripts still execute before `DOMContentLoaded`, so a slow one delays that event.

## Verification

    curl -s https://shop.example.com/ | grep -cE '<script(?![^>]*(defer|async|type="module"))[^>]*src='

Zero matches means no parser-blocking external scripts remain. Report the count before and after, and the LCP delta from a throttled Lighthouse run.
