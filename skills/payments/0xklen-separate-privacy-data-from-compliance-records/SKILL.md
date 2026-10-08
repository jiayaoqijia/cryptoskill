---
name: separate-privacy-data-from-compliance-records
description: Use when a compliance obligation and a privacy obligation pull in opposite directions, and you must keep the screening record intact without letting identifiable data sprawl across systems.
---

# Separate privacy data from compliance records

Anti-money-laundering rules say keep the evidence; data-protection rules say minimise, purpose-
limit and delete. The reconciliation is architectural: one narrow, lawful compliance record and a
deliberately small footprint everywhere else.

## Procedure

1. Name the lawful basis per processing activity before writing code. Sanctions screening and
   record-keeping typically rest on a legal obligation, whereas marketing analytics rests on
   consent — and a record kept on the wrong basis is unlawful however useful it is.

```
       cat > ropa.csv <<'CSV'
       activity,basis,purpose,retention
       sanctions_screen,legal_obligation,AML,5y
       kyc_verify,legal_obligation,AML,5y
       product_analytics,consent,growth,13m
       CSV
```

2. Keep the compliance record to what the obligation requires. For a screen that is: subject
   identifier, list digest, timestamp, result, reviewer. Not the customer's whole file.

3. Split the stores. The AML record lives in a restricted archive with its own access log; the
   product, analytics and marketing systems must not be able to read it and must not duplicate it.

       grep -rn "kyc_\|sanctions_" services/*/config.yaml | grep -v "aml-archive"

   Every hit outside the archive service is a leak path to close.

4. Support subject requests with a defined carve-out. Where a legal obligation requires retention,
   the response says the record is retained for that purpose; it does not disclose a suspicious-
   activity report.

5. Delete on the day the period ends, automatically. A retention policy with manual deletion is a
   policy with no deletion.

6. Log access to the compliance store. Who read a record and why is part of the control, and it is
   also how you show a breach did or did not reach the vault.

## Pitfalls

- Copying the KYC result into the CRM "so support can see it", which doubles the exposure and
  creates a store with none of the archive's controls.
- Writing full statutory records into application logs. Logs get shipped, indexed and copied; the
  purpose limitation does not survive the pipeline.
- Deleting a screening record when a customer closes their account, which destroys the obligation
  the regime imposes.
- Treating the record of an AML decision as the customer's to receive. Some of it is protected,
  and the carve-out is jurisdiction-specific.
- Assuming minimisation means deletion everywhere. Compliance retention is itself an exception,
  and both rules have to be written down per activity.

## Verification

    python3 -c 'import csv;r=list(csv.DictReader(open("ropa.csv")));
    assert all(x["basis"] and x["retention"] for x in r); print(len(r),"activities mapped")'
    grep -rl "kyc_blob\|gov_id_image" services/ | grep -v aml-archive || echo "no stray copies"

A pass maps every activity to a basis and retention and finds no PII copy outside the archive.

Report the processing map, the stores holding identifiable data, the retention clocks, and any
stray copies found. Which basis applies and how a subject request is answered are legal
determinations for a qualified privacy officer and counsel.
