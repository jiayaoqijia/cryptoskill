---
name: ac-api-design
description: "Public API contracts, their first shape and their evolution: REST, GraphQL or gRPC style choice, resource and error models, RFC 9457 problem details, pagination, idempotency keys, OpenAPI specs, breaking-change judgement, versioning schemes, Deprecation and Sunset headers. Use when asking \"design this endpoint\", \"REST or GraphQL or gRPC\", \"what should the error response look like\", \"add pagination\", \"make this POST safe to retry\", \"write the OpenAPI spec\", \"is this a breaking change\", \"do we need v2\", \"add a Sunset header\", \"deprecate this endpoint\". Not for internal module boundaries or retiring a whole feature or system; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# API Design

## Overview

Two leaves cover the public contract: its first shape — style, resources, error model, pagination, idempotency, the OpenAPI spec — and its evolution — breaking-change rules, version schemes, deprecation signals and sunset. Design the contract, then keep old clients safe while it changes.

## When to use

- Designing an endpoint, picking REST, GraphQL or gRPC, writing the spec.
- Error shapes, status codes, pagination, retry-safe mutations.
- Judging whether a change breaks clients; diff gates on the spec.
- Version schemes, Deprecation and Sunset headers, migration guides.

## When not to use

- Internal module or code boundaries — outside this skill.
- Retiring a whole feature or system — outside this skill.
- Library version-number policy — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/api-design.md` | New public contract | "design this endpoint" |
| `subskills/api-versioning.md` | Change a live contract | "is this a breaking change" |

## See also

- `subskills/api-design.md` — the first contract.
- `subskills/api-versioning.md` — every contract after it.
