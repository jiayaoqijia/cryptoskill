---
name: dependency-risk-and-updates
domain: software-engineering/dependency-risk-and-updates
trigger: "Keeping dependencies moving without ambush or rot."
anti_trigger: "Not for application code refactoring, and not for vulnerability triage of shipped systems."
scope: "Keeping dependencies current without ambush."
status: seedling
---

# Dependency risk and updates

## Standard

Two failure modes bracket dependency management, and they pull in opposite directions. Never updating means the application runs versions with known, published, sometimes weaponised flaws, and eventually cannot be updated at all because everything around a very old version has moved. Updating constantly means every build absorbs changes nobody examined, and the application breaks for reasons no code review explains.

The workable discipline is a middle path with structure: scheduled, small, reviewed updates — where each update's diff is looked at and each release's notes are at least skimmed for behaviour changes — plus an out-of-band channel for security releases that skips the schedule but not the review. Automated everything means unexamined; never anything means calcified; scheduled-with-review is the only setting that treats the dependency base as a managed surface.

Primary sources: <https://slsa.dev/> and <https://reproducible-builds.org/>.

## Decision rules

- Record the update cadence for routine updates and the separate path for security releases.
- Record for each direct dependency its criticality — how much of the application stops without it.
- Require the release notes or changelog to be checked for a behaviour change, not just the version number.
- Batch routine updates small enough that a revert is a revert of one thing.
- Record the out-of-band update's rule: it skips the schedule, not the review, and not the test run.
- Favour dependencies that are maintained and boring; abandonment risk is a dependency risk.

## Procedure

1. Inventory direct dependencies and classify each by criticality.
2. Set the routine cadence and the security-release exception rule.
3. For each update, read the changelog for breaking or behavioural changes.
4. Run the update through the normal test and release path, one or few at a time.
5. Record each update in a log with the reason and the notes-checked confirmation.
6. Re-review the criticality classification quarterly.

## Anti-patterns

- Updating everything at once once a quarter.
- Never updating, then being forced to by a security event on an unupdatable tree.
- A security-release path that skips tests to be fast.
- Treating a minor version bump as risk-free by definition.
- Choosing a dependency by stars without checking its maintenance record.

## Done checklist

- [ ] Dependencies inventoried and classified.
- [ ] Routine cadence and exception rule set.
- [ ] Changelog check required per update.
- [ ] Updates batched small with revert capability.
- [ ] Security path defined including tests.
- [ ] Update log maintained.

## Sources

- Supply-chain levels: <https://slsa.dev/>
- Reproducibility as an update verification tool: <https://reproducible-builds.org/>
- Semantic versioning: <https://semver.org/>
