---
name: color-contrast
domain: software-engineering/design-taste
trigger: "Is this contrast OK; check these colors; build a palette; is this colorblind safe; WCAG contrast; too many colors"
anti_trigger: "Type hierarchy without color (subskills/typography.md); spacing and density (subskills/spacing.md); the full axe-level conformance audit"
scope: "Palette construction, WCAG 2.2 contrast math, and colorblind safety inside this skill's UI judgments"
status: seedling
---
# Color and Contrast

## Standard

- **WCAG 2.2 SC 1.4.3, Contrast (Minimum)**: 4.5:1 for normal text, 3:1 for large text (https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- **WCAG 2.2 SC 1.4.11, Non-text Contrast**: 3:1 for UI boundaries, icons, and focus indicators (https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
- **WCAG 2.2 SC 1.4.1, Use of Color**: never signal by hue alone (https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).
- **Relative luminance**: the ratio is computed from linearized channels (https://www.w3.org/TR/WCAG22/#dfn-relative-luminance).
- **60-30-10 palette**: 60 neutral base, 30 secondary, 10 accent. ⚠️ Practitioner convention from interior design.
- **Color blindness**: about 1 in 12 men (8%) carries a red-green defect (https://www.colourblindawareness.org/colour-blindness/). WebAIM covers the contrast mechanics: https://webaim.org/articles/visual/colorblind.

## Decision rules

1. If normal text scores under 4.5:1, shift lightness on one side. Never fix it with a heavier weight.
2. Large text (24 px and up, or 18.66 px bold and up) needs 3:1.
3. If a border, icon, or control carries meaning, hold 3:1 against its adjacent colors.
4. If hue alone marks an error or success, add an icon or a text label.
5. If the palette feels loud, spend it as 60 neutral, 30 secondary, 10 accent.
6. If two accents compete on one screen, keep one.
7. If red and green carry the state, add shape or text, then verify in grayscale.

## Procedure

1. List every foreground and background pair: text, controls, borders, icons.
2. Compute the ratio for each pair:

   ```python
   def linear(c):
       c = c / 255
       return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

   def luminance(rgb):
       r, g, b = [linear(c) for c in rgb]
       return 0.2126 * r + 0.7152 * g + 0.0722 * b

   def contrast(a, b):
       hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
       return (hi + 0.05) / (lo + 0.05)
   ```

3. Classify text as normal or large.
4. Record pass or fail against the threshold for each pair.
5. Run the 3:1 check on non-text elements that carry meaning.
6. Desaturate the view. States must stay readable.
7. Rebalance the palette toward the 60-30-10 budget.
8. Log failing pairs with their hex values and the required target.

## Anti-patterns

- Placeholder gray on labels. Fix: 4.5:1.
- Brand accent as body-text color below threshold. Fix: a darker text variant token.
- Error by hue alone. Fix: icon plus message.
- Eight-color palettes. Fix: the budget.
- Contrast checked by eye. Fix: compute the ratio.

## Done checklist

- [ ] Every foreground/background pair computed and recorded.
- [ ] All normal text at 4.5:1 or above; all large text at 3:1 or above.
- [ ] Meaning-carrying non-text at 3:1 or above.
- [ ] No state carried by hue alone.
- [ ] Palette rebalance recorded.

## Sources

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
- https://www.colourblindawareness.org/colour-blindness/
- https://webaim.org/articles/visual/colorblind
