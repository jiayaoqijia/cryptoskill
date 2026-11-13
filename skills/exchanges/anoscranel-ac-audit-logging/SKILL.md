---
name: ac-audit-logging
description: "Building logs that serve as evidence rather than telemetry: what events an audit trail must record and who its reader is, tamper-evidence through hash chaining and external anchoring, append-only storage and the deletion problem, query patterns for investigators, retention and privacy tension with the trail's purpose, structured event schema for auditability, and the written audit record. It explains how to make a log that can be trusted after the fact; it never recommends a log product and never claims tamper-proof, only tamper-evident. Use when asking \"audit log\", \"tamper evident\", \"hash chain log\", \"append only log\", \"who changed this record\", \"immutable log\", \"audit trail design\", \"compliance evidence\", \"log integrity\", \"sequence number gap\". Not for observability and SLO telemetry (ac-reliability), not for structured logging in general (ac-reliability), not for access control decisions themselves (ac-security-engineer)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Audit logging

## Overview

An audit log is a different object from a telemetry log. Telemetry answers "how is the system behaving"; an audit trail answers "who did what, when, and what was the state before" — and its reader is not an engineer at a dashboard but an investigator, an auditor, or a court, months later, possibly hostile to the system's operators. Everything about its design follows from that reader.

The central property is integrity: a trail that can be edited after the fact is not evidence, and the honest engineering term is tamper-evident, not tamper-proof. Hash chaining makes local edits detectable; anchoring the chain's head somewhere the system cannot reach makes even a full rewrite visible. The second property is completeness — the absence of an expected event is itself a finding, which means sequence gaps must be visible rather than smoothed over.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/92/final> and <https://www.rfc-editor.org/rfc/rfc6962.html>.

## When to use

- When a system must answer who changed what, and when.
- When a compliance or regulatory regime requires evidence-grade records.
- When log integrity must survive a compromised host.
- When designing what an investigator can query, years later.

## When NOT to use

- For operational telemetry and SLO metrics (use ac-reliability).
- For application logging in general (use ac-reliability).
- For authorization and access-control rules (use ac-security-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-to-record.md` | `software-engineering/what-to-record` | The event set, the actor identity problem, and the before-and-after state. |
| `subskills/hash-chaining-and-anchoring.md` | `software-engineering/hash-chaining-and-anchoring` | Chain each entry to its predecessor and anchor the head off-host. |
| `subskills/append-only-storage.md` | `software-engineering/append-only-storage` | Write-once storage, the deletion problem, and who can rotate. |
| `subskills/sequence-and-gaps.md` | `software-engineering/sequence-and-gaps` | Sequence numbers, visible gaps, and the silence they can indicate. |
| `subskills/investigator-queries.md` | `software-engineering/investigator-queries` | Answering who-changed-what-when without a forensic project. |
| `subskills/retention-and-privacy.md` | `software-engineering/retention-and-privacy` | Retention law, personal data in the trail, and redaction without rewriting. |
| `subskills/audit-record.md` | `software-engineering/audit-record` | The written audit record: event set, chain, storage, and verification. |

## Status and honest limits

Audit trails are governed by rules that vary by jurisdiction and regime, and this skill designs the engineering object, not the compliance opinion — whether a given trail satisfies a given regulation is a question for the accountable officer. The integrity mechanisms here detect alteration; they do not prevent a sufficiently privileged attacker from stopping the logger entirely, which is why the record treats silence as a signal, not an absence of news.
