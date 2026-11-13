---
name: cds-bond-basis
domain: investing/cds-bond-basis
trigger: "Explaining why a cash bond and its CDS trade at different levels."
anti_trigger: "Not for predicting convergence, and not for credit analysis."
scope: "Why the cash bond and the derivative diverge, and what closes the gap."
status: seedling
---

# CDS-bond basis

## Standard

The basis is the difference between a bond's spread over the risk-free curve and the CDS spread for the same entity and maturity. In theory they should be close, since both price the same default risk. In practice they diverge, and the divergence is one of the most informative observations in credit: it reflects funding costs, deliverability, supply and demand for the two instruments, and the difficulty of shorting the cash bond.

The sign of the basis tells a story. A negative basis — CDS cheaper than the bond spread — can reflect the cost of financing the bond position, which is what an arbitrageur must pay to hold it. A positive basis can reflect a shortage of the bond, or a constraint on those who would short it. Reading the basis as mispricing without those frictions is how a trade that looks like arbitrage becomes a financing position.

Primary sources: <https://www.federalreserve.gov/> and <https://www.isda.org/>.

## Decision rules

- Record the bond's spread to the curve and the CDS spread for the matching maturity.
- Record the basis and its sign.
- Record the financing cost of holding the bond and the cost of shorting where possible.
- Record any deliverability or cheapest-to-deliver effects.
- Record what would close the basis and over what horizon.
- Record the size the market can absorb, since the basis trade is often capacity-constrained.

## Procedure

1. Compute the bond's spread to the risk-free curve.
2. Record the CDS spread for the same maturity.
3. Compute the basis and sign.
4. Record the financing cost of the cash leg.
5. Record any constraint on shorting or delivering.
6. Write the basis analysis with its assumed convergence.

## Anti-patterns

- Treating a wide basis as free money without the financing cost.
- Comparing a bond and CDS of different maturities or seniorities.
- Ignoring the difficulty of shorting the cash bond.
- Assuming convergence within a period the trade cannot be held for.
- Sizing the trade beyond the bond's liquidity.

## Done checklist

- [ ] Bond spread computed.
- [ ] CDS spread recorded for the same maturity.
- [ ] Basis computed and signed.
- [ ] Financing recorded.
- [ ] Constraints recorded.
- [ ] Convergence assumption written.

A further check is to state which side of the basis the participant can actually access: a buyer of the bond who finances cheaply and a short seller who cannot borrow the bond face different opportunities from the same visible gap, and the record should name which of the two the strategy requires before treating the basis as a signal.

## Sources

- Market rates and credit data: <https://www.federalreserve.gov/>
- Credit derivatives documentation standards: <https://www.isda.org/>
- Spread and rate series: <https://fred.stlouisfed.org/>
