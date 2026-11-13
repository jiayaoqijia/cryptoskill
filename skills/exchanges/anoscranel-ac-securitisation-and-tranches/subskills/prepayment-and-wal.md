---
name: prepayment-and-wal
domain: investing/prepayment-and-wal
trigger: "Working out how long a securitisation tranche will actually be outstanding."
anti_trigger: "Not for forecasting prepayment speeds, and not for duration arithmetic on plain bonds."
scope: "Prepayment assumptions, weighted average life, and why stated maturity misleads."
status: seedling
---

# Prepayment and weighted average life

## Standard

A mortgage or consumer pool does not amortise on its stated schedule: borrowers refinance, move, and repay early, so the principal returned in any period depends on a prepayment speed that is an assumption rather than a contract term. Weighted average life is the average time to return of principal under that assumption, and it is the number a tranche's risk should be measured against.

The consequence is that the stated legal maturity is close to meaningless for valuation. A tranche with a thirty-year maturity may have a weighted average life of three years at a fast prepayment speed and eight at a slow one, and its price sensitivity changes with the speed itself. Prepayment risk is therefore two risks in one: the level of rates and the behaviour of borrowers, which do not always move together.

Primary sources: <https://www.sec.gov/investor> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the prepayment assumption used and its source.
- Record the weighted average life at that assumption and at a faster and slower one.
- Record the tranche's stated legal maturity separately.
- Record the pool's composition and the borrowers' refinancing incentives.
- Record how prepayment affects the tranche's position in the waterfall over time.
- Record the sensitivity of price to a change in the speed assumption.

## Procedure

1. Record the stated maturity and the assumed speed.
2. Compute weighted average life at that speed.
3. Recompute at faster and slower speeds.
4. Record the price sensitivity across the range.
5. Record the borrower and rate conditions that drive the speed.
6. Write the life summary with its assumption.

## Anti-patterns

- Valuing a tranche against its legal maturity.
- Using a single prepayment speed without a range.
- Assuming prepayment behaves symmetrically when rates rise and fall.
- Ignoring how amortisation moves the tranche through the waterfall.
- Treating a dealer's model output as the speed itself.

## Done checklist

- [ ] Speed assumption recorded with source.
- [ ] WAL at the assumption recorded.
- [ ] WAL range recorded.
- [ ] Legal maturity recorded separately.
- [ ] Price sensitivity recorded.
- [ ] Drivers recorded.

The asymmetry matters for a tranche's risk profile: when rates fall, prepayments accelerate and a premium-priced tranche loses its excess yield exactly when it was most valuable; when rates rise, prepayments slow and the tranche extends into the period when its coupon is least attractive. Both directions of the assumption work against the holder, which is why the range is recorded rather than a point.

## Sources

- Mortgage and asset-backed disclosure: <https://www.sec.gov/investor>
- Housing and rate data: <https://www.federalreserve.gov/>
- Prepayment and rate series: <https://fred.stlouisfed.org/>
