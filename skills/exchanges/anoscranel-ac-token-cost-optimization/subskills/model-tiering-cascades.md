---
name: model-tiering-cascades
domain: prompt-engineering/model-tiering-cascades
trigger: "Choosing which tier of model a task or step should run on."
anti_trigger: "Not for request-packing, and not for eval-suite design."
scope: "Routing work to the cheapest tier that clears the bar, with escalation."
status: seedling
---

# Model tiering and cascades

## Standard

Providers sell the same interface at several price points. A cascade routes a task to the cheapest tier first and escalates only on evidence the cheap tier failed: a self-check, a judge, or an explicit failure. The saving is not the price gap; it is the gap multiplied by the fraction of work the cheap tier genuinely handles. If the cheap tier handles seventy percent, the blended cost falls most of the way toward the cheap rate for those requests.

The honest version measures before it cascades. Each escalation route carries its own failure mode — a lenient check lets weak answers through, a strict check pays strong-model prices twice, and a naive confidence reading can be worse than no check at all. The quality bar is per task, the check's error rate is measured against a sample, and the whole cascade is only kept if the measured blend beats the single-tier alternative.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/models/overview> and <https://platform.openai.com/docs/models>.

## Decision rules

- Establish the quality bar per task type before routing anything.
- Measure the cheap tier's pass rate on a fixed sample before trusting it.
- Escalate on a stated signal, and record the signal's own error rate.
- Compute blended cost per task from the measured pass rate, not the hoped-for one.
- Keep a single-tier baseline; a cascade that does not beat it is complexity without saving.
- Re-measure when either tier changes; tiering decisions rot as models update.

## Procedure

1. Define the task and its quality bar in a checkable form.
2. Run the cheap tier over a fixed sample; measure pass rate and judge agreement.
3. Choose the escalation signal and measure its error budget.
4. Compute blended dollars per task at the measured rates.
5. Compare against the single-tier baseline.
6. Keep the cascade only if it wins, and re-measure after any model change.

## Anti-patterns

- Cascading because it sounds thrifty, without a measured pass rate.
- A judge stricter than the task needs, paying strong-model rates twice.
- Escalating on model-stated confidence without calibrating it.
- Never re-measuring after a provider updates a tier.
- Treating the cheap tier as one tier — tier ladders differ across tasks.

## Done checklist

- [ ] Quality bar stated per task.
- [ ] Cheap-tier pass rate measured on a fixed sample.
- [ ] Escalation signal and its error rate recorded.
- [ ] Blended cost computed from measured rates.
- [ ] Single-tier baseline compared.
- [ ] Re-measure trigger set on tier changes.

## Sources

- Model tier overviews: <https://docs.anthropic.com/en/docs/about-claude/models/overview>
- Model catalogue: <https://platform.openai.com/docs/models>
- Pricing tables: <https://docs.anthropic.com/en/docs/about-claude/pricing>
