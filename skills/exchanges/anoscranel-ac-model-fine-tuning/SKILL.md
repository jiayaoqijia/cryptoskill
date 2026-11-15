---
name: ac-model-fine-tuning
description: 'Adapting a pretrained model to your task by changing its weights: when fine-tuning beats prompting at all, the training-data craft of instruction pairs and preference pairs, SFT and its overfit traps, LoRA-class parameter-efficient methods, preference optimisation from RLHF to DPO, evaluating during training rather than after, serving the trained adapter beside its pinned base model with canary probes against quality drift, and the fine-tuning pipeline record. It explains the adaptation pipeline and its failure modes; it never promises a benchmark score. Use when asking "fine-tune a model", "LoRA adapter", "SFT", "DPO", "preference optimization", "RLHF alternative", "training data curation", "adapter serving", "catastrophic forgetting", "fine-tuning record", "canary probes", "base model pinned". Not for ML systems practice around the trained model (ac-ml-systems-practice), not for prompt and context craft (ac-prompt-engineer), not for model evaluation suites for selection (ac-model-evaluation).'
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Model fine-tuning

## Overview

Fine-tuning changes a model's weights to specialise it; prompting changes only what it reads. The trade is fundamental: weights bake behaviour in permanently and cheaply at inference, while prompts keep behaviour provisional and editable at the cost of context tokens every single call. Fine-tuning earns its place when prompting has demonstrably failed at the task or the behaviour cannot fit the window — a format so stable it justifies training, a domain vocabulary the model keeps missing, latency savings from shorter prompts.

This skill covers the adaptation pipeline: the decision to train at all, the data craft that decides the outcome before training starts, supervised fine-tuning and its overfitting traps, parameter-efficient adaptation, preference optimisation for behaviour that demonstrations cannot capture, evaluation during training, and serving the result. The systems practice around trained models belongs to a sibling skill; the craft of writing prompts belongs to its own.

Primary sources: <https://huggingface.co/docs/transformers/training> and <https://huggingface.co/docs/peft/index>.

## When to use

- When deciding whether to fine-tune or keep prompting.
- When curating instruction or preference training data.
- When choosing between full, supervised, and parameter-efficient methods.
- When preference optimisation is needed to shape behaviour.
- When serving a fine-tuned model or adapter.

## When NOT to use

- For the ML systems practice around a trained model in production (use ac-ml-systems-practice).
- For prompt and context craft (use ac-prompt-engineer).
- For evaluation suites used to select between models (use ac-model-evaluation).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/whether-to-finetune.md` | `software-engineering/whether-to-finetune` | The prompting-first test, and what weights buy that prompts cannot. |
| `subskills/training-data-craft.md` | `software-engineering/training-data-craft` | Instruction pairs and preference pairs, where quality makes or breaks the run. |
| `subskills/supervised-finetuning.md` | `software-engineering/supervised-finetuning` | SFT mechanics, loss curves, and the overfitting traps. |
| `subskills/parameter-efficient-methods.md` | `software-engineering/parameter-efficient-methods` | LoRA and adapter methods, rank and placement choices, merging. |
| `subskills/preference-optimisation.md` | `software-engineering/preference-optimisation` | From RLHF to DPO, reward models, and the data they need. |
| `subskills/evaluating-during-training.md` | `software-engineering/evaluating-during-training` | Held-out checks inside the loop, checkpoints, and early stopping. |
| `subskills/serving-the-adapted-model.md` | `software-engineering/serving-the-adapted-model` | Adapter deployment, base-model pinning, and drift when the base updates. |
| `subskills/finetuning-record.md` | `software-engineering/finetuning-record` | The written record: data version, recipe, metrics, and what failed. |

## Status and honest limits

Fine-tuning results are famously non-reproducible: the same data and recipe can diverge across library versions, random seeds, and base-model patches that providers ship silently. Nothing here promises a score or recommends a method; it states what each method does, what it costs, what data it requires, and the failure modes the record should catch. The decision to train is a commitment — base-model updates can silently invalidate a fine-tune, and a model that quietly regressed is worse than one that was never trained.
