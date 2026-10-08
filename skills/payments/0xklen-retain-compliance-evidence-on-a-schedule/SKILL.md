---
name: retain-compliance-evidence-on-a-schedule
description: Use when setting how long screening results, alerts, decisions and travel-rule records are kept, and how they are stored so an examiner can verify them years later.
---

# Retain compliance evidence on a schedule

The record is the control. A screen that happened but cannot be evidenced is treated as a screen
that did not happen, so retention is designed around reconstructing a decision, not around
archiving files.

## Procedure

1. Classify each record type and attach a retention period with its source:

       cat > retention.csv <<'CSV'
       record_type,period_years,basis,format
       sanctions_screen_result,5,BSA 31 CFR 1010.430(a),json
       travel_rule_payload,5,BSA/FATF R.16,encrypted_json
       kyc_verification_ref,5,AMLD5 as applied,pdf_ref_only
       alert_disposition,5,internal policy,json
       CSV

2. Store records immutably. Use object-lock in compliance mode with a retention-until date, so a
   compromised application identity cannot rewrite history.

       aws s3api put-object --bucket compliance-archive --key "$ID" --body "$ID.json" \
         --object-lock-mode COMPLIANCE --object-lock-retain-until-date "2031-01-01T00:00:00Z"

3. Write a hash chain: each record's digest includes the previous record's digest, so a gap or an
   edit is detectable without trusting the store.

       python3 -c 'import hashlib,json;s=open("prev.json","rb").read();
       print(hashlib.sha256(s+open("rec.json","rb").read()).hexdigest())'

4. Keep the queryable index separate from the evidence blob. The index is small and lets you
   answer "what did we do on date X", while the blob holds the full payload under lock.

5. Encrypt payloads and keep the key outside the archive account. Retention without key custody
   is only an availability plan.

6. Test the retrieval path on a timer, not on the first examination. Pull a record from two years
   back and confirm it decrypts and validates against its hash.

## Pitfalls

- Retaining decision metadata but not the input. Without the list digest and the screened subject,
  the decision cannot be re-evaluated.
- Letting retention run past the period because deletion is manual. Legal hold is the exception;
  the default should be automated expiry.
- Storing person-level data in the immutable archive beyond its period, which converts a records
  programme into a data-protection problem.
- Assuming a backup is an archive. Backups rotate; the archive must be addressable by record id
  for the whole period.
- Skipping the hash chain, then discovering during an examination that no one can show the record
  was not altered.

## Verification

    python3 -c 'import csv;r=list(csv.DictReader(open("retention.csv")));
    print(len(r),"types"); assert all(x["basis"] for x in r); print("all basis-cited")'
    aws s3api get-object-retention --bucket compliance-archive --key sample.json | jq -r '.Retention.Mode'

A pass shows every record type cites a retention basis and the archive returns `COMPLIANCE` mode
for a sampled object.

Report the record types, periods and bases, the archive location, the last successful retrieval
test, and any keys without an expiry. Final decisions about retention periods and holds belong to
a qualified compliance officer and counsel.
