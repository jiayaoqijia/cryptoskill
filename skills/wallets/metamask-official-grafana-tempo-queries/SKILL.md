---
name: grafana-tempo-queries
description: Query backend traces in Grafana Tempo with TraceQL — find traces by service or span attribute, fetch a trace by id, inspect its span tree, and enumerate tag values. Covers the datasource-proxy access path, the credential-expiry failure that returns empty results indistinguishable from "no data", the negative control that proves a filter actually applied, and the id/kind/base64 decoding quirks in the response. Use when investigating backend latency, checking what the backend recorded for a request, or establishing which infrastructure tiers a trace reaches. Triggers on Tempo, TraceQL, Grafana traces, backend span inspection, "does the backend have this trace", or tracing a request past the API boundary.
maturity: experimental
---

# grafana-tempo-queries

Tempo holds **backend** spans. Client spans from the extension and mobile go to Sentry via the SDK's own transport and never appear here — so a Tempo trace normally starts at an inbound server span, and a missing root is expected rather than broken. Mobile sends no trace context to the backend: its `tracePropagationTargets` name no backend host and it does not set `propagateTraceparent`, so a backend trace for a mobile request shares no trace id with the mobile client's spans. To join the two halves, see `sentry-grafana-correlation`.

## Setup

Everything goes through Grafana's datasource proxy. Authenticate with a service account token. Keep the host, datasource uid, org id, and token in your environment — this repository is public, so never commit them.

```bash
# Set these once per shell, from your own Grafana instance:
#   GRAFANA_HOST   e.g. https://grafana.<your-org-domain>
#   TEMPO_UID      the Tempo datasource uid (see discovery below)
#   GRAFANA_ORG    the numeric org id the datasource belongs to
#   GRAFANA_TOKEN  a service account token, Viewer role, scoped to the Tempo datasource
BASE="$GRAFANA_HOST/api/datasources/proxy/uid/$TEMPO_UID"
AUTH=(-H "Authorization: Bearer $GRAFANA_TOKEN" -H "X-Grafana-Org-Id: $GRAFANA_ORG")
```

Create the token under Administration, Service accounts. A Viewer-role account is
sufficient for every query in this skill, and the token is revocable on its own without
disturbing anything else you have open.

If your Grafana disallows service accounts and there is genuinely no token path, a browser
`grafana_session` cookie works in the same header slot:

```bash
AUTH=(-H "Cookie: grafana_session=$GRAFANA_SESSION" -H "X-Grafana-Org-Id: $GRAFANA_ORG")
```

Reach for that only after confirming a token cannot be issued. A session cookie carries
your whole Grafana authority rather than one datasource's read access, expires on a
schedule you do not control, and cannot be revoked without ending your own session. It is
also indistinguishable from you in an audit log.

Discover the datasource uid rather than guessing it:

```bash
curl -s "$GRAFANA_HOST/api/datasources" "${AUTH[@]}" \
  | node -e 'JSON.parse(require("fs").readFileSync(0)).filter(d=>d.type==="tempo").forEach(d=>console.log(d.uid,d.name))'
```

## Check the instrument before believing a result

**A stale session returns HTTP 401 with an empty body, and a naive parser reports that as zero results** — indistinguishable from "this data does not exist". This is the single most expensive failure mode here: it produces confident negative conclusions about instrumentation coverage.

```bash
# 1. Prove you are authenticated. Do this first, every session.
curl -s -o /dev/null -w 'grafana auth: HTTP %{http_code}\n' "$GRAFANA_HOST/api/user" "${AUTH[@]}"

# 2. Prove the filter is actually being applied, with a query that must match nothing.
curl -s -G "$BASE/api/search" "${AUTH[@]}" \
  --data-urlencode 'q={span.db.system = "not-a-real-db-xyz"}' \
  --data-urlencode "start=$START" --data-urlencode "end=$NOW" \
  | node -e 'const j=JSON.parse(require("fs").readFileSync(0));console.log("control traces:",(j.traces||[]).length,"(must be 0)")'
```

If several different filters all return exactly your `limit`, the filter is not being applied — treat the results as unfiltered until the negative control returns 0.

## Core queries

Every endpoint wants an explicit epoch-seconds window. Omitting it on a by-id lookup makes the request hunt across all blocks and hit a context deadline. A window is not always enough: a by-id lookup of a session-length trace has returned 500 with one.

```bash
NOW=$(date +%s); START=$((NOW-3600))
```

**Search by TraceQL.** Returns trace summaries plus the spans that matched.

```bash
curl -s -G "$BASE/api/search" "${AUTH[@]}" \
  --data-urlencode 'q={resource.service.name="my-service"}' \
  --data-urlencode "start=$START" --data-urlencode "end=$NOW" \
  --data-urlencode "limit=20"
```

**Fetch one trace in full** (OTLP JSON: resource batches → scope spans → spans).

```bash
curl -s "$BASE/api/traces/$TRACE_ID?start=$START&end=$NOW" "${AUTH[@]}"
```

**Enumerate values for a tag** — useful for inventorying what a fleet emits. Expect a `502` on high-cardinality tags; fall back to inspecting individual traces rather than concluding the tag is unused.

```bash
curl -s -G "$BASE/api/v2/search/tag/span.db.system/values" "${AUTH[@]}" \
  --data-urlencode "start=$START" --data-urlencode "end=$NOW"
```

## TraceQL patterns worth knowing

| Goal | Query |
| --- | --- |
| One service | `{resource.service.name="svc-name"}` |
| Several services | `{resource.service.name=~"(svc-a|svc-b)-prd"}` |
| Attribute present at all | `{span.db.system != nil}` |
| Attribute absent, which a `!=` comparison skips | `{span.db.system = nil}` |
| Span kind | `{kind=server}`, `{kind=client}` |
| Slow spans | `{duration > 1s}` |
| **Two conditions anywhere in the same trace** | `{resource.service.name="svc-a"} && {span.db.system != nil}` |

The last one is the important one: `&&` between two brace groups is a **trace-level** conjunction, not a single-span filter. It answers "does a request into this service reach a database at all", which is how you map how deep a trace goes without reading traces one at a time.

## Reading the response

- **Span and trace ids are base64**, not hex. Decode before comparing them to anything from a header or from Sentry: `Buffer.from(id,"base64").toString("hex")`.
- **`kind` is a string** (`SPAN_KIND_SERVER`, `SPAN_KIND_CLIENT`, `SPAN_KIND_INTERNAL`), not the numeric enum. Filtering on `sp.kind === 2` silently matches nothing.
- **Search results drop leading zeros from trace ids.** A 31-character id is a 32-character id with a leading zero; zero-pad before using it anywhere else, or the lookup fails for a reason that looks like absence.
- **`rootServiceName: "<root span not yet received>"`** means the trace's root is not in Tempo. For client-originated requests that is the normal case — the root is a client span living in Sentry — and it is the marker for finding them.
- Resource attributes carry deployment context (`service.name`, kubernetes pod/namespace/cluster, region); span attributes carry the request (`http.*`, `net.*`, `db.*`).

## Deep links for sharing

A link is more useful than a pasted id. Build a Grafana Explore URL with the query pre-filled:

```bash
node -e '
const left={datasource:process.env.TEMPO_UID,
  queries:[{refId:"A",datasource:{type:"tempo",uid:process.env.TEMPO_UID},queryType:"traceql",query:process.argv[1]}],
  range:{from:"now-6h",to:"now"}};
console.log(`${process.env.GRAFANA_HOST}/explore?orgId=${process.env.GRAFANA_ORG}&left=${encodeURIComponent(JSON.stringify(left))}`);
' '<trace-id-or-traceql>'
```

Prefer an absolute `from`/`to` when the link needs to outlive the event; a relative window slides off it and the reader opens an empty result. The Explore state in a link can be dropped across an SSO redirect, so a reader who is not yet signed in can land on an empty Explore.

## Failure modes

| Symptom | Cause | Response |
| --- | --- | --- |
| All queries return 0 | Session expired (401, empty body) | Check `/api/user` first |
| Every filter returns exactly `limit` | Filter not applied | Run the negative control |
| By-id lookup times out | No time window | Pass `start`/`end` |
| Tag-values returns 502 | High cardinality | Inspect traces directly |
| Cloudflare error 1015 instead of JSON | Parallel requests tripped the rate limit in front of Grafana | Send requests one at a time |
| Id from search not found elsewhere | Leading zeros stripped | Zero-pad to 32 chars |
| Kind filter matches nothing | Comparing to a number | Compare to `SPAN_KIND_*` |
| Trace has no root | Root is a client span | Expected; see `sentry-grafana-correlation` |
