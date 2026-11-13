---
name: ubiquitous-language
domain: software-engineering/ubiquitous-language
trigger: "Building shared vocabulary with domain experts; naming classes after business concepts; resolving naming drift between code and speech"
anti_trigger: "Writing database schemas or technical terms in domain discussions (subskills/repositories-and-ports.md); drawing context boundaries (subskills/bounded-contexts.md)"
scope: "Building and maintaining a shared language between domain experts and code"
status: seedling
---

# Ubiquitous Language

## Standard

- **Evans, Eric, _Domain-Driven Design: Tackling Complexity in the Heart of Software_ (2003)**: the ubiquitous language connects domain experts and developers through a rigorous shared vocabulary used in speech, diagrams, and code alike. <https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217> ⚠️ cited without URL.
- **Vernon, Vaughn, _Implementing Domain-Driven Design_ (2013)**: vocabulary must be uncompromisingly modeled after business reality, rejecting technical shorthand in domain classes. <https://www.informit.com/store/implementing-domain-driven-design-9780321834577>

## Decision rules

1. Every class, method, and variable name in the domain layer must appear verbatim in the glossary maintained jointly with domain experts.
2. If domain experts use two different words for distinct concepts, the code must never conflate them into a single overloaded term.
3. If technical implementation terms (like `DTO`, `Record`, or `Manager`) appear in core business rules, refactor them immediately into domain actions.
4. When spoken language shifts in the business, code must be refactored to match within the same release cycle.

## Procedure

1. Convene domain experts and developers to map out core business workflows on a whiteboard or shared document.
2. Record every specialized noun and verb used by experts; discard generic technical verbs like `process` or `handle`.
3. Create a living glossary document stored in the repository where every term has exactly one unambiguous definition.
4. Name domain classes, entities, and methods using this exact glossary without abbreviations or database jargon.
5. Review pull requests by reading code aloud to verify whether it reads like a precise description of the business process.

## Anti-patterns

- Using generic technical nouns (`Data`, `Info`, `Manager`, `Processor`) instead of precise domain concepts (`Invoice`, `Shipment`, `BillingAccount`).
- Maintaining a static dictionary that diverges from the vocabulary actually spoken by domain experts after month one.
- Translating business terms into technical abbreviations inside domain code to save keystrokes.

## Done checklist

- [ ] A living glossary exists and is reviewed regularly with domain experts.
- [ ] Every core class and method name matches a term from the shared glossary.
- [ ] No database columns or technical artifacts dictate domain naming choices.
- [ ] Code reads naturally when spoken aloud by a domain expert.

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

## Sources

- Evans, Eric. _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley, 2003. ⚠️ cited without URL.
- Vernon, Vaughn. _Implementing Domain-Driven Design_. Addison-Wesley, 2013. <https://www.informit.com/store/implementing-domain-driven-design-9780321834577>
