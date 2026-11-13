---
name: incremental-delivery
domain: software-engineering/incremental-delivery
trigger: "\"Build it step by step\", \"start with a walking skeleton\", \"keep main green\", \"this change is getting too big\", \"how do I land this in pieces\"."
anti_trigger: "Planning the task list; throwaway experiments (subskills/spikes-prototypes.md); branch policy."
scope: "Building in small verified steps: walking skeleton, one change per commit, always green"
status: "seedling"
---

# Incremental Delivery

## Standard

- **Small batches**: DORA ties small batches and trunk integration at least daily to higher delivery performance; integration cost grows with branch lifetime (https://dora.dev/capabilities/trunk-based-development/).
- **Atomic commit**: one stable, independent unit of change that builds and passes tests on its own (GitHub Blog, "Write Better Commits").
- **Walking skeleton**: the thinnest end-to-end path through all layers, deployed early (Cockburn).
- **Branch by abstraction / Parallel Change** for changes that cannot land in one step. Parallel Change = expand, migrate, contract (Danilo Sato, 13 May 2014, https://martinfowler.com/bliki/ParallelChange.html).
- **Feature flags** hide unfinished work on main.
- Trunk-based work *correlates* with higher performance (*Accelerate*, 2018). Not proven causal.

## Decision rules

1. Each step leaves main buildable, green and deployable.
2. One step = one reason to change. A refactor and a behaviour change are two steps.
3. Order inside a task: (a) failing test or characterization test, (b) structure change if needed, (c) behaviour change, (d) cleanup.
4. A step that cannot be green in about an hour gets split. ⚠️ House heuristic.
5. Incomplete user-facing work ships dark behind a flag, default off.
6. A change that touches a contract other code depends on uses Parallel Change: add new, move callers, remove old, each as its own commit.
7. Verify after every step: run the tests that cover the change, plus the fast suite.
8. Stop and reslice when a step's diff passes about 400 changed lines. ⚠️ House threshold, aligned to review size limits.

## Procedure

1. Start the feature with a walking skeleton: route → handler → storage → response, hard-coded where needed, deployed behind a flag.
2. Write the list of steps for the task. Each step names its test.
3. For each step:
 1. Write or update the test. See it fail for the right reason.
 2. Make the smallest change that passes.
 3. Run `pre-commit run` and the relevant tests.
 4. Commit with a message stating the one reason.
4. Push at least daily. Merge through the required checks.
5. When a step reveals new work, add it to the list. Do not widen the current step.
6. For a contract change, run Parallel Change:
 - Expand: add the new path beside the old one.
 - Migrate: move callers one by one.
 - Contract: delete the old path once no caller remains.
7. Turn the flag on for internal users, then widen. Remove the flag after full rollout.

## Anti-patterns

- A week of local work, then one huge PR.
- "WIP" commits that break main; refactor and feature in one commit.
- Long-lived branch instead of a flag; flag never removed.
- Skipping tests because "it is a small change".

## Done checklist

- [ ] Walking skeleton deployed early.
- [ ] Every commit on main builds and passes tests.
- [ ] Each commit has one reason.
- [ ] Unfinished work is behind a flag.
- [ ] Contract changes followed expand-migrate-contract.

## Sources

- <https://github.blog/developer-skills/github/write-better-commits-build-better-projects/>

- https://dora.dev/capabilities/trunk-based-development/ · https://martinfowler.com/bliki/ParallelChange.html
