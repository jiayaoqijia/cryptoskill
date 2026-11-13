---
name: contamination
domain: prompt-engineering/contamination
trigger: "Assessing whether benchmark data has leaked into training."
anti_trigger: "Not for dataset provenance in research, and not for prompt leakage attacks."
scope: "Why held-out data no longer guarantees a fresh test."
status: seedling
---

# Contamination

## Standard

A benchmark measures what a model can do only if the model has not already memorised its answers. Frontier models are trained on large fractions of the public web, and public benchmarks are on the public web; the questions they contain, and often their answers, are candidates for inclusion in training data. A contaminated benchmark's score is partly a memory test, and after a benchmark becomes a target that labs train and select against, its scores stop declining gracefully and start inflating: the measure becomes the goal, and the goal stops measuring the construct.

The practical defences are structural, not cryptographic. Time-splitting — building cases from material created after the model's training cutoff — keeps freshness for a while. Private case construction, drawn from your own production requests and never published, is the strongest guarantee available to a practitioner, and the one reason an internal suite outperforms every public benchmark for adopt-and-route decisions. Canary strings and memorisation probes detect the grossest contamination; absence of a probe firing is weak evidence, and the posture is to assume some contamination for any public data and weight such scores accordingly.

Primary sources: <https://arxiv.org/abs/2306.05685> and <https://github.com/EleutherAI/lm-evaluation-harness>.

## Decision rules

- Treat every public benchmark's score as partly a memory measurement; weight it accordingly.
- For adopt-decisions, prefer suites built from private production data.
- Date-stamp cases and prefer post-cutoff material where public sources must be used.
- Where possible, run memorisation probes adapted from canary practice as a coarse check.
- Record the training-cutoff date of each model compared, beside its scores.
- Never publish your private set; publishing converts it into training data for the next generation.

## Procedure

1. Classify each suite as public, semi-public, or private.
2. Date every public case; note which predate the models' training cutoffs.
3. Run canary or memorisation probes on public suites where feasible.
4. Weight the decision toward private, production-sourced cases.
5. Record each model's training cutoff beside the comparison.
6. Rotate in fresh cases on a stated cadence so the suite ages slower than the models.

## Anti-patterns

- Quoting public benchmark scores as pure capability.
- Publishing a private set in the act of writing it up.
- Probing for contamination, finding none, and concluding the data is clean.
- Comparing models while forgetting their cutoffs differ.
- A frozen suite used for years while models train past it.

## Done checklist

- [ ] Suites classified public or private.
- [ ] Case dates and training cutoffs recorded.
- [ ] Probes run where feasible.
- [ ] Private data weighted for adopt-decisions.
- [ ] Cutoffs stated beside scores.
- [ ] Fresh-case rotation cadence set.

## Sources

- Task design and contamination survey: <https://arxiv.org/abs/2306.05685>
- Evaluation harness practice: <https://github.com/EleutherAI/lm-evaluation-harness>
- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
