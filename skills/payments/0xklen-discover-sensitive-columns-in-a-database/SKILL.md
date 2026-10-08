---
name: discover-sensitive-columns-in-a-database
description: Use when you need to know which database columns hold personal data before classification or protection work. Find them by name, by sampled value, and by JSON key.
---

# Discover sensitive columns in a database

You cannot classify what you have not found. This skill finds PII columns by name and by the shapes of the values inside them, then labels each one.

## Procedure

1. Pull the full column list with comments:
   `psql "$DB" -c "select table_name, column_name, data_type, col_description(('public.'||table_name)::regclass, ordinal_position) from information_schema.columns where table_schema='public'"`

2. Match names against a growing taxonomy: email, phone, name, address, dob, ssn, national_id, iban, card, ip, geo, device, cookie.

3. For unmatched columns, sample the values and test against the same taxonomy:
   ```sql
   select count(*) from t where col ~ '^[^@]+@[^@]+\.[^@]+$';
   ```

4. Check JSON and JSONB columns by key: `select distinct jsonb_object_keys(metadata) from t limit 50`, then recurse into nested objects.

5. Check free-text columns for embedded identifiers using tight patterns, capping the scan with `limit` to bound cost.

6. Record findings in a data dictionary: `table.column, category, sensitivity, owner`.

7. Mark encrypted or hashed columns distinctly from raw PII so downstream tools treat them correctly.

8. Run it monthly as a job and diff the new columns; schema drift adds PII silently.

9. Feed the labels into tooling: a masking view or query-time policy keyed on the dictionary.

## Pitfalls

- A column named `ref` or `data` holds PII as often as one named `email`; scan the data, not only the names.
- Sampling misses rare formats; combine name matching with a value profile rather than either alone.
- Encrypted columns look like random strings and pass every regex; record them as encrypted, not absent.
- Views and materialised views duplicate tables and are routinely missed.
- A foreign key into a PII table propagates sensitivity; a bare `user_id` in a public table is a link, not neutral.

## Verification

    psql "$DB" -f discover_sensitive.sql | tee sensitive-columns.txt && test -s sensitive-columns.txt

Report the columns found by name, by sampled value, and by JSON key, plus every column needing manual review.
