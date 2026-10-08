---
name: minimise-collected-personal-data
description: Use when a form, schema, or payload collects more personal data than the stated purpose needs. Cut fields at the source and prove the write path rejects the extras.
---

# Minimise collected personal data

Extra fields are liability with no owner. This skill removes data from collection and payloads down to the minimum the stated purpose actually requires.

## Procedure

1. Restate each purpose as an action: "send invoice", "detect fraud". A field that serves no action is a removal candidate.

2. List currently collected fields straight from the request schema:
   `rg -n "required|nullable|maxLength" src/api/schemas/ | head -80`

3. Justify every field against its purpose in one line each. No justification means drop it.

4. Prefer derived-at-use over stored: compute an age band from a date only if a band is not enough, otherwise store the band and not the date.

5. Swap broad identifiers for narrow ones where the purpose allows: store `country` not the full address; store `email_hash` not the raw address for matching.

6. Drop fields that are never populated: `select count(col)::float/count(*) from t` for each column. Usage under 0.01 is a removal candidate once the purpose is confirmed not to need it.

7. Stop the write at the source, not at the display: delete the field from the insert and update statements and from the API contract, then bump the API version.

8. Add a regression test that the field is now rejected: `pytest tests/test_schema.py -k rejects_unknown_field`.

9. Re-run the field inventory and diff the count before and after the change.

## Pitfalls

- Hiding a field in the UI does not stop collection; the form still posts it and the table still stores it.
- "We might need it later" is not a purpose; speculative fields accumulate and widen breach blast radius.
- Removing storage but leaving the field in logs keeps the data; scrub logs in the same change.
- Free-text inputs invite over-collection; cap length and constrain the charset to what the purpose permits.
- A field removed from the API but left nullable in the DB gets repopulated by an old client until the contract version is enforced.

## Verification

    rg -c "ssn|passport_number|mother_maiden" src/ || echo "no over-collected fields remain in src"
    git diff --stat | tail -1

Report the fields removed, the fields kept with their purpose, and any DB column still holding data that must be purged.
