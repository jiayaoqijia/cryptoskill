---
name: pseudonymise-records-for-analysis
description: Use when analysts need to link records across datasets without seeing identities. Replace direct identifiers with stable tokens and hold the key in a separate store.
---

# Pseudonymise records for analysis

Analysts need linking keys, not identities. This skill replaces direct identifiers with tokens so analysis still works without exposing the person.

## Procedure

1. Split the stores: a `mapping` table holding `(real_id, token)` under tight access, and an `analysis` table holding only tokens and no identity columns.

2. Use a deterministic token when linkage across datasets is required:
   `token = hex(hmac_sha256(key, tenant_id + ":" + real_id))`, with `key` in a secrets manager and never in the analysis store.

3. Use a random token when linkage is not required: `token = uuid4()`. Random tokens deliberately weaken cross-dataset joins.

4. Include the tenant or dataset in the HMAC input so one person gets different tokens per dataset, blocking cross-dataset correlation.

5. Coarsen quasi-identifiers alongside the token: keep `age_band` not `dob`, `region` not postcode. Check that no token group in a released cohort is smaller than k=5.

6. Transform in one pass so intermediates never land:
   `create table analysis_events as select hmac_id(user_id) as token, date_trunc('day', ts) as day, event_type from events;`

7. Define key rotation: re-key annually and keep old mappings only as long as needed to join historical extracts.

8. Verify no direct identifiers slipped through: `rg -n "@|\+?[0-9]{10,}" analysis_dump.csv | head`.

9. Publish only from the analysis store. Analysts must have no query path to the mapping table.

## Pitfalls

- A salt stored next to the data is reversible by anyone with DB access; split the secret across two systems.
- Consistent tokens let an insider link a leaked analysis row back to a named user; the mapping table's access control is the only defence.
- High-cardinality quasi-identifiers (exact timestamps, rare diagnoses) re-identify even with a token in place.
- Pseudonymisation is not anonymisation; the data stays personal and keeps its obligations.
- Hashing emails without a key is brute-forceable against a dictionary of known addresses.

## Verification

    rg -n "@|\b[0-9]{10,}\b" analysis_dump.csv || echo "no direct identifiers found"
    psql "$ANALYSIS_DB" -c "select min(cnt) from (select token, count(*) cnt from analysis_events group by token) s"

Report the token scheme, where the key is held, and the smallest released cohort size.
