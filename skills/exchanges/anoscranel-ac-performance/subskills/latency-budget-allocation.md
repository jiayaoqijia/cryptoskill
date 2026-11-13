---
name: latency-budget-allocation
domain: software-engineering/latency-budget-allocation
trigger: "\"how much time can each layer take\", \"budget the request path\", \"time-box the call chain\"."
anti_trigger: "Choosing timeout values for failure bounding (ac-resilience-budgets); SLO thresholds (ac-reliability)."
scope: "Breaking a latency budget across a call chain, and holding each layer to its share."
status: seedling
---

# Latency budget allocation

## Standard

A user-facing budget — the page loads in a second, the API responds in 300 milliseconds — is not one number but an allocation. Between the user and any piece of work sit several layers — the network, the edge, the service, the database — and each consumes a share. Budget allocation makes the shares explicit and holds each layer to its own quota, so one layer's slow new feature does not silently spend the budget the others assumed they owned.

The discipline changes the argument inside a team. Without a written allocation, "is this fast enough" is a negotiation where every layer claims innocence because each is only mildly slow. With one, the question becomes a lookup: this layer owns 80 milliseconds, is taking 140, and is therefore the defect — regardless of whether 140 feels fast.

## Decision rules

1. Derive the user-facing budget first; the allocation flows down from it, never upward from estimates.
2. Allocate shares by layer — transport, service processing, backing stores, fan-out waits.
3. A sync call chain's budget is the sum of its stages; a fan-out's is the max of the parallel branches.
4. Every allocated share has an owner; unowned budget gets spent by whoever arrives last.
5. Record the total slack deliberately: a chain at 100% of budget has no room for degradation.
6. The allocation is re-derived when the user-facing budget changes, not patched piecemeal.

## Procedure

1. State the user-facing budget per critical path.
2. Decompose the path into stages and map the sync and fan-out structure.
3. Assign each stage a share and an owner; write them down together.
4. Measure each stage's actual spend against its share.
5. For stages over budget, open work; for stages far under, consider reallocation.
6. Re-derive the whole allocation when the top-level budget changes.

## Anti-patterns

- Allowing each internal team to justify its latency in isolation.
- A chain whose stages sum to the entire budget with no slack.
- Treating a fan-out as a sum of its branches rather than the max.
- A written allocation that has never been measured against reality.
- Letting the slowest layer claim the whole budget by arriving last.
- No re-derivation after the user-facing target changed.

## Done checklist

- [ ] Top-level budget stated per path.
- [ ] Stages mapped with sync and fan-out structure.
- [ ] Shares assigned and owned.
- [ ] Slack deliberately present.
- [ ] Stage spends measured against shares.
- [ ] Allocation re-derived on budget change.

## Sources

- Google's wide-area latency work: <https://research.google/pubs/pub44843/>
- Critical path budgeting: <https://www.kernel.org/doc/html/latest/>
- Front-end critical rendering path: <https://web.dev/learn/performance/>
