---
name: accessibility
domain: writing/slide-decks
trigger: "make this deck accessible; check the exported PDF; write alt text for my slides; WCAG for presentations"
anti_trigger: "Wider web-frontend WCAG work (outside this skill); choosing the chart itself (subskills/charts-per-claim.md); filename conventions (subskills/recurring-qa.md)"
scope: "Exported-deck accessibility, alt structure, reading order, contrast, captions, file metadata"
status: seedling
---

# Accessibility

## Standard

- **WCAG 2.2, SC 1.4.3 Contrast (Minimum)**: text contrast at least 4.5 to 1; large text at least 3 to 1. <https://www.w3.org/TR/WCAG22/#contrast-minimum>
- **WCAG 2.2, SC 1.4.11 Non-text Contrast**: chart marks, icons, and indicators at least 3 to 1 against adjacent colors. <https://www.w3.org/TR/WCAG22/#non-text-contrast>
- **WCAG 2.2, SC 1.2.2 Captions (Prerecorded)**: spoken word in a recorded export needs captions. <https://www.w3.org/TR/WCAG22/#captions-prerecorded>
- **WebAIM PowerPoint techniques**: reading order is set by the reading-order pane, not by visual order; every informative image carries alt text; decorative images are marked decorative. <https://webaim.org/techniques/powerpoint/>
- **File metadata**: the document title is set before export. ⚠️ practitioner convention; exact steps vary by tool.

## Decision rules

1. If exporting to PDF, export as tagged PDF. An untagged PDF breaks screen-reader order.
2. If a chart or image carries the point, the alt text states the claim, not the filename.
3. Color never carries meaning alone. Pair hue with a label, pattern, or shape.
4. The contrast thresholds bind the slide master and the charts, not only the body text.
5. Reading order follows the skim order: headline, evidence, annotation.
6. A narrated or recorded export ships with captions or a transcript.
7. Apply WCAG contrast numbers even for projection. Ambient light makes projected contrast worse than measured. ⚠️ practitioner application.

## Procedure

1. On every slide, put the headline first in reading order.
2. Write one sentence of alt text per visual, drawn from its claim.
3. Check every text-and-background and series-and-background pair with the WebAIM contrast checker: <https://webaim.org/resources/contrastchecker/>
4. Add redundant encoding to any color-only series: direct labels, patterns, or shapes.
5. Set the document title and author in the file properties.
6. Export tagged, and open the exported file to confirm order and tags survived.
7. Attach captions or a transcript file beside any exported narration.

## Anti-patterns

- Grey or gradient text below 4.5 to 1 because it "elegantly fades".
- Alt text reading "image", "chart", or left blank on an informative visual.
- Red-versus-green series with no labels.
- An exported PDF where each slide is a single image.
- A narrated video export with no captions.
- Reading order scrambled after template edits. Fix: re-run the order check after every master change.

## Done checklist

- [ ] Every text pair meets 4.5 to 1; every non-text pair meets 3 to 1.
- [ ] Every visual has claim-bearing alt text or is marked decorative.
- [ ] Reading order matches the skim order on every slide.
- [ ] Distribution export is tagged.
- [ ] Captions or a transcript ship with any spoken word.
- [ ] Document title and author metadata set.

## Sources

- WCAG 2.2: <https://www.w3.org/TR/WCAG22/>
- WebAIM, PowerPoint accessibility techniques: <https://webaim.org/techniques/powerpoint/>
- WebAIM contrast checker: <https://webaim.org/resources/contrastchecker/>
- IBCS, notation with redundant encoding: <https://www.ibcs.com/standards/>
