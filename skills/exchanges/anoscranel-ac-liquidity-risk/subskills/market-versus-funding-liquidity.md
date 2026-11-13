---
name: market-versus-funding-liquidity
domain: investing/market-versus-funding-liquidity
trigger: "Distinguishing an asset that cannot be sold from a book that cannot raise cash."
anti_trigger: "Not for predicting a crisis, and not for margin mechanics on one position."
scope: "Two different constraints that fail in different ways."
status: seedling
---

# Market versus funding liquidity

## Standard

Market liquidity is a property of the asset and the market it trades in: how much can be sold, how quickly, and at what price concession. Funding liquidity is a property of the balance sheet: whether cash is available when an obligation falls due. The two are measured differently, and a portfolio can be rich in one and poor in the other.

The distinction matters because the remedies differ. A market-liquidity problem is addressed by holding assets that sell easily or by accepting a longer horizon; a funding-liquidity problem is addressed by holding a cash buffer or committed credit. A portfolio that holds only liquid assets but finances them short can fail on funding, and one that holds a large cash buffer but only illiquid assets can fail on market access when the buffer is exhausted.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the market-liquidity profile: days to liquidate per holding at a stated participation rate.
- Record the funding profile: cash, committed facilities, and the maturity of liabilities.
- Record which obligations are dated and which are callable.
- Record the overlap: obligations that can only be met by selling.
- Record the buffer required to meet dated obligations without selling.
- Record the trigger at which the buffer falls below the requirement.

## Procedure

1. Build the market-liquidity profile by holding.
2. Build the funding profile with maturities and commitments.
3. Map obligations onto the funding profile.
4. Identify obligations that require asset sales.
5. Compute the buffer and its minimum.
6. Write the two profiles separately before combining them.

## Anti-patterns

- Treating liquid assets as a substitute for committed funding.
- Treating a cash buffer as sufficient when liabilities are callable at will.
- Measuring liquidity only at the portfolio level and not by obligation.
- Assuming a facility will be available when it is most needed.
- Combining the two profiles into one number that hides which constraint binds.

## Done checklist

- [ ] Market-liquidity profile recorded.
- [ ] Funding profile recorded.
- [ ] Dated obligations recorded.
- [ ] Sale-dependent obligations identified.
- [ ] Buffer computed with a minimum.
- [ ] Trigger level set.

The two profiles also interact through the calendar: a funding obligation that falls due on a date when market liquidity is seasonally thin, such as a holiday period, combines the two constraints, and the record should flag any dated obligation that lands in a window when selling would be unusually costly.


## Sources

- Liquidity standards and market infrastructure: <https://www.bis.org/>
- Investor education on liquidity risk: <https://www.investor.gov/introduction-investing>
- Market data for volume baselines: <https://fred.stlouisfed.org/>
