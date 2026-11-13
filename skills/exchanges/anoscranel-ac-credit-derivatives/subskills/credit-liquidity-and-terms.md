---
name: credit-liquidity-and-terms
domain: investing/credit-liquidity-and-terms
trigger: "Assessing whether a credit position can be entered, held, and exited."
anti_trigger: "Not for venue due diligence in general, and not for predicting spreads."
scope: "Dealer liquidity, documentation, and counterparty terms."
status: seedling
---

# Credit liquidity and terms

## Standard

Credit derivatives trade over the counter, so liquidity is a dealer relationship rather than an order book. The observable proxies are the bid-offer spread, the size a dealer will show, and whether the name trades at all in the maturity needed. For single names outside the major indices, the honest assessment is often that the position can be entered but not exited at a predictable price.

The terms carry the second layer of risk. The counterparty's credit stands behind the contract, collateral terms determine what must be posted when the position moves, and the documentation version determines the event definitions. A hedge against a default that is only as good as the dealer's own credit is a hedge with a correlation the record should state.

Primary sources: <https://www.isda.org/> and <https://www.bis.org/>.

## Decision rules

- Record the bid-offer spread in basis points and the size available at that spread.
- Record which maturities trade and which are quoted only on request.
- Record the counterparty, its credit standing, and the collateral agreement.
- Record the documentation version and any negotiated amendments.
- Record the margin terms: initial margin, variation margin, and thresholds.
- Record the exit route if the dealer stops making a market.

## Procedure

1. Collect bid-offer and size for the maturity traded.
2. Record liquidity by maturity and note the gaps.
3. Record counterparty and collateral terms.
4. Record documentation version and amendments.
5. Record margin thresholds and the funding they imply.
6. Write the liquidity and terms assessment.

## Anti-patterns

- Assuming an index-level bid-offer applies to a single name.
- Ignoring the counterparty's credit when the hedge is the position.
- Overlooking collateral thresholds that turn a hedge into a funding call.
- Treating a quoted price as executable at size.
- Assuming the dealer relationship survives a stress event.

## Done checklist

- [ ] Bid-offer and size recorded.
- [ ] Liquidity by maturity recorded.
- [ ] Counterparty and collateral recorded.
- [ ] Documentation version recorded.
- [ ] Margin thresholds recorded.
- [ ] Exit route written.

The practical test is to obtain a two-way price at the intended size, not a one-way quote: a dealer who will buy protection but not sell it is not making a market, and the asymmetry is the most direct statement of how the position could be exited if the view changed.

## Sources

- Market documentation and conventions: <https://www.isda.org/>
- Counterparty and margin standards: <https://www.bis.org/>
- Regulatory context: <https://www.federalreserve.gov/>
