---
name: borrow-and-short-constraints
domain: investing/borrow-and-short-constraints
trigger: "Establishing whether a short position can actually be held."
anti_trigger: "Not for the case against a company, and not for market-structure theory."
scope: "Locates, hard-to-borrow names, recall risk, and borrow cost."
status: seedling
---

# Borrow and short constraints

## Standard

A short sale requires borrowed shares, and the borrow is a market of its own. Easy-to-borrow names cost little and can be shorted in size; hard-to-borrow names carry a fee that can reach annualised rates in the double digits, and the supply can disappear. The fee is charged continuously, so a short held for months pays it for months, and the position's economics include that cost from the first day.

Recall is the risk that distinguishes shorting from most other trades. The lender can demand the shares back, and the broker allocates the recall across clients, which can force a covering purchase at the worst moment. A short positioned as if it could be held indefinitely is therefore mis-sized, and the record should state the borrow fee, the recall exposure, and the plan if the shares are recalled.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the borrow availability and the fee, with the date and time checked.
- Convert the fee into an annualised cost and into a cost per holding period.
- Record the historical borrow behaviour of the name, including any squeezes.
- Record the recall risk and the covering plan if shares are recalled.
- Record the short interest and days-to-cover, as context rather than as a forecast.
- Size the short so that a recall and a squeeze are survivable.

## Procedure

1. Check borrow availability and fee at the intended size.
2. Compute the annualised and period cost of the borrow.
3. Review the name's history of borrow tightness and squeezes.
4. Write the recall and squeeze plan with a covering rule.
5. Record short interest and days to cover.
6. Size the position against the squeeze scenario.

## Anti-patterns

- Assuming a short can be held for as long as the thesis requires.
- Ignoring the borrow fee in the trade's economics.
- Sizing a crowded short as if the exit were liquid.
- Treating short interest as a directional signal.
- Having no plan for a recall.

## Done checklist

- [ ] Borrow availability and fee recorded with time.
- [ ] Annualised and period cost computed.
- [ ] Borrow history and squeezes reviewed.
- [ ] Recall and squeeze plan written.
- [ ] Short interest and days to cover recorded.
- [ ] Size tested against the squeeze scenario.

## Sources

- Short sale regulation and disclosure: <https://www.sec.gov/investor>
- Trading practice and margin guidance: <https://www.finra.org/>
- Investor education on short selling: <https://www.investor.gov/introduction-investing>
