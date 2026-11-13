---
name: nav-loans
domain: investing/nav-loans
trigger: "Reading a fund-level loan secured on the portfolio's net asset value."
anti_trigger: "Not for predicting returns, and not for the allocation decision."
scope: "Fund-level borrowing against the portfolio and its cost."
status: seedling
---

# NAV loans

## Standard

A net asset value loan is borrowing at the fund level, secured on the portfolio rather than on investors' commitments. It lets a fund make a distribution, fund a follow-on, or bridge a liquidity need without selling assets, and it moves the borrowing from the investor's balance sheet to the fund's.

The consequences are three. The leverage is inside the vehicle, so the reported volatility of the fund's assets understates the volatility of the investor's position. The loan has covenants tied to the portfolio's value, which can be breached by a valuation decline and can force asset sales at the worst moment. And the interest cost reduces the return while the distribution it funded may have been treated as a return of capital.

Primary sources: <https://www.federalreserve.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the facility size relative to the portfolio's net asset value.
- Record the interest cost and its priority in the waterfall.
- Record the covenants and the valuation basis they reference.
- Record what the proceeds funded: distribution, follow-on, or bridge.
- Record the effect on reported leverage and on the return.
- Record the maturity and the refinancing risk.

## Procedure

1. Record the facility size and its ratio to NAV.
2. Record the cost and waterfall position.
3. Record covenants and valuation basis.
4. Record the use of proceeds.
5. Compute the effect on reported leverage.
6. Write the analysis with the covenant path.

## Anti-patterns

- Treating a NAV loan as equivalent to investor-level leverage.
- Ignoring the covenant tied to a valuation the sponsor produces.
- Assuming a distribution funded by borrowing is a return of capital.
- Overlooking refinancing risk at maturity.
- Comparing funds without adjusting for fund-level leverage.

## Done checklist

- [ ] Facility size and ratio recorded.
- [ ] Cost and priority recorded.
- [ ] Covenants recorded.
- [ ] Use of proceeds recorded.
- [ ] Leverage effect computed.
- [ ] Maturity risk recorded.

The distribution question is worth resolving explicitly with the fund's own documents: a distribution funded by borrowing does not reduce the investor's exposure, and treating it as a realised return overstates the performance in the same way that borrowing to pay a dividend overstates a company's earnings. Recording the source of each distribution is what prevents the confusion.


## Sources

- Fund financing disclosure: <https://www.sec.gov/investor>
- Credit conditions and leverage: <https://www.federalreserve.gov/>
- Analysis standards: <https://www.cfainstitute.org/>
