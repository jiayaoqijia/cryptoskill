---
name: verify-a-reserve-attestation-report
description: Use when relying on a reserve report to say a stablecoin is backed. Checks the attestation's scope, freshness, custodian, and whether it proves what it appears to prove.
---

# Verify a reserve attestation report

An attestation shows that, at a past moment, a named custodian saw certain assets. It usually does not prove completeness of liabilities, current holding, or that you can actually redeem. Read the scope before trusting the number.

## Procedure

1. Identify the report type: a full audit (an opinion on financials) versus an attestation (agreed-upon procedures on balances). Most "proof of reserves" is the weaker latter.
2. Check the as-of date and the report date. A report dated 40 days after the as-of date is already stale in a fast market.
3. Find the custodian(s) named and whether they sit in a favourable jurisdiction with segregation. Assets at an affiliate of the issuer are not arm's-length.
4. Read the scope sentence: does it cover *all* reserves and *all* liabilities, or only the assets? An attestation covering only assets cannot show backing, because backing is a ratio.
5. Check the maturity and liquidity of the reserve: T-bills maturing in 90 days are not cash for a same-day redemption run.
6. Compute coverage from the reported figures:
   `python3 -c "print(round(reserves/liabilities,4))"` -> must exceed 1.00.
7. Confirm the report is signed by a recognised firm; a self-published dashboard is not an attestation, and an issuer's own API is not independent evidence.

## Pitfalls

- Equating an attestation with an audit: no opinion, no GAAS, no liability testing.
- Ignoring the as-of date and treating a quarterly number as current.
- Reserves held partly by an affiliated entity, netting out on a consolidated basis and hiding a hole.
- A coverage ratio above 1.00 that counts illiquid loans to related parties as reserves.
- Trusting a "live" reserve page whose data source cannot be checked outside the issuer.
- The auditor's name carries the weight, not the letterhead: check the firm is registered and the engagement partner is named.
- A reserve report can be true and the coin still fail, if reserves are lent out or encumbered.
- Comparing two issuers' coverage ratios is meaningless if their accountants scope liabilities differently.
- Quarterly attestations cannot see an intra-quarter hole; a run inside the window is invisible to the report.

## Verification

    python3 -c "print(round(reserves/liabilities,4))"   # >= 1.00, and note reserve liquidity
    # report as-of date within the staleness window your policy allows (e.g. 30 days)

Report the report type, as-of date, custodian, coverage ratio, and reserve liquidity, and state what the scope does not cover.
