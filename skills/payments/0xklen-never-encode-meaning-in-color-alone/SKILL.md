---
name: never-encode-meaning-in-color-alone
description: Use when status, errors or chart series are distinguished only by hue. Adds a second channel — icon, label, pattern or shape — so colour-blind users still read the signal.
---

# Never encode meaning in colour alone

Red text for an error and green for success is invisible to a deuteranope and unreadable in forced-colors mode. Any meaning carried by hue needs a second, non-colour channel.

## Procedure

1. Inventory every place colour carries information: status dots, diff lines, form validation, chart series, badges, validation borders. Each needs a redundant cue.
2. Add an icon or glyph to status colour: a check for success, a filled triangle-warning for error, an info circle for notice. The icon alone should be enough to read the state.
3. Add a text label where space allows: colour the badge *and* write the state — `● Failed` not just a red dot. This also fixes colour-blindness, dark mode and print.
4. For charts, vary three channels, not one: colour, plus a named legend entry, plus a marker shape (circle/square/triangle) or line dash (solid/dashed/dotted).
       <Line series={a} stroke="var(--s1)" strokeDasharray="0"   />
       <Line series={b} stroke="var(--s2)" strokeDasharray="4 2" />
5. Prefer a palette that is distinguishable under deuteranopia, protanopia and tritanopia (Okabe–Ito or a colour-blind-safe Brewer set), not the default categorical rainbow.
6. For form errors, do not rely on a red border: pair it with an inline message and, where the field is invalid, `aria-invalid="true"` plus `aria-describedby` pointing at the message.
7. Check forced-colors mode (`@media (forced-colors: active)`): background colours are dropped, so keep a border or an icon that survives, and use system colour keywords like `CanvasText`.
8. Verify by greyscale: desaturate the screenshot; if two states become the same grey, the channel is missing.

## Pitfalls

- A green/red pair as the only cue on a data table, where "up" and "down" become identical in greyscale.
- A success toast that fades before it is read and carries meaning only in its border colour.
- Diff views relying on red/green with no `+`/`-` gutter, unreadable for the ~8% of men with red-green deficiency.
- Colour-blind-safe palette chosen but applied with the same marker shape for every series, so two lines still overlap ambiguously.

## Verification

    # Greyscale the page and diff two states:
    npx playwright screenshot --viewport-size=1280,900 http://localhost:3000/orders /tmp/color.png
    magick /tmp/color.png -colorspace Gray /tmp/gray.png
    # Then confirm each status also has text or an icon in the DOM:
    grep -rn "status-" src/components/StatusBadge.tsx

With the grey image, every distinct state must still be distinguishable, and each status element must contain a text label or an `aria-label`. Report the redundant cues added per status and any remaining colour-only signal.
