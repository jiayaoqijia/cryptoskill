---
name: audit-charts-for-misleading-encoding
description: Use when reading or producing a chart, dashboard, or infographic. Checks for truncated axes, bad scaling, and picked ranges that distort the message.
---

# Audit Charts for Misleading Encoding

Most deceptive charts are not fabricated — they are honest numbers drawn with an encoding chosen to exaggerate. Check the geometry, not the caption.

## Procedure

1. Check the y-axis baseline. Bars must start at zero; a bar chart starting at 97 turns a 1% difference into a full-height cliff. `grep -n 'ylim\|set_ylim\|min:' chart_config`.
2. Check scaling for area/radius marks. A circle encodes value by area = π r², so doubling the value needs r × 1.41, not r × 2. Report the mapping used.
3. Check the x-domain. A "trend" over 3 cherry-picked days is not a trend; widen to the full available period and see if it survives.
4. Check dual axes. Two overlaid lines on independent scales can be made to cross anywhere; they imply causation that is not in the data.
5. Check for a log axis presented as linear or vice versa. A log axis compresses the tail; label it.
6. Check units and denominators. "Cases per 100k" vs "cases" reverses the ranking between a small and a large region.
7. Redraw the honest version and compare the impression. If your conclusion flips, the chart was load-bearing and the original claim fails.

```python
import matplotlib.pyplot as plt
# always anchor bar charts at zero
plt.bar(labels, values)
plt.ylim(0, max(values) * 1.05)   # not plt.ylim(min(values), max(values))
```

## Pitfalls

- 3D pie charts and perspective bars distort area non-linearly; refuse to read precise values from them.
- Truncated axes are legitimate for line charts *showing change* and illegitimate for bars *showing magnitude* — say which convention the chart follows.
- Missing gridlines and unlabelled tick marks force the reader to interpolate; supply the numbers.
- Colour scales that map a continuous value through a rainbow hide the midpoint.
- Small-multiple panels often omit a shared scale; confirm each panel uses the same range.

## Verification

    grep -nE 'ylim|set_ylim|xlim|log|symlog' plot.py

Bars anchored at zero, area marks scaled by sqrt, axes labelled with units. Report: "Y-axis truncated at 97 (bars not zero-based) — the 1.2% gap renders as a full-height drop; redrawn from zero it is flat."
