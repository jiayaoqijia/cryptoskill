---
name: metrics-definition-layer
domain: software-engineering/metrics-definition-layer
trigger: "Giving each number exactly one definition and one owner."
anti_trigger: "Not for recommendation, and not for a specific tool choice."
scope: "One definition per metric, and the drift that follows from many."
status: seedling
---

# Metrics definition layer

## Standard

Active users, churn rate, average order value: each is a business concept that must become a computation before it can be displayed. When the computation lives in each report and each dashboard, the same word drifts into two numbers — different filters, different windows, different exclusions — and trust in all of them falls. A metrics definition layer is one shared definition, a single expression over the model, with versions and ownership, that every surface consumes.

The mechanics that keep it honest are mundane. The definition names its inputs and its filters and its time grain explicitly; it is versioned, so a change is visible and dated, rather than a silent edit that rewrites history; and it has an owner who answers for the definition, not merely for the code. A defined metric is close to a leaf in this pack in miniature, except that its consumers are queries rather than readers.

Primary sources: <https://www.kimballgroup.com/> and <https://martinfowler.com/>.

## Decision rules

- Record one definition per metric, including inputs, filters, time grain, and exclusions.
- Record the metric's owner and its review cadence.
- Version the definition, and date every change.
- Record which surfaces consume it, and check them when the definition changes.
- Record metrics that intentionally differ — such as two churn definitions — as separate names.
- Reject metric names that differ only by implementation detail.

## Procedure

1. List the recurring metrics and search for divergent implementations of the same name.
2. Write the canonical definition with inputs and filters.
3. Name an owner per metric.
4. Register the version, and date the change log.
5. Route every surface to the shared definition.
6. Review the definitions at a fixed cadence, and on every modeling change.

## Anti-patterns

- Three dashboards, three active-user numbers.
- A definition edited in place, silently rewriting history.
- Verification by eyeballing two dashboards, never by counting rows.
- An unowned metric everyone consumes and nobody maintains.
- A single change reshipped to five surfaces, amended at four.

## Done checklist

- [ ] One written definition per metric.
- [ ] Owner per metric named.
- [ ] Versioning with dated changes.
- [ ] Consumers enumerated.
- [ ] Same-name divergence surfaced.
- [ ] Review cadence set.

The layer's consumers decide its shape more than its authors do: a definition that can only be evaluated inside one query engine is a definition three teams will reimplement rather than adopt. Favor definitions expressible over the shared model itself — filters, grains, and arithmetic — so that the implementation travels wherever the model does.

## Sources

- Metrics definition techniques: <https://www.kimballgroup.com/>
- Data modeling resources: <https://martinfowler.com/>
- Data warehousing references: <https://clickhouse.com/docs/>
