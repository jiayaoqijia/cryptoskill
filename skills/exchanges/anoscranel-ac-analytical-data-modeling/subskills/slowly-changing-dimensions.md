---
name: slowly-changing-dimensions
domain: software-engineering/slowly-changing-dimensions
trigger: "Keeping history truthful when descriptive data changes."
anti_trigger: "Not for operational schema change, and not for recommending a store."
scope: "Preserving history as descriptive data changes, types one to four."
status: seedling
---

# Slowly changing dimensions

## Standard

Dimension attributes change: a customer moves region, a product is reclassified, a salesperson changes team. The question is what a historical fact should show when queried today, and the answer is a policy, chosen per attribute, not a default. Type 1 overwrites: history is not kept, and old facts appear under the new value. Type 2 adds a new row with its own key and effective dates: history is kept, facts stay attached to the value they had. The choice must be per attribute, because "corrected postcode" and "new sales region" have different truth requirements.

Type 2 is the workhorse and carries the mechanics that break when they are not thought through: the new surrogate key means facts loaded after the change must attach to the new row, the effective-date columns must partition time without gaps or overlaps, and the current-row flags must have exactly one true per natural key at any moment. Types 3 and 4 handle narrower cases — a previous-value column, or a mini-dimension for rapidly changing attributes — and hybrid policies are common:overwrite the typo, version the reclassification.

Primary sources: <https://www.kimballgroup.com/> and <https://martinfowler.com/>.

## Decision rules

- Choose the change policy per attribute, and record why in application terms.
- For type 2, record the effective-date columns and the current-row flag scheme.
- Verify the time slices: no gaps, no overlapping ranges, one current row per natural key.
- Record how late-arriving facts attach: to the row current at the fact's date, not today's.
- Record the behaviour for corrections: is a bad value backdated or superseded forward.
- Record the row-count growth type 2 implies and its storage consequence.

## Procedure

1. List the changing attributes and the reporting requirement for each.
2. Assign a type per attribute, with the reasoning.
3. For type 2, design the date range and current flag columns.
4. Write the late-arriving fact rule.
5. Write the correction rule.
6. Test with a real change mid-period and a report spanning it.

## Anti-patterns

- Type 2 everywhere because it is safest, growing dimensions without limit.
- Type 1 on an attribute that reports compare over time.
- Overlapping effective ranges that attach facts to two rows.
- Late facts joined to today's dimension row, silently rewriting history.
- A change policy that lives in a pipeline's code rather than in the model documentation.

## Done checklist

- [ ] Change policy per attribute with reasoning.
- [ ] Type 2 date columns and flags designed.
- [ ] Time slices verified for gaps and overlaps.
- [ ] Late-arriving fact rule written.
- [ ] Correction rule written.
- [ ] Mid-period change tested.

## Sources

- Dimensional modeling techniques: <https://www.kimballgroup.com/>
- Data modeling patterns: <https://martinfowler.com/>
- Data warehousing references: <https://clickhouse.com/docs/>
