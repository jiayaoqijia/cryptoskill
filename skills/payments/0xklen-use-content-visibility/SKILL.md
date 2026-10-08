---
name: use-content-visibility
description: Use when long pages jank on scroll because offscreen subtrees still render. Applies content-visibility and contain to skip layout and paint.
---

# Use content-visibility

`content-visibility: auto` lets the browser skip layout, paint and style for offscreen content, and it is the cheapest large win on article and feed pages. It needs a reserved size or it shifts and scrolls badly.

## Procedure

1. Identify the long, repeated subtrees: article sections, feed cards, comment lists, footer blocks.
2. Add a placeholder size so the scrollbar stays honest before the section renders:

       .article-section {
         content-visibility: auto;
         contain-intrinsic-size: auto 500px;   /* width from layout, height estimate */
       }

3. Prefer the `auto <length>` form, which remembers the last-rendered size; a bare `500px` reflows on the first paint of each section.
4. For elements that are always visible, use plain containment to isolate their cost:

       .card { contain: layout paint style; }

5. Test scroll: run Performance with 6x CPU throttling and scroll the page; skipped sections should show near-zero rendering time in the frame chart.
6. Keep it off the LCP element and off any element that must be measured by JS before it renders (see the pitfalls).

## Pitfalls

- Applying it to the first viewport, which delays the LCP element and can make LCP worse.
- Omitting `contain-intrinsic-size`, so each section reports zero height until rendered, then the scrollbar jumps on scroll.
- Using a bad intrinsic size on a page with anchor links, where `#section-7` scrolls to the wrong place because skipped sections are collapsed.
- Expecting JS-measured values (`getBoundingClientRect`) of skipped subtrees to be correct; they are not rendered.
- Assuming it speeds up an element that is on screen; onscreen subtrees render exactly as before.

## Verification

    # DevTools Performance: record a throttled scroll, then
    # Rendering panel -> "Paint flashing" shows skipped sections not repainted

    document.querySelectorAll('.article-section').forEach(el => el.style.contentVisibility)

Every repeated section must report `auto` while the LCP element does not. Report the scroll frame-rate before and after at 6x throttling.
