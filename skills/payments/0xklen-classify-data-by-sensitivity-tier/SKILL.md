---
name: classify-data-by-sensitivity-tier
description: Use when access, export, and encryption rules need a label to key on and none exists. Assign each data category a small, enforceable tier set and the controls each tier requires.
---

# Classify data by sensitivity tier

Every access, export, and encryption rule needs a tier to key on. This skill assigns each category a tier and the concrete controls that tier mandates.

## Procedure

1. Define three or four tiers with concrete meanings: Public, Internal, Confidential (PII), Restricted (special-category, financial, or health). Never more tiers than you can enforce.

2. Assign categories: product catalogue = Public; internal metrics = Internal; name, email, address = Confidential; health, biometrics, precise geolocation = Restricted.

3. Attach controls per tier: who may read, whether it may leave the region, minimum encryption, logging requirement, retention class.

4. Tag the data at the source with a column comment, asset tag, or catalogue entry keyed to `table.column`.

5. Enforce by policy, not by comment: row-level security, masking views, or IAM conditions on the tag.

6. Set export rules: Restricted data must not reach local laptops or third-party tools; block it with DLP or remove the export path.

7. Define breach impact per tier so triage can prioritise: a Restricted breach is a notification candidate, an Internal one is not.

8. Review the mapping with the data owner at least yearly and on every schema change.

9. Publish a one-page tier-to-control mapping so engineers apply it without asking.

## Pitfalls

- Too many tiers collapse into "everything is Confidential"; keep the set small and enforceable.
- Classification living only in a spreadsheet drifts from reality; tie it to the catalogue and the schema.
- Aggregation escalates tier; a large enough list of Internal rows becomes Restricted when it can profile people.
- Derived data inherits the highest tier of its inputs; a summary of health data is still health data.
- Tiers without an enforcement point are documentation, not a control.

## Verification

    psql "$DB" -c "select distinct sec_tier, count(*) from classified_assets group by 1 order by 1"

Report the tier counts, any untiered asset, and the controls actually enforced per tier today.
