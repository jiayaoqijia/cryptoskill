---
name: instrument-a-service-with-otel-metrics
description: Use when a service needs observable behaviour in production — adds RED and USE metrics via OpenTelemetry with bounded label cardinality and SLO-sized histogram buckets.
---

# Instrument a service with OpenTelemetry metrics

Instrument the request boundary for RED (Rate, Errors, Duration) and the host for USE (Utilisation, Saturation, Errors). Any series that is on neither a dashboard nor a paging alert is cost without benefit.

## Procedure

1. Pin the SDK version so instrument names are reproducible:
       pip install 'opentelemetry-sdk==1.24.0' 'opentelemetry-exporter-otlp-proto-grpc==1.24.0'
   Check `pip show opentelemetry-sdk` reports exactly that version before writing code.

2. Define counters and histograms once at module import, not per request:
       from opentelemetry import metrics
       meter = metrics.get_meter("checkout")
       reqs = meter.create_counter("http.server.requests")
       dur = meter.create_histogram("http.server.duration.ms", unit="ms",
           explicit_bucket_boundaries_advisory=[10,25,50,100,250,500,1000,2500])

3. Time at the outermost middleware and label with bounded values — route template, method, status class:
       route="/orders/{id}"   # never "/orders/8412"

4. Restrict label keys to `route`, `method`, `status_class`, `service`, `version`. Add a unit test asserting `set(metric.attributes) == ALLOWED` so a stray label is caught in CI.

5. Set histogram buckets from the SLO, not from a tutorial default. If the SLO is p99 < 500 ms, buckets must straddle 500 — `[10,25,50,100,250,500,1000,2500]` does, a seconds-scale default recording milliseconds does not.

6. Export every 15 s over OTLP to the collector sidecar on `localhost:4317` using a batch reader; never export synchronously from the request path.

7. Derive four alert rules from these series: error ratio > 1% for 5 min, p99 > SLO for 10 min, request rate drop > 50% vs 1 h ago, saturation (in-flight / max concurrent) > 0.8.

## Pitfalls

- Labelling with the raw URL path: `/orders/8412` and `/orders/8413` become distinct series, cardinality explodes, and the TSDB OOMs.
- Recording duration in seconds while the metric name and buckets are milliseconds — every observation lands in the last bucket and p99 reads as the bucket ceiling.
- Timing inside the handler instead of around it, so time in deserialisation, TLS and queueing is invisible.
- Using client-side summaries (quantiles computed in-process) instead of histograms; you cannot aggregate quantiles across pods or across time windows.

## Verification

    curl -s localhost:8889/metrics | grep http_server_duration_ms_bucket | head
    curl -s localhost:8889/metrics | grep -c '^http_server_duration_ms_bucket'

Report the boundary that was instrumented, that series count is unchanged after 10k requests (no per-request growth), and that the four alert rules load (`amtool check-config alerts.yml`).
