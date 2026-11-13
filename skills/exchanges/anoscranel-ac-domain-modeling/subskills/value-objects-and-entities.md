---
name: value-objects-and-entities
domain: software-engineering/value-objects-and-entities
trigger: "Distinguishing entities from value objects; eliminating primitive obsession; modeling immutable domain concepts"
anti_trigger: "Designing aggregate roots and invariants (subskills/aggregates-and-consistency.md); defining repository contracts (subskills/repositories-and-ports.md)"
scope: "Distinguishing identity versus attribute equality and eliminating primitives"
status: seedling
---

# Value Objects and Entities

## Standard

- **Evans, Eric, _Domain-Driven Design_ (2003)**: objects defined primarily by their identity are entities; objects defined solely by their attributes are immutable value objects. <https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217> ⚠️ cited without URL.
- **Fowler, Martin, "Value Object" pattern description**: a value object is a small object representing a descriptive aspect of the domain with no conceptual identity, making aliasing safe through immutability. <https://martinfowler.com/bliki/ValueObject.html>

## Decision rules

1. If two instances have different attribute values but represent the same business concept across time, model them as an entity with a unique identifier.
2. If two instances with identical attributes are completely interchangeable, model them as an immutable value object.
3. Eliminate primitive obsession by wrapping raw strings, numbers, and dates into domain-specific value objects that enforce validation rules upon creation.
4. Value objects must be strictly immutable; any operation that modifies a value object must return a new instance rather than mutating state in place.

## Procedure

1. Audit domain models to identify objects possessing distinct lifecycle continuity versus descriptive attributes.
2. Replace raw primitive types (like strings for email addresses or floats for currency) with dedicated value object classes.
3. Encapsulate validation and formatting logic inside value object constructors to guarantee that invalid states cannot be instantiated.
4. Implement equality checks based on structural attribute comparison for value objects and unique identifier comparison for entities.

## Anti-patterns

- Using primitive strings and integers everywhere, resulting in scattered validation logic and invalid state bugs.
- Mutating value object attributes in place after creation, leading to subtle sharing bugs and side effects.
- Giving value objects unique database identifiers and treating them like entities unnecessarily.

## Done checklist

- [ ] Entities possess unique identifiers and track lifecycle continuity.
- [ ] Value objects are strictly immutable and compared by structural attributes.
- [ ] Primitive obsession is eliminated by wrapping raw data types in domain value objects.
- [ ] Validation rules are enforced at value object instantiation time.

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

Furthermore, careful attention to this domain modeling practice prevents architectural drift, aligns engineering teams with product strategy, and ensures that complex domain invariants remain encapsulated and fully testable across all application lifecycle phases.

## Sources

- Evans, Eric. _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley, 2003. ⚠️ cited without URL.
- Fowler, Martin. "Value Object". MartinFowler.com. <https://martinfowler.com/bliki/ValueObject.html>
