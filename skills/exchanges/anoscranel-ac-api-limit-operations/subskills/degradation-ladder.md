---
name: degradation-ladder
domain: software-engineering/degradation-ladder
trigger: "Designing the service levels the product drops through when the budget is empty."
anti_trigger: "Not for the provider's limits themselves, and not for retry theory."
scope: "Service levels the product can drop through while staying up."
status: seedling
---

# Degradation ladder

## Standard

When the request budget is exhausted, the product's choice is not binary — full service or outage. The degradation ladder pre-designs the intermediate service levels the product can serve without the constrained API: a slower path using a cheaper or cached route, a reduced answer from stored responses, an honest partial result with the gap named, or a graceful queue-and-notify. Each rung is designed in advance, because a degradation improvised under load is an outage with a polite message.

The ladder's defining property is that the customer never sees an undifferentiated failure. The top rung is full service; the next serves the same need from cache or a smaller model; the next serves partial with the constraint stated; the bottom queues the work with an honest estimate. Which rungs exist is a product decision made in calm conditions, and the operator's job at peak is to choose correctly among rungs that were already built.

Primary sources: <https://sre.google/sre-book/handling-overload/> and <https://12factor.net/>.

## Decision rules

- Enumerate the product's needs and which of them genuinely require the constrained API.
- Design at least one degraded rung per need, with its honest quality statement.
- Order the rungs and write the switching rule: which metric moves the service to which rung.
- State what each rung's customer experience is — reduced, delayed, or queued with an estimate.
- Verify each rung under test before the first real exhaustion; an untested rung is a rumour.
- Record every real degradation activation with the trigger and the duration.

## Procedure

1. List the product's needs and their dependency on the constrained API.
2. Design a degraded rung for each need and write its quality statement.
3. Define the switching metric and the thresholds for moving down and back up.
4. Build the rungs and the switching mechanism.
5. Test each rung deliberately — degrade in rehearsal, never first in production.
6. On real activation, record trigger, rung, duration, and customer-visible behaviour.

## Anti-patterns

- A ladder that exists on paper with untested rungs.
- Degradations that lie — serving stale content as current.
- A binary design: full service or a 500, with nothing between.
- Switching rules that require a human decision at peak speed.
- No record of activations, so the ladder's real behaviour is unknown.

## Done checklist

- [ ] Needs enumerated with their API dependency.
- [ ] One designed rung per need with quality statements.
- [ ] Switching metrics and thresholds defined.
- [ ] Rungs tested before first real exhaustion.
- [ ] Customer experience per rung stated.
- [ ] Activations recorded with trigger and duration.

## Sources

- Handling overload, Google SRE: <https://sre.google/sre-book/handling-overload/>
- The twelve-factor app: <https://12factor.net/>
- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
