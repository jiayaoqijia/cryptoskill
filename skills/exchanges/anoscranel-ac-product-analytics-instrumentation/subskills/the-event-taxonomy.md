---
name: the-event-taxonomy
domain: software-engineering/the-event-taxonomy
trigger: "Designing or reviewing the event taxonomy as a governed schema."
anti_trigger: "Not for warehouse schema design, and not for reading event data."
scope: "The schema that naming conventions enforce and governance maintains."
status: seedling
---

# The event taxonomy

## Standard

The taxonomy is the schema: the set of events, their properties, their types, and the rules that decide whether a proposed new event belongs in it. Well-designed, it makes queries boring — a question about feature usage resolves to a known event with known properties. Undesigned, every analyst invents a personal dialect, and the same human action appears under three names across platforms.

Governance is what keeps the schema honest. A taxonomy without a review path ossifies — teams stopped adding events because their proposals sat unanswered — or rots — teams add events freely and every quarterly review unearths duplicates. The balance is a lightweight proposal path with response-time expectations, a single owner per event, and a periodic deduplication pass that retires unused events with their last-seen dates recorded.

Primary sources: <https://en.wikipedia.org/wiki/Clickstream> and <https://en.wikipedia.org/wiki/Customer_data_platform>.

## Decision rules

- The taxonomy is written, version-controlled, and queryable — not tribal memory.
- Every event has a named owner and a documented question it exists to answer.
- A proposal path with stated response time keeps additions from going around the schema.
- Periodic deduplication: same-action events merged, unused events retired with dates recorded.
- Cross-platform parity is a first-class reviewed state: web, mobile, and server paths all fire it.
- Breaking taxonomy changes use a new version, never a silent rename.

## Procedure

1. Draft the initial events covering the core user journey, not everything.
2. For each: name, owner, the question it answers, platform-parity list.
3. Adopt the proposal path with response-time expectations.
4. Run a quarterly pass: deduplication, retirement of unused, type audits.
5. Version the taxonomy; breaking changes roll the version.
6. Record the gaps the review finds instead of hiding them.

## Anti-patterns

- Asking teams to name events "intuitively" — every intuition differs.
- Governance so slow that teams route around it.
- No dedup: event_3 emerges beside signup_completed, both alive for years.
- Retiring events with a record of their replacement relation.
- Silently renaming events to clean them up.

## Done checklist

- [ ] Taxonomy written and version-controlled.
- [ ] Every event owned and question-stated.
- [ ] Proposal path with response time adopted.
- [ ] Deduplication pass run with dates recorded.
- [ ] Platform parity reviewed.
- [ ] Gaps recorded, not hidden.

## Sources

- Background on clickstream data and its quality classes: <https://en.wikipedia.org/wiki/Clickstream>
- The data aggregation class into which event streams typically land: <https://en.wikipedia.org/wiki/Customer_data_platform>
- Localization edge all instrumentation must care about: <https://cldr.unicode.org/>
