---
name: observability
domain: software-engineering/observability
trigger: "\"add tracing\", \"nobody knows why prod behaves like this\", \"set up structured logging\", \"instrument this service\"."
anti_trigger: "Setting an SLO, an error budget or an alert threshold (subskills/slo-reliability.md); running the outage and the postmortem (subskills/incident-response.md); browser-side vitals and render cost; back-end latency budgets and load tests."
scope: "Logs, metrics, traces with OpenTelemetry; what to instrument"
status: "seedling"
---

# Observability

## Standard

- **OpenTelemetry** is the vendor-neutral, CNCF-graduated standard for traces, metrics and logs (https://opentelemetry.io). Instrument to the spec and send by OTLP, and the backend stays an ops choice.
- **Majors (Honeycomb)**: observability is the ability to ask new questions of production without shipping new code (https://www.honeycomb.io/blog/observability-engineering). That needs high-cardinality events, not pre-decided aggregates.
- **RED method** (Rate, Errors, Duration; Tom Wilkie) per request-driven service; **USE** (Utilization, Saturation, Errors; Brendan Gregg) per host.
- **Four golden signals** (SRE Book ch6): latency, traffic, errors, saturation.
- **Correlation** is the test that matters: a log line, a span and a metric all carry the trace id, so a user report becomes a query.

## Decision rules

1. Instrument what a reader will use. A panel nobody opens is waste.
2. Structured JSON logs, one event per line, with level, message, trace id and service.
3. Duration uses percentiles, never averages.
4. Bound attribute cardinality: no user id, no raw path as a metric label.
5. Sample traces by head and tail rules, and keep every trace that carries an error.
6. Tracing earns its keep from the second service onward.
7. Message content capture is opt-in. The GenAI conventions mark `gen_ai.input.messages` and `gen_ai.output.messages` Opt-In.
8. One backend per signal is enough. A second backend is ops cost.

## Procedure

1. List the paths a user complaint would name. Those are the instrumentation targets.
2. Add the SDK and set the endpoint from the environment, not from code:
   ```bash
   OTEL_SERVICE_NAME=orders OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4318
   ```
3. Wrap each inbound request in a span. Propagate trace context on outbound calls.
4. Emit three metrics per endpoint: request count, error count, duration histogram.
5. Replace print statements with structured events that carry the trace id.
6. Set resource attributes: `service.name`, `service.version`, `deployment.environment`.
7. Add one uptime check from outside the system. An internal health check cannot see a dead host.
8. Add error tracking that groups by release, so "did my deploy break it" has an answer.
9. Set retention per signal against its reader count.
10. Verify: force an error in dev, then find it from the dashboard without reading code.
11. Add the cardinality review to the same PR. A new attribute is new cost.

## Anti-patterns

- Averages for latency; dashboards with no reader.
- A trace id in the log that never reaches the span.
- A metric label holding a user id or a raw URL.
- Message bodies captured by default.
- Three backends for one team.
- Instrumenting only the happy path.

## Done checklist

- [ ] Spans cover inbound and outbound calls, with context propagated.
- [ ] RED metrics exist per endpoint, in percentiles.
- [ ] Logs are structured and carry the trace id.
- [ ] An external uptime check runs.
- [ ] Cardinality is bounded and reviewed.
- [ ] A forced dev error is findable from the dashboard.

## Sources

- <https://www.honeycomb.io/blog/observability-engineering>
- <https://clickhouse.com/resources/engineering/red-use-methods>
- <https://eunomia.dev/ebpf-qa/2026-09-17-genai-agent-invoke-agent-chat-execute-tool-sibling-tree/>
- https://opentelemetry.io/docs/concepts/observability-primer/ · https://sre.google/sre-book/monitoring-distributed-systems/
