---
name: route-container-logs-to-a-collector
description: Use when container logs vanish on restart or are trapped in the node. Configures stdout/stderr plus a log driver or sidecar so lines reach a durable collector with rotation and metadata.
---

# Route Container Logs to a Collector

The node's local json-file log is capped and lost when the pod is deleted; a syslog or a file inside the container is invisible to `kubectl logs`. Logs must go to stdout/stderr and be shipped by the runtime or an agent to a durable store.

## Procedure

1. Write logs to stdout/stderr, never to a file inside the container. A container app that logs to `/var/log/app.log` shows nothing in `docker logs` and nothing in `kubectl logs`.
2. Pick a driver/the path:
   - Docker default `json-file` with rotation: `--log-driver json-file --log-opt max-size=10m --log-opt max-file=5`.
   - Ship directly: `--log-driver fluentd --log-opt fluentd-address=fluentd:24224 --log-opt tag=app`.
   - Kubernetes: use a node-level agent (Fluent Bit DaemonSet) tailing `/var/log/containers/*.log`, plus `kubectl logs` for spot checks.
3. Ensure the app does not buffer forever: set `PYTHONUNBUFFERED=1`, or call `fflush`, so lines appear in real time and are not lost on SIGKILL.
4. Attach metadata the collector can index: pod, namespace, container, and a `request_id`/`trace_id` field. A log line with no correlation id cannot be joined to a trace.
5. Emit structured JSON so a query can filter by field:
   `{"ts":"2026-10-08T12:00:00Z","level":"error","msg":"db timeout","request_id":"a1b2"}`.
6. Cap cardinality of labels sent to the metrics/log backend; a per-request id as a log label (not a field) explodes index size.
7. In Kubernetes, run the Fluent Bit DaemonSet with a `tail` input and a `kubernetes` filter so every line gets `namespace`, `pod`, `container` without app changes.
8. Verify end to end: emit a known line and find it in the collector within the pipeline's flush interval.

## Pitfalls

- Docker's default `json-file` driver has no rotation unless configured; on a chatty app it fills the node's disk and the kubelet evicts pods. Always set `max-size`.
- Writing to a log file inside the container means the data lives in the container's writable layer and dies with the pod; a volume only helps if something tails it.
- Buffered stdout (block-buffered when not a TTY) delays lines and loses the last buffer on SIGKILL — force line buffering.
- Kubernetes does not rotate app logs it did not write; the agent must be running before logs matter (order the DaemonSet early).
- A sidecar logging agent duplicates node-agent shipping and doubles cost; pick one collection path per node.
- Logging full request bodies or headers ships secrets and PII into a broad-access store; redact at the emitter.
- Timestamping client-side in local time makes correlation across nodes wrong; always UTC ISO-8601.

## Verification

    docker run -d --log-opt max-size=10m --log-opt max-file=3 app:x
    docker logs --since 1m x | grep CORRELATION_ID
    kubectl logs <pod> -c app --tail=1    # same line

The emitted line appears via the runtime and in the collector, and the driver config shows a size cap. Report the shipping path and the observed line in the backend.
