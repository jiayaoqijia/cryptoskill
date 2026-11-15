---
name: serving-the-adapted-model
domain: software-engineering/serving-the-adapted-model
trigger: "Deploying a fine-tuned model or adapter into service."
anti_trigger: "Not for the training loop, and not for application-level serving concerns."
scope: "Adapter deployment, base-model pinning, and drift when the base updates."
status: seedling
---

# Serving the adapted model

## Standard

A fine-tuned model is a compound artifact: the base weights plus the adaptation, and its identity is both together. Pinning the base is therefore the first serving decision — a provider that silently updates the base model can invalidate the adapter without a single change on your side, and the failure looks like a slow quality drift that no code review will find. The record captures the pair: base revision plus adapter version, deployed together or not at all.

Unmerged adapters trade inference overhead for swapability: many task adapters over one base is an efficient serving pattern, with routing by task and a clean rollback story — the adapter registry being the thing to keep tidy. Merged weights are faster and simpler to serve but freeze the pair; either way the serving plan decides the merge choice made upstream. Fallback is the last leg: the untuned base on the same endpoint is the graceful degradation target when the adapter misbehaves.

Primary sources: <https://huggingface.co/docs/peft/index> and <https://huggingface.co/docs/transformers/training>.

## Decision rules

- Pin the base-model revision in deployment; never a floating "latest".
- Record the base-adapter pair as a single compound version both in training and serving.
- Keep the adapter registry formal: names, versions, pinned base, and the data version each traces to.
- Choose merged vs unmerged from the serving plan, not from training convenience.
- Configure a fallback to the untuned base and test the fallback path, not only the happy path.
- Detect quality drift with a canary probe set scored on a schedule, with an alert on the trend.

## Procedure

1. Fix the base-model revision and record it.
2. Deploy the adapter or merged weights with the pair versioned together.
3. Wire the fallback path to the untuned base with the routing change written.
4. Define a canary probe set: short, fixed, scored automatically, deployed-like inputs.
5. Schedule scoring with a drift alert threshold.
6. Rehearse rollback: adapter off, base pinned, canary re-scored.

## Anti-patterns

- Serving against an unpinned "latest" base model.
- Adapters deployed without registry naming their data version.
- Choosing merge early, later needing adapter swap.
- No fallback: the first drift becomes an incident.
- No canary: drift is discovered by users.

## Done checklist

- [ ] Base revision pinned and recorded.
- [ ] Compound version: base + adapter deployed as a pair.
- [ ] Registry traces each adapter to its data version.
- [ ] Fallback wired and tested.
- [ ] Canary probes scored on a schedule.
- [ ] Rollback rehearsed.

## Sources

- PEFT, adapter loading and configuration: <https://huggingface.co/docs/peft/index>
- Training docs, save and share: <https://huggingface.co/docs/transformers/training>
- LoRA paper for adapter-merging mechanics: <https://arxiv.org/abs/2106.09685>
