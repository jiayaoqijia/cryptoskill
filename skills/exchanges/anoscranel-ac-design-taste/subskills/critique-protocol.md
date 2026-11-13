---
name: critique-protocol
domain: software-engineering/design-taste
trigger: "Critique this UI; review this mock; run a design crit; what is wrong with this screen; give me a critique order; host this critique"
anti_trigger: "Scoring against the 0-10 rubric (subskills/rubric-scoring.md); the Nielsen ten-heuristic protocol (subskills/heuristic-evaluation.md); building the UI itself"
scope: "The order, checklist, and hosting etiquette of a design critique in this skill"
status: seedling
---
# Critique Protocol

## Standard

- **Nielsen Norman Group, "How to Conduct a Heuristic Evaluation"**: evaluators pass independently, then merge findings (https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/).
- **Gestalt principles**: the eye groups by proximity and similarity before it reads detail (https://www.nngroup.com/articles/gestalt-proximity/).
- **Scanning research**: layout and position steer first fixations (https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/).
- **Perception order** layout, hierarchy, type, color, interaction: ⚠️ practitioner convention; it matches how the eye resolves, from coarse geometry to fine detail.
- **Crit format**: silent written notes before discussion, to protect independent judgment (NN/g, same how-to article).

## Decision rules

1. If a fix appears before the problem has words, stop. Name the problem first.
2. If the squint test fails, fix hierarchy and spacing before type or color.
3. If feedback is a feeling ("cluttered", "cheap"), convert it: element, attribute, effect.
4. If two options trade off, judge by the user's top task, not by preference.
5. If a crit has 12 findings, ship the top three against the top task. Depth beats coverage.
6. If reviewers disagree, keep both readings, then arbitrate with the rubric, not the louder voice.

## Procedure

1. Write the user and the top task in one sentence.
2. Look at the screen for 30 seconds. Note the first three things the eye hits.
3. Pass 1, layout: grid, dominant region, alignment of edges.
4. Pass 2, hierarchy: the eye path matches the task order.
5. Pass 3, type: measure, scale steps, weights.
6. Pass 4, color: accent count, state signaling, contrast suspects.
7. Pass 5, interaction: affordances, feedback, empty and error states.
8. Squint test: what survives the blur?
9. Write each finding as one problem statement with evidence, ranked by damage to the top task.
10. Host a crit: a two-minute presentation, silent notes, discussion, recorded decisions.

## Anti-patterns

- Pitching fixes first. Fix: three observations before any solution.
- Taste words without attributes. Fix: element, attribute, effect.
- Reviewing only the hero. Fix: run the whole flow, including empty and error states.
- Scoring mid-critique. Fix: finish all passes first.
- The loudest reviewer wins. Fix: silent written notes before talk.

## Done checklist

- [ ] User and top task written in one sentence.
- [ ] All five passes run in order.
- [ ] Findings are problem statements with evidence.
- [ ] Findings ranked by damage to the top task.
- [ ] Squint test result recorded.

## Sources

- https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- https://www.nngroup.com/articles/gestalt-proximity/
- https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/
- https://lawsofux.com/
