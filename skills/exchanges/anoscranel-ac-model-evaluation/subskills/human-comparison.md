---
name: human-comparison
domain: prompt-engineering/human-comparison
trigger: "Running human side-by-side and preference collection honestly."
anti_trigger: "Not for judge calibration, and not for grading rubric design in general."
scope: "Preference data and side-by-side as a separate instrument."
status: seedling
---

# Human comparison

## Standard

Some constructs cannot be scored by any check or judge: helpfulness, tone fit with a product, and quality-of-writing in the subjective sense. For these, the instrument is the blind side-by-side — a human sees two outputs, unlabelled as to model and order, and picks a winner or a tie. The design is the defence: blind order removes position bias, model labels removed removes allegiance, ties allowed prevents forced distinctions that inject noise, and light guidelines beat heavy rubrics because a heavy rubric turns a preference study into a rubric-compliance study.

Preference data is a statistical instrument like any other: few raters and few comparisons give a noisy win-rate, and the reading needs the same interval honesty as any other metric — a 55 percent preference on 40 comparisons is a tie wearing a tiebreaker's clothes. Raters also disagree with each other, and inter-rater agreement is worth measuring: it bounds how much of the "preference" is the construct and how much is the rater. The instrument answers a specific question — which output do people prefer when shown both — and reading it as general quality is how a suite drifts from evidence into marketing.

Primary sources: <https://arxiv.org/abs/2306.05685> and <https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback>.

## Decision rules

- Blind the order and the model identity on every comparison shown.
- Allow ties; forced choices manufacture noise.
- Give light guidelines, not a rubric that hijacks the judgement.
- Compute inter-rater agreement and report it with the win-rate.
- Report the number of raters and comparisons with every preference percentage.
- Mark within-noise preferences as ties in the record.

## Procedure

1. Sample output pairs from the same task distribution for every model pair.
2. Randomise position and strip model identity before display.
3. Give raters the construct's one-line definition and a tie option.
4. Collect enough comparisons to bound the interval at a stated width.
5. Compute win-rates and inter-rater agreement.
6. Record the protocol — guidelines, blindness, sample story — beside the numbers.

## Anti-patterns

- Showing the models' names to raters.
- Forcing a winner on every pair.
- Preference on 20 comparisons reported as a victory.
- A rubric so detailed the raters grade the rubric instead.
- Reading a preference on one construct as overall quality.

## Done checklist

- [ ] Order and identity blinded.
- [ ] Tie option present and honoured.
- [ ] Guidelines light and stated.
- [ ] Comparison count sufficient for the stated interval.
- [ ] Inter-rater agreement computed.
- [ ] Protocol recorded beside results.

## Sources

- Human evaluation methodology survey: <https://arxiv.org/abs/2306.05685>
- Preference data and human feedback context: <https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback>
- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
