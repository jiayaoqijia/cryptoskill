---
name: accrual-and-daycount
domain: software-engineering/accrual-and-daycount
trigger: "Computing interest or accrual over a period."
anti_trigger: "Not for legal or accounting interpretation, and not for rate forecasting."
scope: "Day-count conventions, compounding, and period arithmetic."
status: seedling
---

# Accrual and day-count

## Standard

Interest over a period depends on a convention that specifies which days are counted in the numerator and which in the denominator. Actual over actual divides the actual days elapsed by the actual days in the year; thirty over three-sixty treats every month as thirty days and every year as three hundred sixty; actual over three-sixty-five uses a fixed denominator. The same rate and the same period produce different amounts under each.

The choice is contractual rather than technical, and it must match the instrument. A bond and a loan with the same rate and term can accrue differently because their conventions differ, and a system that applies one convention to both will be wrong for one of them. The record states the convention per instrument type and the day-count function that implements it.

Primary sources: <https://www.isda.org/> and <https://www.iso20022.org/>.

## Decision rules

- Record the day-count convention per instrument type.
- Record the date inclusion rule: whether the start date, the end date, or both are counted.
- Record the compounding frequency and the method for partial periods.
- Record the treatment of non-business days and any following or modified-following rule.
- Record the rate's basis and whether it is annualised, since the accrual depends on it.
- Record the rounding point in the accrual calculation.

## Procedure

1. Record the convention and the instrument types it applies to.
2. Implement day counting with an explicit inclusion rule.
3. Record compounding and partial-period treatment.
4. Record business-day adjustment rules.
5. Record the rounding point.
6. Test across a leap year, a month boundary, and a partial period.

## Anti-patterns

- Using one convention for all instruments.
- Excluding both the start and the end date, losing a day.
- Ignoring leap years in the denominator.
- Compounding annually while accruing daily without recording the reconciliation.
- Applying a business-day adjustment backwards, which shortens a period unnecessarily.

## Done checklist

- [ ] Convention recorded per instrument.
- [ ] Inclusion rule recorded.
- [ ] Compounding and partial periods recorded.
- [ ] Business-day rule recorded.
- [ ] Rounding point recorded.
- [ ] Tested across leap year and boundaries.

The thirty-over-three-sixty convention deserves its own caution because it is counter-intuitive to anyone who has not met it: a period from the thirty-first of January to the first of March is treated as one day, not thirty, and a system that counts actual days will differ from the contractual accrual by an amount that appears arbitrary until the convention is known.


## Sources

- Financial instrument documentation standards: <https://www.isda.org/>
- Payment and settlement standards: <https://www.iso20022.org/>
- Financial reporting standards: <https://www.ifrs.org/>
