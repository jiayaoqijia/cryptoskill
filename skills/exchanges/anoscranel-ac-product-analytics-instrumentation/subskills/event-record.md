---
name: event-record
domain: software-engineering/event-record
trigger: "Writing the record of instrumentation state, changes, and known loss."
anti_trigger: "Not for reading analytics data, and not for warehouse schema."
scope: "The written record: taxonomy version, known gaps, taxonomy-change log."
status: seedling
---

# Event record

## Standard

The event record is the instrumentation state document: the taxonomy version in production, the platform parity table, the known loss classes, the identity and session policies, and the dated change log. It exists so that a number can be read honestly — every count from the stream comes with the question "which taxonomy version, which platforms, which loss classes were known at that date" — and so that the moment instrumentation is found broken, the record says since when.

The change log section carries the history: version bumps, renames, retired events, the date they left, the discovery date of each loss class. The record is append-only like every record leaf in this pack; a taxonomy change is an amendment with a date and a migration note, never a silent rewrite of the plan.

Primary sources: <https://en.wikipedia.org/wiki/Clickstream> and <https://osf.io/prereg/>.

## Decision rules

- The record states the current taxonomy version and the platform parity table.
- The identity and session policies are recorded with their adoption dates.
- Each known loss class carries a discovery date and a size estimate class (not guess-timate).
- Taxonomy changes are dated amendments with migration notes.
- Breaking-usage events (dead columns, false joins) traced back through the record at review time.
- The record names the plan owner and the next review date.

## Procedure

1. Record the taxonomy version, parity table, identity and session policies.
2. Add each known loss class with its discovery date and size class.
3. Amend with dated entries on every taxonomy change.
4. Record engine scopes (retired events, renamed events) with their last-seen date.
5. Note broken-usage events discovered at the review.
6. Re-read the record before any reporting pass so its caveats reach the report.

## Anti-patterns

- Reporting numbers with no taxonomy version attached.
- Loss classes discovered but never recorded.
- Renames recorded but no migration note.
- The record rewritten on each release instead of amendment.
- No next-review date so nobody ever looks.

## Done checklist

- [ ] Version and parity table recorded.
- [ ] Identity and session policies dated.
- [ ] Loss classes with discovery dates and magnitudes.
- [ ] Taxonomy changes as dated amendments.
- [ ] Retired events carry last-seen dates.
- [ ] Next review date written.

The record also settles disputes over count discrepancies: when two dashboards disagree, the first question is which taxonomy version and which loss accounting each query assumed, and the record answers it without archaeology.

## Sources

- Event stream data quality classes: <https://en.wikipedia.org/wiki/Clickstream>
- Pre-registered specifications: <https://osf.io/prereg/>
- Object and relation model in the analysis layer: <https://en.wikipedia.org/wiki/Customer_data_platform>
