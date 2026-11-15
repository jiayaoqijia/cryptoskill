---
name: preference-optimisation
domain: software-engineering/preference-optimisation
trigger: "Shaping behaviour that demonstrations cannot capture, via preferences."
anti_trigger: "Not for supervised format learning, and not for policy or safety adjudication."
scope: "From RLHF to DPO, reward models, and the data they need."
status: seedling
---

# Preference optimisation

## Standard

Some behaviour cannot be demonstrated, only compared: tone, helpfulness, refusal calibration. Preference optimisation trains on choices — given a prompt, response A is preferred to response B — and moves the model toward the chosen and away from the rejected. The classical route, RLHF, learns a reward model from the preferences then optimises the policy against it; the direct route, DPO, skips the reward model and optimises the preference comparison directly against the policy's own likelihood.

The reward model is where RLHF's risk concentrates: it learns the annotators' preferences, including their biases — verbosity, confidence, agreement — and the policy optimises whatever it learned, sometimes to absurdity. Preference data quality is therefore tighter than instruction-tuning: annotators must be consistent, disagreement must be measured, and the policy's optimisation must be bounded lest it game the learned reward. DPO reduces the machinery, so the data must be cleaner still.

Primary sources: <https://huggingface.co/docs/trl/index> and <https://arxiv.org/abs/2305.18290>.

## Decision rules

- Use preference optimisation only for behaviour a demonstration cannot show — comparison is the content.
- Measure annotator agreement and reject batches below the stated threshold.
- Bias-check preference pairs: verbosity and agreeableness are annotator favourites.
- In RLHF, evaluate the reward model alone before optimising the policy against it.
- Record the KL or reference penalty; unbounded optimisation games the reward.
- Test the result for over-optimisation: does the policy optimise the preference or the grader.

## Procedure

1. Define the behaviour dimension the preference data targets.
2. Collect prompt-and-pair batches and measure annotator agreement.
3. Reject and re-collect batches below the threshold.
4. Choose the mechanism — RLHF with reward model, or direct DPO — and record why.
5. Train with a stated optimisation bound; record the reference policy.
6. Evaluate on preferred-vs-rejected probes designed to catch reward gaming.

## Anti-patterns

- Preference data collected without consistency measurement.
- The policy optimising an unevaluated reward model.
- No bound: the policy finds the grader's blind spot and exploits it.
- Preference tuning as a substitute for decided policy — safety adjudication is not a data problem.
- Treating every formatting problem as a preference problem when demonstrations would do.

## Done checklist

- [ ] Behaviour dimension the preferences capture is stated.
- [ ] Annotator agreement measured; low batches rejected.
- [ ] Verbosity and confidence biases checked in the pairs.
- [ ] Reward-model-only evaluation done before policy optimisation.
- [ ] Optimisation bound and reference policy recorded.
- [ ] Reward-gaming probes run on the result.

## Sources

- TRL: Trainer for preference methods: <https://huggingface.co/docs/trl/index>
- Direct Preference Optimisation paper: <https://arxiv.org/abs/2305.18290>
- PEFT methods for bounded-parameter optimisation: <https://huggingface.co/docs/peft/index>
