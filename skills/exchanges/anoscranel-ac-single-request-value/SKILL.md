---
name: ac-single-request-value
description: "Maximum value from every request to a metered or rate-limited model API: batching sub-questions into one planned request, packing context so one round trip answers many needs, when a clarifying question earns its round trip, pre-reading so the request arrives prepared, multi-part outputs in one call, degrading rather than retrying, and the per-request ledger. It treats requests per answer as the cost metric; it never recommends a provider. Use when asking \"per request limits\", \"RPM\", \"RPD\", \"free tier\", \"how do I ask more in one prompt\", \"batch sub-questions\", \"maximize each API call\", \"request budget\", \"pack my questions into one prompt\". Not for prompt wording and instruction design (ac-prompt-engineer), not for the HTTP mechanics of calling model APIs (ac-llm-api-integration), not for cloud cost attribution of infrastructure (ac-cost-aware-engineering)."
license: MIT
metadata:
  domain: prompt-engineering
status: seedling
---

# Single-request value

## Overview

When an API prices or meters per request — a cap of so many requests per minute, a free daily allowance, or a pay-per-call tariff — the unit of economy is no longer the token or the dollar but the request itself. A wasteful question is not one word too long; it is a round trip too many. Ten sub-questions asked in ten separate calls burn ten requests; under a cap they multiply cost and can stall mid-sequence — work done, answers withheld.

This skill is the craft of treating every request as precious. Its centre is the packing decision — what belongs in one request —, and outward to the habits around it: preparing before calling, structuring one response into many deliverables, deciding when a clarification earns its round trip, stopping retries, and keeping the ledger that turns limit arithmetic into a measurable discipline.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://ai.google.dev/gemini-api/docs/rate-limits>.

## When to use

- When the provider limits requests per minute or per day, or prices per request.
- When a free tier's daily allowance is the binding constraint on what can be done.
- When a work session would otherwise stall mid-sequence after requests run out.
- When the same content needs several small outputs and one call could carry them all.

## When NOT to use

- For prompt wording, instruction form, and model knob choices (use ac-prompt-engineer).
- For HTTP mechanics, auth, streaming, and the tool-use loop (use ac-llm-api-integration).
- For infrastructure cost attribution and unit economics of systems (use ac-cost-aware-engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/request-economy.md` | `prompt-engineering/request-economy` | Reading the limit: requests as the binding currency, and the arithmetic of allowance. |
| `subskills/batching-sub-questions.md` | `prompt-engineering/batching-sub-questions` | Asking in one packed request what would otherwise be ten calls. |
| `subskills/packing-and-context.md` | `prompt-engineering/packing-and-context` | Loading one request with the evidence, the questions, and the output contract. |
| `subskills/single-request-multi-output.md` | `prompt-engineering/single-request-multi-output` | One response structured into several deliverables by design, not parsing luck. |
| `subskills/clarification-economics.md` | `prompt-engineering/clarification-economics` | When a clarifying question is worth a round trip, and when a staged-response contract is better. |
| `subskills/preparation-and-caching.md` | `prompt-engineering/preparation-and-caching` | Reading local and computing cheaply before spending a request. |
| `subskills/no-retry-degradation.md` | `prompt-engineering/no-retry-degradation` | Answering from the response already received rather than burning a retry. |
| `subskills/value-record.md` | `prompt-engineering/value-record` | The per-request ledger: what each request was for, what it returned, what remains. |

## Status and honest limits

Packing work into fewer, denser requests trades structure for economy; a packed request demands more careful drafting and its failures are larger, since a malformed multi-part request wastes the whole call rather than one small one. Nothing here recommends a provider or tariff; limit regimes change, and the record should state the allowance and date from the vendor's current published page.
