---
name: candidate-formation
domain: software-engineering/architecture-survey
trigger: "Converting an observed structural finding into a bounded improvement candidate with a proposed boundary, risk profile, and validation plan"
anti_trigger: "Identifying structural smells (subskills/structural-smells.md); ranking multiple candidates (subskills/ranking-criteria.md)"
scope: "Turning a finding into a bounded candidate: concrete pain and cited evidence, proposed responsibility boundary, affected callers, expected benefit, risk, and proportionate validation."
status: seedling
---

# Candidate Formation

## Standard

- **Evans, _Domain-Driven Design_ (2003)**: refactoring toward a deeper model requires bounding responsibilities so that domain concepts match explicit module boundaries. <https://www.oreilly.com/library/view/domain-driven-design-tackling/0321125215/>
- **IEEE Std 1471-2000**: architectural descriptions and improvement proposals must define boundaries, interfaces, and rationale clearly. ⚠️ cited without URL.
- ⚠️ House convention: a candidate proposal must state what it explicitly excludes to prevent scope creep during subsequent implementation phases.

## Decision rules

1. If a finding affects multiple disparate packages, split the candidate into independent module-level proposals rather than creating a monolithic refactoring task.
2. If a proposed responsibility boundary does not eliminate the cited evidence pattern, reject the candidate formulation and revise the boundary definition.
3. If migration risk involves potential data corruption or breaking public interfaces, mandate integration test coverage in the validation strategy.
4. If expected benefit is purely stylistic without improving testability, coupling, or maintainability, do not form a candidate.

## Procedure

Description of steps for forming bounded improvement candidates:
1. Extract the concrete evidence trail (file paths, line ranges, and observed smells) associated with the target architectural finding.
2. Define the exact pain point caused by the current structure, such as high coupling, untestable constructors, or duplicated policy logic.
3. Propose a new responsibility boundary that encapsulates the behavior and specifies which modules absorb or relinquish duties.
4. Inventory all affected callers and trace how their dependency paths will be redirected under the new boundary.
5. Estimate migration and regression risks, and outline a proportionate validation strategy (unit tests, integration suites, or static analysis gates) scaled to the codebase size.

## Anti-patterns

- Formulating vague candidates that propose general cleanup without specifying new module boundaries.
- Omitting affected callers or failing to check reverse dependencies.
- Proposing massive multi-system rewrites as a single indivisible candidate.
- Designing complex validation harnesses for trivial internal refactoring candidates.

## Done checklist

- [ ] Evidence trail and concrete pain point documented for the finding.
- [ ] Proposed responsibility boundary and module encapsulation defined.
- [ ] Affected callers and dependency redirection paths listed.
- [ ] Migration and regression risks assessed.
- [ ] Proportionate validation strategy specified.

## Sources

- Evans, Eric. _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley Professional, 2003. <https://www.oreilly.com/library/view/domain-driven-design-tackling/0321125215/>
- Institute of Electrical and Electronics Engineers. _IEEE Std 1471-2000: IEEE Recommended Practice for Architecture Description of Software-Intensive Systems_. IEEE, 2000. ⚠️ cited without URL.
