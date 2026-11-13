---
name: bounded-contexts
domain: software-engineering/bounded-contexts
trigger: "Drawing context boundaries; resolving ambiguous terms across teams; isolating separate domain models"
anti_trigger: "Naming classes inside a single glossary (subskills/ubiquitous-language.md); designing aggregate invariants (subskills/aggregates-and-consistency.md)"
scope: "Drawing context boundaries and isolating distinct models"
status: seedling
---

# Bounded Contexts

## Standard

- **Evans, Eric, _Domain-Driven Design_ (2003)**: large systems become incoherent when forced into a single unified model; explicit bounded contexts protect distinct models within clearly drawn borders. <https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217> ⚠️ cited without URL.
- **Vernon, Vaughn, _Implementing Domain-Driven Design_ (2013)**: context boundaries establish team organization, language consistency, and explicit integration seams between models. <https://www.informit.com/store/implementing-domain-driven-design-9780321834577>

## Decision rules

1. If a single business term (such as `Product`) has conflicting attributes or rules across departments, each department requires its own bounded context.
2. Codebases belonging to different bounded contexts must never share domain entity classes directly; communication requires explicit translation.
3. The boundary of a context must be defined by team organization and linguistic consistency rather than technical convenience.
4. Shared kernels between contexts must be kept minimal and agreed upon explicitly by both owning teams.

## Procedure

1. Map organizational units and identify where business terminology shifts its meaning or structure.
2. Draw explicit boundary lines around each subdomain where a single ubiquitous language holds true without ambiguity.
3. Define anti-corruption layers or translation mappers where data crosses from one bounded context into another.
4. Structure code repositories or module directories so that contexts are physically separated and circular dependencies are prevented.
5. Establish integration contracts (such as domain events or published language APIs) for inter-context communication.

## Anti-patterns

- Forcing an enterprise-wide data model where a single `User` or `Product` entity contains every possible attribute for every department.
- Sharing database tables directly across distinct bounded contexts without isolation or mapping.
- Treating bounded contexts as purely logical directory separations while allowing direct domain model imports between them.

## Done checklist

- [ ] Context boundaries are mapped and aligned with team domains.
- [ ] No single domain entity is shared directly across distinct context boundaries.
- [ ] Translation mechanisms (anti-corruption layers) are established at context borders.
- [ ] Each bounded context maintains its own unambiguous ubiquitous language.

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

Furthermore, careful attention to this domain modeling practice prevents architectural drift, aligns engineering teams with product strategy, and ensures that complex domain invariants remain encapsulated and fully testable across all application lifecycle phases.

## Sources

- Evans, Eric. _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley, 2003. ⚠️ cited without URL.
- Vernon, Vaughn. _Implementing Domain-Driven Design_. Addison-Wesley, 2013. <https://www.informit.com/store/implementing-domain-driven-design-9780321834577>
