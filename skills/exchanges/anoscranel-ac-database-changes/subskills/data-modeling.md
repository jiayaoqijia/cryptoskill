---
name: data-modeling
domain: software-engineering/data-modeling
trigger: "\"design the tables\", \"what should the primary key be\", \"should this be NoSQL\", \"normalise this schema\"."
anti_trigger: "Changing a live schema (subskills/schema-migrations.md); public API resource and error shape; internal module boundaries."
scope: "Schema design, keys, constraints, normalisation trade-offs"
status: "seedling"
---

# Data Modeling

## Standard

- **The axis is access patterns, not hype**: schema-on-write versus schema-on-read. A relational store enforces structure at write time and catches bad data at insertion; a document store enforces later, in application code, and pays for a new query pattern with a new table.
- **Constraints are the backbone**: unique prevents duplicate processing, foreign keys hold referential integrity, NOT NULL and check hold domain rules. Integrity sits closest to the data.
- **Keys**: a surrogate key is stable and opaque; a natural key is readable but changes with the world.
- **Normalisation** removes update anomalies; denormalisation buys a read. Denormalise only for a measured pattern, with the update path written down.

## Decision rules

1. Start relational. A single Postgres instance serves millions of rows, so "NoSQL because it scales" is premature. ⚠️ Vendor capacity figures are single-sourced.
2. Every mutable write crosses a layer where a constraint and a validation both run.
3. A retried mutation carries a durable, client-derived idempotency key with a uniqueness constraint. A key generated in memory turns a safe retry into a duplicate.
4. Name things in one tense: plural tables, singular columns, timestamps ending in `_at`.
5. Nullable means "unknown is a real state". If a value is required, add NOT NULL.
6. Money is an integer of minor units or a numeric type, never a float.
7. Prefer a status column to a hard delete. A real delete needs a recorded reason and a backup.
8. Denormalised fields need a named owner and one write path.
9. A hard-to-reverse schema choice gets a record (out of scope for this leaf: the record format).

## Procedure

1. Write the entities and the questions the data must answer.
2. Draw the relationships and pick each key.
3. Mark each column: type, nullability, default, constraint.
4. Draft the DDL:
   ```sql
   CREATE TABLE orders (
     id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
     customer_id bigint NOT NULL REFERENCES customers(id),
     status      text   NOT NULL CHECK (status IN ('open','paid','shipped')),
     total_minor bigint NOT NULL CHECK (total_minor >= 0)
   );
   CREATE UNIQUE INDEX ON orders (idempotency_key);
   ```
5. Add an index for every query you can name now.
6. Test the constraints with rows that must be rejected.
7. Route reads and writes through one tested data layer.
8. Record the schema review: what changed, what coexists, what the rollback is.
9. Commit the schema as a versioned migration (subskills/schema-migrations.md).
10. Prove the restore path before the first production write.

## Anti-patterns

- A natural key on a field the business edits.
- A nullable column that means three different things.
- A denormalised total updated in two places.
- A float money column.
- Validation only in the application, so one importer corrupts data silently.
- An index nobody queried.

## Done checklist

- [ ] Every table has a key, constraints and a named owner.
- [ ] Nullability decided per column.
- [ ] Idempotency key with a unique constraint per retried mutation.
- [ ] Queries that need an index have one.
- [ ] Restore path proven before production writes.
- [ ] Hard-to-reverse choices recorded.

## Sources

- <https://vetoralabs.com/system-design/concepts/trade-offs/sql-vs-nosql>
- https://www.postgresql.org/docs/current/ddl-constraints.html
