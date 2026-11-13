---
name: fleet-lockfile-management
domain: software-engineering/fleet-lockfile-management
trigger: "Coordinating dependency pins across many repositories."
anti_trigger: "Not for one repository's lockfile, and not for choosing what to depend on."
scope: "Coordinating pins across many repositories."
status: seedling
---

# Fleet lockfile management

## Standard

One repository's lockfile is a solved problem; a hundred repositories' lockfiles are a fleet, and fleets behave like gardens — each one slightly different, each one aging at its own pace, and the ones nobody works on quietly becoming the ones nobody can update. The fleet question is not how to pin but how to keep a hundred pins coherent: aligned enough that a security release can be applied everywhere in a day, and independent enough that one team's update never blocks another's.

The practices that scale are mechanical. A shared, automated update process — a bot opening small, visible, reviewable pull requests per repository — keeps the fleet moving without a meeting. A fleet-wide inventory of what is pinned where answers the only question that matters in a security event: which repositories hold the affected version. And an explicit rule for repositories that are dormant — update them or archive them — prevents the subset that cannot be updated from growing.

Primary sources: <https://reproducible-builds.org/> and <https://slsa.dev/>.

## Decision rules

- Maintain a fleet inventory: repository, direct dependencies, pinned versions, last-updated date.
- Prefer automated per-repository update pull requests over coordinated manual waves.
- Measure fleet coverage: after a security release, how many repositories hold the fixed version within a day, a week.
- Define the dormant-repository rule: automated updates continue, or the repository is archived.
- Record the owner of the automation itself and the escalation when the bot fails.
- Align tooling and lockfile formats across the fleet where possible; divergence is its own cost.

## Procedure

1. Build the inventory from the fleet's repositories and lockfiles.
2. Deploy automated update pull requests per repository.
3. Record the merge rule: who merges routine updates and on what evidence.
4. Measure the day-one and week-one coverage after the next security release.
5. Apply the dormant rule; archive what will not take updates.
6. Record the automation owner and its failure escalation.

## Anti-patterns

- A security event answered by grepping each repository by hand.
- Dormant repositories accumulating years of unpinnable drift.
- Manual coordinated upgrades of everything, requiring every team to agree.
- Automation whose failures nobody is paged about.
- Fleet coverage never measured, so the process is assumed rather than known.

## Done checklist

- [ ] Fleet inventory maintained.
- [ ] Automated update pull requests in place.
- [ ] Merge rule recorded.
- [ ] Coverage measured on a real event.
- [ ] Dormant rule applied.
- [ ] Automation owner and escalation recorded.

## Sources

- Reproducible builds at scale: <https://reproducible-builds.org/>
- Supply-chain integrity levels: <https://slsa.dev/>
- Continuous integration practice: <https://martinfowler.com/articles/continuousIntegration.html>
