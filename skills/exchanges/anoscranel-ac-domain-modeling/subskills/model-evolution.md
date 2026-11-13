---
name: model-evolution
domain: software-engineering/model-evolution
trigger: "Refactoring toward deeper insight; making implicit concepts explicit; applying the strangler fig migration pattern"
anti_trigger: "Drawing initial context boundaries (subskills/bounded-contexts.md); defining ubiquitous language (subskills/ubiquitous-language.md)"
scope: "Refactoring toward deeper insight and evolving models over time"
status: seedling
---

# Model Evolution

## Standard

- **Evans, Eric, _Domain-Driven Design_ (2003)**: domain models are never finished; continuous refactoring toward deeper insight transforms awkward code into supple, expressive designs. <https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217> ⚠️ cited without URL.
- **Fowler, Martin, "Strangler Fig Application" pattern**: legacy systems are replaced incrementally by building a new bounded context around the old one and routing traffic piece by piece. <https://martinfowler.com/bliki/StranglerFigApplication.html>

## Decision rules

1. When domain experts introduce new distinctions in conversation, developers must refactor the code model to make those implicit concepts explicit.
2. Refactoring toward deeper insight must be driven by business value and conceptual clarity rather than technical vanity.
3. Replacing legacy models must use incremental migration patterns (such as the strangler fig) rather than risky, monolithic rewrites.
4. Supple design principles must be applied to remove side effects, simplify interfaces, and make domain operations read like intention-revealing prose.

## Procedure

1. Listen for awkward phrasing or complex workarounds in team discussions as signals that the current domain model is inadequate.
2. Extract implicit concepts into explicit value objects or domain services when business rules outgrow their current placement.
3. Refactor interfaces iteratively, keeping existing tests green while improving domain expressiveness and removing accidental complexity.
4. When migrating legacy subsystems, intercept traffic at the boundary and route features one by one into the new domain model.

## Anti-patterns

- Treating the initial domain model as a fixed specification and resisting refactoring as business understanding deepens.
- Attempting high-risk, big-bang rewrites of legacy domain models instead of incremental strangler migrations.
- Accumulating domain logic inside procedural scripts because refactoring the model feels too time-consuming.

## Done checklist

- [ ] Implicit domain concepts are made explicit as understanding deepens.
- [ ] Refactoring is performed iteratively without breaking existing domain tests.
- [ ] Legacy systems are migrated incrementally using strangler patterns.
- [ ] Supple design principles keep domain interfaces clean and intention-revealing.

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

Furthermore, careful attention to this domain modeling practice prevents architectural drift, aligns engineering teams with product strategy, and ensures that complex domain invariants remain encapsulated and fully testable across all application lifecycle phases.

Additionally, rigorous adherence to this principle safeguards system modularity and domain integrity over time.

## Sources

- Evans, Eric. _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley, 2003. ⚠️ cited without URL.
- Fowler, Martin. "Strangler Fig Application". MartinFowler.com. <https://martinfowler.com/bliki/StranglerFigApplication.html>
