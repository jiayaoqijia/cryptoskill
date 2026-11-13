---
name: ai-slop-anti-patterns
domain: software-engineering/design-taste
trigger: "This UI looks like AI slop; why does this look like a default template; make this design less generic; fix my LLM-generated UI"
anti_trigger: "Contrast math on one palette (subskills/color-contrast.md); the general critique order (subskills/critique-protocol.md); copy quality"
scope: "The recurring visual tells of default LLM-generated UI inside this skill, each paired with its fix"
status: seedling
---
# AI-Slop Anti-Patterns

## Standard

- **Anthropic's frontend-design skill**: the anti-slop framing this leaf extends (https://github.com/anthropics/skills/tree/main/skills/frontend-design).
- **Law of Similarity**: identical repeated cards blur into one undifferentiated mass (https://lawsofux.com/law-of-similarity/).
- **Material Design 3 shape tokens**: one radius per component class, from a scale (https://m3.material.io/styles/shape/overview).
- **The default purple-blue gradient tell**: ⚠️ practitioner convention; it is the stock choice of unattended generation, not a standard.

## Decision rules

1. If the screen could belong to any product, one element must become task-specific and distinctive.
2. If the same card repeats in a grid, vary it deliberately on one axis, or break the grid for the primary object.
3. If a gradient has no semantic reason, delete it.
4. If icons outnumber labels, keep labels and keep only the icons that cut recognition cost.
5. If every gap is the same cramped value, widen section gaps first.
6. If the accent is the stock purple-blue, pick the palette deliberately and write the choice down.
7. If every element shouts at the same volume, hold the hierarchy to three levels.

## Procedure

1. Squint. If nothing dominates, fix the hierarchy before anything else.
2. Count the inventory: accents, radii, families, icon styles, card types.
3. Compare against the default template: centered hero, gradient, sub-copy, three cards.
4. List each tell found.
5. Apply the matching decision rule per tell.
6. Squint again. One clear focal path must survive the blur.
7. Run the logo-swap test: drop in a competitor's logo. If nothing looks wrong, the design is still generic.

## Anti-patterns

- Adding decoration to cure blandness. Fix: delete first, then hierarchy.
- Randomizing values to escape sameness. Fix: tokens chosen with intent.
- A new gradient on the same template. Fix: change the composition.
- Filling empty space with content. Fix: whitespace is the fix.
- Copying a trendy site wholesale. Fix: constraints and written brand decisions generate identity.

## Done checklist

- [ ] Each surviving gradient has a stated semantic reason.
- [ ] One radius per component class, from the scale.
- [ ] Every icon either carries a label or earns its place.
- [ ] One accent per view.
- [ ] The logo-swap test shows a distinctive composition.

The reliable tell is not any single choice but the absence of a decision: default shadows, evenly spaced everything, and a palette assembled from a framework's tokens all indicate that nothing was chosen against an alternative. Naming the alternative that was rejected is what turns a style into a taste.

## Sources

- https://github.com/anthropics/skills/tree/main/skills/frontend-design
- https://lawsofux.com/law-of-similarity/
- https://m3.material.io/styles/shape/overview
