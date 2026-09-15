---
name: sentry-grafana-correlation
description: Join one trace across Sentry and Grafana Tempo by trace id to see the whole client-to-backend path, and diagnose why a half is missing. Covers the split-store model (client spans reach Sentry through the SDK and survive only head sampling; backend spans reach Tempo through tail sampling and Sentry through environment routing), the classification of both-halves / client-only / backend-only outcomes with the sampling and routing rule that causes each, and the id-padding, time-window, and query-syntax traps that make a present trace look absent. Use when a trace looks truncated, a backend span has no parent, per-hop latency needs attributing across the seam, or you need to know which store should hold a given span. Triggers on cross-stack trace, orphaned span, trace id lookup, client-backend correlation, split waterfall, or "where did the rest of the trace go".
maturity: experimental
---

# sentry-grafana-correlation

One request produces spans in two stores, joined only by `trace_id`. Reading a trace end to end means querying both and knowing which absences are expected.

Prerequisite: `grafana-tempo-queries` for the Tempo side, `sentry-mcp-queries` for richer Sentry work.

## The model — what lands where, and why a half goes missing

| Span | Reaches | Gated by |
| --- | --- | --- |
| Client (`pageload`, `navigation`, `http.client`, custom) | Sentry, via the SDK transport | the head decision of the context the span joins: the client's `tracesSampleRate`, or a sampled flag propagated from another client realm |
| Backend (`http.server`, internal, db, messaging) | Tempo, via the collector | collector tail-sampling policy |
| Backend, additionally | Sentry, if the collector forwards it | an environment attribute on any span in the trace matching a routing policy |

Three consequences drive every diagnosis below:

- **The client's sampled flag and the client's own retention are separate decisions.** The propagated `traceparent` flag tells the backend whether to record; the client's head sampling decides whether the client span is kept. When the flag says record and head sampling drops the client span, the backend records a span whose parent was never stored anywhere — an orphan. This is the normal case at low client sample rates, not an anomaly. The same split happens inside one client with two realms, such as an extension's UI and background: a realm that continues a propagated context as sampled keeps its spans while the originating realm's head sampling drops their parent, so client-side orphans appear in Sentry too.
- **A `-00` (not-sampled) flag can suppress the backend span entirely**, because a parent-respecting sampler delegates to "never record" for an unsampled remote parent. No backend span is created at all — different from one being dropped later.
- **Backend spans reach Sentry only if some span in their trace carries an environment attribute that matches a routing policy.** Tail sampling routes whole traces: one matching span forwards the trace with every service in it. A service that expresses environment under a different attribute name is absent from Sentry only in traces where no other span matches, and is still present in Tempo.

## Setup

Keep organisation slugs, project ids, and hosts in your environment — do not commit them.

```bash
# SENTRY_ORG, SENTRY_PROJECT_ID (numeric), SENTRY_AUTH_TOKEN
# plus the grafana-tempo-queries variables for the Tempo side
```

## Query the Sentry half

```bash
curl -fsS -G "https://sentry.io/api/0/organizations/$SENTRY_ORG/events/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  --data-urlencode "dataset=spans" \
  --data-urlencode "field=span.op" --data-urlencode "field=span_id" \
  --data-urlencode "field=parent_span" --data-urlencode "field=span.description" \
  --data-urlencode "field=timestamp" \
  --data-urlencode "query=trace:$TRACE_ID" \
  --data-urlencode "project=$SENTRY_PROJECT_ID" \
  --data-urlencode "statsPeriod=24h" \
  --data-urlencode "sort=-timestamp"
```

A syntax trap that produces misleading emptiness:

- **Any field you sort on must also be selected.** Sorting by `-timestamp` without requesting `timestamp` returns `400 orderby must also be in the selected columns or groupby` — and a script that swallows errors reports it as no results.

`!has:parent_span` selects root spans in a spans query run through Sentry MCP `search_events`. If a raw `/events/` call rejects the filter, request `parent_span` as a field and filter client-side.

Use `project=-1` to search every project at once when you do not yet know which one should hold the span — that is how you tell "in the wrong project" apart from "absent".

## Procedure — Tempo to Sentry

Use when you have a backend trace and want its client context.

1. Find client-originated backend traces: search your services in Tempo, then keep the results whose `rootServiceName` reports the root was never received. Those reference a client parent that is not in Tempo.
2. **Zero-pad each trace id to 32 characters** before querying Sentry. Tempo search strips leading zeros, and an unpadded id returns nothing for a reason that looks like absence.
3. Query Sentry for `trace:<id>`, first in the client's project, then with `project=-1`.
4. Classify with the table below.

## Procedure — Sentry to Tempo

Use when a Sentry trace looks truncated at the network boundary.

1. Take the trace id from the Sentry trace view.
2. Look for backend spans of that trace in Sentry itself first. If the collector forwards backend spans for that environment, both halves may already be in one place and no cross-store hop is needed. Check presence with an attribute that marks backend spans (a tenant id, for example), not `span.op:http.server`: server spans were 2.9% of backend spans in one measurement, so keying on them can read as none present. Keep `http.server` for the nesting check below.
3. Otherwise fetch the trace from Tempo by id, with a time window that brackets the client span's timestamp.
4. If Tempo has nothing, the backend either never recorded it (a `-00` flag), or its trace fell outside the tail-sampling policy.

## Classification

| What you find | Meaning | Where to look next |
| --- | --- | --- |
| Client and backend spans, backend parented on the client's request span | Healthy join; per-hop latency is attributable | — |
| Client and backend spans, backend parented on an enclosing operation root | Propagation is attaching the wrong parent, so the backend span sits beside its caller instead of beneath it | The client's header-injection path |
| Backend spans only, client parent referenced but nowhere | Orphan: the flag instructed recording, head sampling discarded the client span. Or no client span was active when the request went out, so the SDK sent a parent id from its scope's propagation context that no span carries | Client sample rate, or decoupling the flag from head sampling, or whether a span is active at the call site |
| Client spans only, no backend span anywhere | Either no header was propagated to that host, or the flag was `-00` so the backend never created a span | Propagation targets (`tracePropagationTargets`), then whether `traceparent` is sent at all (`propagateTraceparent`, off by default in the Sentry SDK, since an OpenTelemetry backend does not read Sentry's own `sentry-trace` header), then the flag |
| Backend in Tempo but not in Sentry when it should be | Environment attribute does not match a forwarding policy | The service's environment tagging |
| Nothing in either store | Head-sampled out end to end | Expected at low sample rates |

## Checking whether a backend span nests correctly

Nesting takes the parent identity and the times, not the picture. Take the backend `http.server` span's `parentSpanId` (hex-decode it from Tempo's base64), then look that id up among the client's spans in Sentry:

- Resolves to an `http.client` span whose description matches the same URL, and the backend span starts before that span ended → correctly nested beneath the request that caused it. A backend span that starts after the `http.client` span ended cannot be its child, whatever the id says (one recorded case started 318 seconds after).
- Resolves to a transaction root or custom operation span → the backend span is a sibling of its caller; hop latency cannot be read off the waterfall.
- Resolves to nothing in either store → orphan.

Node services truncate span starts to whole milliseconds, because the OpenTelemetry JS SDK stamps a start from `Date.now()`. A start and an end within the same millisecond do not establish which came first.

## Traps

- **Time windows differ per store.** Tempo retention is typically much shorter than Sentry's, so an older trace legitimately exists in one and not the other. Confirm the window before concluding a half is missing.
- **Window a parent lookup on the parent, not the child.** A parent starts before its child, so a window that opens at the child's start excludes the parent by construction and manufactures a false orphan.
- **Client-observed duration includes time no span records.** An `http.client` span also holds time in any tier that emits no spans, such as a CDN in front of the backend, and time queued for a connection once Chrome's six-connections-per-origin limit is full.
- **Verify credentials on both sides first.** A Grafana token without datasource scope and an out-of-scope Sentry token both present as empty results, which read as "no data" rather than as "not allowed". Confirm each side returns something before concluding a half is missing.
- **A relative time window on a shared link expires.** Pin absolute ranges when the link needs to outlive the incident.
- **One sampling decision can be shared across a long-lived trace id.** If a client reuses a trace id across many operations, the proportion of spans marked sampled will not match the nominal client rate; do not read that ratio as an effective sample rate.
