---
name: ac-reliability
description: "Running a service reliably: OpenTelemetry instrumentation with logs, metrics and traces, SLOs and error budgets, burn-rate alerting, backup and DR targets, incident response and blameless postmortems. Use when asking \"add tracing\"\"how do I instrument this service\", \"why is prod slow\",, \"set up structured logging\", \"instrument this service\", \"set an SLO\", \"write the alert rule\", \"error budget\", \"backup and DR plan\", \"prod is down\", \"run the incident\", \"write the postmortem\". Not for rollout mechanics, performance budgets and load tests, or browser-side vitals; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Reliability

## Overview

Three leaves operate a service in production: instrument it so questions have answers, set the reliability target and alerting on it, and run the outage when it comes. Instrument, then target, then respond.

## When to use

- Adding structured logs, metrics or traces to a service; choosing what to instrument.
- Writing an SLI/SLO, an error-budget policy, burn-rate alert rules, RTO/RPO per tier.
- Declaring and running an outage; status communications; the postmortem.

## When not to use

- Canary ramps, rollback mechanics or release staging — outside this skill.
- Latency budgets, profiling, load tests — outside this skill.
- Browser-side Core Web Vitals — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/observability.md` | Logs, metrics, traces | "add tracing" |
| `subskills/slo-reliability.md` | SLOs, error budgets, alerts, DR | "set an SLO" |
| `subskills/incident-response.md` | Run an outage, postmortem | "prod is down" |

## See also

- `subskills/observability.md` — see the system.
- `subskills/slo-reliability.md` — set the bar.
- `subskills/incident-response.md` — hold the bar when it breaks.
