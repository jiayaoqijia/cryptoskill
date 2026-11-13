---
name: typography
domain: software-engineering/design-taste
trigger: "Review this type; fix the typography; what font sizes; pair these fonts; the text feels off; build the type hierarchy"
anti_trigger: "Color and contrast math (subskills/color-contrast.md); gap and density decisions (subskills/spacing.md); writing copy"
scope: "Type scale, pairing, measure, tracking, and hierarchy rules inside this skill's UI judgments"
status: seedling
---
# Typography

## Standard

- **The Elements of Typographic Style Applied to the Web**: measure (line length) of 45 to 75 characters (http://webtypography.net/2.1.2).
- **WCAG 2.2 SC 1.4.8, Visual Presentation**: blocks of text stay at or under 80 glyphs per line (https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html).
- **Material Design 3 type scale**: a named token scale, not ad-hoc sizes (https://m3.material.io/styles/typography/type-scale-tokens).
- **Law of Similarity**: same-looking text reads as the same class (https://lawsofux.com/law-of-similarity/).
- **Pairing rules and weight budgets**: ⚠️ practitioner convention, no single canonical source.

## Decision rules

1. If hierarchy is weak, fix size and weight before touching color.
2. If body copy runs past 75 characters per line, narrow the column. If under 45, widen the column or raise the size. The cap is 80 glyphs per WCAG 1.4.8.
3. If more than two families appear, cut to two: one for text, one for display. Better: one family with several weights.
4. If size jumps look random, set a modular scale. Ratios of 1.125 to 1.333 suit dense UI. ⚠️ Practitioner convention.
5. If everything is regular weight, set three levels: display, body, caption.
6. If letterspacing appears on body text, remove it. Tracking belongs on caps and small labels.
7. If body line-height is below 1.4 or above 1.6, adjust it into that band. Headings run tighter.

## Procedure

1. List every text style on the screen: family, size, weight, line-height.
2. Find the base size and the ratio between steps.
3. Measure the longest text line. Count its characters.
4. Desaturate or squint. Hierarchy must survive without color.
5. Count families and weights. More than two families or four weights is soup.
6. Check line-height against size for body and display.
7. Check alignment: left for running text; centering only for short display copy.
8. Write each finding with the exact size and weight involved.

## Anti-patterns

- Same size everywhere, "for consistency". Fix: scale steps.
- Color as the only hierarchy signal. Fix: size and weight first.
- Five font families. Fix: a two-family budget.
- Centered body paragraphs. Fix: left align.
- Justified text without hyphenation. Fix: left align.
- Letterspaced body serif. Fix: reserve tracking for caps and labels.

## Done checklist

- [ ] Base size and scale ratio written down.
- [ ] Longest measure between 45 and 75 characters (hard cap 80).
- [ ] Hierarchy reads after desaturation.
- [ ] Two families at most; four weights at most.
- [ ] Body line-height inside 1.4 to 1.6.

## Sources

- http://webtypography.net/2.1.2
- https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html
- https://m3.material.io/styles/typography/type-scale-tokens
- https://lawsofux.com/law-of-similarity/
