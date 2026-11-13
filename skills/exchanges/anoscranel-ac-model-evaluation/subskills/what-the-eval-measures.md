---
name: what-the-eval-measures
domain: prompt-engineering/what-the-eval-measures
trigger: "Deciding what the evaluation measures before building any case."
anti_trigger: "Not for prompt wording, and not for running the harness."
scope: "Deciding the question and decision the eval serves."
status: seedling
---

# What the eval measures

## Standard

An evaluation begins with the decision it serves, not with examples. "Is model A better than model B" is not a question until "better at what" is answered in the task's own terms: which outputs the product actually consumes, what makes them acceptable, and what failure costs. An eval built without that anchor measures whatever its cases accidentally contain — often surface fluency — and ranks models by a property the decision does not use.

The measured construct should be named before a single case is written: task accuracy against a defined answer key, instruction adherence to a stated spec, robustness under malformed input, refusal behaviour on a stated category, latency, or cost. Each name implies different case design and a different scoring tier. A suite that mixes constructs without naming them produces one aggregate number that answers no question in particular, and the number will still be quoted — named constructs are what stop it being quoted for the wrong decision.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/evaluate> and <https://arxiv.org/abs/2306.05685>.

## Decision rules

- State the decision the evaluation informs: adopt, reject, upgrade, or route.
- Name the measured construct in task terms before writing any case.
- Separate constructs that need different case designs into separate sub-suites.
- Define acceptance per construct: what makes an output acceptable, in one sentence each.
- State the population of real requests the cases must represent.
- Record the cost of each failure type, so scoring weights follow consequences.

## Procedure

1. Write the decision the eval serves and who owns it.
2. List candidate constructs from the task's real output consumers.
3. Name the primary construct and mark others secondary.
4. Define acceptance for each construct in one sentence.
5. Describe the request population the cases must sample.
6. Assign scoring weight by failure cost, not by counting convenience.

## Anti-patterns

- Cases written before the construct is named.
- One aggregate score spanning unrelated constructs.
- Measuring fluency because it is easy to notice.
- Weights that follow case counts rather than failure costs.
- An eval with no decision attached — measurement as a hobby.

## Done checklist

- [ ] Decision and owner stated.
- [ ] Primary construct named in task terms.
- [ ] Acceptance defined per construct.
- [ ] Request population described.
- [ ] Failure costs recorded.
- [ ] Weights assigned by cost.

## Sources

- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
- Survey of task design in language-model evaluation: <https://arxiv.org/abs/2306.05685>
- Open evaluation harness practice: <https://github.com/EleutherAI/lm-evaluation-harness>
