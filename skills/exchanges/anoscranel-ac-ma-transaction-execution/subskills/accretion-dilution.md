---
name: accretion-dilution
domain: investing/accretion-dilution
trigger: "Testing whether a transaction adds to or subtracts from the acquirer's earnings per share."
anti_trigger: "Not for a valuation opinion, and not for trading the deal."
scope: "How the acquirer's earnings per share moves, and when the test misleads."
status: seedling
---

# Accretion and dilution

## Standard

Accretion/dilution compares the acquirer's pro forma earnings per share against its standalone EPS. The arithmetic is simple: the target's earnings plus synergies, minus the after-tax cost of cash paid and the new shares issued for stock consideration. If pro forma EPS exceeds standalone EPS the deal is accretive; otherwise dilutive.

The test's honesty depends on remembering what it does not measure. It is an earnings test, not a value test: a deal funded with cheap debt is accretive by construction while adding leverage risk. A stock deal for a company with a lower price-to-earnings ratio than the buyer is mechanically accretive while possibly destroying value — the buyer's own multiple is the benchmark that decides the direction. EPS accretion from a purchase-price allocation change is an accounting artefact, not a business improvement. The test is a screen that must be read beside the value arithmetic.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://pages.stern.nyu.edu/~adamodar/>.

## Decision rules

- Compute standalone and pro forma EPS on identical share counts and periods.
- For cash consideration, deduct after-tax financing costs at the actual funding cost.
- For stock consideration, use the shares issued at the exchange ratio, including any collar effect.
- Include synergies net of costs-to-achieve, phased by year, not at run rate at close.
- State the price-to-earnings comparison between buyer and target — the mechanical direction of a stock deal follows from it.
- Report accretion/dilution by year for the first two or three years, not just the first.

## Procedure

1. Record the buyer's standalone earnings and share count.
2. Add the target's contributed earnings and net synergies by year.
3. Deduct after-tax financing costs for cash consideration; add new shares for stock consideration.
4. Compute pro forma EPS by year and compare against standalone EPS.
5. State the buyer and target price-to-earnings comparison.
6. Record the result with the financing assumptions visible.

## Anti-patterns

- Calling a deal accretive when only a purchase-accounting artefact moved EPS.
- Using run-rate synergies in the first-year test.
- Omitting the second- and third-year test where integration costs land.
- Treating EPS accretion as proof of value created.
- Forgetting that cheap debt makes almost any cash deal accretive.

## Done checklist

- [ ] Standalone and pro forma EPS on identical bases.
- [ ] Financing costs after tax at actual funding cost.
- [ ] Share issuance at exchange ratio.
- [ ] Synergies phased by year net of costs.
- [ ] Price-to-earnings comparison stated.
- [ ] Multi-year accretion/dilution reported.

## Sources

- Deal disclosure and pro forma filings: <https://www.sec.gov/edgar/search/>
- Valuation reference material: <https://pages.stern.nyu.edu/~adamodar/>
- Investor education on merger effects: <https://www.investor.gov/introduction-investing>
