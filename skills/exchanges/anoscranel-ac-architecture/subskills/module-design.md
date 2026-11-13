---
name: module-design
domain: software-engineering/module-design
trigger: "\"Where should this code live\", \"this module does too much\", \"split this package\", \"reduce coupling\", \"design the interface between these modules\"."
anti_trigger: "Whole-system structure and service splits (subskills/architecture.md); public HTTP/RPC contracts; line-level cleanup."
scope: "Internal module boundaries, coupling, cohesion, deep vs shallow modules"
status: "seedling"
---

# Module Design

## Standard

- **Deep modules** (John Ousterhout, *A Philosophy of Software Design*, 2018): a simple interface hiding a lot of function. Shallow modules add interface cost for little gain.
- **Information hiding** (Parnas, CACM 1972): each module hides one design decision likely to change. (https://dl.acm.org/doi/10.1145/361598.361623)
- **SOLID** pays off at module boundaries, not per class. ⚠️ Its ROI is unmeasured: no controlled study backs it.
- **Dependency rule**: dependencies point toward the stable core (Martin, *Clean Architecture*, 2017).
- Change effort tracks module coupling and churn more than any single complexity metric (Nagappan & Ball, ICSE 2005).
- Language features replace some GoF patterns: sealed types and pattern matching over Visitor; DI over Singleton.

## Decision rules

1. A module owns one reason to change. Two unrelated reasons → split.
2. Prefer fewer, deeper modules. A wrapper that only forwards calls → remove it.
3. The interface exposes intent, not steps. Callers should not need to call A, then B, then C in order.
4. No cycles between modules. A cycle means a missing module or a misplaced type.
5. Domain code never imports framework, database or HTTP code. Adapters import the domain.
6. Pass dependencies in (constructor or parameter). No hidden globals.
7. Things that change together live together. Use git history: files that co-change in most commits belong in one module.
8. Add an interface only when there are two real implementations or a test seam needs one.
9. Pull a shared module out after the third duplicate, not the first.

## Procedure

1. Map current modules and their imports. Tools: `dependency-cruiser` (JS/TS), `pydeps` or `import-linter` (Python), `go list -deps`, `cargo modules`.
2. Find co-change clusters: `git log --name-only --since=6.months` and count file pairs that change together.
3. Mark problems: cycles, shallow wrappers, god modules, domain importing infrastructure.
4. For each module, write one sentence: "This module hides ___." Can't write it → boundary is wrong.
5. Design the target: list modules, each with its hidden decision and public interface (function signatures and types only).
6. Check the target against rules 1–9.
7. Move code in small refactoring steps under test coverage (out of scope for this leaf: the refactoring recipes). One move per commit.
8. Encode boundaries as CI rules, e.g. `import-linter` contract "domain may not import adapters".
9. Record a boundary change that is hard to reverse as an ADR.

## Anti-patterns

- An interface per class with one implementation.
- "utils" or "common" module that everything imports.
- Splitting by technical layer only (controllers/, services/, models/) when features change across all three.
- Pass-through methods that add a layer and no logic.
- Circular imports fixed with lazy imports instead of a boundary change.

## Done checklist

- [ ] Each module has a one-sentence "hides" statement.
- [ ] No import cycles.
- [ ] Domain has no framework or I/O imports.
- [ ] Boundary rules enforced in CI.
- [ ] Moves done under green tests.

## Sources

- <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- <https://go.dev/blog>
- <https://www.iso.org/standard/78176.html> S3.1
- https://github.com/sverweij/dependency-cruiser
