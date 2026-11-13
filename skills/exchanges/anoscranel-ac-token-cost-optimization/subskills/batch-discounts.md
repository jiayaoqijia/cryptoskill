---
name: batch-discounts
domain: prompt-engineering/batch-discounts
trigger: "Deciding whether a workload should pay batch rates instead of realtime."
anti_trigger: "Not for batch endpoint mechanics, and not for request-packing."
scope: "Trading latency for the batch discount, honestly."
status: seedling
---

# Batch discounts

## Standard

Batch APIs offer a documented discount — commonly around half the realtime rate — in exchange for asynchronous completion measured in hours rather than seconds. The trade is clean when the work was never interactive: classification over a corpus, evaluation runs, backfills, enrichment. The batch queue converts a discount into a scheduling commitment, and the decision is whether the consumer of the results can absorb that delay.

The dishonest version treats batch as free money and queues work that users are waiting for. The honest version classifies workloads by their latency budget first: interactive requests stay on the realtime path; anything whose results are consumed next morning or next week is a batch candidate on its merits. The discount is then applied only where the latency budget permits it.

Primary sources: <https://platform.openai.com/docs/guides/batch> and <https://docs.anthropic.com/en/docs/build-with-claude/batch-processing>.

## Decision rules

- Classify the workload's latency budget before considering the discount.
- Record the discount and the turnaround window from the provider's dated docs.
- Batch only work whose consumers are not blocked on the result.
- Keep an eye on partial failure: a partially failed batch is re-run work, not free work.
- Size the batch queue so a retry after partial failure does not double the spend.
- Measure the realized saving per task against the realtime baseline, not the headline.

## Procedure

1. List workloads and their latency budgets.
2. Mark everything with a budget beyond the batch turnaround as batch-eligible.
3. Record the discount and turnaround from the provider documentation, dated.
4. Pilot one workload; measure realized per-task cost and turnaround.
5. Check partial-failure handling and the retry cost.
6. Adopt where it wins; leave interactive paths on realtime.

## Anti-patterns

- Batching user-facing requests to chase the headline discount.
- Assuming the turnaround window; it is a commitment, not a guess.
- Ignoring partial failure until a re-run doubles a month's spend.
- Comparing headline discount rather than realized per-task dollars.
- Forgetting capacity in the other direction: batch does not raise interactive limits.

## Done checklist

- [ ] Latency budgets classified.
- [ ] Batch-eligible set defined.
- [ ] Discount and turnaround recorded with date.
- [ ] Pilot measured on realized dollars.
- [ ] Partial-failure retry cost checked.
- [ ] Interactive paths kept realtime.

A further boundary to draw is between batch and queue: batching is a pricing decision against the provider, not a scheduling decision inside your system. Work that needs sequencing, retries, or dependency ordering keeps that structure regardless; the batch API only changes when the calls are made, not what depends on them. Conflating the two yields batch jobs that act like workflows and lose the discount anyway when partial failures force serial re-runs.

## Sources

- Batch API guide: <https://platform.openai.com/docs/guides/batch>
- Message Batches API: <https://docs.anthropic.com/en/docs/build-with-claude/batch-processing>
- Pricing context: <https://docs.anthropic.com/en/docs/about-claude/pricing>
