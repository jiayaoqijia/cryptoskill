---
name: ac-durable-execution
description: "Running long-lived work that must survive restarts: workflow state and durable checkpoints, sagas and compensating actions, exactly-once effects through idempotency, activity timeouts and heartbeats, versioning a workflow that is already running, human-in-the-loop waits, and the written workflow record. It explains how to make a process resumable and how that fails; it never recommends a workflow engine and never guarantees completion. Use when asking \"durable execution\", \"workflow engine\", \"saga pattern\", \"compensating transaction\", \"distributed transaction\", \"long running process\", \"resume after crash\", \"workflow versioning\", \"human approval step\", \"temporal workflow\". Not for event messaging and outbox patterns (ac-event-driven-architecture), not for queue delivery semantics alone (ac-webhook-and-async-delivery), not for CI pipeline orchestration (ac-ci-and-release)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Durable execution

## Overview

A process that runs for minutes, days, or months cannot hold its state in memory, because a restart erases it. Durable execution makes the state explicit: each step records its outcome durably, the workflow can resume from the last recorded point, and the process becomes a sequence of recoverable transitions rather than a running function.

This skill covers that structure: how checkpoints and replay produce resumability, how a saga uses compensating actions instead of a distributed transaction, how idempotency keys make effects safe to repeat, how activities fail and how heartbeats detect a dead worker, how a workflow is versioned while instances are running, and how a human approval step waits without holding a resource. Messaging and delivery semantics belong to other skills.

Primary sources: <https://www.enterpriseintegrationpatterns.com/> and <https://aws.amazon.com/builders-library/>.

## When to use

- When a process must survive a restart or a deploy.
- When a multi-step operation needs to undo partial work on failure.
- When a workflow must be changed while instances are mid-flight.
- When a step requires human approval or an external callback.

## When NOT to use

- For event-driven messaging and the outbox pattern (use ac-event-driven-architecture).
- For webhook delivery guarantees alone (use ac-webhook-and-async-delivery).
- For CI pipeline orchestration and deployment (use ac-ci-and-release).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/workflow-state-and-checkpoints.md` | `software-engineering/workflow-state-and-checkpoints` | Durable state, replay, and what makes a resume correct. |
| `subskills/sagas-and-compensation.md` | `software-engineering/sagas-and-compensation` | Compensating actions, ordering, and the fact that compensation is not rollback. |
| `subskills/idempotent-activities.md` | `software-engineering/idempotent-activities` | Keys, deduplication, and making a repeated effect safe. |
| `subskills/activity-timeouts-and-heartbeats.md` | `software-engineering/activity-timeouts-and-heartbeats` | Detecting a stuck step and retrying it without duplication. |
| `subskills/workflow-versioning.md` | `software-engineering/workflow-versioning` | Changing a definition while instances are running. |
| `subskills/human-in-the-loop.md` | `software-engineering/human-in-the-loop` | Waiting for approval without holding a worker or a transaction. |
| `subskills/workflow-record.md` | `software-engineering/workflow-record` | The written record: states, compensations, timeouts, and versioning policy. |

## Status and honest limits

Durable execution shifts complexity rather than removing it: the state is explicit, but the versioning and the compensation design become the hard parts. Compensation is a business decision about what undoing means, not an inverse operation, and some effects cannot be compensated at all — a sent email, an executed trade, a deleted record. Nothing here guarantees completion, and a workflow whose compensations have never been run in a test has compensations of unknown behaviour.
