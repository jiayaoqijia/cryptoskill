# Database Migration Assistant with Rollback

A PostgreSQL migration assistant that makes schema changes safe and repeatable. It provides plan/apply/rollback workflows with drift detection, and exposes stable CLI tools that AI agents can call. Designed for production safety: preview first, confirm, then execute.

---

## 1. Overview

Database schema changes are continuous in real projects. Common problems include:

- Environments drifting out of sync.
- Manual SQL execution with risky rollback.
- Migration steps scattered across scripts, docs, and tribal knowledge.

This skill provides a repeatable, auditable migration workflow for PostgreSQL. It standardizes versioned SQL files, maintains a migration history table, and exposes predictable CLI tools so AI agents can plan, execute, and explain changes safely.

---

## 2. Goals and Non-Goals

### Goals

- Provide a versioned migration workflow with clear ordering.
- Support safe rollback using down migrations.
- Maintain a history table to track applied changes.
- Offer scriptable CLI tools for planning, applying, and rolling back.
- Enable AI-enhanced behavior: planning, drift detection, and readable diagnostics.

### Non-Goals

- Not a full ORM or replacement for Flyway/Liquibase.
- Not designed for complex business data migrations.
- PostgreSQL-only for now; MySQL/SQLite may be added later.

---

## 3. Directory Structure

Recommended location in this repository:

```text
ai-productivity/
  database/
    database-migration-assistant/
      SKILL.md
      README.md
      scripts/
        migration_utils.py
        plan_migrations.py
        apply_migrations.py
        rollback_migrations.py
        generate_migration.py
      migrations/
        20260208_120000_create_users_table.sql
        20260208_121500_add_index_on_users_email.sql
      examples/
        example.env
        example_usage.md
        demo_agent.py
        demo_prompt.txt
```

---

## 4. Migration File Format

### 4.1 Naming Convention

Each migration is a single `.sql` file:

```text
YYYYMMDD_HHMMSS_description.sql
```

Example:

```text
20260208_120000_create_users_table.sql
20260208_121500_add_index_on_users_email.sql
```

The timestamp orders migrations. The filename (without extension) is the version.

### 4.2 Up/Down Sections

Each file contains both an up section and a down section:

```sql
-- MIGRATION: create_users_table
-- DIRECTION: up
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- DIRECTION: down
DROP TABLE IF EXISTS users;
```

Rules:

1. `-- DIRECTION: up` to the next `-- DIRECTION:` is the up SQL.
2. `-- DIRECTION: down` to end of file is the down SQL.
3. If `down` is missing, the migration is treated as non-reversible.

---

## 5. Migration History Table

The tool maintains a `schema_migrations` table to track executed migrations:

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(64) NOT NULL,
    name TEXT NOT NULL,
    checksum TEXT NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    direction VARCHAR(8) NOT NULL,
    status VARCHAR(16) NOT NULL,
    error_message TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_schema_migrations_version_dir
    ON schema_migrations(version, direction)
    WHERE status = 'success';
```

Field meanings:

- `version` migration version (from filename).
- `name` migration name (from `-- MIGRATION:` or filename).
- `checksum` hash of the SQL contents for drift detection.
- `direction` `up` or `down`.
- `status` `success` or `failed`.
- `error_message` failure details when applicable.

---

## 6. Scripts and Responsibilities

### `migration_utils.py`

Common utilities:

- Read DB connection from `DB_URL`.
- Ensure `schema_migrations` exists.
- Compute checksum.
- List and parse migration files.
- Load applied migrations from database.

Suggested interface:

```python
def get_db_connection() -> psycopg2.extensions.connection: ...
def ensure_schema_table(conn) -> None: ...
def compute_checksum(sql_text: str) -> str: ...
def parse_migration_file(path: Path) -> dict: ...
def list_migration_files(migrations_dir: Path) -> list[Path]: ...
def get_applied_up_migrations(conn) -> list[dict]: ...
```

### `plan_migrations.py`

Produces a migration plan and detects drift.

Inputs:

- `--migrations-dir`

Outputs:

- Applied versions.
- Pending versions.
- Drift report if checksums differ.

### `apply_migrations.py`

Applies pending up migrations in order.

Key behaviors:

- Supports `--dry-run` to preview SQL without executing.
- Wraps each migration in its own transaction.
- Stops on first failure and records the error.

### `rollback_migrations.py`

Rolls back the latest applied migration or down to a target version.

Key behaviors:

- Only rolls back migrations with a `down` section.
- Writes a `direction='down'` record on success.

### `generate_migration.py`

Generates a new migration template:

- Creates a timestamped filename.
- Inserts up/down placeholders.

---

## 7. CLI Usage

### 7.1 Plan Migrations

```bash
python scripts/plan_migrations.py --migrations-dir migrations
```

### 7.2 Dry Run and Apply

```bash
python scripts/apply_migrations.py --migrations-dir migrations --dry-run
python scripts/apply_migrations.py --migrations-dir migrations
```

### 7.3 Rollback Latest Migration

```bash
python scripts/rollback_migrations.py --migrations-dir migrations
```

### 7.4 Generate a New Migration Template

```bash
python scripts/generate_migration.py --migrations-dir migrations --name add_user_status_column
```

---

## 8. Environment and Dependencies

### Environment Variable

```bash
export DB_URL="postgresql://user:password@localhost:5432/mydb"
```

### Python Dependencies

```text
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
```

---

## 9. AI Agent Usage Guidance

Recommended agent behavior:

1. Run `plan` first and summarize the changes.
2. Require explicit user confirmation before `apply` or `rollback`.
3. If drift is detected, stop and warn the user clearly.
4. Explain failures in plain language and suggest fixes.

---

## 10. Safety and Best Practices

1. Migration files are append-only; never edit applied migrations.
2. Always back up production before applying changes.
3. Use dry-run in staging before production.
4. Keep migrations small and reversible.

---

## 11. Limitations and Future Work

Current limitations:

1. PostgreSQL only.
2. Rollback depends on valid `down` sections.
3. No concurrency lock to prevent parallel migration runners.

Possible improvements:

1. Add MySQL/SQLite support.
2. Provide schema diffing and risk scoring.
3. JSON output for easier agent parsing.
4. CI/CD integration for pre-deploy validation.

---

## 12. Demo Expectations (for PR Submission)

When submitting a PR, include screenshots that show:

1. The agent loading this skill.
2. The input prompt.
3. Tool execution steps with parameters.
4. Final response output.

Suggested demo flow (CLI):

1. Set `DB_URL`.
2. Generate a migration template.
3. Run `plan`.
4. Run `apply` with `--dry-run`.
5. Run `apply` (real).
6. Run `rollback`.

Suggested demo flow (Agent):

1. Use `examples/demo_agent.py`.
2. Use the prompt in `examples/demo_prompt.txt`.

Example prompt:

```
Plan migrations for the project and show any drift. If clean, apply them in dry-run mode.
```

---

## 13. Summary

This skill offers a safe, repeatable PostgreSQL migration workflow that an AI agent can reliably operate. It is designed for real-world use with clear planning, safe execution, and rollback support.
