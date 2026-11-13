---
name: bundle-budgets
domain: software-engineering/bundle-budgets
trigger: "Keeping build output size from growing silently."
anti_trigger: "Not for runtime performance budgets, and not for lint rules in general."
scope: "Size budgets enforced in CI and what they should measure."
status: seedling
---

# Bundle budgets

## Standard

A bundle budget is a CI rule that fails the build when output size crosses a stated threshold. Its purpose is not the number itself but the conversation it forces: every growth crosses a limit visible to everyone, and the person adding the growth must justify it or remove it. Without a budget, size grows one dependency at a time and is only noticed when a user complains.

The thresholds should come from the application's own baseline and from what the entry point must contain, not from another application's numbers. A useful initial set is modest: an eager-entry budget at the level where load behaviour starts to degrade, a per-route budget so one route cannot hide in the entry, and an asset budget for fonts and images that often outweigh the script.

Primary source: <https://web.dev/learn>.

## Decision rules

- Set budgets from a measured baseline, and state the baseline in the record.
- Budget the eager entry separately from lazy chunks; they have different users.
- Budget the largest chunks and assets individually, not only the total.
- Fail CI on breach; warn within a band so small growth is visible before it crosses.
- Record every deliberate threshold change with the reason and the approver.
- Distinguish compressed over-the-wire size from disk size, and budget the wire size.

## Procedure

1. Measure the current build output by chunk, compressed and uncompressed.
2. Set entry, per-route, and asset budgets from the measured baseline.
3. Wire the budgets into CI so a breach fails the build configuration check.
4. Add a warning band ten to twenty percent below each failure threshold.
5. On breach, inspect the delta — new dependency, barrel, or asset — before any threshold change.
6. Record threshold changes and their rationale.

## Anti-patterns

- Copying budget numbers from an unrelated project.
- Budgeting only the total, which lets a route hide its growth in a shared chunk.
- Raising the threshold as the response to a breach.
- Measuring disk size when the wire is compressed differently.
- A budget nobody sees because it lives in a config file outside review.

## Done checklist

- [ ] Baseline measured by chunk.
- [ ] Entry, route, and asset budgets set from it.
- [ ] CI failure wired on breach.
- [ ] Warning band configured.
- [ ] Breach procedure documented: inspect before adjust.
- [ ] Threshold-change log kept.

## Sources

- Performance budgets practice guide: <https://web.dev/learn>
- HTTP compression and transfer size: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Compression>
- Lighthouse budget auditing: <https://github.com/GoogleChrome/lighthouse>
