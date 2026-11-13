---
name: ac-handoff
description: "Handoff craft for a general agent: writing a handoff a stranger can resume on one read, and resuming one safely. Seven leaves: handoff-artifact (state capsule done / doing / next, decisions, open questions, pointers; SBAR and I-PASS), context-selection (what to pass and leave; outcomes over transcripts; the handoff tax), constraints-verbatim (copy constraints verbatim; binding-state check after compression), resumption-check (verify before acting, reconcile drift, ask versus assume), session-handoff (checkpoint file is the state; continue the same session), person-handoff (shift reports, on-call handover, acknowledgment closes the loop), quality-bar (one-read acceptance test, completeness checklist, anti-patterns). Use when asking 'write a handoff', 'hand this off', 'so someone else can pick this up', 'shift handover', 'resume from this handoff', 'what should I pass on'. Not for: user-facing documentation (use ac-technical-writing), status reports (use ac-business-writing), or note-taking and inbox capture."
license: MIT
metadata:
  domain: collaboration
---

# Handoff

## Overview

The craft of transferring work between people, sessions, and agents. Two halves: writing a handoff a stranger can resume on one read, and resuming one safely; verify the state before acting on it. The reader is an agent or engineer about to hand work over or pick handed-off work up, not a documentation tool.

## When to use

- Ending a session, shift, or task with work unfinished and someone else will continue it.
- Picking up handed-off work and needing to resume without re-reading a transcript.
- Incidents and on-call transitions: state must survive a change of person.
- Switching between models or agents mid-task.

## When NOT to use

User-facing documentation is outside: it serves readers across months, not one receiver across one resumption. Routine status reports with no work transfer are outside; a status update is not a handoff. Personal note capture is outside; handoffs transfer state to a different actor. Sharing context inside one continuous conversation needs no artifact.

## Subskill index

| Leaf | domain segment | scope (one line) |
|---|---|---|
| `subskills/handoff-artifact.md` | `collaboration/handoff-artifact` | What a handoff document contains: state capsule (done / doing / next), decisions with rationale, open questions, artifact pointers; SBAR and I-PASS anchors; the one-read test |
| `subskills/context-selection.md` | `collaboration/context-selection` | What to pass and what to leave: relevance filter, outcomes over transcripts, size budgets; the handoff tax and how it reverses with direction |
| `subskills/constraints-verbatim.md` | `collaboration/constraints-verbatim` | Never summarize constraints: copy must / must-not / may rules verbatim and run a binding-state check after any compression |
| `subskills/resumption-check.md` | `collaboration/resumption-check` | Consumer side: verify state before acting, reconcile drift, confirm freshness, ask versus assume; never act on a stale handoff |
| `subskills/session-handoff.md` | `collaboration/session-handoff` | Agent and session handoffs: the checkpoint file is the state; continue the same session where possible; partial-file continuation; the running ledger |
| `subskills/person-handoff.md` | `collaboration/person-handoff` | Colleague, shift, and incident handoffs: shift reports, on-call transition, acknowledgment closes the loop, escalation notes |
| `subskills/quality-bar.md` | `collaboration/quality-bar` | The acceptance test: a stranger resumes on one read; completeness checklist; living-handoff update protocol; anti-patterns |

## Status and honest limits

- Seedling: built from the public canon cited in each leaf; the one-read test has not yet been measured across many real handoffs.
- The two arXiv papers cited are recent (2026) and not yet widely replicated; use their numbers as evidence of mechanism, not as universal constants.
- The craft favors written handoffs. A fast verbal handoff degrades to the same rules under less time.

⚠️ Open question: no public study yet measures one-read resumption error rates for document-style handoffs; the one-read test is a house acceptance test derived from clinical read-back practice.
