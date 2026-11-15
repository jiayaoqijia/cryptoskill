---
name: whether-to-finetune
domain: software-engineering/whether-to-finetune
trigger: "Deciding whether to fine-tune at all, or keep prompting."
anti_trigger: "Not for choosing a training framework, and not for prompt craft."
scope: "The prompting-first test, and what weights buy that prompts cannot."
status: seedling
---

# Whether to fine-tune

## Standard

The default is prompting, and the burden of proof sits on training. Fine-tuning is justified when prompting has demonstrably failed — enough attempts, honest few-shot baselines, real effort on the context — or when the requirement is structurally beyond prompting: a stable output format worth baking in, a domain vocabulary the model repeatedly misses, or inference savings from prompts that no longer carry long instructions. The honest record shows the prompting baseline and why it fell short, before any training run exists.

The second test is data. Training needs hundreds to thousands of quality examples for the behaviour in question, and the team must be able to produce or source that data at a standard higher than the model's current output — feeding the model its own mediocre generations teaches it to be mediocre with confidence. Both tests must pass: prompting failure alone without data is a data problem; data without a prompting failure is a solution looking for a task.

Primary sources: <https://huggingface.co/docs/transformers/training> and <https://platform.openai.com/docs/guides/fine-tuning>.

## Decision rules

- Run the prompting baseline first and record it: examples, context budget, and failure evidence.
- State what weights would buy this task that context cannot: format permanence, latency, or knowledge.
- Confirm the data exists at scale and quality before any run.
- Prefer fine-tuning for stable, high-volume, well-defined behaviours; avoid it for exploratory or shifting tasks.
- Cost the full pipeline: data curation, training, evaluation, serving, and future re-training.
- Record the re-training trigger: base-model updates, task drift, and quality regression each mean another run.

## Procedure

1. Write and run the honest prompting baseline with few-shot examples.
2. Document its specific failure modes.
3. Test what the model needs: format, vocabulary, or behaviour — and whether context can hold it.
4. Inventory the available training data: volume, quality, provenance, and rights.
5. Compare total cost of ownership between the prompted and trained options.
6. Record the decision with the evidence, whichever way it goes.

## Anti-patterns

- Fine-tuning as the first resort: no baseline, no data assessment.
- Training to fix what a better prompt solves in an afternoon.
- Fine-tuning for a task that will change next quarter.
- Using the model's own output as training data without verifying quality.
- Forgetting the re-training commitment hidden in every fine-tune.

## Done checklist

- [ ] Prompting baseline recorded with failure evidence.
- [ ] The specific thing weights would buy is stated.
- [ ] Data inventory: volume, quality, provenance.
- [ ] Total-cost comparison done.
- [ ] Re-training trigger stated.
- [ ] Decision recorded with evidence.

## Sources

- Training documentation overview: <https://huggingface.co/docs/transformers/training>
- Provider fine-tuning guide: <https://platform.openai.com/docs/guides/fine-tuning>
- Background on adaptation, full fine-tuning feasibility, and LoRA trade-offs: <https://arxiv.org/abs/2106.09685>
