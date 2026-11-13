---
name: survey-scope
domain: software-engineering/architecture-survey
trigger: "Determining what parts of a repository to inspect, which entry points matter, and how to sample callers without exhaustive enumeration"
anti_trigger: "Judging structural quality (subskills/evidence-versus-judgment.md); forming bounded improvement candidates (subskills/candidate-formation.md)"
scope: "Scoping the read-only survey: stack, entry points, ownership boundaries, dependency direction, runtime paths, tests, and existing architecture records; sampling callers to distinguish recurring problems from isolated files; coverage discipline."
status: seedling
---

# Survey Scope

## Standard

- **Feathers, _Working Effectively with Legacy Code_ (2004)**: defining change boundaries requires identifying existing test harnesses and entry points before inspecting internal dependencies. <https://www.pearson.com/store/p/working-effectively-with-legacy-code/P100000885233>
- **Martin, _Clean Architecture_ (2017)**: dependency direction dictates which modules know about others; scoping must trace inward from entry points toward core domain rules. <https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/>
- ⚠️ House convention: a survey must explicitly declare its sampling boundaries so readers know which directories were omitted from static inspection.

## Decision rules

1. If the repository lacks documented entry points, locate public API handlers, CLI command definitions, or main execution loops before examining internal modules.
2. If a directory contains generated code, vendor bundles, or third-party dependencies, exclude it from structural finding tallies but note its presence in the scope summary.
3. If sampling reveals identical structural patterns across three or more disconnected modules, elevate the pattern from an isolated quirk to a repository-wide finding.
4. If tests exist for a target module, include test coverage and testability seams in the scope assessment; untestable modules receive higher risk weighting during candidate formation.

## Procedure

1. Inventory repository file extensions, build configuration files, package manifests, and existing architecture documentation to map the technology stack and declared module boundaries.
2. Identify all primary entry points (HTTP routers, event listeners, CLI entry scripts, worker loops) and trace their immediate outbound dependencies down one layer.
3. Sample representative files from core domain modules, data access layers, and utility helpers rather than attempting line-by-line reading of every file in large trees.
4. Record explicit coverage boundaries in the survey metadata: list inspected directories, skipped test folders, ignored generated assets, and known unexamined subtrees.
5. Verify that all static assumptions about dependency direction are checked against actual import statements or build dependency graphs before proceeding to structural analysis.

## Anti-patterns

- Assuming every subdirectory is relevant without checking build files or manifests.
- Treating third-party library code or generated SDKs as part of the core application architecture.
- Claiming exhaustive repository coverage after inspecting only a single top-level package.
- Skipping entry point identification and starting structural reviews from arbitrary internal utility files.

## Done checklist

- [ ] Repository stack and entry points identified.
- [ ] Sampling boundaries and ignored directories explicitly recorded.
- [ ] Representative modules sampled across domain and infrastructure layers.
- [ ] Dependency direction verified against actual import paths.
- [ ] Coverage limits stated in the survey metadata.

## Sources

- Feathers, Michael. _Working Effectively with Legacy Code_. Prentice Hall, 2004. <https://www.pearson.com/store/p/working-effectively-with-legacy-code/P100000885233>
- Martin, Robert C. _Clean Architecture: A Craftsman's Guide to Software Structure and Design_. Prentice Hall, 2017. <https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/>
