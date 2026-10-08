---
name: align-icons-with-text-baseline
description: Use when icons sit visually off from their labels. Aligns glyphs to the text baseline with vertical-align and optical sizing, and fixes icon-only buttons with padding.
---

# Align icons with the text baseline

A 20 px SVG next to 16 px text lands wherever its box falls, so a row of labelled buttons reads as jittery. Optical alignment is a small, mechanical fix.

## Procedure

1. Normalise icon size to a token ladder that matches the type scale — typically `16 / 20 / 24 px` (`1rem / 1.25rem / 1.5rem`) — rather than whatever the export gave you.
2. Align inline icons to the text baseline explicitly:
       .icon { width: 1em; height: 1em; vertical-align: -0.125em; fill: currentColor; }
   The small negative offset centres the glyph on the x-height instead of sitting on the descender line.
3. Size icons in `em` when they sit inline with text so they scale with font-size; use `rem` for standalone icon buttons.
4. Use `currentColor` for `fill`/`stroke` so an icon inherits the text colour — an icon that does not change colour with its button is the most common inconsistency.
5. For icon-plus-label buttons, align with flexbox and centre the pair, leaving a token gap:
       .btn { display: inline-flex; align-items: center; gap: var(--space-2); }
6. Keep every icon on the same viewBox (24×24) and the same visual weight, or a 1.5 px-stroke icon next to a 2 px-stroke icon looks bolder and unrelated.
7. Round the glyph edges to the pixel grid — an icon whose box is 20.5 px renders blurry. Use whole `rem` sizes.
8. For icon-only buttons provide an accessible name and a 44 px hit area (see the touch-target skill) — an icon is not a label.

## Pitfalls

- Icons at three different sizes in one toolbar (14/18/20) because they came from three sources.
- `vertical-align: middle`, which aligns to the middle of the line box (including leading), not the glyph, so it sits visibly high.
- A coloured icon hard-coded (`fill="#333"`) that stays dark on a dark background when the label flips to light.
- Stroke width scaling with the icon size after a `transform: scale()`, so a scaled-down icon looks hairline-thin.

## Verification

    # Confirm icons inherit colour and carry an accessible name when alone:
    grep -rnE '<svg[^>]*fill="#' src/**/*.tsx            # hard-coded fills
    grep -rn 'aria-hidden="true"' src/**/*.tsx | wc -l    # decorative icons marked
    # visually: screenshot the toolbar and check glyph centres sit on the x-height

Inline icons should use `currentColor` and `1em` sizing; icon-only buttons must have an `aria-label`. Report the icon ladder, the baseline offset, and any hard-coded fill or mis-sized glyph.
