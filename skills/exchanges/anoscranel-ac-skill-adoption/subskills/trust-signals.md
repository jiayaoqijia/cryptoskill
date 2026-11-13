---
name: trust-signals
domain: skill-authoring/trust-signals
trigger: "Evaluating whether a third-party agent skill is actively maintained; checking issue tracker health; interpreting automated security scan verdicts before adoption"
anti_trigger: "Inspecting skill prompt text for instruction injection (subskills/security-vetting.md); checking software license compatibility (subskills/provenance-and-license.md)"
scope: "Judging skill trustworthiness via maintenance recency, issue tracker hygiene, independent security scan verdicts, changelog quality, author track record, and distinguishing popularity metrics from safety guarantees"
status: "seedling"
---

# Trust Signals

## Standard

- **OWASP Top 10 for LLM Applications**: guidelines on evaluating third-party components, supply-chain risks, and untrusted instruction sources in AI workflows. <https://genai.owasp.org>
- **SLSA provenance framework**: supply-chain security standards requiring verifiable build integrity, change tracking, and transparent provenance metadata. <https://slsa.dev>

## Decision rules

- **Demand active maintenance recency**: reject skills with no commits, issue responses, or dependency updates within the past twelve months unless the codebase is strictly feature-complete and static.
- **Inspect issue tracker hygiene**: examine whether bug reports receive maintainer responses, whether security vulnerabilities are acknowledged and patched, and whether toxic or stagnant communication patterns dominate the repository.
- **Require independent automated security scan verdicts**: verify that the skill passes automated static analysis and supply-chain vulnerability scanners without unresolved high-severity alerts.
- **Treat download volume strictly as popularity**: recognize that high install counts measure marketing reach or convenience rather than functional reliability or absence of malicious intent.

## Procedure

1. Inspect the target repository commit history to determine the date of the most recent substantive update.
2. Review the public issue tracker and pull request history to check maintainer responsiveness and resolution speed for reported bugs.
3. Check independent security scan badges or audit reports attached to the registry listing for unresolved vulnerabilities.
4. Read the release notes and changelog files to evaluate whether version bumps correspond to meaningful bug fixes and feature additions or empty cosmetic churn.
5. Cross-reference author identity and past repository contributions to assess track record and reliability.
6. Compile observed trust signals into a adoption decision score before proceeding to source-code security vetting.

## Anti-patterns

- Adopting unmaintained skills with stale codebases under the assumption that simple prompt files never break.
- Confusing high GitHub star counts or registry install metrics with rigorous security audits.
- Ignoring open security advisory tickets or unresolved bug reports in the repository issue tracker.
- Relying on vague author promises rather than verifiable commit history and changelog records.

## Done checklist

- [ ] Repository commit recency verified within acceptable timeframe.
- [ ] Issue tracker hygiene and maintainer responsiveness evaluated.
- [ ] Automated security scan verdicts checked and free of high-risk alerts.
- [ ] Changelog and release notes reviewed for verifiable change history.
- [ ] Author track record and reputation assessed.

## Sources

- OWASP Foundation. _OWASP Top 10 for Large Language Model Applications_. <https://genai.owasp.org>
- SLSA Security Working Group. _Supply-chain Levels for Software Artifacts Framework_. <https://slsa.dev>
