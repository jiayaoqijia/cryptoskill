---
name: provenance-and-license
domain: skill-authoring/provenance-and-license
trigger: "Checking author identity and commit history for third-party skills; verifying software license compatibility; deciding whether an unlicensed skill can be legally adopted"
anti_trigger: "Auditing skill instructions for prompt injection (subskills/security-vetting.md); configuring staged installation directories (subskills/install-gating.md)"
scope: "Evaluating author identity, commit history lineage, fork versus original repository status, SPDX license compatibility, and the legal risks of adopting unlicensed code"
status: "seedling"
---

# Provenance and License

## Standard

- **SPDX License List**: authoritative catalogue of standardized open-source software licenses and legal terms. <https://spdx.org/licenses/>
- **Semantic Versioning 2.0.0**: specification for version numbering that communicates breaking interface changes versus backward-compatible updates. <https://semver.org>

## Decision rules

- **Verify author identity and commit lineage**: trace repository commit history to ensure contributions originate from verifiable maintainers rather than anonymous shadow accounts or automated scraping forks.
- **Require explicit open-source licensing**: reject any skill repository lacking a recognized SPDX license file, as absence of copyright permission legally prohibits redistribution, modification, or commercial use.
- **Check license compatibility with local projects**: ensure the skill's license does not impose restrictive copyleft obligations that contaminate proprietary internal codebases or agent packs.
- **Distinguish original repositories from unverified forks**: prefer upstream source repositories over derivative forks unless the fork provides active maintenance and security backports that upstream abandoned.

## Procedure

1. Inspect repository root files for standard license documentation such as LICENSE or LICENSE.md and identify the exact SPDX identifier.
2. Cross-reference the identified software license against organizational legal policies and permissible open-source categories.
3. Review commit contributor graphs and pull request histories to verify author authenticity, release frequency, and developer reputation.
4. Check whether the repository maintains clear version tags adhering strictly to semantic versioning standards for dependency tracking.
5. Record license status, copyright holder details, and provenance metadata in the official evaluation log before granting adoption approval.
6. Halt the adoption process immediately if copyright terms are absent, ambiguous, proprietary, or incompatible with operational requirements.

## Anti-patterns

- Adopting unlicensed third-party skills under the assumption that public repositories are automatically released into the public domain.
- Trusting repository metadata with mismatched author names, conflicting copyright notices, or unverified contributor accounts.
- Integrating copyleft-licensed skills into proprietary agent frameworks without conducting a formal legal review.
- Failing to distinguish between original author commits and unverified automated scraping forks that lack provenance.

## Done checklist

- [ ] Repository license file located and SPDX identifier recorded accurately.
- [ ] License compatibility verified against organizational open-source guidelines.
- [ ] Author identity and commit history lineage authenticated successfully.
- [ ] Semantic versioning release tags checked for dependency tracking.
- [ ] Legal provenance approval documented thoroughly in evaluation log.
- [ ] Copyright terms confirmed valid and compliant for operational use.

## Sources

- Software Package Data Exchange. _SPDX License List and Legal Standards_. <https://spdx.org/licenses/>
- Preston-Werner, Tom. _Semantic Versioning 2.0.0 Specification_. <https://semver.org>
