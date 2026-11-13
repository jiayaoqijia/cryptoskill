---
name: fallback-chains
domain: software-engineering/fallback-chains
trigger: "Falling back to another provider or model when the primary is throttled."
anti_trigger: "Not for ranking providers, and not for the single-request craft."
scope: "Provider and model fallbacks, and their honest switching costs."
status: seedling
---

# Fallback chains

## Standard

A fallback chain names, in advance, the sequence of providers or models the system tries when the primary cannot serve: primary first, then the first fallback, then the next, each entry with the reason it is trusted and the cost of switching to it. The chain is a resilience pattern with a specific honesty requirement: providers differ — in behaviour, in strengths, in output conventions — so the answer that arrives from the third link is not identical to one from the first, and the system must either label the difference or absorb it in testing.

The chain's economics deserve design rather than reflex. A fallback is not free: the alternate provider has its own limits, its own pricing, and its own latency; a chain that funnels peak traffic into a fallback sized for trickling is an outage scheduled one step later. Every link needs its own budget, and the chain as a whole needs the question answered: when the first two are throttled, what does the third actually get hit with?

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://12factor.net/>.

## Decision rules

- Name the chain in configuration, with each link's reason and its own limit budget.
- Test each link with production-shaped traffic, not a smoke handshake.
- Define the failure signal that moves to the next link: throttling, timeout, or error budget.
- Define the honesty rule: label fallback-sourced answers, or verify equivalence in tests.
- Budget the chain's tail: the last link's allowance must survive the first links' failures.
- Re-read every link's limit contract on the same cadence as the primary's.

## Procedure

1. List candidate links with their reasons for trust.
2. Configure the chain order and the signal that advances it.
3. Set each link's own budget from its own contract.
4. Test the whole chain by forcing each link to fail in turn.
5. Decide the labelling or equivalence rule and implement it.
6. Review the chain on the same re-read cadence as the limit contract.

## Anti-patterns

- An implicit chain: any available key, any available provider, decided at error time.
- Untested links that reveal their incompatibility during the first real throttle.
- A fallback sized far below the traffic the chain funnels into it.
- Silently serving a different provider's behaviour as if identical.
- Chain changes made during an incident and never recorded.

## Done checklist

- [ ] Chain configured with per-link reasons and budgets.
- [ ] Advancement signal defined.
- [ ] Every link tested with production-shaped traffic.
- [ ] Labelling or equivalence rule implemented.
- [ ] Tail-link budget sized for upstream failure.
- [ ] Chain reviewed with the contract cadence.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- The twelve-factor app: <https://12factor.net/>
- Provider rate-limit documentation, Google: <https://ai.google.dev/gemini-api/docs/rate-limits>
