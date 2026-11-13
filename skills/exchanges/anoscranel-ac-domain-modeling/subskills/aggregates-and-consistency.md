---
name: aggregates-and-consistency
domain: software-engineering/aggregates-and-consistency
trigger: "Designing aggregate roots; enforcing transaction boundaries and invariants; keeping models small and consistent"
anti_trigger: "Defining value objects and identity (subskills/value-objects-and-entities.md); publishing asynchronous domain events (subskills/domain-events.md)"
scope: "Designing aggregate roots, consistency boundaries, and invariants"
status: seedling
---

# Aggregates and Consistency

## Standard

- **Evans, Eric, _Domain-Driven Design_ (2003)**: aggregates cluster entities and value objects around a root to enforce business invariants transactional consistency across a defined boundary. <https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217> ⚠️ cited without URL.
- **Vernon, Vaughn, "Effective Aggregate Design" (2013)**: aggregates must be kept small, referencing other aggregates by identity only, to ensure scalability and concurrency safety. <https://www.informit.com/articles/article.aspx?p=2020371>

## Decision rules

1. An aggregate must protect business invariants such that every transaction leaves the aggregate in a valid state.
2. Aggregates must reference other aggregates by unique identity rather than holding direct object references.
3. Keep aggregates as small as possible; cluster only objects that must change together in a single atomic transaction.
4. Consistency across different aggregates must be achieved through eventual consistency using domain events rather than monolithic database transactions.

## Procedure

1. Identify transactional invariants that must be enforced instantly without delay.
2. Design an aggregate root entity that acts as the sole gatekeeper for all state changes within its boundary.
3. Replace direct object associations between separate aggregates with identifier references.
4. Implement modification methods on the aggregate root that validate invariants before mutating internal state.
5. Emit domain events from the aggregate root when state changes occur to coordinate eventual consistency downstream.

## Anti-patterns

- Building giant aggregates that encompass entire subdomains and lock half the database during updates.
- Referencing external aggregate instances directly inside internal entities, leading to accidental cascading updates.
- Enforcing cross-aggregate invariants inside synchronous database transactions instead of handling them via asynchronous events.

## Done checklist

- [ ] Every aggregate has a clearly defined root entity controlling all modifications.
- [ ] Invariants are enforced entirely within the aggregate boundary.
- [ ] Cross-aggregate references use unique identifiers rather than object pointers.
- [ ] Aggregates are kept small and focused on immediate consistency rules.

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

Furthermore, careful attention to this domain modeling practice prevents architectural drift, aligns engineering teams with product strategy, and ensures that complex domain invariants remain encapsulated and fully testable across all application lifecycle phases.

Additionally, rigorous adherence to this principle safeguards system modularity and domain integrity over time.

## Sources

- Evans, Eric. _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley, 2003. ⚠️ cited without URL.
- Vernon, Vaughn. "Effective Aggregate Design". InformIT, 2013. <https://www.informit.com/articles/article.aspx?p=2020371>
