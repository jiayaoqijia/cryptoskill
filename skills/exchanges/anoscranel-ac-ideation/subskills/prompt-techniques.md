---
name: prompt-techniques
domain: critical-thinking/prompt-techniques
trigger: "A divergent pass that has stalled or produces only obvious ideas; needing a different angle to break a fixed frame"
anti_trigger: "Framing the decision before generating (subskills/framing-the-question.md); scoring and filtering the resulting ideas (subskills/convergence-scoring.md)"
scope: "A bank of idea-generation prompts with when to use each: SCAMPER, analogical transfer, inversion, constraint add/remove, worst-idea flip, morphological analysis, 10x and 0.1x"
status: "seedling"
---

# Prompt Techniques

## Standard

- **Eberle, _SCAMPER_ (1971)**: substitute, combine, adapt, modify, put to another use, eliminate, reverse — a checklist that forces a change to each attribute of the existing thing. <https://www.mindtools.com/ao2rt8j/scamper/>
- **Gick & Holyoak (1980)**: analogy to a solved problem in another domain transfers the solution structure when the surface details differ. <https://doi.org/10.1016/0010-0285(80)90013-4>
- **Zwicky, morphological analysis**: combine independent attribute lists into a grid and explore the cells for new combinations. ⚠️ The attribution to Zwicky is conventional; the method is often re-described without his full formal apparatus. <https://www.swemorph.com/>
- **10x and 0.1x framing**: forcing a ten-times or one-tenth target breaks the assumption that the current scale is fixed.

## Decision rules

1. If the ideas are all variants of one thing, use SCAMPER or add/remove constraint, not more of the same prompt.
2. If the problem feels novel but resembles a solved one elsewhere, use analogical transfer.
3. If the room is stuck defending the status quo, use inversion or the worst-idea flip.
4. If the design space has several independent axes, use morphological analysis.
5. If the session treats the current scale as given, use 10x and 0.1x.

## Procedure

1. Pick one technique; state which and why before applying it.
2. SCAMPER: run each of the seven verbs against the current thing, one at a time.
3. Analogical transfer: name the essential structure, find a field that already solved it, map the solution back.
4. Inversion: ask "what would guarantee failure", list the answers, then reverse each one.
5. Constraint add/remove: remove one constraint and see what opens up; add one and see what tightens.
6. Worst-idea flip: generate the worst ideas, then flip each into its opposite.
7. Morphological analysis: list 2 to 4 independent attributes, list values for each, combine the cells, scan the grid.
8. 10x and 0.1x: restate the target ten times bigger, then one-tenth; generate at each scale.

## Anti-patterns

- **Technique-hopping.** Switching techniques every two minutes; none runs deep. Fix: one technique, run to a quota.
- **SCAMPER without a target.** Running verbs against nothing in particular. Fix: fix the thing being transformed first.
- **Forced analogy.** A distant field applied with no structural match. Fix: match the structure, not the surface.
- **Worst ideas kept, not flipped.** The flip is the whole point. Fix: always produce the opposite of each.
- **10x without 0.1x.** "10x" alone becomes fantasy. Fix: run both; each changes the frame differently.

## Done checklist

- [ ] One technique was named and justified before use.
- [ ] The technique produced a set of ideas, not a single idea.
- [ ] Ideas were captured as they came, not filtered.
- [ ] At least one technique forced a change of frame, not a variation on it.

## Sources

- Eberle, _SCAMPER_: <https://www.mindtools.com/ao2rt8j/scamper/>
- Gick & Holyoak (1980): <https://doi.org/10.1016/0010-0285(80)90013-4>
- Zwicky, morphological analysis: <https://www.swemorph.com/>