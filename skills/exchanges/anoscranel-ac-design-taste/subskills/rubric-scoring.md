---
name: rubric-scoring
domain: software-engineering/design-taste
trigger: "Score this design; rate this UI out of ten; compare this round to the last critique; give me a design rubric"
anti_trigger: "Running the critique itself (subskills/critique-protocol.md); a Nielsen pass with severity (subskills/heuristic-evaluation.md); performance scoring"
scope: "The 0-10 anchored rubric across six dimensions inside this skill, plus caps, deltas, and reporting"
status: seedling
---
# Rubric Scoring

## Standard

- **Behaviorally Anchored Rating Scales (BARS)**: anchors beat vibes for repeatable scores. ⚠️ Psychometrics convention, applied here as house practice.
- **NN/g severity method**: scores become comparable only when rated against written anchors with reasons (https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/).
- **WCAG 2.2** is the floor that caps the color score (https://www.w3.org/TR/WCAG22/).

## The rubric

Six dimensions: layout, type, color, spacing, motion, consistency.

| Score | Anchor meaning |
|---|---|
| 0-2 | No structure; elements float without a grid, scale, or hierarchy |
| 3-4 | Structure exists but is applied inconsistently |
| 5-6 | Consistent and competent, but generic |
| 7-8 | Clear hierarchy; deliberate palette, scale, and rhythm |
| 9-10 | Distinctive and exemplary; survives the logo-swap test |

## Decision rules

1. Score each dimension on its own. Discuss deltas before any averaging.
2. If a WCAG contrast pair fails, color caps at 4.
3. If spacing or radius values sit off the scale, consistency caps at 4.
4. If two rounds differ by more than 2 on a dimension, re-read the anchor text. Neither side wins by seniority.
5. Judge against the anchors, never against personal preference.
6. If a dimension is absent (a static mock has no motion), mark n/a, never 0.
7. If torn between two numbers, take the lower one. Critiques exist to find problems. ⚠️ House convention.

## Procedure

1. Declare the scope and the surfaces scored.
2. Read the anchor table aloud, all six dimensions.
3. Finish the critique pass first. Scores come after observations.
4. Score layout, type, color, spacing, motion, consistency, with one evidence line each.
5. Apply the caps and the n/a marks.
6. Compare against the previous round. Explain every delta larger than 2 in writing.
7. Report the six scores and name the lowest two as the fixes.

## Anti-patterns

- One overall vibe score. Fix: six dimensions.
- Scoring before observing. Fix: critique first, score second.
- Reading 5 as failure. Fix: 5 is competent and generic; decide whether the product needs more.
- Averaging away a broken axis. Fix: report caps and name the lowest axis.
- Marking absent dimensions 0. Fix: mark n/a.

## Done checklist

- [ ] Six dimensions scored, each with an evidence line.
- [ ] Caps applied wherever a hard failure exists.
- [ ] Deltas above 2 explained in writing.
- [ ] The lowest two dimensions named as the fixes.

## Sources

- https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
- https://www.w3.org/TR/WCAG22/
