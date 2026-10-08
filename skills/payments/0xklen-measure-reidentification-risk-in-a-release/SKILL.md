---
name: measure-reidentification-risk-in-a-release
description: Use when releasing a dataset that is meant to be anonymous and uniqueness could still identify people. Compute k-anonymity on the quasi-identifiers and generalise until the release is defensible.
---

# Measure reidentification risk in a release

A dataset that looks anonymous can still be unique. This skill estimates uniqueness over the quasi-identifiers and coarsens until the release is defensible.

## Procedure

1. Enumerate the quasi-identifiers in the release: age, sex, postcode, job, dates, and any rare attributes.

2. Compute k-anonymity by grouping on the quasi-identifier set and finding the smallest group:
   ```sql
   select min(cnt) from (
     select age, sex, left(postcode,3) pc, count(*) cnt
     from rel group by 1,2,3) s;
   ```

3. Target k >= 5 for a public release and k >= 3 for tightly controlled sharing. Anything below needs generalisation of the smallest groups.

4. Generalise the highest-cardinality identifiers: exact age to five-year bands, full postcode to sector, day to month.

5. Recompute after each change and document the trade between utility and risk.

6. Check uniqueness against external data. A rare combination appearing once is re-identifiable at k >= 5 if a public register maps it.

7. Watch duration and relative-time attacks: birth date plus an event date can recover a direct identifier.

8. Consider differential privacy for aggregate releases, adding calibrated noise and publishing the privacy budget (epsilon).

9. Write the release statement: quasi-identifiers present, k achieved, and the external-data check performed.

## Pitfalls

- Removing names is not anonymisation; uniqueness in the quasi-identifiers re-identifies the row.
- k-anonymity ignores homogeneity and background knowledge; a same-valued group still discloses its sensitive attribute.
- Small cells in a cross-tab (counts of one or two) leak; suppress or generalise them.
- Free-text and comments are quasi-identifiers and cannot be bucketed; remove or manually review them.
- Over-coarsening destroys utility and pushes analysts back to the raw store, defeating the release.

## Verification

    psql "$REL_DB" -c "select min(cnt) from (select q1,q2,left(q3,3) q3,count(*) cnt from rel group by 1,2,3) s"   # must be >= k target

Report the k achieved, the quasi-identifiers generalised, the external-data check, and any residual unique row.
