---
name: ac-multitenancy-and-isolation
description: "Building systems that serve many customers from one deployment without leaking between them: tenancy models and their cost, data isolation levels from shared rows to separate databases, tenant context propagation and the failure where it is lost, noisy-neighbour effects and fair scheduling, per-tenant quotas and limits, row-level security and its bypass paths, and the written isolation record. It explains the isolation boundary and how it fails; it never gives legal or compliance advice. Use when asking \"multitenancy\", \"tenant isolation\", \"row level security\", \"noisy neighbour\", \"per-tenant rate limit\", \"shared schema versus separate database\", \"tenant context\", \"cross-tenant leak\", \"isolation model\". Not for authentication and authorisation mechanics (ac-security-engineer), not for database schema design and migrations (ac-database-changes), not for privacy obligations on personal data (ac-privacy-engineering)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Multitenancy and isolation

## Overview

Multitenancy is a shared deployment serving separate customers, and every design decision in it is a trade between isolation and cost. Separate databases per tenant give the strongest boundary at the highest cost; shared rows with a tenant column give the lowest cost with a boundary that depends entirely on every query remembering to filter. Both are legitimate, and the failure mode is choosing one without knowing which.

This skill covers that boundary and how it breaks. It covers the tenancy model's cost, the isolation levels and what each actually guarantees, the propagation of tenant context and the paths where it is lost, the noisy-neighbour problem and fair scheduling, per-tenant quotas, row-level security and the ways applications bypass it, and the record that makes the choice explicit. Authentication mechanics and privacy obligations belong to other skills.

Primary sources: <https://csrc.nist.gov/> and <https://owasp.org/>.

## When to use

- When designing or reviewing a multi-tenant system.
- When a cross-tenant leak, or a near-miss, needs investigating.
- When one tenant's load degrades another's service.
- When choosing between shared and separate data stores.

## When NOT to use

- For authentication, sessions, and authorisation mechanics (use ac-security-engineer).
- For schema design and migration execution (use ac-database-changes).
- For privacy obligations and subject requests (use ac-privacy-engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/tenancy-models.md` | `software-engineering/tenancy-models` | Shared rows, shared schema, separate schemas, separate databases, and their costs. |
| `subskills/isolation-levels.md` | `software-engineering/isolation-levels` | What each model actually guarantees, and what it leaves to discipline. |
| `subskills/tenant-context-propagation.md` | `software-engineering/tenant-context-propagation` | Carrying the tenant through every call, and the paths where it is lost. |
| `subskills/noisy-neighbour.md` | `software-engineering/noisy-neighbour` | Shared resource contention, fair scheduling, and the tenant that starves others. |
| `subskills/tenant-quotas-and-limits.md` | `software-engineering/tenant-quotas-and-limits` | Per-tenant rate limits, storage caps, and the response when they are hit. |
| `subskills/row-level-security.md` | `software-engineering/row-level-security` | Policy enforcement in the database, and the application paths that bypass it. |
| `subskills/isolation-record.md` | `software-engineering/isolation-record` | The written record: model, boundary, enforcement point, and test evidence. |

## Status and honest limits

Isolation is only as strong as its weakest enforcement point, and a system can be correctly designed and still leak through a cache, a background job, an analytics replica, or a support tool that queries without a tenant filter. Nothing here guarantees isolation, and a claim of isolation without a test that attempts a cross-tenant read is a claim rather than a finding.
