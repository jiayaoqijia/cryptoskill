---
name: propagate-trace-context-across-services
description: Use when a request spans several services and logs cannot be joined — propagates W3C traceparent headers through every hop, including async queues, so one trace_id reconstructs the call.
---

# Propagate trace context across services

Metrics say what, logs say where, but only a linked trace says which hop caused it. Propagate the W3C `traceparent` header through every synchronous and asynchronous hop; a single broken hop splits one request into two unrelated traces.

## Procedure

1. Use the W3C format, not a bespoke header:
       traceparent: 00-<32-hex trace-id>-<16-hex span-id>-01
   `00` is the version and the last field is trace flags (`01` = sampled).

2. Extract inbound context at the edge and start a server span; never mint a new trace id when one is present:
       ctx := otel.GetTextMapPropagator().Extract(r.Context(), propagation.HeaderCarrier(r.Header))

3. Inject on every outbound call:
       otel.GetTextMapPropagator().Inject(ctx, propagation.HeaderCarrier(req.Header))

4. For async queues, put `traceparent` in the message headers, not the body, and resume it in the consumer:
       # producer
       headers["traceparent"] = format_traceparent(span.get_span_context())
       # consumer
       ctx = extract(headers)
       with tracer.start_as_current_span("consume", context=ctx): ...

5. Across a fan-out, create one span per message *linked* to the producer's batch span rather than parented to it, so the fan-out stays visible without a fake serial chain.

6. Sample consistently at the edge (`parentbased_traceidratio`, e.g. 0.01) and pass the decision downstream in the trace flags. Independent per-service sampling breaks the trace.

7. Configure the collector to keep tail-based samples of all error traces regardless of the head rate — you want the 1% of failures, not 1% of everything.

## Pitfalls

- Starting a fresh trace in each service: you get N orphan traces and cannot follow the chain. This is the single most common instrumentation bug.
- Sampling independently per service, so a downstream service drops the context and the trace ends mid-path.
- Putting `traceparent` in the message body, where serializers mangle it and consumers never read it.
- Clock skew between hosts, so a child span appears to start before its parent; use propagated timestamps rather than local ones when rendering the waterfall.

## Verification

    curl -sf -H 'traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' localhost:8080/orders/1
    grep -c '4bf92f3577b34da6a3ce929d0e0e4736' <(kubectl logs -l app-a,app-b,app-c --tail=1000)

Report: the header format used, the services confirmed under one trace id (A→B→queue→C), and the edge sampling rate plus tail-based keep policy.
