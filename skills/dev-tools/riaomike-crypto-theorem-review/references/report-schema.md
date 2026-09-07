# Review Report Schema

Use this exact positive structure. Omit a domain section only after stating it is not applicable and why.

## Header

```text
Reviewed object:
Exact source/artifact version:
Requested review depth:
Evidence inspected:
Capabilities unavailable:
```

## Verdict matrix

| Dimension | Status | Evidence | Limitation |
|---|---|---|---|
| Statement well-formedness | | | |
| Proof completeness/validity | | | |
| Reduction validity | | | |
| Security implication | | | |
| Parameters/probability | | | |
| Complexity/concrete cost | | | |
| Citations/version identity | | | |

Allowed statuses: verified, supported with limitations, unverified, contradicted, not assessable.

## Claim and obligation tables

| Claim ID | Type | Source claim/location | Reviewer status | Evidence/derivation | Dependencies |
|---|---|---|---|---|---|

| Obligation ID | Required step | Status | Gap or evidence | Downstream consequence |
|---|---|---|---|---|

## Security context

```text
Security notion/game:
Adversary powers:
Setup/model:
Assumptions:
Reduction loss:
Composition/concurrency boundary:
Implementation/side-channel exclusions:
```

## Parameter and complexity ledgers

| Symbol | Meaning | Domain/unit | Source/derivation | Constraints | Consistent? |
|---|---|---|---|---|---|

| Cost claim | Operation model | Variables/regime | Setup/amortization | Memory/communication | Failure terms | Status |
|---|---|---|---|---|---|---|

## Findings

### Blocking

Each item: `ID — location — evidence — consequence — evidence/repair required`.

### Major

Each item: `ID — location — evidence — consequence — recommended resolution`.

### Minor

Each item: `ID — location — clarity/maintenance impact — suggestion`.

## Citations and versions

| Citation | Exact version/identifier | Claim supported | Location checked | Status/discrepancy |
|---|---|---|---|---|

## Bounded conclusion

State:

1. strongest verified conclusion;
2. conditions/assumptions under which it holds;
3. first unresolved or invalid implication step;
4. unverified evidence and capabilities;
5. whether mechanized verification ran, with checker/version/result when it did.

