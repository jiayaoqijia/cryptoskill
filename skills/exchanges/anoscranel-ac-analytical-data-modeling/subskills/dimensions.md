---
name: dimensions
domain: software-engineering/dimensions
trigger: "Designing the descriptive context that facts are sliced by."
anti_trigger: "Not for operational schema, and not for reporting the result."
scope: "Descriptive context, keys, and the flat-versus-snowflaked choice."
status: seedling
---

# Dimensions

## Standard

A dimension row is the descriptive context of a fact: the product, the customer, the calendar date, the store. Its job is to be grouped, filtered, and labelled, and its design test is whether every question about context can be written as a straightforward join and a filter. A dimension carries its own surrogate key, its descriptive attributes, and, for large dimensions, hierarchies expressed as columns the query can roll up along.

The key decision is the surrogate key. Natural business keys — product codes, customer numbers — change, get reused, and arrive from source systems with errors, so the dimension owns a meaningless key that the fact references, and the natural key becomes an attribute. The second decision is what to do when a row's attributes change, which is the slowly-changing-dimension question and has its own treatment.

Primary sources: <https://www.kimballgroup.com/> and <https://martinfowler.com/>.

## Decision rules

- Give every dimension a surrogate key, and record the natural key as an attribute.
- Record the source of each attribute and who owns its definition.
- Record the hierarchies present as columns, and verify they roll up without a bridge.
- Flag conformed dimensions shared between facts, and hold their definition centrally.
- Record the expected row count and growth, particularly for unbounded dimensions like dates.
- Keep attributes atomic and describable, not encoded values that need a lookup to read.

## Procedure

1. List the descriptive attributes and their sources.
2. Choose the surrogate key scheme.
3. Mark each hierarchy and its levels as columns.
4. Mark every dimension that will be shared across facts as conformed.
5. Validate attribute values against their definitions with a profile pass.
6. Record row counts and expected growth.

## Anti-patterns

- A fact joined on a natural business key that changes or is reused.
- Encoded attributes readable only with a manual.
- A shared customer dimension defined differently in two facts.
- Hierarchies resolved in the query rather than in the model.
- A monster dimension of unrelated attributes serving every fact in the warehouse.

## Done checklist

- [ ] Surrogate keys chosen.
- [ ] Attribute sources and owners recorded.
- [ ] Hierarchy columns marked.
- [ ] Conformed dimensions flagged and centralized.
- [ ] Attributes profiled against definitions.
- [ ] Row counts and growth recorded.

A practical habit keeps a dimension honest: when an attribute's meaning is disputed, write the two candidate definitions on one page and name the reports each would change. Most disputes end immediately, because the parties discover they are describing different facts rather than disagreeing about one, and the attribute splits into two instead of being argued into a compromise that serves neither.

## Sources

- Dimensional modeling techniques: <https://www.kimballgroup.com/>
- Analytical modeling patterns: <https://martinfowler.com/>
- Data modeling references: <https://clickhouse.com/docs/>
