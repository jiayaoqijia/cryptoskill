---
name: evaluating-during-training
domain: software-engineering/evaluating-during-training
trigger: "Measuring quality inside the training loop, not after."
anti_trigger: "Not for offline model-selection suites, and not for prompt grading."
scope: "Held-out checks inside the loop, checkpoints, and early stopping."
status: seedling
---

# Evaluating during training

## Standard

Training without in-loop evaluation is a single bet placed blind. The loop needs three instruments: the held-out loss as an early-warning curve, task-metric checkpoints on the quarantined evaluation set at fixed intervals, and judge-based spot checks on free-form outputs that the loss cannot score. Together they let the run stop when it should instead of when the epochs run out, and produce evidence that improvement generalised rather than memorised.

The task-metric checks need honest anchors: the untuned model's score on the same set — the baseline — and the deployment-like probes distinct from the templated training style. A gain recorded only on training-style inputs is a template artefact, and the fix is to include an unchanged-behaviour set: examples adjacent to the target task on which regression would be alarming, to catch the catastrophic forgetting SFT can cause.

Primary sources: <https://huggingface.co/docs/trl/index> and <https://huggingface.co/docs/transformers/training>.


The in-loop instruments earn their keep only if their thresholds were stated before the run began; a stopping rule improvised while watching the curve is a post-hoc justification dressed as a method, and the record should expose it by carrying the pre-registered rule verbatim beside the curve that triggered it.

## Decision rules

- Hold out evaluation data before curation ends and quarantine it from curation.
- Anchor every metric with the untuned model's baseline on the same set.
- Checkpoint on a fixed interval and evaluate at each cut.
- Include an unchanged-behaviour set to catch collateral regressions.
- Score free-form outputs with a judge calibrated to verified examples, never raw.
- State the early-stop rule in advance: which metric, which threshold, which direction.

## Procedure

1. Quarantine evaluation sets: task, deployment-like probes, unchanged-behaviour set.
2. Record the untuned model's baseline on every set.
3. Train with checkpointing at a fixed interval.
4. Evaluate each checkpoint on each set and build the curve.
5. At the pre-stated stopping point, tag the checkpoint candidate.
6. Verify the chosen candidate on the varied-probe set and on a second seed.

## Anti-patterns

- Evaluation data carved from the training set.
- One free-form probe judge, uncalibrated.
- Only task metrics checked, no unchanged-behaviour probe.
- Stopping rules improvised mid-run to justify the trend.

## Done checklist

- [ ] Three quarantined sets prepared before curation ended.
- [ ] Baselines on every metric recorded.
- [ ] Checkpoint curve built at intervals.
- [ ] Unchanged-behaviour regression checked.
- [ ] Stop rule applied as stated in advance.
- [ ] Chosen checkpoint verified on varied probes + second seed.

## Sources

- Trainer suite, eval callbacks: <https://huggingface.co/docs/trl/index>
- Training docs, checkpoints: <https://huggingface.co/docs/transformers/training>
- Preference paper, offline-metric framing: <https://arxiv.org/abs/2305.18290>
