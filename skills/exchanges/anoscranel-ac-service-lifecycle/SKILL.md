---
name: ac-service-lifecycle
description: "The start-to-stop life of a long-running service: startup ordering and readiness versus liveness, configuration load and validation before traffic, graceful shutdown and connection draining, in-flight work at termination, health endpoints and their levels, dependency startup order and circuit-breaking into unavailable dependencies, and the written lifecycle record. It explains how a service comes up and goes down correctly; it never recommends a runtime or orchestrator and never promises an availability. Use when asking \"readiness versus liveness\", \"graceful shutdown\", \"connection draining\", \"health check\", \"startup ordering\", \"SIGTERM handling\", \"warmup\", \"why do requests fail during deploys\", \"why does the service start but crash after\". Not for CI pipeline wiring and deployment strategy (ac-ci-and-release), not for resilience budgets around steady-state calls (ac-resilience-budgets), not for container and runtime configuration (ac-performance)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Service lifecycle

## Overview

A service spends its life starting, serving, and stopping — and two of those three are where correctness is lost. A service that starts before its dependencies are ready accepts traffic it cannot serve; a service that stops without draining abandons requests mid-flight. The steady state in between is what most engineering attention covers, but the edges are what actually page people at night.

This skill covers the edges. Startup covers the ordering of dependency checks and the difference between being alive and being ready to serve. Shutdown covers signal handling, the drain sequence, and what happens to work in progress. Health endpoints cover what each check should and should not verify. The deployment story — pipelines and rollouts — is a different skill; so are steady-state resilience and container tuning.

Primary sources: <https://sre.google/> and <https://martinfowler.com/>.

## When to use

- When a service starts slowly, crashes after startup, or serves errors during warmup.
- When deploys drop in-flight requests or connections pile up at shutdown.
- When health endpoints flap or say healthy while the service cannot serve.
- When a service depends on others that may not be up when it starts.

## When NOT to use

- For pipelines, release strategy, and rollout mechanics (use ac-ci-and-release).
- For timeouts, retries, and circuit breakers around steady-state calls (use ac-resilience-budgets).
- For container CPU and memory tuning (use ac-performance).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/startup-and-readiness.md` | `software-engineering/startup-and-readiness` | Startup ordering, readiness versus liveness, and refusing traffic until able. |
| `subskills/configuration-load.md` | `software-engineering/configuration-load` | Loading and validating configuration before accepting work. |
| `subskills/graceful-shutdown.md` | `software-engineering/graceful-shutdown` | Signal handling, drain sequences, and deadline-driven termination. |
| `subskills/in-flight-work.md` | `software-engineering/in-flight-work` | Requests, jobs, and transactions that are running when termination arrives. |
| `subskills/health-endpoints.md` | `software-engineering/health-endpoints` | Liveness, readiness, and what each check should actually verify. |
| `subskills/dependency-ordering.md` | `software-engineering/dependency-ordering` | Starting against dependencies that are slow, absent, or flapping. |
| `subskills/lifecycle-record.md` | `software-engineering/lifecycle-record` | The written record: startup steps, drain plan, deadlines, and health semantics. |

## Status and honest limits

Lifecycle behaviour depends on the runtime and orchestrator, which differ in signal delivery, timeout defaults, and kill semantics; the mechanics here are portable, the defaults are not. Nothing here recommends a runtime, and a shutdown plan that has never been tested under production load is a plan that will be discovered to be wrong during the first incident it was written for.
