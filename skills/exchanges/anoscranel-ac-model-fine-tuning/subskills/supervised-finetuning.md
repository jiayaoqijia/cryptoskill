---
name: supervised-finetuning
domain: software-engineering/supervised-finetuning
trigger: "Running supervised fine-tuning and reading its training signals."
anti_trigger: "Not for preference optimisation, and not for the model's production lifecycle."
scope: "SFT mechanics, loss curves, and the overfitting traps."
status: seedling
---

# Supervised fine-tuning

## Standard

Supervised fine-tuning computes loss on the target tokens of the training pairs and updates the weights to reduce it. The visible signals are the training loss, which falls as the model memorises, and the held-out loss, which falls while the model generalises and then rises when it begins to memorise instead. The gap between the two is the overfit signal, and the checkpoint at the held-out minimum is usually the model worth keeping.

The traps are specific. The model can learn the surface pattern of the training pairs — the template, not the task — and the loss will drop convincingly while the behaviour on varied inputs collapses. It can also forget: single-domain training datasets are apt to narrow the model on everything else, which is catastrophic forgetting, and mixed general-purpose data counterweights it. The evaluation set for the held-out loss must be the deployment-like data, otherwise the curve measures the wrong generalisation.

Primary sources: <https://huggingface.co/docs/transformers/training> and <https://huggingface.co/docs/datasets/index>.

## Decision rules

- Watch the training and held-out losses separately and plot both across epochs.
- Stop at or near the held-out minimum; more epochs after it is memorisation.
- Reserve evaluation data resembling deployment input, quarantined before curation ends.
- Mix general-purpose data when the target data is narrow, weighted to preserve breadth.
- Save multiple checkpoints at intervals; the best one is picked after the run, not during.
- Test on varied-input benchmarks (not the templated training style) before accepting the result.

## Procedure

1. Fix the data versions and reserve the held-out sets.
2. Compute a baseline: the untuned model on the same verification set.
3. Train with held-out evaluation checkpointed at intervals.
4. Plot both losses across time/epochs and identify the held-out turning point.
5. Test the chosen checkpoint against varied-input probes and the failure-mode set.
6. Train a second seed to check the result holds beyond seed noise.

## Anti-patterns

- Only looking at the training loss as it falls.
- Training well past the held-out turning point because "more is better".
- Testing only on the templated training style.
- No general-data counterweight in a narrow dataset.
- One seed and one run: nothing in fine-tuning is real before the seed replication.

## Done checklist

- [ ] Data versions fixed, held-out sets quarantined at curation time.
- [ ] Loss curves plotted for training and held-out separately.
- [ ] The held-out turning point identified.
- [ ] Checkpoints saved and scored on varied inputs.
- [ ] General-data counterweight added for narrow data.
- [ ] A second seed holds the result.

## Sources

- Transform Library training docs: <https://huggingface.co/docs/transformers/training>
- Datasets documentation: <https://huggingface.co/docs/datasets/index>
- LoRA paper background on full fine-tuning feasibility constraints: <https://arxiv.org/abs/2106.09685>
