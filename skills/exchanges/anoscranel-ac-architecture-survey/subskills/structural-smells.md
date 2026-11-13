---
name: structural-smells
domain: software-engineering/architecture-survey
trigger: "Identifying scattered policy, repeated coordination, pass-through layers, hidden side effects, and verify-hostile seams in a codebase"
anti_trigger: "Separating evidence from judgment (subskills/evidence-versus-judgment.md); forming bounded improvement candidates (subskills/candidate-formation.md)"
scope: "The catalog of architectural smells: scattered policy, repeated coordination, unclear lifecycle ownership, pass-through layers, duplicated boundaries, hidden side effects, and verify-hostile seams."
status: seedling
---

# Structural Smells

## Standard

- **Feathers, _Working Effectively with Legacy Code_ (2004)**: verify-hostile seams occur when dependencies are instantiated directly inside constructors, making unit testing impossible without external services. <https://www.pearson.com/store/p/working-effectively-with-legacy-code/P100000885233>
- **Martin, _Clean Architecture_ (2017)**: architectural boundary violations appear as pass-through layers that forward data without adding logic or enforcing policy. <https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/>
- ⚠️ House convention: structural smells must be identified by observable code patterns, such as `new` instantiations in business logic or multi-layered method forwarding, rather than abstract intuition.

## Decision rules

1. If business validation rules are duplicated across three or more endpoint handlers, classify the pattern as scattered policy.
2. If multiple modules independently coordinate transaction boundaries and retry logic without a shared abstraction, classify the pattern as repeated coordination.
3. If an object passes method calls through four or more consecutive layers without altering data or enforcing rules, classify the pattern as a pass-through layer smell.
4. If domain functions trigger network requests or file writes without explicit parameter injection, classify the pattern as hidden side effects.

## Procedure

1. Scan codebase imports and constructor signatures for hardcoded dependencies and direct instantiations that prevent mocking or unit testing.
2. Search for duplicated conditional logic, error handling blocks, or validation checks spread across controllers and domain handlers.
3. Trace data flow paths from entry points down to storage layers to identify redundant wrapper classes that perform no transformation.
4. Inspect database interaction code and global state mutations to locate hidden side effects executed outside explicit transaction boundaries.
5. Document each identified smell with its specific observable evidence pattern, affected file paths, and potential maintenance impact.

## Anti-patterns

- Labeling every large file or long function as an architectural smell without inspecting its dependency graph.
- Ignoring pass-through wrappers that exist to satisfy framework boilerplate requirements.
- Confusing normal domain event dispatching with hidden side effects.
- Treating minor syntax variations as distinct structural smells.

## Done checklist

- [ ] Repository scanned for hardcoded instantiations and verify-hostile seams.
- [ ] Scattered policy and duplicated validation logic cataloged.
- [ ] Pass-through layers and redundant wrappers identified.
- [ ] Hidden side effects and unmanaged global mutations recorded.
- [ ] Each smell linked to observable evidence and affected paths.

## Sources

- Feathers, Michael. _Working Effectively with Legacy Code_. Prentice Hall, 2004. <https://www.pearson.com/store/p/working-effectively-with-legacy-code/P100000885233>
- Martin, Robert C. _Clean Architecture: A Craftsman's Guide to Software Structure and Design_. Prentice Hall, 2017. <https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/>
