---
name: parameter-efficient-methods
domain: software-engineering/parameter-efficient-methods
trigger: "Choosing between full fine-tuning, LoRA, and adapter methods."
anti_trigger: "Not for the serving side alone, and not for preference optimisation."
scope: "LoRA and adapter methods, rank and placement choices, merging."
status: seedling
---

# Parameter-efficient methods

## Standard

Full fine-tuning updates every weight; parameter-efficient methods freeze the base and train a small addition — for LoRA, low-rank matrices inserted beside chosen weight layers, at a fraction of the memory and cost, with the base model untouched underneath. The trade is capacity: a low-rank adapter cannot learn as much as full tuning, and the art is choosing rank and placement so the adapter carries the task without the cost of full training.

Rank is the primary dial: a very low rank carries format and style adaptations cheaply; a domain-knowledge shift needs higher rank or full fine-tuning. Placement matters next — the original LoRA work showed attention projections carry most tasks, but which layers benefit varies by task. Adapters can stay separate (swappable, many-to-one over the base) or be merged into the weights (faster inference, one adapter per artifact) — and that choice interacts with the serving plan.

Primary sources: <https://huggingface.co/docs/peft/index> and <https://arxiv.org/abs/2106.09685>.

## Decision rules

- Start with LoRA-class methods before full fine-tuning; the fail-safe is real.
- Move to full fine-tuning only after higher-rank adapters demonstrably plateau.
- Record rank, target modules, and scaling per run; anyone reproducing needs all three.
- One adapter per data version, named and versioned like code artifacts.
- Decide merged vs unmerged at design time; both are valid but only one fits a serving plan.
- Compare the adapter's held-out gain against the prompting baseline and record both.

## Procedure

1. Start at the lowest sensible rank for the task class.
2. Record the target modules the run trains.
3. Train, evaluate, and record the gain with exact hyperparameters.
4. If the gain plateau is inadequate, raise rank before abandoning PEFT.
5. Those still short move to full fine-tuning with memory and cost budgeted.
6. Name, version, and store every adapter beside its data version.

## Anti-patterns

- Full fine-tuning by default; the memory and cost to prove a small task.
- Rank chosen arbitrarily high, with no record of where the gain stops.
- Unversioned ad-hoc adapters that cannot be traced to a dataset version.
- Merged weights where serving needs separable adapters.
- Comparing the adapter result to the untuned model, not the prompting baseline.

## Done checklist

- [ ] Rank and target modules recorded per run.
- [ ] Gain compared against the prompting baseline.
- [ ] Rank increased before concluding PEFT is insufficient.
- [ ] Full fine-tuning costed in memory, money, and time.
- [ ] Adapters named and versioned like code.
- [ ] Merge decision recorded with the serving plan.

## Sources

- PEFT library documentation: <https://huggingface.co/docs/peft/index>
- Original LoRA paper: <https://arxiv.org/abs/2106.09685>
- Trainer library: <https://huggingface.co/docs/trl/index>
