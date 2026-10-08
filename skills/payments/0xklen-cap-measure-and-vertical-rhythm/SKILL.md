---
name: cap-measure-and-vertical-rhythm
description: Use when prose runs edge to edge or line spacing is arbitrary. Sets a 45–75 character measure with ch units, a base line-height, and a rhythm unit so text blocks scan cleanly.
---

# Cap measure and set vertical rhythm

Text that spans a 1440 px window returns the eye to the wrong line on wrap; the ideal measure is 45–75 characters, roughly 66. Set it with `ch` and the layout follows the font.

## Procedure

1. Constrain prose with `max-width` in `ch`, which scales with the font: `max-width: 66ch` for body, `45–60ch` for captions and sidebars, `75ch` as the hard ceiling for reading text.
2. Never cap measure on a full-bleed container — apply it to the text element, or use `max-inline-size` on the paragraph itself so cards and grids are unaffected.
       .prose p { max-inline-size: 66ch; }
3. Set a body line-height of `1.5` (0.5 leading). Anything under `1.3` for multi-line body text is hard to track; over `1.7` and lines stop reading as a paragraph.
4. Establish a rhythm unit the whole layout shares — take the body line-height in px (24 px at a 16/1.5 body) and space block elements by multiples of it via `margin-block-start`.
5. Trim the extra space at the ends of a text block with the lobotomised-owl selector:
       .prose > * + * { margin-block-start: var(--space-4); }
   so the first and last children carry no stray margin against the container.
6. Keep headings closer to the text they introduce than to the block above: `h2 { margin-block: 2.5rem 0.5rem }`. A visually equal gap above and below makes a heading float.
7. Use `text-wrap: balance` on headings (short, 1–3 lines) and `text-wrap: pretty` on body to avoid orphans, where supported — never `balance` on long body copy, which is capped by the browser.
8. Apply measure per-language: a CJK or Arabic locale needs a shorter or different cap; do not assume a Latin `66ch` fits translated copy.
9. Give long-form content a wider gutter instead of a wider measure: pull the column to `66ch` and let the surrounding margins absorb the extra viewport width, rather than stretching the text.
10. Keep a smaller measure for UI labels and table cells (about `30–40ch`) so a single column does not dominate and force horizontal scanning.

## Worked example

A doc page at 16 px/1.5 has a 24 px line box. Setting `--space-4: 1rem` gives a 16 px gap between paragraphs and `--space-8: 2rem` a 32 px gap before an `h2`. Both are multiples of the 24 px rhythm unit's half, so headings and paragraphs sit in a consistent two-line cadence. The paragraph itself is capped at `66ch`, roughly 700 px at this size — well under the 75-character ceiling.

## Pitfalls

- Fixing measure in px, so raising the font size past the cap pushes text past 75 characters again.
- One measure for everything, so a two-column card grid inherits a 66ch cap and leaves a ragged column.
- Line-height set in `em` on a large heading, compounding to huge leading as the size grows — use a unitless value.
- Vertical rhythm that ignores the line box: a 24 px gap under 40 px line boxes reads as tight because the leading is inside the box, not between blocks.

## Verification

    # Report the character measure of each paragraph (approx via ch):
    node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto(process.argv[1]);const m=await p.\$\$eval('p',els=>els.slice(0,20).map(e=>({ch:Math.round(e.getBoundingClientRect().width/(parseFloat(getComputedStyle(e).fontSize)*0.5)),lh:getComputedStyle(e).lineHeight})));console.log(m);await b.close();})()" http://localhost:3000

Every prose paragraph should measure roughly 45–75 characters and share one line-height. Report the measure token, the rhythm unit, and any paragraph outside the range.
