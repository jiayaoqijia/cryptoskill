---
name: private-assets-and-lockups
domain: investing/private-assets-and-lockups
trigger: "Evaluating private assets where the valuation is a mark, not a price."
anti_trigger: "Not for choosing a fund manager, and not for tax planning."
scope: "Infrastructure, private credit, and the marks that are not prices."
status: seedling
---

# Private assets and lockups

## Standard

A private asset is valued by a mark, and a mark is an opinion refreshed periodically by someone with an interest in the number. That is not a scandal; it is the structure. The consequence is that reported volatility understates risk, correlations with public markets look lower than they are, and the price at which you can exit is negotiated rather than observed.

Infrastructure and private credit are the two broad categories most often offered to individual investors, and they differ in what the mark depends on: infrastructure on long-dated contracted cash flows, private credit on the borrower's ability to repay. In both cases the lockup is the price of admission, and the exit queue is the risk that appears exactly when everyone wants out.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the valuation method: cost, mark, appraisal, or observable transaction.
- Record the mark's date and who produces it.
- Record the lockup term, the exit queue rules, and any gate.
- Treat marks as evidence of a range, not as a price.
- Compare the fund's stated volatility with what a sale would reveal; note the gap.
- Size the position so that a lockup cannot force an unrelated sale.

## Procedure

1. Identify the asset class and the valuation method.
2. Record the mark, its date, and its producer.
3. Record the lockup, the exit queue, and the gates.
4. Estimate the mark-to-sale gap from any available transaction data.
5. Check the fee structure, including any performance fee.
6. Write the record with the liquidity constraint stated.

## Anti-patterns

- Treating a quarterly mark as a market price.
- Using reported volatility to size an illiquid position.
- Ignoring the exit queue until it is invoked.
- Assuming a gate applies only to others.
- Sizing with capital that a near-term goal needs.

## Done checklist

- [ ] Asset class and valuation method recorded.
- [ ] Mark, date, and producer recorded.
- [ ] Lockup, exit queue, and gates recorded.
- [ ] Mark-to-sale gap estimated.
- [ ] Fee structure recorded.
- [ ] Liquidity constraint stated in the record.

## Sources

- Regulatory context for private-fund disclosure: <https://www.sec.gov/investor>
- Investor education on private and illiquid assets: <https://www.investor.gov/introduction-investing>
- Rate context for opportunity cost: <https://fred.stlouisfed.org/>

The lockup's real cost is not the wait; it is the correlation between the moment you need liquidity and the moment the queue forms. Exit queues lengthen exactly when marks are being questioned, which means the investor who planned to sell 'if needed' discovers that the plan assumed a market that exists only in calm periods.

Fee structures deserve the same scrutiny as the mark: a performance fee on a mark that is later revised downward produces a fee paid on a gain that never existed. Record whether the fee crystallises on marks or on realisations, and note the clawback terms if any.

