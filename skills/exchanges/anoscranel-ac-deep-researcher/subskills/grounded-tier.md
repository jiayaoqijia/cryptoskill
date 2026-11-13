---
name: grounded-tier
domain: research-operations/grounded-tier
trigger: "\"ground this answer with citations\", \"I need sources Google itself has checked\", \"give me a cited answer on X\", \"the cascade couldn't prove it\"."
anti_trigger: "Routine lookups, sweeps, and fan-out search (subskills/retrieval-cascade.md); the grounded tier is conditional, never the default."
scope: "Firing the grounded search tier correctly: its gate conditions, batched sub-questions, mandatory citations, and the failure fallback"
status: "seedling"
---

# The grounded tier (conditional)

## Standard

The grounded tier answers through a search-grounded model and
returns source URLs with the answer. It fires only under three conditions:

1. The requester explicitly asked for a cited, grounded answer.
2. The claim is load-bearing, contested, or single-source and needs citations
 that the usual cascade did not produce.
3. The keyless tiers failed to yield a citable answer.

Batching is the discipline: related sub-questions go in one call as a numbered
list, because the quota counts requests, not sub-questions. Five to six
sub-questions per call is the sweet spot. The call pattern: send the numbered
list as ONE request to any search-grounded endpoint that returns source URLs,
and run it in the background when latency matters.

Citations are the tier's whole value. A grounded answer without source URLs is
a failed call. Retry it once, then fall back through the cascade. Two wording
rules are measured, not folklore: appending a terse-answer suffix strips the
citation metadata, and a minimal thinking setting strips grounding entirely.
Never use either.

## Decision rules

- Fire when a gate condition holds; otherwise stay in the cascade.
- One batched call beats six separate calls.
- If the return has no sources, the call failed. Never quote an uncited
 grounded answer as grounded.

## Procedure

1. Confirm a gate condition holds.
2. Pack the related sub-questions into one numbered list.
3. Send it as one request; keep the full prose prompt (no terse-answer suffix).
4. Capture the answer and every source URL into the evidence ledger.
5. On a citation-free return, retry once, then fall back and flag the gap.

## Anti-patterns

- The grounded tier as the default for routine lookups; it is the
 latency-expensive lane.
- Ten single-question calls where one batched call works.
- Quoting the answer while discarding the source URLs.
- Shortening the prompt with "answer briefly" and then wondering where the
 citations went.

## Done checklist

- A gate condition is written down before the call.
- The call carries multiple sub-questions where multiple exist.
- The ledger holds the answer plus its source URLs.
- Any citation-free return is marked failed, never used.

The tier's cost is latency and a hard quota, both of which argue for batching related sub-questions into one call rather than issuing them one at a time, and for recording how many calls a study consumed. A study whose grounding calls are not counted cannot be repeated within budget.

## Sources

- <https://osf.io/prereg/>
- <https://training.cochrane.org>
