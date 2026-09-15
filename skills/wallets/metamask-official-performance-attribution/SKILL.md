---
maturity: experimental
name: performance-attribution
description: Attribute release-over-release p75/p95 performance movements to specific code changes via black-box diff analysis
---

# Performance Attribution

Pair a **measured** percentile movement (from Sentry Trace Explorer) with **black-box code-diff analysis** to produce confidence-rated attributions: what changed across releases, how much it moved, and why.

## When To Use

- Explaining a confirmed p75/p95 latency change across releases
- Building a per-release attribution catalogue (change → confidence → metric)
- Auditing whether a "performance initiative" actually moved a metric
- Attributing movement that spans the app repo **and** `@metamask/*` core-package bumps

## Do Not Use When

- The metric movement isn't yet confirmed reliable — run query hygiene first (see `sentry-mcp-queries`: filter superseded/low-sample releases, normalize, verify stored sample size)
- You need proof of causation — this yields *likely contributors*, not isolated causes (see Limitations)
- Pre-merge perf review of a single PR — there is no production metric to attribute yet

## Step 1 — Get the Measurement Right First

Attribution is only as good as the metric. Lock these down before touching code:

- **Percentile.** p75 = typical user (more stable signal). p95 = slowest 5% — *assumed* large-wallet/power users, but **not cohort-verified** (also slow hardware / poor network). Prioritize p95 when the optimization targets data size (memoization, virtualization) that disproportionately helps the tail; trust p75 as the more reliable number.
- **Time window.** Use the **longer (90d) window as primary** — it includes traffic from when older releases were actively used, so the population is representative and comparable across releases. A 30d window over-weights residual users still lingering on old versions → inflated baselines and bigger-looking deltas between *different* populations. Report 90d; cite 30d only as context.
- **Version selection.** Per minor line, anchor on the **highest-sample patch**, never the `.0`. `.0` releases have 10–100× fewer samples and are rollout-biased. See `sentry-mcp-queries` → *Filtering Unreliable Releases* and *Longer-Range (30D+) Queries and Percentile Fidelity*.

## Step 2 — Black-Box Code Analysis

Assess impact on **code content + execution frequency alone**. Deliberately ignore commit messages, PR titles/descriptions, claimed impact, and epic/initiative goals — they bias the read. Base it on: diff content, file location (→ execution frequency), algorithmic complexity, and memoization patterns.

Hot-path categories — a change here can move a render metric:

| Category | Why it matters |
|---|---|
| Build config | Build-time transforms (e.g. React Compiler) apply broadly |
| Selectors | Run on every state change — hottest path |
| Hooks | Affect component lifecycle / re-render frequency |
| Components | Virtualization & render patterns |
| Dependencies | Version bumps change runtime behavior |

Pattern catalogue — what to grep for:

| Pattern | Signal | Confidence |
|---|---|---|
| `createDeepEqualSelector` → `createSelector` + `EMPTY_ARRAY` sentinel | Removes per-change deep compares | HIGH if foundational selector |
| Identity-function selector `(foo => foo)` → real transform | Broken memoization fixed | HIGH if many consumers |
| In-place mutation `.sort()/.reverse()/.splice()` → spread copy | Mutation had broken all downstream memoization | HIGH |
| Build-plugin addition with broad scope | Build-time optimization | HIGH if scope = all `ui/` |
| O(n) string parse → O(1) lookup | Algorithmic reduction | MEDIUM — depends on call frequency |

## Step 3 — Score Confidence

1. **Mechanism** — how does this reduce work? (fewer re-renders / less allocation / better caching)
2. **Frequency** — is the path hot? (selector per state change = hot)
3. **Scope** — how many components/files does it touch?
4. **Match** — does it target what the metric measures?

| Confidence | Criteria |
|---|---|
| HIGH | Clear mechanism + hot path + timing matches the metric move |
| MEDIUM | Mechanism clear, frequency or scope uncertain |
| LOW | Indirect or infrastructure-only |

## Step 4 — Don't Forget Core Packages

App-repo diffs miss work shipped as `@metamask/*` version bumps — it surfaces only as a `package.json` change. For each bump between releases, read the package CHANGELOG "Changed"/"Fixed" sections for state-size reduction, caching, fewer RPC calls, batching, or data-structure/field deprecations. (Commands and the packages to watch live in the repo file.)

## Reading / Writing an Attribution Catalogue

- Release-header totals = the **measured** improvement for the whole release
- Table rows = **likely contributors**, not isolated causes
- "High confidence" = mechanism + timing + population align
- Always keep an **Unattributed** section for movement no change explains
- Flag high-variance metrics (a noisy confirmation-popup p95) as inconclusive, not as wins

## Limitations

- **Correlation, not causation** — change + improvement in the same release does not prove the change caused it
- **Release totals, not isolated impact** — a "-44%" reflects the entire release, not one change
- **Production variance** — user hardware and network are uncontrolled, and each release's user mix differs (early updaters on a new release, lingering users on an old one)
- **Code analysis, not runtime profiling** — based on structure, not measured execution paths
- **p95 cohort is assumed, not verified** — no power-user segmentation
- **Window choice changes the baseline** — always state which window a number came from

For more precise attribution: per-optimization feature flags / A-B tests, CI synthetic benchmarks, and verified user-cohort segmentation. Threshold remote feature flags assign each user to a fixed group by hashing a per-user id (the canonical profile ID, or the MetaMetrics ID before a profile exists), so a threshold flag gives a stable A/B split.
