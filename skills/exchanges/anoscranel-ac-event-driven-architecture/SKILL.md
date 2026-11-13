---
name: ac-event-driven-architecture
description: "Designing systems that communicate through events rather than calls: event versus command and what each implies, ordering and partitioning, the exactly-once illusion and idempotent consumers, the transactional outbox, schema evolution of events across producers and consumers, replay and rebuild, and backpressure when consumers fall behind. Use when asking \"event sourcing\", \"CQRS\", \"outbox pattern\", \"exactly once\", \"at least once\", \"consumer lag\", \"event schema versioning\", \"replay the event log\", \"should this be an event or a command\", \"backpressure\". Not for general module and system structure (ac-architecture), not for schema migrations of a database (ac-database-changes), not for API contract design (ac-api-design)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Event-driven architecture

## Overview

An event says that something happened; a command says that something should happen. The distinction looks semantic and is structural: a command has one intended recipient and can be rejected, while an event has many potential consumers and is a fact the producer no longer controls. Systems that blur the two acquire the coupling of synchronous calls with the debugging difficulty of asynchronous ones.

This skill covers the consequences: ordering is a property of the partition rather than the topic, delivery is at-least-once so consumers must be idempotent, the outbox pattern is how a database change and its event stay consistent, schemas evolve on both sides so compatibility is a contract, replay is a feature that requires the log to be the source of truth, and backpressure is what prevents a slow consumer from taking down a producer.

Primary sources: <https://www.enterpriseintegrationpatterns.com/> and <https://www.cncf.io/>.

## When to use

- When deciding whether a message should be an event or a command.
- When ordering, duplication, or consumer lag is a problem.
- When a database write must publish an event atomically.
- When an event schema changes and consumers exist.

## When NOT to use

- For module boundaries and system structure (use ac-architecture).
- For database schema migration mechanics (use ac-database-changes).
- For external API contracts (use ac-api-design).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/events-versus-commands.md` | `software-engineering/events-versus-commands` | A fact versus an instruction, and the coupling each creates. |
| `subskills/ordering-and-partitioning.md` | `software-engineering/ordering-and-partitioning` | Where ordering is guaranteed, and what the partition key decides. |
| `subskills/idempotency-and-delivery.md` | `software-engineering/idempotency-and-delivery` | At-least-once delivery, the exactly-once illusion, and idempotent consumers. |
| `subskills/outbox-and-consistency.md` | `software-engineering/outbox-and-consistency` | Publishing an event atomically with the state change that caused it. |
| `subskills/event-schema-evolution.md` | `software-engineering/event-schema-evolution` | Compatibility across producers and consumers that deploy separately. |
| `subskills/replay-and-rebuild.md` | `software-engineering/replay-and-rebuild` | Replaying the log, rebuilding projections, and the cost of both. |
| `subskills/backpressure-and-lag.md` | `software-engineering/backpressure-and-lag` | Consumer lag, flow control, and the failure a slow consumer creates. |

## Status and honest limits

Broker semantics differ in ways that matter: ordering guarantees, retention, and delivery guarantees are properties of the specific system and its configuration, not of the pattern. Nothing here substitutes for reading the broker's documentation for the settings you use. An event-driven design also concentrates operational risk in the broker and the schema registry, and a design that treats either as infrastructure rather than as part of the contract will be surprised by their failure modes.
