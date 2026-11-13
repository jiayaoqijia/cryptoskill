---
name: post-install-lifecycle
domain: skill-authoring/post-install-lifecycle
trigger: "Re-verifying third-party skills upon update; detecting drift between installed copies and upstream repositories; setting audit cadences; pruning unused skills"
anti_trigger: "Deciding whether to build or adopt a skill (subskills/build-vs-adopt.md); performing initial security vetting before install (subskills/security-vetting.md)"
scope: "Managing adopted skills post-installation through upstream drift detection, scheduled security audits, retirement of unused packages, and strict workspace hygiene"
status: "seedling"
---

# Post-Install Lifecycle

## Standard

- **NIST SP 800-218 Secure Software Development Framework**: ongoing maintenance, vulnerability monitoring, and lifecycle configuration management guidelines. <https://csrc.nist.gov>
- **Semantic Versioning 2.0.0**: rules governing upstream updates, patch releases, and breaking change detection for dependency management. <https://semver.org>

## Decision rules

- **Re-verify upstream updates before merging**: run security scans and integrity checks on every new release tag before applying updates to installed third-party skills.
- **Detect drift between local copies and upstream**: regularly compare active skill files against the canonical upstream repository to catch silent modifications or abandoned maintenance.
- **Establish a scheduled audit cadence**: review active agent skills quarterly to ensure continued relevance, security posture, and compliance with operational requirements.
- **Prune unused skills immediately**: remove adopted skills from the active workspace as soon as their operational utility ceases, preventing instruction clutter and unmonitored attack surface.

## Procedure

1. Monitor upstream repository release channels and commit feeds for security patches and version updates across all adopted packages.
2. Run automated comparison tools to detect divergence between locally installed skill files and upstream canonical source trees.
3. Conduct quarterly security and utility audits across all active third-party agent skills deployed in the production workspace.
4. Execute removal and rollback procedures promptly for any adopted skill that fails maintenance criteria, exhibits drift, or remains unused.
5. Update local metadata logs to record verification timestamps and current version hashes for all active third-party dependencies.
6. Archive audit records securely to maintain a transparent compliance and provenance trail of all adopted agent components.

## Anti-patterns

- Leaving adopted third-party skills installed indefinitely without checking for upstream security patches or dependency updates.
- Accepting upstream repository updates blindly without running cryptographic hash verification or automated security scans.
- Retaining unused or obsolete skills in active directories, thereby expanding unnecessary security exposure and prompt clutter.
- Failing to track drift between local workspace modifications and upstream master repositories over time.

## Done checklist

- [ ] Upstream release monitoring channels configured for all active skills.
- [ ] Drift detection checks executed between local and upstream source files.
- [ ] Quarterly audit schedule established and documented in operational logs.
- [ ] Unused or obsolete skills pruned completely from active workspace directories.
- [ ] Metadata logs updated with verification timestamps and current version hashes.

## Sources

- National Institute of Standards and Technology. _NIST SP 800-218 Secure Software Development Framework_. <https://csrc.nist.gov>
- Preston-Werner, Tom. _Semantic Versioning 2.0.0 Specification_. <https://semver.org>
