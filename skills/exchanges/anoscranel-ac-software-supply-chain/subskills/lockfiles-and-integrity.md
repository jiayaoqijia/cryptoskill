---
name: lockfiles-and-integrity
domain: software-engineering/lockfiles-and-integrity
trigger: "Making dependency resolution reproducible through lockfiles."
anti_trigger: "Not for choosing dependencies, and not for vulnerability scanning."
scope: "What a lockfile pins and what it does not."
status: seedling
---

# Lockfiles and integrity

## Standard

A lockfile records the exact versions — and in most ecosystems the content hashes — of every dependency the application resolves, so a fresh install reproduces the same dependency tree the last build used. Without it, an install resolves ranges afresh each time, and the build depends on the state of the registry at the moment it runs: reproducibility by luck, and luck is not a release strategy.

What a lockfile pins is what was resolved, not what was reviewed. The file records that version 1.4.2 of a package is what the application uses; it does not say whether anyone read 1.4.2, whether it is current, or whether a transitive dependency underneath it resolved to something nobody chose at all. A stale lockfile is reproducible and drifting at once — perfectly reproducing a decision made two years ago by someone who has left.

Primary source: <https://slsa.dev/>.

## Decision rules

- Commit the lockfile and make CI install from it, failing if the lockfile is out of sync.
- Record the lockfile format's guarantees: version only, or version plus content hash.
- Distinguish your declared dependencies from the transitively resolved ones someone did not choose.
- Record the update cadence and the check that flags a dependency unpinned-newer than a security release.
- Verify a fresh clone builds the same tree as the recorded lockfile.
- Record who may merge a lockfile change and under what review.

## Procedure

1. Confirm the project has a lockfile and CI installs locked, not floating.
2. Record the format and whether it hashes content or only names versions.
3. Export the resolved tree and count direct versus transitive dependencies.
4. Verify a fresh install reproduces the identical tree.
5. Wire a sync check: lockfile out of sync with manifests fails CI.
6. Document the update cadence and the merge rule for lockfile-only changes.

## Anti-patterns

- Regenerating the lockfile casually, silently moving hundreds of transitive versions.
- Mixing locked and unlocked installs across environments.
- Treating the lockfile as the review record — it records what resolved, not what was examined.
- Installing with a different registry than CI uses and expecting identical resolution.
- Lockfile changes merged without a diff of resolved versions.

## Done checklist

- [ ] Lockfile committed and CI installs from it.
- [ ] Format guarantees recorded.
- [ ] Resolved tree exported; direct and transitive counted.
- [ ] Fresh install reproducibility verified.
- [ ] Sync check wired in CI.
- [ ] Update cadence and merge rule documented.

## Sources

- Supply-chain integrity framework: <https://slsa.dev/>
- Reproducible builds principles: <https://reproducible-builds.org/>
- Semantic versioning and pinning: <https://semver.org/>
