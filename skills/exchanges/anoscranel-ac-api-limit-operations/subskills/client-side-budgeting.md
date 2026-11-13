---
name: client-side-budgeting
domain: software-engineering/client-side-budgeting
trigger: "Enforcing the allowance before the request leaves, not after the rejection returns."
anti_trigger: "Not for prompt packing, and not for generic backoff theory."
scope: "Token buckets and quotas enforced before the request is sent."
status: seedling
---

# Client-side budgeting

## Standard

The provider enforces its limit at the boundary and answers excess with a 429; a well-operated system never lets a request reach that boundary when the local budget already knows it cannot be afforded. Client-side budgeting maintains the provider's allowance as a local, shared budget — a token bucket refilled at the contract's rate — and each outbound request decrements it before it is sent. When the bucket is empty, the request waits in a queue with a deadline rather than bouncing off the provider and counting against the rejection statistics.

The design consequence is that throttling moves inside the system, where it can be scheduled, prioritised, and surfaced. A queue with priorities lets the product decide what survives a constrained minute — the interactive request ahead of the batch job — and a deadline on each queued request lets the caller learn "not now" in seconds instead of hanging forever. The provider's 429 becomes a rare signal of contract change rather than a routine operating condition.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://sre.google/sre-book/handling-overload/>.

## Decision rules

- Maintain the allowance as a shared budget refilled at the contract's documented rate.
- Decrement before send; a request that cannot be afforded is queued, not sent.
- Prioritise the queue by product value, and state the priority rule in the configuration.
- Give every queued request a deadline and a rejection path that answers its caller promptly.
- Distinguish the budget's refill rate from its burst capacity, and size both from the contract.
- Track queue depth and wait times as first-class operational metrics.

## Procedure

1. Extract the refill rate and burst capacity from the limit contract.
2. Implement the shared budget with the request-cost that matches the binding dimension.
3. Wire the outbound path through the budget: decrement, or queue.
4. Configure the priority rule and the deadline per caller class.
5. Add queue depth, wait time, and budget-exhaustion metrics.
6. Load-test against the contract so the first saturation is in rehearsal, not production.

## Anti-patterns

- Sending optimistically and treating 429 as the budget.
- A single global queue that lets batch traffic starve interactive traffic.
- Queue deadlines so long that callers hang instead of hearing a fast no.
- Refilling the bucket at a remembered rate rather than the documented one.
- No metrics until the first incident forces an investigation.

## Done checklist

- [ ] Budget refilled at the documented rate.
- [ ] Decrement-before-send in the outbound path.
- [ ] Priority rule configured and stated.
- [ ] Per-class deadlines with prompt rejection paths.
- [ ] Queue and wait metrics instrumented.
- [ ] Saturation rehearsed under load test.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- Handling overload, Google SRE: <https://sre.google/sre-book/handling-overload/>
- Provider rate-limit documentation, Google: <https://ai.google.dev/gemini-api/docs/rate-limits>
