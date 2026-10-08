---
name: preload-web-fonts-to-avoid-flash
description: Use when a custom font causes a flash of invisible or unstyled text. Preloads the file, matches fallback metrics, and picks font-display deliberately.
---

# Preload web fonts to avoid flash

A late-loading webfont either hides text (FOIT) or swaps it (FOUT); both are visible jank. Preloading the file and matching the fallback's metrics removes most of it.

## Procedure

1. Self-host the font rather than calling a third-party CDN at runtime — it removes a round trip, an extra DNS/TLS handshake, and a privacy leak.
2. Subset to the characters you actually ship (Latin, or Latin + the accents in use) with `glyphhanger` or `fonttools`:
       pyftsubset Inter.woff2 --unicodes="U+0000-00FF,U+2000-206F" --flavor=woff2 --output-file=inter-subset.woff2
3. Preload only the font used above the fold, and only the one weight/variant on the critical path. Preloading every weight competes with the CSS and images for bandwidth:
       <link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
   The `crossorigin` attribute is required even for same-origin fonts; omit it and the browser fetches twice.
4. Choose `font-display` deliberately:
       font-display: swap;    /* text visible immediately in fallback, then swaps */
       font-display: optional;/* no swap if slow — best for near-zero CLS */
   Avoid `block` (up to 3 s invisible) and `auto`.
5. Match the fallback's metrics so the swap does not reflow. Tune with `size-adjust`, `ascent-override` and friends:
       @font-face {
         font-family: "Inter Fallback";
         src: local("Arial");
         size-adjust: 107%;
         ascent-override: 90%;
       }
       body { font-family: Inter, "Inter Fallback", system-ui, sans-serif; }
6. Set `font-synthesis: none` if you ship the true italic/bold, so a missing weight does not get a smeared fake.
7. Use a variable font file for multiple weights to cut requests from four to one; weigh the larger single file against the savings.
8. Re-check Cumulative Layout Shift after the change — a well-tuned swap should contribute under 0.02.

## Pitfalls

- `preload` without `crossorigin`, causing a duplicate download and a worse waterfall than no preload at all.
- Preloading four weights and three icon fonts, which starves the actual content and delays first paint.
- `font-display: block` on icon fonts so glyphs pop in late and shift every row.
- Subsetting to the visible characters on the page, so a user typing an accent into a form sees tofu.

## Verification

    # Confirm the preload and the fallback declaration exist together:
    grep -n 'rel="preload".*font' index.html
    grep -n 'size-adjust\|font-display' src/styles/*.css
    # And measure CLS after load:
    npx lighthouse http://localhost:3000 --only-categories=performance --output=json | \
      node -e "let d='';process.stdin.on('data',c=>d+=c).on('end',()=>console.log(JSON.parse(d).audits['cumulative-layout-shift'].numericValue))"

CLS below 0.1 (font contribution under ~0.02), one preloaded font on the critical path, `font-display` set explicitly. Report the subset size, the display mode, and the measured CLS.
