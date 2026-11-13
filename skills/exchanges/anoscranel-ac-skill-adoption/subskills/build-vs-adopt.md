---
name: build-vs-adopt
domain: skill-authoring/build-vs-adopt
trigger: "Deciding whether to adopt a third-party skill or author it from scratch; calculating total cost of adoption including maintenance and security surface; evaluating fork versus author decisions"
anti_trigger: "Staging and gating skill installation files (subskills/install-gating.md); auditing installed skills for drift and updates (subskills/post-install-lifecycle.md)"
scope: "Weighing the total cost of adoption against authoring custom skills, identifying when thin self-written prompts beat heavyweight dependencies, and evaluating extension or forking paths"
status: "seedling"
---

# Build Versus Adopt

## Standard

- **Semantic Versioning 2.0.0**: dependency management principles governing interface stability, breaking changes, and upgrade costs. <https://semver.org>
- **Software Engineering Economics**: comparative analysis of custom development versus third-party component integration and maintenance debt. <https://www.sei.cmu.edu>

## Decision rules

- **Calculate total cost of adoption**: factor in not only initial download time but also ongoing maintenance overhead, security vetting effort, API drift monitoring, and compatibility debugging.
- **Prefer thin self-written skills for core workflows**: author bespoke markdown prompt instructions locally when the required logic is straightforward and avoids third-party dependency bloat.
- **Adopt third-party skills for complex standardized domains**: integrate specialized external skills when domain expertise, complex parsing logic, or extensive reference material makes self-authoring inefficient.
- **Choose forking or extending as middle paths**: when an existing skill is ninety percent effective but flawed, fork and adapt it locally rather than maintaining an unmanageable patch cascade.

## Procedure

1. Define the exact operational requirements and expected output quality for the target agent workflow.
2. Estimate the engineering hours required to author and test a custom self-written skill from scratch.
3. Audit candidate third-party skills to measure integration complexity, maintenance overhead, and security exposure.
4. Compare total ownership costs between building bespoke prompts and adopting external packages.
5. Select the optimal path—authoring custom instructions, adopting a vetted third-party skill, or forking and adapting an existing repository.
6. Document the adoption rationale and cost trade-offs in project decision records.

## Anti-patterns

- Adopting heavyweight third-party packages for trivial tasks that require only a few lines of plain prompt instructions.
- Building complex domain parsers from scratch when robust, well-maintained third-party skills are already available.
- Ignoring ongoing maintenance debt and dependency rot when calculating the true cost of third-party adoption.
- Adopting unverified external codebases merely to save initial drafting time without weighing security risks.

## Done checklist

- [ ] Operational workflow requirements defined clearly.
- [ ] Custom authoring effort estimated in engineering hours.
- [ ] Third-party adoption overhead and security risks audited.
- [ ] Cost-benefit analysis completed between building, adopting, and forking.
- [ ] Optimal adoption path selected and documented in decision records.

## Sources

- Preston-Werner, Tom. _Semantic Versioning 2.0.0 Specification_. <https://semver.org>
- Software Engineering Institute. _Principles of Software Engineering Economics and Component Integration_. <https://www.sei.cmu.edu>
