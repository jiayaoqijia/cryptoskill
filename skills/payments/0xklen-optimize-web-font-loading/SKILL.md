---
name: optimize-web-font-loading
description: Use when text is invisible during load or fonts cause a swap jump. Applies font-display, subsetting, preload and metric overrides.
---

# Optimize Web Font Loading

Web fonts are discovered late in CSS, block text paint, and change line breaks when they swap. Handled well they are invisible; handled badly they cause both a blank-text delay and a layout jump.

## Procedure

1. Count what ships and subset it to the glyphs you use, cutting a 200 kB family to under 30 kB:

       pyftsubset Inter.ttf --flavor=woff2 --unicodes-file=unicode.txt \
         --layout-features='*' --output-file=inter-subset.woff2

2. Always set a display strategy; `swap` shows fallback text immediately, `optional` avoids the reflow entirely at the cost of not showing the font on slow loads:

       @font-face { font-family: Inter; src: url(/f/inter.woff2) format('woff2'); font-display: swap; }

3. Preload the one font used above the fold so the request starts with the document:

       <link rel="preload" href="/f/inter.woff2" as="font" type="font/woff2" crossorigin>

4. Neutralise the swap shift with a metric-matched fallback via `size-adjust`, `ascent-override` and `descent-override` on a local `@font-face`.
5. Use `unicode-range` on subset faces so a page only downloads the Cyrillic block when it renders Cyrillic.
6. Host same-origin; a third-party font origin adds DNS, TLS and connection latency you would otherwise avoid.

## Pitfalls

- Loading four weights and styles when the design uses two; each is a separate blocking file.
- `font-display: block` with a 3 s block period, which is the worst-case invisible-text delay.
- Omitting `crossorigin` on the preload, causing a second fetch because preload defaults to a different CORS mode.
- Subsetting to Latin but leaving an emoji or symbol face unsubsetted at full size.
- Ignoring the fallback metrics, so the swap moves every line of copy by a few pixels and registers as CLS.

## Verification

    fc-scan --format '%{family} %{fontversion}\n' inter-subset.woff2 && ls -l inter-subset.woff2

The subset must be under 40 kB and the swap shift must not appear in a layout-shift observer. Report the file size and the CLS contribution from the font swap.
