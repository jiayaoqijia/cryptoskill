---
name: dependency-management
domain: software-engineering/dependency-management
trigger: "\"add this library\", \"upgrade dependencies\", \"this package is abandoned\", \"should we vendor it\", \"check the licence\"."
anti_trigger: "Where security checks sit in the lifecycle; signing and SBOM policy; schema and ORM migration mechanics; CI gate order."
scope: "Adding, pinning, upgrading and removing dependencies; lockfiles, bots, licence intake"
status: "seedling"
---

# Dependency Management

## Standard

- **Lockfile discipline**: commit the lockfile, pin transitive dependencies, verify hashes. The lockfile is part of the release artifact.
- **Two update bots**: Dependabot (native to GitHub, zero setup) and Renovate (configurable, self-hostable). Neither is authoritative; the guardrails are.
- **Bus factor is the attack surface**: the xz-utils backdoor (CVE-2024-3094; https://www.cisa.gov/news-events/alerts/2024/03/29/reported-supply-chain-compromise-affecting-xz-utils-data-compression-library-cve-2024-3094) was a social-engineered maintainer insertion over two years, and build provenance would not have caught it.
- **License intake**: SPDX expressions identify licenses; copyleft code sits behind a process boundary and gets a legal review before shipping.
- **Scorecard** (https://scorecard.dev): OpenSSF grades a repository on pinned dependencies, branch protection, fuzzing and maintenance signals. ⚠️ The thresholds below are practitioner guidance, not a published standard.

## Decision rules

1. No new dependency for something the standard library does in a few lines.
2. Before adding: check maintenance signals, license, download count and transitive count. A one-function package with twelve dependencies is a bad trade.
3. Commit the lockfile. Any hand edit re-runs the resolver.
4. Auto-merge patches and minors only, with the full suite green. Majors ride a reviewed PR.
5. Refuse a Scorecard below 5, review 5 to 7, adopt 7 and above. ⚠️ Practitioner thresholds.
6. A single-maintainer dependency is a risk. Record it, and prefer the alternative.
7. Removing a dependency means removing its configuration and its transitive lock entries.
8. An incompatible license is **human-gated**: legal review precedes the merge.

## Procedure

1. State the problem the dependency solves, and write the two-line alternative.
2. Check the package: last release, open issue count, maintainer count, license.
3. Read the transitive tree before committing: `npm ls --all`.
4. Add it pinned and commit the lockfile:
   ```bash
   npm install left-pad@1.3.0 --save-exact
   ```
5. Record the license as an SPDX expression.
6. Add the package to the SBOM step (out of scope for this leaf: SBOM policy itself).
7. Configure the bot:
   ```json
   { "extends": ["config:recommended"], "rangeStrategy": "pin" }
   ```
8. Set auto-merge to patches and minors with a green suite; majors by hand.
9. Review each dependency PR: version diff, license change, transitive additions.
10. Audit quarterly: unused, abandoned, and versions behind by a year.
11. To remove: delete the import, the lock entry, the config and the wrapper tests.

## Anti-patterns

- A dependency added for one line of code.
- Installing with a caret, then wondering what changed overnight.
- Majors auto-merged without reading the changelog.
- A lockfile edited by hand.
- A transitive dependency nobody tracked until an advisory landed.
- Pin-and-forget, until a breaking release forces the upgrade.

## Done checklist

- [ ] The dependency solves a stated problem better than the alternative.
- [ ] Lockfile committed and pinning holds.
- [ ] License recorded as an SPDX expression.
- [ ] Bot rules set: patch and minor auto, major reviewed.
- [ ] Transitive tree reviewed at add time.
- [ ] Quarterly audit scheduled.

## Sources

- <https://docs.github.com/en/code-security/dependabot>
- <https://spdx.org/ids-how>
- <https://openssf.org/blog/2026/09/10/tech-talk-recap-a-practitioners-guide-to-cra-readiness/>
- https://scorecard.dev
