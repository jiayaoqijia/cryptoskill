---
name: metrics-and-their-misuse
domain: software-engineering/metrics-and-their-misuse
trigger: "Using complexity and size numbers without being used by them."
anti_trigger: "Not for team performance metrics, and not for benchmarking."
scope: "What complexity measures measure."
status: seedling
---

# Metrics and their misuse

## Standard

Analysis tools produce numbers: lines, cyclomatic complexity, nesting depth, duplication percentage. Each is a proxy for something a reader cares about — complexity proxies the difficulty of holding a function in mind — and each fails when promoted from proxy to target. A complexity threshold enforced as a law generates functions split arbitrarily to duck the number, each simpler and the whole harder to follow.

The productive use is as a sorting key, not a gate. High-complexity findings are a reading order for review attention: the functions most worth a careful read, ranked. Duplication percentages locate the code that changes together but lives apart, which is where copy-paste bugs breed. Both uses keep the number subordinate to judgement; a gate flips that order, and the code adapts to the gate rather than the reader.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Record which metrics the tool produces and what each proxies.
- Use complexity and size findings as review priorities, not as merge gates.
- Treat a sudden metric change as a question, never as a verdict.
- Watch trends rather than absolute values; a slow rise across a module says more than one high function.
- Never tie a metric to individual evaluation; the moment you do, the metric is dead.
- Record when a metric stopped correlating with anything anyone cares about, and drop it.

## Procedure

1. List the metrics available and each one's proxy.
2. Decide the use per metric: sorting key, trend, or dropped.
3. Run the metrics and record the distribution, not just the maxima.
4. Pick the top findings by metric and read them with judgement.
5. Track module-level trends across releases.
6. Prune metrics that no longer inform anything.

## Anti-patterns

- A merge gate on a complexity number.
- Refactoring to duck a metric threshold, reducing the number and raising the difficulty.
- Reporting only the worst function rather than the distribution.
- Metrics attached to individuals.
- A dashboard of metrics nobody can say what they proxy.

## Done checklist

- [ ] Metrics listed with their proxies.
- [ ] Use per metric decided.
- [ ] Distribution recorded.
- [ ] Top findings read with judgement.
- [ ] Trends tracked per module.
- [ ] Dead metrics pruned.

The distribution matters more than the maximum: one function at complexity forty in a codebase whose median is six is a different situation from a module whose every function sits at fifteen, and a gate on the maximum would push the first case to split and ignore the second entirely.

## Sources

- Code quality metrics discussion: <https://martinfowler.com/bliki/CodeSmell.html>
- Goodhart's law and measurement: <https://en.wikipedia.org/wiki/Goodhart%27s_law>
- Empirical software measurement: <https://dl.acm.org/>
