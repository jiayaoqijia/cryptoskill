---
name: ac-inbound-triage
description: "Routing index for inbound work before it is worked: decide what to do first, what to schedule, what to hand off, and what to drop. Seven leaves: queue-definition (one intake point, scope, service classes, queue versus backlog), triage-axes (urgency, impact, reversibility, effort, dependency, ownership), dispositions (act now, schedule, delegate, drop), severity-escalation (severity matrix, paging threshold, escalation ladder), batching-wip (context-switch cost, protected blocks, batch windows, WIP limits), triage-log (one line per item, review cadence, aging report, median and oldest age), false-urgency (manufactured urgency, deadline provenance, renegotiation, the 24-hour test). Use when asking 'triage my inbox', 'triage this queue', 'what do I do first', 'everything is urgent', 'sort these requests', 'my backlog is out of control'. Not for: planning work already accepted (that is task planning), writing the reply itself, or incident command during an active outage."
license: MIT
metadata:
  domain: collaboration
---

# Inbound Triage

## Overview

Inbound triage decides, for each item waiting for attention, one of four dispositions — act now, schedule, delegate, or drop — and the order in which the rest wait. It decides what gets done and when. It does not do the work, write the reply, or plan work already accepted. The reader is an agent or person facing an inbox, queue, or backlog and needing to sort it before starting.

## When to use

- An inbox, queue, or request list has piled up and the order of attack is unclear.
- Several things are all being called urgent at once.
- A backlog has grown faster than it drains and nothing is getting dropped.
- Requests arrive faster than one person can handle them.

## When NOT to use

Planning work already accepted is outside; that is task planning, not triage. Writing the reply to a request is outside; triage decides the disposition, not the wording. Incident command during an active outage is outside; severity escalation here covers requests and pre-incident severity, not running a live incident.

## Subskill index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/queue-definition.md` | `collaboration/queue-definition` | Define the queue before triaging it: one intake point, in scope versus deflected, service classes with response targets, queue versus backlog |
| `subskills/triage-axes.md` | `collaboration/triage-axes` | The axes that decide order: urgency, impact, reversibility, effort, dependency, ownership; the Eisenhower matrix as a frame |
| `subskills/dispositions.md` | `collaboration/dispositions` | The four dispositions with criteria: act now, schedule, delegate, drop; honest timeboxes and recorded drops |
| `subskills/severity-escalation.md` | `collaboration/severity-escalation` | Severity classes and escalation: matrices for incidents and requests, paging threshold, a ladder of named people |
| `subskills/batching-wip.md` | `collaboration/batching-wip` | Batching by type and honest WIP limits: context-switch cost, protected blocks, batch windows |
| `subskills/triage-log.md` | `collaboration/triage-log` | The log: one line per item, review cadence, the aging report, median and oldest age instead of raw count |
| `subskills/false-urgency.md` | `collaboration/false-urgency` | Defending against manufactured urgency: deadline provenance, the renegotiation script, the 24-hour test, saying no |

## Status and honest limits

- Seedling: assembled from the public canon cited in each leaf; the specific timeboxes and WIP numbers are house thresholds, not measured constants.
- The Eisenhower matrix carries disputed attribution; treat it as a shared frame, not a law.
- Triage is a judgment process, not a formula. The axes and dispositions narrow the decision; they do not make it for you.
- A queue that is never reviewed degrades into a second inbox; the log exists to prevent that, and it only works if someone reads it.

⚠️ Open question: no public study measures which triage axis most predicts bad outcomes in a general inbox; the axis weights below are house defaults, adjustable per context.