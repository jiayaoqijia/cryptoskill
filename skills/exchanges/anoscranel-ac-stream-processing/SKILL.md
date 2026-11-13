---
name: ac-stream-processing
description: "Computing over unbounded data as it arrives: event time versus processing time, watermarks that declare a stream complete, windowing by tumbling, sliding, and session, handling late and out-of-order events, state and its size, aggregation functions over streams, streaming joins, and the written stream record. It explains how correctness is defined when the data has no end; it never recommends a framework and never promises a latency. Use when asking \"stream processing\", \"watermark\", \"event time\", \"processing time\", \"tumbling window\", \"sliding window\", \"session window\", \"late data\", \"out of order events\", \"streaming join\", \"windowed aggregation\", \"why is my stream count wrong\", \"allowed lateness\". Not for event delivery between services and consumer lag (ac-event-driven-architecture), not for market data collection specifically (ac-market-data-collection), not for durable workflows and sagas (ac-durable-execution)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Stream processing

## Overview

A batch has an end; a stream does not, and every mechanism in stream processing exists to answer the one question that makes unbounded computation possible: when is a result complete? The answer is constructed, not given — a watermark declares how far event time has progressed; a window says which events belong together; allowed lateness says how long the door stays open. Get those wrong and a dashboard undercounts forever in a way that no rerun fixes, because the data that would have completed it was discarded.

This skill covers the construction: event time versus processing time and the skew between them, watermarks and their honesty, window types and what each is for, late events and side outputs, state and its growth, aggregation over streams, and streaming joins. Event delivery between services has its own skill; so do market-data pipelines and durable workflows.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://martinfowler.com/>.

## When to use

- When computing aggregates or joins over unbounded data as it arrives.
- When a result must be correct by event time, not by arrival time.
- When late events are expected and must be handled by policy, not by luck.

## When NOT to use

- For event delivery, outbox patterns, and consumer lag (use ac-event-driven-architecture).
- For market data collection pipelines and their watermarks (use ac-market-data-collection).
- For durable workflows, sagas, and compensated processes (use ac-durable-execution).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/event-versus-processing-time.md` | `software-engineering/event-versus-processing-time` | Two clocks, their skew, and which one the answer must be correct in. |
| `subskills/watermarks.md` | `software-engineering/watermarks` | Declaring event time complete, and the honesty of the declaration. |
| `subskills/windowing.md` | `software-engineering/windowing` | Tumbling, sliding, session, and global windows, and what each answers. |
| `subskills/late-and-out-of-order.md` | `software-engineering/late-and-out-of-order` | Late-arrival policy, allowed lateness, and where discarded events go. |
| `subskills/state-and-size.md` | `software-engineering/state-and-size` | What a stream computation must remember, and its growth. |
| `subskills/streaming-joins.md` | `software-engineering/streaming-joins` | Joining unbounded inputs, and the state each join type requires. |
| `subskills/stream-record.md` | `software-engineering/stream-record` | The written record: time semantics, windows, lateness policy, and state bounds. |

## Status and honest limits

A watermark is a guess about the future — it asserts that no event older than X will arrive, and the world violates the assertion at every network hiccup and every clock skew. Correctness in stream processing is therefore always a chosen trade: how late you tolerate versus how long you wait. Nothing here recommends a framework, and a stream design that does not state its lateness policy has not defined what its own numbers mean.
