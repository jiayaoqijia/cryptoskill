---
name: spin-off-mechanics
domain: investing/spin-off-mechanics
trigger: "Working through a spin-off distribution and when-issued trading."
anti_trigger: "Not for predicting the spun entity's value, and not for the investment case."
scope: "Distribution ratios, when-issued trading, and index inclusion."
status: seedling
---

# Spin-off mechanics

## Standard

A spin-off distributes shares in a subsidiary to the parent's holders, usually in a stated ratio. Between the announcement and the distribution, the market often trades the new shares on a when-issued basis, which lets a price form before the shares exist and lets holders adjust their exposure. The when-issued price is the market's estimate of the spun entity, and the parent's price should reflect it.

Three mechanics decide the outcome. The distribution ratio fixes how many new shares each parent share yields. Index treatment determines whether the spun entity is added and whether holders receive forced buying or selling. And the record date determines who receives the shares, which is a separate date from the distribution date and the ex-date.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the distribution ratio, the record date, and the distribution date.
- Record whether when-issued trading exists and its ticker.
- Record the when-issued price against the parent's implied valuation.
- Record the index treatment of both entities.
- Record the tax treatment where disclosed, as a question for a professional if unclear.
- Record the holder's resulting position and any fractional share handling.

## Procedure

1. Record the distribution terms and dates.
2. Check for when-issued trading.
3. Compare the when-issued price with the implied valuation.
4. Record index inclusion or deletion for both entities.
5. Compute the resulting position including fractions.
6. Write the mechanics summary.

## Anti-patterns

- Confusing the record date with the distribution date.
- Ignoring when-issued trading and pricing the entity from nothing.
- Assuming the spun entity will be added to an index.
- Forgetting fractional shares and their cash settlement.
- Treating the spin as tax-free without checking.

## Done checklist

- [ ] Ratio and dates recorded.
- [ ] When-issued status recorded.
- [ ] Valuation comparison recorded.
- [ ] Index treatment recorded.
- [ ] Resulting position computed.
- [ ] Tax question recorded.

A further consideration is the parent's remaining business: the sum of the two entities' market values after the distribution often differs from the parent's price before it, and the difference reflects the market's view of the separated businesses rather than an arbitrage, so the comparison belongs in the record with that caveat attached.


Recording the distribution ratio and the when-issued ticker together is what lets a later reader reconstruct the position at any date between announcement and distribution, which is the window in which most of the ambiguity about what the holder actually owned exists.

## Sources

- Spin-off filings and information statements: <https://www.sec.gov/edgar/search/>
- Disclosure framework: <https://www.sec.gov/investor>
- Investor education on corporate events: <https://www.investor.gov/introduction-investing>
