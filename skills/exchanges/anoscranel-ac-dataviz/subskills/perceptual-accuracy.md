---
name: perceptual-accuracy
domain: writing/dataviz
trigger: "A pie or bubble chart is proposed; two encodings compete for one quantity"
anti_trigger: "Choosing the comparison class and chart family (subskills/chart-selection.md); palette construction and contrast ratios (subskills/colour-and-accessibility.md); axis distortion (subskills/misleading-patterns.md)"
scope: "Ranking visual encodings by how accurately the eye decodes them; why pie donut and bubble charts lose"
status: seedling
---

# Perceptual Accuracy

## Standard

- **Cleveland & McGill, "Graphical Perception", _JASA_ 79(387), 1984**: the empirical ranking, most accurate first — position on a common scale, position on non-aligned scales, length, angle and slope, area, volume, colour hue. <https://doi.org/10.1080/01621459.1984.10478080>
- **Wilke, "Aesthetic mapping"**: the same ranking restated as a table from data variable to visual channel. <https://clauswilke.com/dataviz/aesthetic-mapping.html>
- **Few, "Rules for Using Color"**: hue carries identity, not magnitude; the eye cannot order hues. <https://www.perceptualedge.com/articles/visual_business_intelligence/rules_for_using_color.pdf>
- **FT Visual Vocabulary**: each family lists what it encodes well and badly. <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>
- ⚠️ House convention: a quantity is never carried by hue alone, and never by area when a bar would fit.

## Decision rules

1. If the reader must compare values precisely, share one position scale: bars or a dot plot.
2. If values sit in separate panels, keep one scale across panels; non-aligned position is the second rung.
3. If a rectangle's width also varies, it encodes area, which ranks below length.
4. If the chart uses angle or slope, restrict it to one whole with few parts.
5. If the chart uses area, treat the reading as ordinal: bigger, not "twice as big".
6. If hue encodes a number, replace it with position or a lightness ramp.
7. If the chart uses volume or perspective, drop it.
8. If two encodings tie on rank, take the one that also works in greyscale.

## Procedure

1. Name the encoding the chart actually uses, not the one the library calls it.
2. Place it on the rungs above. <https://doi.org/10.1080/01621459.1984.10478080>
3. Ask what the claim needs: an order, a rough size, or an exact value.
4. If the need is exact and the encoding is low, the chart fails at step 3.
5. Convert the low-ranked encoding to position: pie to sorted bar, bubble to bar or dot.
6. For a pie, check part count and near-ties; both are fatal at the angle rung.
7. For a bubble, confirm area tracks the value, not the radius.
8. Note the surviving limitation in the caption where the encoding stays.

## Anti-patterns

- **Pie with five or more slices.** Angles sit low and near-ties vanish. Fix: sorted bars with values.
- **Donut as a progress ring.** The hole removes the reference the angle needed. Fix: one number against a target, or a bar.
- **Bubble sized by value.** Radius set to value squares the perceived area. Fix: scale area to value, or use bars.
- **Colour ramp for a category.** Hue cannot be ordered by eye. Fix: position, or a ramp if the variable is ordinal.
- **Two panels on two scales.** Non-aligned position invites false comparison. Fix: one shared scale.

## Done checklist

- [ ] The encoding is named in Cleveland-McGill terms.
- [ ] Its rank matches the precision the claim needs.
- [ ] No pie, donut, or bubble survives unless the claim is only ordinal.
- [ ] Any area or hue encoding is documented as ordinal.
- [ ] The chart still reads in greyscale.

## Sources

- Cleveland & McGill 1984: <https://doi.org/10.1080/01621459.1984.10478080>
- Wilke, "Aesthetic mapping": <https://clauswilke.com/dataviz/aesthetic-mapping.html>
- Few, "Rules for Using Color": <https://www.perceptualedge.com/articles/visual_business_intelligence/rules_for_using_color.pdf>
- FT Visual Vocabulary: <https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary>