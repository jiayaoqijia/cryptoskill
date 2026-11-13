---
name: ac-scheduled-jobs
description: "Designing and diagnosing work that runs on a schedule rather than on request: run semantics when a trigger is missed, at-least-once delivery and idempotent job bodies, singleton execution and the lock that prevents overlaps, long-run and overdue jobs, backfill and catch-up after downtime, monitoring liveness versus completion, and the written schedule record. It explains the semantics of time-triggered work; it never recommends a scheduler and never treats silence as success. Use when asking \"cron job\", \"scheduled job\", \"missed run\", \"job overlap\", \"singleton lock\", \"catch up after downtime\", \"backfill schedule\", \"why didn't the 9am job run\", \"job still running\", \"at least once job\". Not for multi-step durable workflows (ac-durable-execution), not for queue delivery to endpoints you don't own (ac-webhook-and-async-delivery), not for CI pipeline scheduling (ac-ci-and-release)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Scheduled jobs

## Overview

A scheduled job is work that starts because the clock says so, not because a user asked. That single difference creates every problem this skill covers: nobody is watching when it runs, the trigger can be missed while the system is down, two instances can fire at once, and a job that silently stops running produces no error at all — only an absence that surfaces weeks later as stale data.

The central design decision is run semantics: when a trigger time is missed, does the job run late, run once, skip, or run twice? The answer must be chosen deliberately rather than inherited from a scheduler's default, because it decides what the system guarantees after every restart, deploy, and outage. The second decision is idempotency: schedule delivery is at-least-once in practice, so the body must tolerate running twice — or running while the previous run is still going.

Primary sources: <https://www.rfc-editor.org/rfc/rfc3339> and <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>.

## When to use

- Designing cron-style jobs and their behaviour on restart, overlap, or downtime.
- Diagnosing jobs that did not run, ran twice, or never stopped running.
- Deciding catch-up semantics after an outage window.
- Building liveness monitoring for time-triggered work.

## When NOT to use

- For multi-step workflows with compensation (use ac-durable-execution).
- For webhook delivery outward (use ac-webhook-and-async-delivery).
- For CI scheduled pipelines (use ac-ci-and-release).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/missed-run-semantics.md` | `software-engineering/missed-run-semantics` | What happens when a trigger time passes while the system is down or busy. |
| `subskills/overlap-and-singleton.md` | `software-engineering/overlap-and-singleton` | The lock that keeps one run at a time, and what happens when it is held. |
| `subskills/idempotent-job-bodies.md` | `software-engineering/idempotent-job-bodies` | Writing a job body that is safe to run twice, in order, at the wrong time. |
| `subskills/long-running-and-overdue.md` | `software-engineering/long-running-and-overdue` | Jobs that outlive their interval, and the queue of missed triggers behind them. |
| `subskills/catchup-and-backfill.md` | `software-engineering/catchup-and-backfill` | What runs after downtime: catch-up policy and bounded replay. |
| `subskills/liveness-monitoring.md` | `software-engineering/liveness-monitoring` | Detecting a job that stopped without erroring — dead-man's-switch design. |
| `subskills/schedule-record.md` | `software-engineering/schedule-record` | The written record: every job, its trigger, semantics, and owner. |

## Status and honest limits

Scheduler behaviour on missed triggers is implementation-specific: some run once, some run every missed instance, some skip — this skill frames the decision but the deployed scheduler's own documentation is the authority on which options exist. Nothing recommends a product, and the hardest failure in this class is invisible: a job removed by mistake produces no alert, only an absence. Every design here assumes that silence is a signal to be monitored, not evidence of health.
