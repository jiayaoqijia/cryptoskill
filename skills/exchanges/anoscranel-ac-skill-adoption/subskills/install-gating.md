---
name: install-gating
domain: skill-authoring/install-gating
trigger: "Staging third-party skill installation in sandboxed environments; running fail-closed checks before skill activation; verifying file hashes against reviewed source"
anti_trigger: "Evaluating author license and copyright provenance (subskills/provenance-and-license.md); deciding whether to adopt or author from scratch (subskills/build-vs-adopt.md)"
scope: "Staged adoption workflow including sandboxed installation, fail-closed gate checks, cryptographic hash verification against reviewed source trees, and clean rollback mechanics"
status: "seedling"
---

# Install Gating

## Standard

- **SLSA Supply Chain Framework**: guidance on secure artifact build pipelines, cryptographic integrity verification, and provenance attestation. <https://slsa.dev>
- **NIST SP 800-218 Secure Software Development Framework**: foundational security practices for verifying software integrity before deployment into production environments. <https://csrc.nist.gov>

## Decision rules

- **Isolate installation to staging directories**: deploy candidate skills into dedicated staging paths or sandboxed volumes before activation to prevent unverified code from contaminating active agent packs.
- **Enforce fail-closed gate checks**: halt the installation pipeline immediately if any automated security scan, syntax check, or license verification step fails.
- **Verify cryptographic hashes against reviewed source**: ensure the exact byte sequence of the installed files matches the source tree that underwent security vetting.
- **Maintain clean rollback capability**: ensure that removing a failed or unwanted skill completely deletes all installed files and leaves no orphaned directories or dangling references.

## Procedure

1. Stage the vetted skill files into a temporary isolated directory separate from production agent skill paths.
2. Generate cryptographic checksums for all staged markdown files, scripts, and configuration assets.
3. Compare generated checksums against the verified source repository state to confirm zero drift or tampering.
4. Execute automated validation gates to test file structure, frontmatter syntax, and instruction integrity.
5. Move staged files into the active skill directory only upon receiving a complete pass verdict from all gates.
6. Execute automated removal scripts to verify that complete rollback succeeds cleanly if post-install issues arise.

## Anti-patterns

- Deploying third-party skill files directly into production active paths without staging or sandboxing.
- Bypassing failed gate checks because the missing constraint appears minor or cosmetic.
- Failing to verify cryptographic hashes between reviewed source files and installed copies.
- Leaving orphaned configuration files or partial directories behind during removal or rollback.

## Done checklist

- [ ] Skill files deployed successfully into isolated staging directory.
- [ ] Cryptographic checksums generated and matched against reviewed source trees.
- [ ] Automated validation gates executed with all checks passing.
- [ ] Staged files promoted to active directory following successful verification.
- [ ] Rollback deletion procedure tested and confirmed clean.

## Sources

- SLSA Security Working Group. _Supply-chain Levels for Software Artifacts Framework_. <https://slsa.dev>
- National Institute of Standards and Technology. _NIST SP 800-218 Secure Software Development Framework_. <https://csrc.nist.gov>
