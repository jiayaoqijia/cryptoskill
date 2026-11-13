---
name: ac-database-changes
description: "Database schema design and zero-downtime schema change: tables, keys, constraints, normalisation trade-offs, expand-migrate-contract, backfills, renames and drops without locking production. Use when asking \"design the tables\", \"what primary key\", \"normalise this schema\", \"should this be NoSQL\", \"add a column with no downtime\", \"rename this column\", \"backfill a table\", \"the migration locked the database\". Not for the first-pass API resource shapes, retiring a public API, feature removal, or backup-and-restore mechanics; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Database Changes

## Overview

Two leaves cover a data schema across its life: first design (keys, constraints, normalisation, idempotency keys) and every later change to a live schema (expand-migrate-contract, batched backfills, safe drops). Design owns the first cut; migrations own every change after go-live.

## When to use

- Designing tables, keys, constraints, indexes; choosing relational vs document storage.
- Changing a live schema with no downtime: rename, backfill, drop, type change.

## When not to use

- Public API resource or error-shape design — outside this skill.
- Retiring a feature or an API surface wholesale — outside this skill.
- Restoring from backup after data loss — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/data-modeling.md` | Schema design | "design the tables" |
| `subskills/schema-migrations.md` | Zero-downtime schema change | "migrate this column" |

## See also

- `subskills/data-modeling.md` — the first design.
- `subskills/schema-migrations.md` — every change after go-live.
