---
name: token-and-cost-per-step
domain: software-engineering/token-and-cost-per-step
trigger: "Attaching tokens and dollars to each step of a run."
anti_trigger: "Not for the offline spend ledger alone, and not for provider rate tables."
scope: "Token and price attached to each step, not just to the request."
status: seedling
---

# Token and cost per step

## Standard

A run's cost is the sum of its generation steps, and each step's cost is visible in the usage object the provider returns: input tokens, cached tokens, output tokens. Captured per step — not aggregated per run or per day — the numbers attribute dollars to the trajectory: which reasoning step, which retrieved-context load, which retry consumed the budget. The per-view differs from a spend ledger: the ledger attributes dollars to tasks and tenants across a bill; this leaf puts them inside one run where a debugging question can reach them.

The arithmetic is deliberately simple: per-step counts multiplied by a dated rate, stored on the span. The value is placement. Cost attached to the span that caused it turns "this run cost forty cents" into "the third retrieval inflation cost twenty-eight of them", and that is a statement someone can act on without another query round.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/pricing> and <https://opentelemetry.io/docs/specs/semconv/gen-ai/>.

## Decision rules

- Record input, cached-input, and output token counts per generation, at capture time.
- Compute dollars per span at a dated rate; the currency belongs to the span that caused it.
- Store both raw counts and computed dollars; rates change and recomputation must be possible.
- Attribute tool-call cost by duration when the tool is metered, by tokens when it wraps a model.
- Sum to run total; reconcile run totals against the provider usage object, not against another aggregation.
- Flag steps whose cost exceeds a stated threshold within the run, not only at the end.

## Procedure

1. Take the usage object at each generation step.
2. Write input/cached/output counts onto that span.
3. Multiply at the dated rate and store dollars beside the counts.
4. Attach duration or usage for wrapped model calls.
5. Sum per run; reconcile against the provider's total.
6. Set and record the per-step threshold alerts.

## Anti-patterns

- Cost totals at the run or day level; per-step attribution lost.
- Dollars without the underlying token counts; recomputation impossible after a rate change.
- Mixing ledger currency into step dollars — keep this single-run.
- Computing from token counts not written at the time — reconstruction drifts.
- No per-step threshold; the expensive step discovered at month's end.

## Done checklist

- [ ] Usage counts on every generation span.
- [ ] Dollars per span at a dated rate.
- [ ] Raw counts stored beside computed dollars.
- [ ] Tool meters attached by duration or tokens.
- [ ] Run sum reconciled against the usage object.
- [ ] Per-step threshold set.

## Sources

- Token pricing basis: <https://docs.anthropic.com/en/docs/about-claude/pricing>
- GenAI usage conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- OpenAI usage context: <https://platform.openai.com/docs/guides/prompt-caching>
