---
name: set-kyc-collection-boundaries
description: Use when deciding how much identity data a product should collect at each tier, where to store it, and when enhanced checks apply, so collection stays justified and auditable.
---

# Set KYC collection boundaries

Collect what the tier requires and nothing more. Over-collection is a liability — it widens the
breach surface and creates data you then have to minimise, delete and answer subject requests
about — and under-collection is a regulatory failure. The boundary is a decision, written down.

## Procedure

1. Define the tiers and the data each one earns, as configuration rather than prose:

       cat > kyc-tiers.yaml <<'YAML'
       tiers:
         tier0: { limits_usd: 0,     collect: [email] }
         tier1: { limits_usd: 1000,  collect: [legal_name, dob, country] }
         tier2: { limits_usd: 50000, collect: [gov_id, selfie, address_proof] }
         edd:   { collect: [source_of_funds, source_of_wealth, beneficial_owners] }
       YAML

2. Bind limits to tiers in code so a tier change is a config diff, not a code path someone
   forgot to update on one endpoint.

3. Use a regulated identity vendor for document capture rather than building OCR and liveness
   yourself. Keep only the vendor's decision and reference id; the document images stay in the
   vendor's system.

       curl -s https://api.idv-vendor.example/v1/verify \
         -H "Authorization: Bearer $IDV_KEY" -d '{"ref":"$CUST"}' | jq '.decision,.reference'

4. Keep identifiable evidence out of general stores. The operational database should hold a
   customer id and a verification reference; the PII lives in the vault with its own access log.

5. Apply enhanced due diligence by trigger, not by feel: a sanctions alert, a high-risk
   jurisdiction, a PEP match, or an unusual source of funds. Each trigger should be a queryable
   field on the record.

6. Retain per the regime that applies, then delete on schedule. Keeping verification documents
   past the retention period is a stored-risk with no benefit.

## Pitfalls

- Storing raw ID scans in S3 with a bucket policy that allows the application role to read them.
  The vendor reference is enough for day-to-day work.
- Collecting a tax id or national number "in case it's useful", which creates a high-value target
  with no tier that requires it.
- Treating one vendor's pass as a permanent KYC. Documents expire, and re-verification cadence is
  part of the programme.
- Letting limits be enforced only at withdrawal; a tier that is not enforced on deposits allows
  the exposure to build before any check runs.
- Building a homegrown sanctions screen on top of the vendor check and calling it KYC complete;
  identity verification and sanctions screening are separate controls.

## Verification

    python3 -c 'import yaml;d=yaml.safe_load(open("kyc-tiers.yaml"));
    print(sorted(d["tiers"])); print("limits bound:", all("limits_usd" in t or t=="edd" for t in d["tiers"]))'

A pass lists every tier with a limit (EDD excepted) and confirms each tier has a bounded
`collect` list.

Report the tier table, the vendor reference kept, the storage location of any document, and the
retention clock. Which tier a customer must reach is a policy and legal judgement that a
qualified compliance lead and counsel decide.
