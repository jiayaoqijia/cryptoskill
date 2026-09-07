# Cryptography Literature Search Protocol

This example protocol defines evidence requirements without binding the skill to a specific search vendor.

## 1. Question decomposition

Represent the target as a conjunction of searchable dimensions:

```text
primitive/problem + property/security notion + model/setup + assumption/family
+ parameter regime + efficiency/novelty dimension
```

Search dimensions independently before requiring the full conjunction; otherwise early terminology differences cause false negatives.

## 2. Discovery log

For every search batch record:

| Date | Source/index | Exact query | Filters | Results screened | Included | Notes |
|---|---|---|---|---:|---:|---|

Use broad discovery sources and field-specific repositories when available. Lack of one database must be visible in the coverage statement.

## 3. Version-aware identity

Create one work record with linked versions:

| Work ID | Version type | Identifier | Date | Inspected | Material differences |
|---|---|---|---|---|---|

Do not silently merge an arXiv version, IACR ePrint, conference paper, journal article, or later revision. The cited version must support the extracted claim.

## 4. Screening

Apply explicit inclusion/exclusion criteria to title/abstract screening and then to full-text screening. Record a reason for every full-text exclusion. Search snippets can support discovery only.

## 5. Claim-evidence extraction

| Work/version | Exact claim | Claim type | Model/assumptions | Parameters | Evidence location | Verification status |
|---|---|---|---|---|---|---|

Use claim types: definition, theorem, proof/reduction, security, empirical, heuristic, or novelty. Preserve caveats and distinguish author claims from reviewer verification.

## 6. Citation chaining and saturation

When capabilities permit:

- inspect backward references of closest works;
- inspect forward citations;
- search key authors, venues, acronyms, and historical terminology;
- add newly discovered synonyms and repeat;
- stop when new batches yield no material new work under a stated rule, or when the time/result budget is reached.

Record the stopping rule. Saturation within a corpus is not global exhaustiveness.

## 7. Closest-work matrix

Compare formal objects and claims, not adjectives:

| Work | Construction/problem | Security notion/model | Assumptions | Parameter regime | Complexity/cost | Difference from target |
|---|---|---|---|---|---|---|

Use compatible cost models or qualify the comparison.

## 8. Bounded conclusion

State sources, queries, dates, and blind spots next to any negative result. Prefer “no matching work was found within this search” over “no prior work exists.” Never turn an incomplete corpus into a universal novelty claim.

