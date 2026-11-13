---
name: ac-message-queues
description: "The middleware layer that decouples producers from consumers: broker topologies and what a direct, fanout, or topic exchange actually routes, delivery guarantees from at-most-once through to effectively-once, acknowledgement and redelivery when a consumer dies mid-message, poison messages and the dead-letter path, priority and fair dispatch, queue backpressure and bounded buffers, competing consumers and ordering under scale-out, and the written queue record. It explains how a queue behaves and where it fails; it never recommends a broker. Use when asking \"message queue\", \"dead letter queue\", \"poison message\", \"ack and redeliver\", \"competing consumers\", \"fanout exchange\", \"topic routing\", \"work queue\", \"priority queue\", \"why did this message arrive twice\", \"prefetch\". Not for event-driven design between your own services (ac-event-driven-architecture), not for webhook delivery to endpoints you do not own (ac-webhook-and-async-delivery), not for durable workflows and sagas (ac-durable-execution)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Message queues

## Overview

A queue takes a message from a producer who does not want to wait and gives it to a consumer who may not exist yet. That simple contract hides the decisions that decide whether a system works: what the broker promises about delivery, what happens when a consumer accepts and dies, where an unreadable message goes, and who receives the next one when several consumers compete.

This skill covers the middleware mechanics: routing topologies and what each exchange type matches, the delivery-guarantee ladder and the acknowledgement machinery that produces each rung, the poison-message path that stops one bad message from wedging a worker, priority and prefetch and fair dispatch, and the bounded-buffer question of what a queue does when consumers cannot keep up. The architectural choice to use events belongs to another skill; this one is about operating the pipe.

Primary sources: <https://www.rabbitmq.com/tutorials/tutorial-one-python> and <https://kafka.apache.org/documentation/>.

## When to use

- Choosing or reading a broker, exchange, or queue topology.
- Deciding the acknowledgement and redelivery model for a consumer.
- Handling a poison message or designing the dead-letter path.
- Diagnosing duplicate delivery, lost delivery, or wedged workers.
- Sizing prefetch, priority, and competing consumers under load.

## When NOT to use

- For event-driven architecture between your own services (use ac-event-driven-architecture).
- For delivering to endpoints you do not control (use ac-webhook-and-async-delivery).
- For durable workflows and compensation (use ac-durable-execution).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/routing-topologies.md` | `software-engineering/routing-topologies` | Direct, fanout, topic, and headers exchanges, and what each route matches. |
| `subskills/delivery-guarantees.md` | `software-engineering/delivery-guarantees` | The ladder from at-most-once to effectively-once, and its cost at each rung. |
| `subskills/ack-and-redelivery.md` | `software-engineering/ack-and-redelivery` | Acknowledgement windows, the death-during-processing case, and redelivery. |
| `subskills/poison-and-dead-letter.md` | `software-engineering/poison-and-dead-letter` | The unreadable message, retry limits, and the dead-letter path with its reasons. |
| `subskills/priority-and-dispatch.md` | `software-engineering/priority-and-dispatch` | Priority queues, prefetch, and the fairness they quietly decide. |
| `subskills/queue-backpressure.md` | `software-engineering/queue-backpressure` | Bounded buffers, what to reject, and where the excess is allowed to go. |
| `subskills/queue-record.md` | `software-engineering/queue-record` | The written record of guarantees, limits, and inspection points. |

## Status and honest limits

A queue's behaviour is a product of its configuration: identical topologies redeliver differently, drop differently, and order differently across brokers and flags. The guarantees described here are the shape of the machinery, not the settings of any one broker, and each claim must be read against the deployment's own documentation. Nothing here recommends a broker, and no queue makes a consumer idempotent — that obligation lands on the consumer regardless of what the pipe promises.
