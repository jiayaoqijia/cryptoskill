---
name: repositories-and-ports
domain: software-engineering/repositories-and-ports
trigger: "Isolating database access from domain logic; defining repository interfaces; implementing hexagonal ports and adapters"
anti_trigger: "Modeling domain entities and value objects (subskills/value-objects-and-entities.md); evolving models (subskills/model-evolution.md)"
scope: "Isolating persistence and side effects from domain logic"
status: seedling
---

# Repositories and Ports

## Standard

- **Evans, Eric, _Domain-Driven Design_ (2003)**: repositories provide the illusion of an in-memory collection for aggregate roots, hiding database queries and persistence mechanics from the domain layer. <https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217> ⚠️ cited without URL.
- **Fowler, Martin, "Repository" pattern description**: a repository mediates between the domain and data mapping layers, acting like a collection of domain objects in memory. <https://martinfowler.com/eaaCatalog/repository.html>

## Decision rules

1. Repository interfaces must be defined entirely in domain terms, accepting and returning aggregate roots rather than database rows or ORM models.
2. The domain layer must never contain SQL queries, ORM annotations, or infrastructure-specific dependencies.
3. Repositories must exist solely for aggregate roots; subordinate entities and value objects within an aggregate are fetched and saved through their root.
4. Infrastructure adapters implement repository ports, translating domain operations into SQL, document store queries, or API calls.

## Procedure

1. Design domain repository interfaces containing collection-like methods (`find_by_id`, `save`, `remove`) using domain nomenclature.
2. Place repository interfaces inside the domain layer while placing concrete database implementations in the infrastructure layer.
3. Use dependency inversion so that application services depend on repository abstractions rather than concrete persistence drivers.
4. Test domain logic independently using in-memory collection stubs before wiring up database adapters.

## Anti-patterns

- Exposing database-specific query builders or ORM query objects directly to domain business logic.
- Creating individual repositories for internal entities that are not aggregate roots.
- Coupling domain models tightly to database schema structures and column naming conventions.

## Done checklist

- [ ] Repository interfaces reside in the domain layer using business terminology.
- [ ] No database or ORM imports exist within domain logic.
- [ ] Repositories exist exclusively for aggregate roots.
- [ ] Concrete persistence adapters implement domain repository ports via dependency inversion.

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

Furthermore, careful attention to this domain modeling practice prevents architectural drift, aligns engineering teams with product strategy, and ensures that complex domain invariants remain encapsulated and fully testable across all application lifecycle phases.

Additionally, rigorous adherence to this principle safeguards system modularity and domain integrity over time.

This ensures clarity and resilience across all tiers of system evolution.

## Sources

- Evans, Eric. _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley, 2003. ⚠️ cited without URL.
- Fowler, Martin. "Repository". MartinFowler.com. <https://martinfowler.com/eaaCatalog/repository.html>
