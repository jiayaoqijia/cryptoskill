---
name: ac-data-contracts
description: "Treating a data feed as an interface with obligations: schema and semantics in a contract, freshness and completeness guarantees, schema evolution and the compatibility rules that decide who breaks, ownership and escalation, quality checks at the boundary, and the written contract record. It explains how to specify a dataset's guarantees; it never certifies a dataset's correctness and never replaces profiling. Use when asking \"data contract\", \"schema registry\", \"data freshness\", \"completeness SLA\", \"data quality checks\", \"who owns this pipeline\", \"breaking schema change\", \"data model change\", \"upstream data changed\". Not for database schema migrations (ac-database-changes), not for event schema evolution between services (ac-event-driven-architecture), not for evaluating an external vendor dataset (ac-alternative-data)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Data contracts

## Overview

A dataset that other teams depend on is an interface, and interfaces need terms. Without them, a producer changes a column and a downstream pipeline breaks silently; a feed arrives six hours late and a dashboard shows yesterday's number as today's; a table that used to be complete for every region stops covering one, and nobody notices until a report is questioned in a meeting.

A data contract states those terms explicitly: the schema and the meaning of each field, the freshness and completeness the producer commits to, the compatibility rules for change, the owner who is accountable, and the checks that verify the commitment. This skill covers how to write and enforce that. Schema migration mechanics and event schema evolution belong to other skills.

Primary sources: <https://csrc.nist.gov/> and <https://www.w3.org/>.

## When to use

- When a dataset has consumers outside the team that produces it.
- When a schema change needs to be communicated before it breaks something.
- When freshness or completeness is assumed rather than agreed.
- When a data quality incident needs a boundary to point at.

## When NOT to use

- For database migration mechanics (use ac-database-changes).
- For event schema evolution in a messaging system (use ac-event-driven-architecture).
- For evaluating an external dataset's provenance (use ac-alternative-data).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/contract-schema-and-semantics.md` | `software-engineering/contract-schema-and-semantics` | Types plus meaning: units, nullability, and what a field is not. |
| `subskills/freshness-and-completeness.md` | `software-engineering/freshness-and-completeness` | Delivery time, coverage, and the guarantees a producer can keep. |
| `subskills/schema-evolution-rules.md` | `software-engineering/schema-evolution-rules` | Additive versus breaking, and who bears the migration. |
| `subskills/ownership-and-escalation.md` | `software-engineering/ownership-and-escalation` | Who is accountable, and what happens when the contract is breached. |
| `subskills/quality-checks-at-the-boundary.md` | `software-engineering/quality-checks-at-the-boundary` | Validating on ingest rather than discovering defects downstream. |
| `subskills/contract-enforcement.md` | `software-engineering/contract-enforcement` | Making the contract executable rather than documentary. |
| `subskills/data-contract-record.md` | `software-engineering/data-contract-record` | The written record: terms, owner, checks, and version. |

## Status and honest limits

A contract is only as good as its enforcement, and a document that nobody validates is a description rather than a contract. Freshness and completeness guarantees are promises about a pipeline's behaviour, and a producer that cannot measure its own lag cannot honour a stated limit. Nothing here certifies that a dataset is correct, and a passing check confirms the properties it tests rather than the absence of other defects.
