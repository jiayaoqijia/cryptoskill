---
name: spend-ledger
domain: prompt-engineering/spend-ledger
trigger: "Building the ledger that attributes dollars to tasks and tenants."
anti_trigger: "Not for request-packing, and not for provider billing portals."
scope: "Attributing dollars to tasks, steps, and tenants."
status: seedling
---

# Spend ledger

## Standard

A provider bill is one number; a spend ledger is the same dollars split by what caused them. Attributed spend turns a bill from a surprise into a budget: which task types, which steps in a pipeline, which tenants or customers drove the dollars. The usage object returned with each response carries input, cached, and output token counts, so the attribution is plumbing — record the counts at request time, multiply by dated rates, and aggregate by the labels that decisions use.

The labels are the design decision. Dollars per task, per step, per tenant, and per model tier each answer a different question, and the ledger should carry enough labels to answer all of them without becoming a data warehouse. The discipline is durable collection at request time — reconstruction from a month-end bill is forensic work, and provider dashboards summarise too late and too coarsely to act on.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/pricing> and <https://osf.io/prereg/>.

## Decision rules

- Record input, cached-input, and output token counts per request, at request time.
- Attach labels before storage: task type, pipeline step, tenant, tier.
- Price the ledger at dated rates; repriced history is a new column, not an overwrite.
- Reconcile the ledger total against the invoice monthly; drift found is drift fixed.
- Alert on dollars-per-task drift, not just on total spend.
- Track the retry count beside the dollars; retries are spend the task did not need.

## Procedure

1. Choose the label set decisions will use: task, step, tenant, tier.
2. Capture the usage counts and labels in one durable write per request.
3. Aggregate per label per day at dated rates.
4. Compare ledger totals against the invoice; reconcile differences.
5. Alert on per-task drift beyond a stated threshold.
6. Review the label set quarterly: relabel when the questions change.

## Anti-patterns

- Total-spend-only tracking: no attribution, no decisions.
- Reconstructing from the invoice after the month closed.
- Labels applied after the fact, from logs that lack the task context.
- Silently repricing history when rates change.
- Alerting only on the total; per-task drift hides under a flat cap.

## Done checklist

- [ ] Usage counts captured at request time.
- [ ] Labels attached in the same write.
- [ ] Dated-rate pricing applied.
- [ ] Monthly invoice reconciliation done.
- [ ] Per-task drift alerts set.
- [ ] Retry counts beside the dollars.

## Sources

- Usage and pricing basis: <https://docs.anthropic.com/en/docs/about-claude/pricing>
- Stated-metric discipline: <https://osf.io/prereg/>
- Batch cost context: <https://platform.openai.com/docs/guides/batch>
