---
name: evidence-versus-judgment
domain: software-engineering/architecture-survey
trigger: "Separating concrete file paths and code patterns from architectural critique; deciding whether an observed pattern is isolated or recurring"
anti_trigger: "Scoping the repository survey (subskills/survey-scope.md); cataloging specific structural smells (subskills/structural-smells.md)"
scope: "The evidence bar: every finding cites concrete observed evidence separated from design judgment; the recurring-versus-isolated test; why unsupported aesthetic claims fail the bar."
status: seedling
---

# Evidence Versus Judgment

## Standard

- **Fowler, _Refactoring_ (2nd ed., 2018)**: code smells point toward deeper structural problems, but each smell must be anchored to concrete syntax or dependency metrics before action is taken. <https://www.oreilly.com/library/view/refactoring-improving-the/9780134757799/>
- **IEEE Std 1010-2004**: software reviews require objective evidence tied directly to artifacts rather than subjective stylistic preferences. ⚠️ cited without URL.
- ⚠️ House convention: any finding that cannot cite a specific file path and line range or import pattern is classified as speculative and excluded from the final report.

## Decision rules

1. If a critique relies on stylistic preference without demonstrating coupling, testability loss, or dependency violation, reject the critique as unsupported aesthetic opinion.
2. If an observed awkward pattern appears in exactly one file and is not called by other modules, classify it as an isolated implementation detail rather than a structural smell.
3. If an observed pattern appears across three or more distinct modules and violates declared dependency direction, classify it as a validated recurring structural finding.
4. If evidence is ambiguous due to missing documentation or complex indirection, mark the finding with a warning symbol and lower its confidence score.

## Procedure

1. Extract exact file paths, line ranges, and relevant code excerpts for every potential architectural issue discovered during repository sampling.
2. Formulate the observed evidence as a factual statement describing what the code currently does (e.g., "Module A directly imports database driver from Module C, bypassing the repository interface").
3. Append the architectural judgment in a separate section labeled Interpretation, explaining why the observed pattern creates coupling, testability friction, or maintenance cost.
4. Apply the recurring-versus-isolated test by searching for matching import patterns or duplicated logic across the rest of the sampled codebase.
5. Filter out all findings that lack concrete file citations or fail the recurrence threshold before drafting candidate improvements.

## Anti-patterns

- Writing survey reports filled with general complaints about code quality without citing specific files.
- Treating a deliberate, documented workaround as an accidental structural flaw.
- Conflating personal naming conventions or formatting preferences with architectural smells.
- Omitting line numbers or file paths when referencing complex dependency loops.

## Done checklist

- [ ] Every finding anchored to concrete file paths and code citations.
- [ ] Factual evidence strictly separated from design interpretation.
- [ ] Recurrence test applied across multiple modules.
- [ ] Unsupported aesthetic opinions filtered out.
- [ ] Ambiguous findings explicitly flagged with warning symbols.

## Sources

- Fowler, Martin. _Refactoring: Improving the Design of Existing Code_. 2nd ed., Addison-Wesley Professional, 2018. <https://www.oreilly.com/library/view/refactoring-improving-the/9780134757799/>
- Institute of Electrical and Electronics Engineers. _IEEE Std 1010-2004: IEEE Standard for Application and Management of Software Engineering Bodies of Knowledge_. IEEE, 2004. ⚠️ cited without URL.
