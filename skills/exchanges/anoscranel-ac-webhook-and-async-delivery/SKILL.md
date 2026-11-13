---
name: ac-webhook-and-async-delivery
description: "Delivering events to endpoints you do not control: the delivery contract and retry schedule, at-least-once semantics and consumer deduplication, signature verification and replay windows, ordering when the receiver needs it, endpoint health and automatic disabling, consumer-side idempotency, and the written delivery record. It explains how outbound delivery behaves and how it fails; it never guarantees delivery and never replaces the receiver's own controls. Use when asking \"webhook delivery\", \"webhook retry\", \"webhook signature\", \"replay attack webhook\", \"at least once delivery\", \"webhook ordering\", \"why did my webhook stop\", \"dead letter for webhooks\", \"webhook idempotency\". Not for event schemas between internal services (ac-event-driven-architecture), not for message queue internals (ac-durable-execution), not for general API authentication (ac-security-engineer)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Webhook and async delivery

## Overview

A webhook is an outbound HTTP request to an endpoint the sender does not control, and that asymmetry decides everything. The sender cannot know whether the request arrived, cannot fix the receiver's downtime, and cannot see the receiver's logs. What it can do is define a delivery contract: what is sent, how often it is retried, how the receiver proves the request is genuine, and what happens when the endpoint stays broken.

This skill covers that contract from both sides: the retry schedule and its limits, the at-least-once semantics that follow from retrying, the signature and timestamp that let a receiver reject a forged or replayed request, the ordering problem when events matter in sequence, and the endpoint health checks that stop a dead endpoint from consuming the sender's capacity forever. Internal event schemas and queue internals belong to other skills.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9110> and <https://csrc.nist.gov/>.

## When to use

- When sending or receiving webhooks and the delivery contract is undefined.
- When a receiver reports duplicate or out-of-order events.
- When a webhook endpoint silently stopped receiving events.
- When designing signature verification and replay protection.

## When NOT to use

- For internal event schemas and the outbox pattern (use ac-event-driven-architecture).
- For durable workflow state and sagas (use ac-durable-execution).
- For general API authentication and token design (use ac-security-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/delivery-contract.md` | `software-engineering/delivery-contract` | What is sent, the retry schedule, and the timeouts the sender applies. |
| `subskills/at-least-once-and-dedup.md` | `software-engineering/at-least-once-and-dedup` | Why retries imply duplicates, and the key that makes them harmless. |
| `subskills/signature-and-replay.md` | `software-engineering/signature-and-replay` | Signing over the raw body, timestamp windows, and rejecting replays. |
| `subskills/ordering-guarantees.md` | `software-engineering/ordering-guarantees` | Sequence numbers, out-of-order arrival, and what a receiver must do. |
| `subskills/endpoint-health-and-disabling.md` | `software-engineering/endpoint-health-and-disabling` | Disabling a failing endpoint and the path back to enabled. |
| `subskills/consumer-side-idempotency.md` | `software-engineering/consumer-side-idempotency` | The receiver's obligation, and how it records what it has processed. |
| `subskills/delivery-record.md` | `software-engineering/delivery-record` | The written record: schedule, signature scheme, ordering, and disable policy. |

## Status and honest limits

Delivery cannot be guaranteed over a network the sender does not control, so every webhook system is at-least-once with a bounded retry horizon, and events beyond that horizon are lost unless the receiver can fetch them. Nothing here makes delivery reliable, and a receiver that has not implemented deduplication will process duplicates regardless of what the sender documents.
