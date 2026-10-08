---
name: inventory-personal-data-flows
description: Use when you must know where personal data lives and moves before a review, DPIA, or deletion project. Build a field-level inventory from schema, code, and vendor config with an owner per hop.
---

# Inventory personal data flows

You cannot minimise, delete, or protect data you have not located. This skill produces a field-level map from system of record to third-party sink, with a named owner on every hop.

## Procedure

1. Freeze the row schema before gathering, in `pii-inventory.csv`: `element,system_of_record,column_or_field,purpose,lawful_basis,retention,recipients,owner`.

2. Enumerate the live schema rather than trusting docs:
   `psql "$DATABASE_URL" -c "select table_name, column_name, data_type from information_schema.columns where table_schema='public' order by 1,2"`

3. Grep for candidate sinks across services:
   `rg -n -i "\b(email|phone|msisdn|ssn|dob|passport|iban|card_number|ip_addr|device_id)\b" -g '!**/test/**' -g '*.py' -g '*.ts'`

4. Walk each hit to its call site and record the destination: own DB, log handler, analytics SDK, error tracker, message topic, outbound HTTP.

5. For every outbound destination capture vendor, region, and the exact field list sent: `rg -n "requests\.(post|put)|axios\.|fetch\(" src/` then read the payload construction.

6. Add every backup, replica, dump file, and CSV export. These are systems of record too and are routinely omitted.

7. Mark each row with a lawful basis: consent, contract, legal obligation, vital interest, public task, legitimate interest. A row with no basis is a finding.

8. Assign a named team per hop. "platform" is not an owner; a person or a team inbox is.

9. Report coverage: tables holding PII versus columns classified, and list every candidate column left unclassified.

## Pitfalls

- Free text and JSONB hide PII; grep never finds `metadata->>'contact'`, so sample rows with `select metadata from users limit 5`.
- Derived copies (search index, cache, warehouse) vanish from inventories built only from the primary DB.
- Test fixtures carry real production data far more often than anyone admits; check `**/fixtures/**` and `seed.sql`.
- An SDK's default auto-capture can send fields to a vendor dashboard you never provisioned.
- Treating `user_id` as non-personal because it is a number is wrong wherever it joins to an identity.

## Verification

    python3 - <<'PY'
    import csv
    rows = list(csv.DictReader(open('pii-inventory.csv')))
    assert rows, "empty inventory"
    assert all(r['owner'] and r['lawful_basis'] for r in rows), "unowned or unbased rows"
    print(len(rows), "elements across", len({r['system_of_record'] for r in rows}), "systems")
    PY

Report the element count, the systems covered, and every column that could not be classified.
