---
name: colour-and-accessibility
domain: writing/dataviz
trigger: "Picking a palette for a chart; a legend that fails in greyscale or for colour-blind readers; contrast that disappears"
anti_trigger: "Judging which chart form to use (subskills/chart-selection.md); where labels sit on the page (subskills/annotation-and-labels.md); a full page or app accessibility audit"
scope: "Sequential versus diverging versus categorical palettes; colour-blind-safe defaults; WCAG 2.2 non-text contrast; redundant encoding"
status: seedling
---

# Colour and Accessibility

## Standard

- **ColorBrewer 2.0** (Harrower & Brewer, _The Cartographic Journal_ 40(1), 2003): sequential for ordered magnitude, diverging for distance from a midpoint, qualitative for unordered categories. <https://colorbrewer2.org/>
- **WCAG 2.2 SC 1.4.11 Non-text Contrast**: graphical objects needed to understand content need 3:1 against adjacent colours. <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html>
- **WCAG 2.2 SC 1.4.1 Use of Color**: colour is never the only carrier of information. <https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html>
- **Color Universal Design (Okabe & Ito)**: eight tested colours that stay distinguishable under common colour blindness. <https://jfly.uni-koeln.de/color/>
- **Colour Blind Awareness**: red-green colour blindness affects about 1 in 12 men and 1 in 200 women. <https://www.colourblindawareness.org/colour-blindness/>
- **Wilke, "Color pitfalls"**: rainbow ramps invent boundaries and break under colour blindness. <https://clauswilke.com/dataviz/color-pitfalls.html>
- ⚠️ House convention: six categorical hues maximum; a seventh category gets a facet or a table.

## Decision rules

1. If the variable is ordered, use a sequential ramp of one hue, carried by lightness.
2. If the variable has a meaningful midpoint, use a diverging ramp with a neutral centre.
3. If the categories are unordered, use a qualitative set and cap it at six. ⚠️ House cap.
4. If the chart must survive colour blindness, start from the Okabe-Ito set or a ColorBrewer safe scheme.
5. If colour carries meaning, add a second channel: direct label, shape, dash, or position.
6. If a graphical object meets its background, check 3:1 before shipping.
7. If the chart prints in greyscale, test it; hue differences vanish, lightness survives.

## Procedure

1. Name the variable type: ordered, diverging, or categorical.
2. Pick the palette job from that name, not from brand colours. <https://colorbrewer2.org/>
3. Start from a colour-blind-safe scheme, then adjust toward the brand.
4. Count categories; above six, facet or regroup instead of adding hues.
5. Give the series the claim is about the strongest contrast; mute the rest.
6. Add the redundant encoding: direct labels first, then shapes or dashes.
7. Check each object against its background at 3:1. <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html>
8. Convert to greyscale, then simulate deuteranopia, and re-read both.

## Anti-patterns

- **Rainbow ramp for a continuous variable.** It creates false boundaries and fails colour blindness. Fix: one-hue ramp.
- **Colour as the only encoding.** A colour-blind reader loses the series. Fix: labels, shapes, or line styles.
- **Seven or more categorical hues.** They stop being distinguishable. Fix: facet, or regroup into "other".
- **Light grey on white.** Fails the 3:1 threshold. Fix: darken until it passes.
- **Red and green as the only pair.** The commonest confusion pair. Fix: blue and orange, plus a marker difference.

## Done checklist

- [ ] The palette job matches the variable type.
- [ ] The scheme is colour-blind safe, or redundancy covers it.
- [ ] Categories stay within six, or the chart is faceted.
- [ ] Every graphical object meets 3:1 against its background.
- [ ] The figure reads in greyscale.

## Sources

- ColorBrewer 2.0: <https://colorbrewer2.org/>
- Harrower & Brewer 2003: <https://doi.org/10.1179/000870403235002042>
- WCAG 2.2 SC 1.4.11: <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html>
- WCAG 2.2 SC 1.4.1: <https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html>
- Okabe & Ito, Color Universal Design: <https://jfly.uni-koeln.de/color/>