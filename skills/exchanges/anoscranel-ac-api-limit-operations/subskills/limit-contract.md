---
name: limit-contract
domain: software-engineering/limit-contract
trigger: "Reading the provider's limit documentation as a contract the system designs against."
anti_trigger: "Not for prompt craft, and not for generic resilience theory."
scope: "Reading the provider's limit documentation and which dimension actually binds."
status: seedling
---

# Limit contract

## Standard

Every metered API publishes a limit contract: requests per minute, requests per day, tokens per minute, and the tiering or programme that sets each number. The contract decides the system's real capacity, and reading it is the first operational act — not after the first outage, but before the first deployment. The document states the numbers, the burst behaviour, the header signals, and the consequence of exceeding; a system designed against a remembered or assumed number is designed against a fiction.

The binding dimension is the one that saturates first for this system's traffic shape. A system with long documents may hit the token-per-minute ceiling while the request count is far from its cap; a chatty tool-loop client hits requests per minute first. Which dimension binds is a property of the traffic, and the design must state it — because the budgeting mechanics differ, and a system budgeting the wrong dimension is throttled by the one it ignored.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://ai.google.dev/gemini-api/docs/rate-limits>.

## Decision rules

- Read the provider's current limit page and record the numbers with the date.
- Identify the binding dimension from the system's own traffic shape, not from the headline limit.
- Record the burst behaviour: whether short bursts are absorbed or immediately throttled.
- Record the response signals — the headers that report remaining allowance, where the provider sends them.
- Record the consequence of exceeding: 429, throttled latency, or hard cut-off.
- Re-read the page on a calendar cadence and on every provider announcement; the contract changes.

## Procedure

1. Fetch the provider's limit documentation and archive it with the date.
2. Extract the numbers per dimension and per tier.
3. Profile the system's own traffic: requests, tokens, and their ratio.
4. Determine which dimension saturates first and by what margin.
5. Record burst behaviour, signals, and exceed-consequences.
6. Set the re-read cadence and name the owner of the re-read.

## Anti-patterns

- Designing against a remembered number from another project.
- Budgeting requests while tokens per minute is the binding dimension, or the reverse.
- Assuming the free-tier numbers for a paid deployment, or the reverse.
- Discovering the burst behaviour during a production peak.
- Reading the limits page once at project start and never again.

## Done checklist

- [ ] Current page archived and dated.
- [ ] Numbers extracted per dimension and tier.
- [ ] Binding dimension determined from real traffic.
- [ ] Burst behaviour recorded.
- [ ] Signals and exceed-consequences recorded.
- [ ] Re-read cadence and owner set.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- Provider rate-limit documentation, Google: <https://ai.google.dev/gemini-api/docs/rate-limits>
- Provider rate-limit documentation, OpenAI: <https://platform.openai.com/docs/guides/rate-limits>
