---
name: vendoring-versus-fetching
domain: software-engineering/vendoring-versus-fetching
trigger: "Deciding whether to copy a dependency into the repository."
anti_trigger: "Not for choosing the dependency, and not for fork governance."
scope: "When to copy a dependency into the repository."
status: seedling
---

# Vendoring versus fetching

## Standard

Vendoring copies a dependency's source into the repository; fetching leaves it in the registry and resolves it at install time. Vendoring buys immutability — the code is in your history, reviewable like your own, and unaffected by a registry outage or a package disappearing. The price is that it buys also: updates become manual merges, security fixes wait for you, and the copy silently diverges from anything upstream fixes.

The honest decision is per-dependency, not per-project. A small, stable, rarely-changing utility is a reasonable vendoring candidate — one file, understood once, no upstream churn. A large, actively-maintained framework vendored is a fork the organisation maintains without admitting it maintains one. The rule of thumb that survives: vendor what is small enough to read, fetch what is too large to own.

Primary source: <https://reproducible-builds.org/>.

## Decision rules

- Record for each vendored dependency: version copied, upstream location, and date.
- Prefer vendoring for small, stable, read-once code; prefer fetching for anything actively maintained.
- Record the divergence risk accepted: an upstream security fix does not arrive on its own.
- Put vendored code through the same review as first-party code, once, at vendoring time.
- Record the reason a dependency is vendored; "always done this way" is not a reason.
- Prefer a lockfile with verified integrity over vendoring when immutability is the only goal.

## Procedure

1. List current vendored dependencies and their upstream versions.
2. Record each one's vendoring reason and the divergence accepted.
3. Measure upstream churn per vendored dependency.
4. Move high-churn vendored code back to fetched and locked.
5. Review the remaining vendored code as first-party, once.
6. Record the decision set and re-review annually.

## Anti-patterns

- Vendoring a framework because a registry was slow once.
- A vendored copy whose upstream has diverged, so fixes silently miss.
- Vendoring to skip reading the dependency; vendoring is a commitment to read it.
- Keeping both vendored and fetched copies of the same package.
- No record of why a copy was taken.

## Done checklist

- [ ] Vendored list with upstream versions and dates.
- [ ] Reasons and accepted divergence recorded.
- [ ] Upstream churn measured.
- [ ] High-churn copies converted to locked fetches.
- [ ] Remaining copies reviewed as first-party.
- [ ] Annual re-review scheduled.

A middle path is worth recording when it fits: a patch file kept in the repository and applied at build time to a fetched dependency preserves upstream tracking while carrying a local fix. It costs a build step and a merge on every update, which is the honest price of not maintaining a silent fork.

## Sources

- Reproducible builds and vendoring: <https://reproducible-builds.org/>
- Source pinning practice: <https://slsa.dev/>
- Semantic versioning: <https://semver.org/>
