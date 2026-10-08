---
name: make-a-schema-migration-reversible
description: Use when shipping a database migration — write and actually run the down path so a bad release can roll back without restoring a backup.
---

# Make a schema migration reversible

An irreversible migration turns a rollback into a data-loss event. Write the down path, run it against a real copy, and prove up → down → up is clean before the migration reaches production.

## Procedure

1. Read the tool's reversibility primitives: Alembic `def downgrade()`, Django `RunPython(forward, reverse)`, Rails `def down`, Flyway `U` scripts, golang-migrate `*.down.sql`.
2. Write forward and reverse together. If the forward drops a column the reverse must re-create it, and you must decide explicitly whether data returns:
```python
def upgrade():
    op.add_column("orders", sa.Column("discount_cents", sa.Integer, nullable=True))
def downgrade():
    op.drop_column("orders", "discount_cents")
```
3. For a destructive forward (drop/rename/truncate) the reverse cannot restore data. Snapshot first and reference the dump in the migration docstring:
```
pg_dump -t orders prod > orders_before.sql
```
4. Test on a copy with real volume, not an empty DB:
```
createdb mig_test && pg_restore -d mig_test dump/orders.dump
alembic upgrade head && alembic downgrade -1 && alembic upgrade head
```
5. Assert the schema matches after the round trip:
```
pg_dump -s mig_test > after.sql && diff before_schema.sql after.sql
```
Schema-only diffs must be empty (ignore comment/`\restrict` noise).
6. For data migrations assert counts and a checksum survive the reverse:
```
SELECT count(*), md5(string_agg(id::text, ',' ORDER BY id)) FROM orders;
```
7. Add a CI job that runs `upgrade head && downgrade base` on a seeded DB and fails on error.

## Pitfalls

- A `downgrade()` raising `NotImplementedError` is not reversible; treat it as a release blocker, not a TODO.
- Dropping and re-adding a column loses defaults, indexes and constraints unless the down path recreates them explicitly.
- Running the down path on a DB containing rows the forward would reject (a new NOT NULL column) fails mid-way — test with production-shaped data.
- On older Postgres, `ADD COLUMN ... NOT NULL DEFAULT` rewrites the table under an exclusive lock; add NULL, backfill, then constrain.

## Verification

```
alembic upgrade head && alembic downgrade -1 && alembic upgrade head && echo REVERSIBLE
```
Passes = prints `REVERSIBLE` with no error and the post-round-trip schema diff is empty. Report: "0007_discount round-tripped up/down/up on a 2M-row copy; schema diff empty; down path documented."
