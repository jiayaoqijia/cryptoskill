---
name: database-migration-assistant
description: PostgreSQL migration assistant that plans, applies, and rolls back schema changes with drift detection for safe AI-agent execution.
author: Apple <skelitalynn@gmail.com>
version: 1.0.0
tags:
  - database
  - postgres
  - migration
  - rollback
  - schema
  - productivity
  - ai
triggers:
  - type: keyword
    keywords:
      - migration
      - database migration
      - schema migration
      - rollback
      - drift
      - postgres
      - schema change
parameters:
  - name: action
    type: string
    required: false
    description: Operation to perform (plan/apply/rollback/generate).
  - name: migrations_dir
    type: string
    required: false
    default: migrations
    description: Directory that contains versioned SQL migration files.
  - name: dry_run
    type: boolean
    required: false
    default: false
    description: If true, show planned SQL without executing it.
  - name: to_version
    type: string
    required: false
    description: Target version for apply or rollback.
  - name: name
    type: string
    required: false
    description: Migration name when generating a template.
prerequisites:
  env_vars:
    - DB_URL
  skills: []
composable: true
persist_state: true
scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: plan_migrations
      description: Build a migration plan and detect drift.
      type: python
      file: plan_migrations.py
      timeout: 30
    - name: apply_migrations
      description: Apply pending up migrations (supports dry-run).
      type: python
      file: apply_migrations.py
      timeout: 60
    - name: rollback_migrations
      description: Roll back the latest migration or down to a target version.
      type: python
      file: rollback_migrations.py
      timeout: 60
    - name: generate_migration
      description: Generate a new migration SQL template.
      type: python
      file: generate_migration.py
      timeout: 30
---

# Database Migration Assistant with Rollback

A PostgreSQL migration assistant that makes schema changes safe and repeatable.  
It provides plan/apply/rollback workflows with drift detection, and exposes stable CLI tools for AI agents to call.  
Designed for production safety: preview first, confirm, then execute.


## Quick Start

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="db_migration_agent",
    skill_paths=["./ai-productivity"],
    scripts_enabled=True
)

result = await agent.run("Plan database migrations for this project")
print(result)

```

## Scripts

| Script | Purpose |
|--------|---------|
| [plan_migrations.py](scripts/plan_migrations.py) | Build a migration plan and detect drift |
| [apply_migrations.py](scripts/apply_migrations.py) | Apply pending up migrations (supports dry-run) |
| [rollback_migrations.py](scripts/rollback_migrations.py) | Roll back the latest migration or to a target version |
| [generate_migration.py](scripts/generate_migration.py) | Generate a new migration SQL template |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DB_URL` | Yes | PostgreSQL connection string, e.g. postgresql://user:pass@host:5432/db |

## Best Practices

1. Always run `plan` and review the output before `apply`.
2. In production, require explicit confirmation and a recent backup.
3. Treat migration files as append-only; never edit applied migrations.
