---
name: spacing
domain: software-engineering/design-taste
trigger: "Fix the spacing; the layout feels cramped; is this gap right; align these elements; density review; whitespace check"
anti_trigger: "Type measure and line-height (subskills/typography.md); color contrast (subskills/color-contrast.md); grid implementation work in code"
scope: "The 4/8 point grid, spacing scales, optical alignment, and density budgets inside this skill's UI judgments"
status: seedling
---
# Spacing

## Standard

- **Material Design 3, layout spacing**: an 8 dp base grid, with 4 dp steps for small items (https://m3.material.io/foundations/layout/understanding-layout/spacing).
- **Apple Human Interface Guidelines, Layout**: consistent margins and rhythm across a screen (https://developer.apple.com/design/human-interface-guidelines/layout).
- **Law of Proximity**: closeness signals grouping before any border does (https://lawsofux.com/law-of-proximity/).
- **Nathan Curtis, "Space in Design Systems"**: name spacing steps like type sizes, and spend them from a scale (https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62 — metered).
- **Optical over mathematical alignment**: trust the eye when the grid and the eye disagree. ⚠️ Practitioner convention.

## Decision rules

1. If gap values look random, snap them to a scale: 4, 8, 12, 16, 24, 32, 48, 64.
2. If related items sit far apart, group by proximity. Add borders last.
3. If a divider looks necessary, try spacing first. Lines are the last resort.
4. If gaps between sections, components, and inline items are equal, order them: section > component > inline.
5. If the grid says aligned but the eye says off, adjust optically: icon centering, cap-height edges, baseline alignment.
6. If a data-dense screen needs more room, shrink steps, never padding below one base unit. Dense admin views live on 4 and 8; marketing pages live on 32 and 64. ⚠️ Practitioner convention.
7. If everything feels cramped, delete content before shrinking the budget.

## Procedure

1. Find the base unit, usually 8.
2. Sample the gap values across the screen.
3. Snap each gap to the scale. Flag off-scale values.
4. Check grouping: related items closer together than unrelated ones.
5. Compare padding inside a component with gaps between components.
6. Run the optical pass: icon centering in buttons, baseline alignment across mixed sizes, edge alignment of blocks.
7. Check density against the screen's purpose.
8. Record fixes as scale steps, not one-off pixel values.

## Anti-patterns

- One-off pixel gaps everywhere. Fix: snap to steps.
- Equal gaps for every relationship. Fix: the section, component, inline order.
- Borders used to express grouping. Fix: proximity first.
- Mathematical alignment trusted against the eye. Fix: optical adjustment.
- Shrinking gaps to dodge scrolling. Fix: cut content.
- Chasing pixel-perfect across breakpoints. Fix: the rhythm matters, not the count.

## Done checklist

- [ ] Base unit named; all gaps on the scale or justified in writing.
- [ ] Grouping expressed by proximity, not borders.
- [ ] Section, component, inline order holds.
- [ ] Optical pass done on icons, baselines, and edges.
- [ ] Density matches the screen's purpose.

## Sources

- https://m3.material.io/foundations/layout/understanding-layout/spacing
- https://developer.apple.com/design/human-interface-guidelines/layout
- https://lawsofux.com/law-of-proximity/
