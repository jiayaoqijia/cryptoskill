---
name: irr-and-its-assumptions
domain: investing/irr-and-its-assumptions
trigger: "Reading a private-fund IRR and knowing what it assumes."
anti_trigger: "Not for comparing IRR across funds without conversion, and not for forecasting returns."
scope: "IRR, reinvestment, timing, and why it flatters early-stage funds."
status: seedling
---

# IRR and its assumptions

## Standard

IRR is the discount rate that makes the present value of a fund's cash flows equal zero. It is a money-weighted measure, so it reflects both the return earned and the pace at which capital was called and returned. That makes it sensitive to timing in a way a time-weighted return is not: a fund that returns capital early records a higher IRR than one that returns the same total later, even when the underlying investments performed identically.

The reinvestment assumption compounds the distortion. IRR implicitly assumes every interim cash flow is reinvested at the IRR itself, which for a fund reporting twenty percent assumes twenty percent redeployment of every distribution. No such opportunity is identified, and the assumption is most flattering precisely when the fund is doing well. The record should state that the metric is a summary of cash-flow timing rather than a compound annual return.

Primary sources: <https://www.cfainstitute.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the IRR, its as-of date, and whether it is gross or net of fees.
- Record the cash-flow schedule the IRR was computed from, or its source.
- Record the fund's age, since IRR is unstable early in life.
- Note the reinvestment assumption explicitly.
- Compare with a money-multiple before treating IRR as a return.
- Where two funds are compared, check whether both IRRs use the same convention.

## Procedure

1. Record the metric, date, and gross or net basis.
2. Obtain the cash-flow schedule or the reported source.
3. Record the fund's age and stage.
4. Note the reinvestment assumption and its effect.
5. Pair the IRR with a multiple and a duration.
6. Write the metric summary with its convention.

## Anti-patterns

- Treating IRR as a compound annual return.
- Comparing an early-stage IRR with a mature fund's.
- Ignoring the gross versus net distinction.
- Quoting an IRR without its as-of date.
- Using IRR alone to rank funds of different vintages.

## Done checklist

- [ ] IRR, date, and basis recorded.
- [ ] Cash-flow source recorded.
- [ ] Fund age recorded.
- [ ] Reinvestment assumption noted.
- [ ] Multiple and duration paired.
- [ ] Convention written.

A useful cross-check is to compute the IRR on the same cash flows with a delay of one quarter applied to every distribution: if the reported figure moves materially, the fund's return is being driven by the timing of its exits rather than by the value it created, and the record should say so before the number is compared with anything else.

## Sources

- Investment performance standards: <https://www.cfainstitute.org/>
- Fund disclosure requirements: <https://www.sec.gov/investor>
- Investor education on fund metrics: <https://www.investor.gov/introduction-investing>
