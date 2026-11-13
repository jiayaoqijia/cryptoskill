---
name: ac-production-debugging
description: "Diagnosing failures in systems you cannot attach a debugger to: reading a stack trace and symbolizing it, getting usable core dumps and debug symbols from production, the heisenbug and why observation changes behaviour, correlation and trace IDs to follow one request across services, log-based hypothesis testing when you cannot reproduce locally, postmortem evidence collection before it expires. It explains how to read production state as evidence; it never recommends a tool and never guesses a cause without a test. Use when asking \"production debugging\", \"stack trace\", \"symbolize\", \"core dump\", \"heisenbug\", \"correlation id\", \"why can't I reproduce this in dev\", \"debug in production\", \"evidence before restart\". Not for the scientific method and local reproduction (ac-debugging), not for observability instrumentation and SLOs (ac-reliability), not for incident command and communications (ac-reliability)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Production debugging

## Overview

A production failure arrives with constraints a local defect does not have: you cannot stop the process, you may have one stack trace and a fragment of logs, the evidence expires when the process restarts, and the act of observing can change what you observe. The skill is reading that state as evidence — extracting what the trace actually says, getting symbols for a binary stripped for production, and forming hypotheses you can test against logs rather than breakpoints you cannot set.

The boundary with general debugging is the debugger. The scientific method — reproduce, hypothesise, minimise — still governs everything here; what changes is that reproduction happens against recorded state, not a live process, and the first move is to preserve evidence before a restart destroys it.

## When to use

- A crash, hang, or wrong result visible only in production.
- A stack trace from an unfamiliar component needs reading and symbolizing.
- A failure cannot be reproduced locally and the only evidence is logs and traces.
- Evidence must be captured before the process restarts or scrolls away.

## When NOT to use

- For a reproducible local defect (use ac-debugging).
- For metrics, tracing instrumentation, and SLOs (use ac-reliability).
- For running the incident and communicating status (use ac-reliability).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/reading-stack-traces.md` | `software-engineering/reading-stack-traces` | What a trace actually says: frames, inlining, async frames, and the top of the stack. |
| `subskills/symbols-and-coredumps.md` | `software-engineering/symbols-and-coredumps` | Debug symbols, stripped binaries, and getting a core dump that can be opened. |
| `subskills/heisenbugs-and-observation.md` | `software-engineering/heisenbugs-and-observation` | Why attaching tools changes timing, and what that does to evidence. |
| `subskills/correlation-across-services.md` | `software-engineering/correlation-across-services` | Correlation and trace IDs: following one request through a system that fans out. |
| `subskills/log-hypothesis-testing.md` | `software-engineering/log-hypothesis-testing` | Testing a hypothesis against logs when you cannot break into the process. |
| `subskills/evidence-preservation.md` | `software-engineering/evidence-preservation` | Capturing state before a restart: dumps, thread lists, heap histograms, and configuration. |
| `subskills/production-debug-record.md` | `software-engineering/production-debug-record` | The written debug record: symptom, evidence, hypothesis, test, outcome. |

## Status and honest limits

Production evidence is circumstantial: a stack trace shows where a process died, not why it was there, and a log line is a claim by the code that wrote it. Every conclusion drawn here is provisional until reproduced or explained. Nothing recommends a specific tool, and in many real episodes the honest result is that the evidence was insufficient and the fix must wait for better instrumentation — which is itself a finding worth recording.
