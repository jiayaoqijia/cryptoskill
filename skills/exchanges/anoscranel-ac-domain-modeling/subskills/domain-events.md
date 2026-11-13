---
name: domain-events
domain: software-engineering/domain-events
trigger: "Expressing state changes as past facts; event storming domain workflows; decoupling side effects via events"
anti_trigger: "Enforcing synchronous transaction consistency within aggregates (subskills/aggregates-and-consistency.md); isolating persistence (subskills/repositories-and-ports.md)"
scope: "Expressing state changes as what happened rather than what to do"
status: seedling
---

# Domain Events

## Standard

- **Fowler, Martin, "Domain Event" pattern description**: a domain event captures significant occurrences within the business domain as immutable facts that happened in the past. <https://martinfowler.com/eaaDev/DomainEvent.html>
- **Brandolini, Alberto, _Introducing Event Storming_ (2013)**: event storming uses orange sticky notes representing past-tense domain events to discover business processes collaboratively. <https://www.leanpub.com/introducing_eventstorming> ⚠️ Event-storming attribution to Alberto Brandolini.

## Decision rules

1. Domain events must always be named in the past tense using verbs that reflect business occurrences (such as `OrderPlaced` or `InvoicePaid`).
2. Events must contain sufficient contextual data or identity references so subscribers can process them without querying the emitter directly.
3. Event handlers must be idempotent, allowing safe reprocessing if message delivery occurs more than once.
4. State changes inside aggregates must publish events, but domain logic must never depend on the success of asynchronous downstream event handlers.

## Procedure

1. Identify critical business state transitions that domain experts care about tracking or auditing.
2. Structure collaborative event storming sessions using past-tense phrasing to map out workflow triggers.
3. Define immutable event records containing timestamps, correlation IDs, and necessary payload attributes.
4. Dispatch domain events from aggregate roots upon successful state mutation within the transaction boundary.
5. Implement asynchronous event handlers for cross-aggregate communication, auditing, and integration tasks.

## Anti-patterns

- Naming events as imperative commands (such as `ProcessOrder` instead of `OrderPlaced`).
- Including volatile aggregate internals inside event payloads that cause coupling issues for consumers.
- Relying on synchronous, tightly coupled chains of method calls for side effects that should be handled asynchronously.

## Done checklist

- [ ] All domain events are named in the past tense.
- [ ] Events carry sufficient identifying context for consumers.
- [ ] Event handlers are designed for idempotency.
- [ ] Cross-aggregate communication relies on events rather than direct synchronous coupling.

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

Furthermore, careful attention to this domain modeling practice prevents architectural drift, aligns engineering teams with product strategy, and ensures that complex domain invariants remain encapsulated and fully testable across all application lifecycle phases.

Additionally, rigorous adherence to this principle safeguards system modularity and domain integrity over time.

This ensures clarity and resilience across all tiers of system evolution.

## Sources

- Fowler, Martin. "Domain Event". MartinFowler.com. <https://martinfowler.com/eaaDev/DomainEvent.html>
- Brandolini, Alberto. _Introducing Event Storming_. Leanpub, 2013. <https://www.leanpub.com/introducing_eventstorming>
