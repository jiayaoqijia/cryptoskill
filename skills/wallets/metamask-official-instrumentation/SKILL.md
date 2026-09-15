---
maturity: experimental
name: instrumentation
description: Create and update Sentry spans, MetaMetrics events, and Segment events — methodology, policies, common pitfalls
---

# Analytics Instrumentation

## When To Use

- Adding or modifying a MetaMetrics (Segment) event
- Adding or modifying a Sentry performance span
- Estimating event or span volume from production data
- Auditing existing instrumentation for correctness

---

## Do Not Use When

- Adding local debug logging with no telemetry destination
- Investigating an existing Sentry error report (use `sentry-mcp-queries`)
- Internal feature flag evaluation not surfaced as an analytics event

---

## Sentry Spans

### Creating a Span

1. **Register a named trace entry** in the repo's trace name enum before writing any span code. Unnamed spans are invisible in Sentry filters.
2. **Use the repo's `trace()` wrapper**, not raw `Sentry.startSpan()`. Wrappers handle cross-process context propagation, active-span inheritance, and consistent tag injection.
3. **Inherit parent automatically** — when no `parentContext` is provided, the wrapper inherits from `Sentry.getActiveSpan()`, making the new span a child of the active parent (e.g., a `pageload` span). That parent is whichever span is active at the call, not necessarily the one that caused the work, which metamask-extension#45527 (stop spans silently attaching to whatever trace happens to be active) proposes to fix. A span started by `trace()` without a callback is active only inside that call, so spans created before its `endTrace()` do not nest under it.

### Updating a Span

- Adding a tag: no governance required
- Renaming a trace name enum entry: grep all callsites; update enum and references atomically
- Changing an `op` value: breaks saved queries and dashboards — coordinate with whoever owns them
- Moving a span's start (`trace()`) or end (`endTrace()`): changes what its duration measures, so a release-over-release delta mixes a performance change with a definition change

---

## MetaMetrics / Segment Events

### Creating an Event

1. **Check the event name enum** — event may already exist under a different phrasing.
2. **Check the segment tracking plan** — event may be registered under a different name than the enum key.
3. **Add to the enum**, then implement the `trackEvent` call.
4. **Pass `excludeMetaMetricsId: true` only for an event that must not carry the user's identity.** It sends the event under the shared anonymous id and drops the profile ids, for every user, not only those who have not opted in. Event names matching `/^send|^confirm/iu` get it by default unless the caller passes `excludeMetaMetricsId: false` (see data domain `knowledge/metrametrics-identity.md`).
5. **Open a data governance review** before merging. There is usually no CI enforcement on schema registration — this step is easy to skip (see data domain `knowledge/segment-governance.md`).
6. **Register in the team's segment tracking plan** before shipping.

### Updating an Event

- Adding a property: requires governance review and schema update
- Renaming an event: deprecate old + add new in tracking plan; coordinate on migration window
- Removing an event: confirm no active dashboards depend on it before removing

---

## Volume Estimation via Sentry

When direct Segment access is unavailable, estimate from Sentry production span data:

1. **Find a correlated HTTP endpoint** — one that fires 1:1 with the event.
2. **Query Sentry Traces Explorer** (aggregate mode):
   ```
   span.op:http.client span.description:*{endpoint}*
   ```
3. **Read the `count()` aggregate.** Span datasets already extrapolate it by each span's sample weight, so it is the estimate. Do not multiply it by `1 / tracesSampleRate`, which extrapolates twice.
4. **Interpret as upper bound** — endpoint may have callers outside the event path.

Caveats: sample population is MetaMetrics opted-in users only. The extension's Sentry integration drops every event unless `consentDecisionMade && optedIn`, and Segment gates differently, so attribution across the two pipelines holds at install granularity, not per session. For longer-range (30D+) or release-over-release queries, the sampled count is **not** comparable at face value — older releases are downsampled / retention-truncated and `.0` releases are sample-thin; see `sentry-mcp-queries` (Longer-Range Queries and Percentile Fidelity) and the `performance-attribution` skill.

---

## Common Pitfalls

| Mistake | Correct Approach |
|---------|-----------------|
| `excludeMetaMetricsId: true` on an event that needs user identity | It sends the event under the shared anonymous id for every user. Reserve it for events that must be anonymous |
| Ship event without tracking-plan registration | No CI gate — add governance review explicitly to PR checklist |
| Raw `Sentry.startSpan()` instead of the repo's `trace()` wrapper | Use the wrapper — handles cross-process context and active-span inheritance |
| New span with no trace name enum entry | Register enum entry first; unnamed spans are invisible in Sentry filters |
| Multiply a span `count()` by `1 / tracesSampleRate` | `count()` is already extrapolated, so read it as the estimate |
| Treat Sentry estimates as exact counts | Probabilistic sample — state sample size and confidence |
