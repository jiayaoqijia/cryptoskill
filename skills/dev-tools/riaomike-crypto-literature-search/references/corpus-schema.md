# Reproducible Corpus Schema

Use these tables or equivalent machine-readable fields. Do not leave a field implicit when it controls screening, evidence status, or the final conclusion.

## Search question

```text
Research question:
Candidate contribution claims:
Domain/security/model/assumption boundaries:
Date/language/publication-type boundaries:
Available capabilities:
Search budget:
```

## Query log

| Query ID | Date/timezone | Source/index | Exact query | Filters | Results returned/screened | New works | Notes |
|---|---|---|---|---|---:|---:|---|

Distinguish proposed queries from executed queries.

## Work and version records

| Work ID | Normalized title | Authors | Version ID/type | Stable identifier | Date | Inspected? | Relation to other versions | Material differences |
|---|---|---|---|---|---|---|---|---|

## Screening log

| Record/version | Stage | Decision | Criterion/reason | Reviewer/evidence | Date |
|---|---|---|---|---|---|

Stages: discovery, title/abstract, full text, identity verification, claim extraction, closest-work inclusion.

## Claim-evidence table

| Claim ID | Work/version | Source claim | Claim type | Model/assumptions | Parameters | Exact location | Verification status | Limitation |
|---|---|---|---|---|---|---|---|---|

Claim types: definition, theorem, proof/reduction, security, empirical, heuristic, novelty. Keep author claim and reviewer status separate.

## Citation edge log

| From work/version | To work/version | Edge type | Verified in source? | Relevance |
|---|---|---|---|---|

Edge types include cites, extends, corrects, attacks, compares, implements, and supersedes.

## Closest-work matrix

| Work/version | Matching claim IDs | Model/setup | Assumptions | Security notion | Parameter regime | Functionality | Cost model/result | Material difference |
|---|---|---|---|---|---|---|---|---|

## Coverage and stopping record

```text
Sources completed:
Query families completed:
Backward/forward chaining completed:
Stopping rule and evidence:
Inaccessible sources:
Excluded source populations:
Unresolved identity/version conflicts:
Remaining search frontier:
Search cutoff date:
```

## Final evidence statuses

- discovered;
- screened-in or screened-out with reason;
- identity verified;
- version inspected;
- claim verified or supported with limitations;
- unverified or contradicted.

Never collapse these statuses into one “included” flag.

