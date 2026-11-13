---
name: affected-target-selection
domain: software-engineering/affected-target-selection
trigger: "Running only the targets a change affects."
anti_trigger: "Not for test selection strategy, and not for deployment."
scope: "Running only what changed, and the false negatives it risks."
status: seedling
---

# Affected-target selection

## Standard

Affected-target selection computes the transitive dependents of a change and runs only those. The saving is large in a monorepo, and the risk is a false negative: a target that should have run did not, because the graph did not know it depended on the change. When that happens, the failure appears in the next stage or in production rather than in CI.

The risk is manageable when the graph is complete and measurable when it is not. Two practices contain it: a scheduled full run that catches what incremental selection missed, and a periodic comparison of the affected set against the set that would have been selected by a wider filter. The record states which of those is in place, because without one the selection is an unmeasured bet.

Primary sources: <https://bazel.build/> and <https://www.cncf.io/>.

## Decision rules

- Record the selection mechanism and the graph it queries.
- Record the fallback for changes that touch shared configuration, which usually widen the set.
- Record the scheduled full run and its cadence.
- Record the false-negative detection method and its result.
- Record the targets excluded deliberately, such as documentation-only paths.
- Record the time saved and the risk accepted, so the trade-off is explicit.

## Procedure

1. Record the selection mechanism.
2. Define the widening rules for shared changes and record them.
3. Schedule a full run at a stated cadence.
4. Compare the affected set with a wider filter and record the difference.
5. Record intentional exclusions.
6. Record the measured saving.

## Anti-patterns

- Selecting affected targets without a full run ever again.
- Excluding a shared configuration path from widening.
- Treating the graph as complete when declarations are known to be incomplete.
- No measurement of what the selection missed.
- Widening every change, which reduces the selection to a full run without saying so.

## Done checklist

- [ ] Selection mechanism recorded.
- [ ] Widening rules recorded.
- [ ] Full run scheduled.
- [ ] False-negative comparison recorded.
- [ ] Exclusions recorded.
- [ ] Saving measured.

The widening rule deserves a named owner as well as a definition: the shared configuration paths that trigger a full run are exactly the ones a hurried change will edit without noticing, so the rule should be enforced by the tooling rather than by the reviewer's memory of which files are special.


## Sources

- Build graph and test selection documentation: <https://bazel.build/>
- Continuous integration practice: <https://www.cncf.io/>
- Build reproducibility reference: <https://reproducible-builds.org/>
