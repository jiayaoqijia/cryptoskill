---
maturity: experimental
name: sentry-quota
description: Catch quota-risky Sentry span instrumentation in code and PRs — fan-out × ungated × no-kill-switch — before it blows the span budget
---

# Sentry Span Quota Guard

Find and fix custom Sentry span instrumentation that blows the project span budget. Operates on **code and PRs**, not Sentry dashboards — you spot the culprit in Sentry (`sentry-mcp-queries`), this skill fixes it in code.

## When To Use

- A PR adds custom Sentry spans (`trace()` calls / `TraceName` entries) — review it before merge.
- A custom span/transaction dominates span volume in Sentry — locate where it's emitted and fix it.
- Auditing controllers/UI for always-on, fan-out-prone instrumentation.
- A custom span is the top span-count contributor and must be cut fast (release blocker).

## Do Not Use When

- Reading the live span counts themselves — that's `sentry-mcp-queries` (Volume Estimation).
- Product-analytics events (Segment / `trackEvent`) — that's `instrumentation`, with data domain `knowledge/segment-governance.md` for Segment governance.
- The span is already behind a per-trace sample gate **and** a kill-switch — already mitigated.
- Error volume. Errors are metered separately from spans and transactions, so no change here moves the error quota.

## Breach Triad

A custom span is a quota risk when these stack. The first three together are the breach profile.

| Signal | Static signature | Why it blows quota |
|---|---|---|
| **Fan-out** | span created in a loop / `.map` / `.forEach` / per-asset / per-account / per-chain / poller | N spans per trace, not 1 |
| **Always-on** | no `tracesSampleRate` sub-rate, no hash gate before the span | every qualifying call emits |
| **No kill-switch** | not guarded by an env flag | disabling needs a release, not a config flip |
| Hot path | data-source / update-pipeline / network callback, not a discrete user action | high call frequency |

Low fan-out + discrete user action + already gated = fine. Don't flag healthy spans.

**The subtlest fan-out has no visible loop: a memoized selector.** A `trace` passed into a memoized selector (`createSelector` / `reselect`, or any function called from `useSelector`) fires on every input change by reference. If the selector also iterates entities, it is fan-out × recompute-frequency. Its volume tracks internal state-churn, not user action, so no user-facing metric predicts it — you cannot capacity-plan it. Treat any `trace` reaching a selector as fan-out.

## Workflow

### PR review (pre-merge gate)
1. `gh pr diff <n>` — scan **added** lines for three things, not two: new `TraceName` entries, new `trace(` call sites, **and a `trace`/trace-callback passed as an *argument*** into a call (`fn(…, trace)`). The third is the one reviews miss — a caller wiring up a function's optional `trace?` param adds instrumentation with no `trace(` site and no `TraceName` entry.
2. Check what already emits. For every trace name the diff adds, maps or reroutes, query the target project over the last 90 days (`sentry-mcp-queries`). A name that already emits is not new instrumentation. Review it as a change to measured volume, and say so first in the verdict, because a reviewer who believes it is new will look for a history that already exists. For a name that is new to the target, the other client where it already ships is the reference class. Before carrying that client's volume over, list which of its top names the diff can actually start in the target.
3. Score each against the breach triad: is the enclosing scope a loop, poller, **or selector**? is there a gate? a kill-switch?
4. Block if a new always-on span has no gate — require a sub-sample gate (`span-sub-sampling`) before merge. Cheaper than a post-ship cherry-pick.
5. If the diff adds no `trace(` sites, no `TraceName` entries, **no `trace` argument passed into a call, bumps no dependency, and adds or changes no SDK integration** → "no new instrumentation", stop. A dependency bump brings whatever instrumentation the package carries at the adopted version, which no grep of this diff can see, and that volume can be `http.client` traffic the tracing context surfaces rather than wrapper spans. An SDK integration such as `browserTracingIntegration()` emits `pageload`, `navigation` and `http.client` spans with no `trace(` site at all.

> **Instrumentation is not always added by an instrumentation PR.** The costliest spans arrive incidentally — a caller passes a `trace` argument into an existing function during an unrelated change (a bug fix, a refactor), so the PR's stated purpose gives no signal to review it for quota. Do not gate this scan on the PR *looking* like instrumentation. And accept the limit: a `trace` argument buried in a bug-fix diff will slip a human reviewer, which is why a runtime backstop is needed. Sentry metric alerts cannot target one transaction name's billed volume, only project and category totals, so the backstop belongs in the sampler (the per-name budget below). This skill lowers the rate; it does not eliminate the class.

### Locate (incident)
1. Grep the span name / `TraceName.X` across the consuming repo **and** the controller package source.
2. Open the call site; read the enclosing scope for the fan-out verdict (loop/poller?).
3. **No grep hits ≠ safe** — the culprit may be on a release ref not checked out. Verify the package version / `gh pr checkout` the shipping ref before concluding clean.

### Audit
1. Sweep the span registries (`TraceName` enums) + `trace(` call sites.
2. Rank by breach triad — surface ungated × hot-path × fan-out first.

### Mitigate
Pick the lowest tier that stops the bleed.

## Mitigation Ladder

| Tier | When | Action |
|---|---|---|
| **0 — Immediate** | a span fans out and is actively breaching on the live release | disable the `trace()` call at source (or env-guard it) + **cherry-pick to the release branch** + file a sev-1 release blocker on the in-flight release milestone |
| **1 — Release containment** | spike concentrated in an old, already-patched release with lingering users. A sampler fix in a newer build does not change that release's rates unless it reads its rate remotely | Sentry **inbound filter** dropping `release:<bad>` spans + force-update. The only dashboard action. Filters target a whole release, not one span — don't filter a release you still want data from. There is no inbound filter by transaction name, only a fixed health-check one. Filtered events do not consume quota, so confirm the drop in the filtered outcomes (`stats_v2` grouped by `reason`), not in Explore. It is not instant: one recorded release filter took 3.8 days from filing to taking effect |
| **2 — Durable** | the span is justified long-term but ungated | deterministic `traceId`-hash sub-sample gate before the span (`span-sub-sampling`) |
| **3 — Wrong tool** | the metric needs full fidelity; sampling loses the signal | move the metric off trace spans — they are the wrong substrate for always-on high-cardinality metrics. Segment is the usual target, but its events can ship unregistered, with no CI check and no billing review (data domain `knowledge/segment-governance.md`), so it is not a free lunch |

Tier 0 + 1 stop the bleed; Tier 2 is the follow-up so the metric returns.

**Prevent the next one, not just this one.** Every tier above requires *naming* the offender first, so a new one runs unbounded until someone catches it. A per-transaction-name budget in the sampler — sample the first N of a name per session, then decay — bounds *any* name with no advance knowledge of which will misbehave. It is the only control that acts before the offender is named, and the only one that catches instrumentation added incidentally rather than deliberately.

## Common Pitfalls

| Mistake | Correct approach |
|---|---|
| Per-call random sampling (`Math.random()` per span) | Deterministic `traceId`-hash bucket — all gated spans in a trace kept-or-dropped together |
| Gate the span in Sentry config | Gate at the call site; for an injected-callback controller span, gate in the callback so every consumer inherits the cap |
| Inbound-filter a release you still need data from | Filters drop the whole release — fix in code (Tier 0/2) instead |
| "No grep hits, so it's safe" | The culprit may be on a release ref not checked out — verify the version/ref |
| Disable the span on `main` only | Cherry-pick to the active release branch — `main` alone leaves the live release breaching |
| Treat "move to Segment" as free | Segment events ship without CI governance or billing review (data domain `knowledge/segment-governance.md`) |
| Ship new always-on instrumentation with no kill-switch | Add an env disable flag on day one — turns a future cut into a config flip, not a cherry-pick |
| An optional `trace?` param passes review because it emits nothing | It is a dormant fan-out — it detonates when any caller supplies the argument. Remove the *param*, not just the argument, so one line can't re-arm it. |
| Disable one entry point of a multi-path change | One change can reach the backend by more than one path (a controller callback *and* a selector param). Audit every entry point it added, not just the one that fired. |
| Read a span that "fires N million times" as one triggered too often | A total is transactions × spans per transaction. Check spans per trace before blaming the trigger: fan-out multiplies the count with no change in how often the trigger fires |
| Filter a release before its successor is fixed | The filter redirects users onto the next build; if that carries the same span, volume only moves. Filter a release only once the build users update to is clean. |
