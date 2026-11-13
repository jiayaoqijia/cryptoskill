---
name: ac-domain-modeling
description: "The craft of modeling a business domain in code, domain-driven: building the shared language between domain experts and developers, drawing context boundaries, designing aggregates and their consistency rules, expressing state changes as domain events, isolating persistence behind repository contracts, and evolving the model as understanding deepens. Use when asking \"model this domain\", \"define our bounded contexts\", \"ubiquitous language\", \"aggregate design\", \"domain events\", \"where does this logic belong\", \"model the business rules\". Not for choosing system topology or structure styles (that is ac-architecture), not for schema migrations and storage mechanics (ac-database-changes), not for surveying an existing codebase for candidates (ac-architecture-survey)."
license: MIT
metadata:
  domain: software-engineering
---

# Domain Modeling

## Overview

The craft of modeling a business domain in code, domain-driven: building the shared language between domain experts and developers, drawing context boundaries, designing aggregates and their consistency rules, expressing state changes as domain events, isolating persistence behind repository contracts, and evolving the model as understanding deepens.

## When to use

- Building a shared vocabulary and mental model with domain experts before writing code.
- Drawing context boundaries when different parts of a system use the same terms for different concepts.
- Designing consistency boundaries and invariants inside aggregate roots.
- Capturing state changes as domain events and isolating domain logic from database mechanics.

## When NOT to use

- Choosing overall system topology, microservices versus monoliths, or C4 container views (use ac-architecture).
- Writing database migration scripts, table normalization, or SQL performance tuning (use ac-database-changes).
- Surveying an existing codebase for structural debt or refactoring opportunities (use ac-architecture-survey).

## Subskill index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/ubiquitous-language.md` | software-engineering/ubiquitous-language | Building and maintaining a shared language between domain experts and code |
| `subskills/bounded-contexts.md` | software-engineering/bounded-contexts | Drawing context boundaries and isolating distinct models |
| `subskills/aggregates-and-consistency.md` | software-engineering/aggregates-and-consistency | Designing aggregate roots, consistency boundaries, and invariants |
| `subskills/domain-events.md` | software-engineering/domain-events | Expressing state changes as what happened rather than what to do |
| `subskills/repositories-and-ports.md` | software-engineering/repositories-and-ports | Isolating persistence and side effects from domain logic |
| `subskills/value-objects-and-entities.md` | software-engineering/value-objects-and-entities | Distinguishing identity versus attribute equality and eliminating primitives |
| `subskills/model-evolution.md` | software-engineering/model-evolution | Refactoring toward deeper insight and evolving models over time |

Additional domain modeling consideration ensures robust software architecture boundaries, clear communication channels between engineers and product owners, and long-term maintainability without technical debt accumulation across service boundaries.

Furthermore, maintaining crisp domain models ensures that architectural decisions reflect real business semantics rather than technical constraints, fostering long-term system maintainability and team alignment.

## Status and limits

Status: seedling. Limits: models domain semantics and business rules in code; does not cover physical infrastructure or relational database tuning.
