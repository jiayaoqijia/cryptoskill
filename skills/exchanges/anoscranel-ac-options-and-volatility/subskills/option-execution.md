---
name: option-execution
domain: crypto-trading/option-execution
trigger: "Handling option execution, assignment, and early exercise mechanics."
anti_trigger: "Not for choosing a structure, and not for pricing."
scope: "Spreads, open interest, assignment and early exercise, and the mechanics that costs hide in."
status: seedling
---

# Option execution

## Standard

Options trade with wider spreads and thinner books than the underlying, so execution costs are a larger share of the outcome. The relevant measures are the bid-ask spread in volatility terms, the open interest at the strike, and the depth available at the quoted price. A structure that looks cheap at mid can be expensive at the prices actually available.

Assignment and early exercise add mechanics that cost money quietly. A short option can be assigned before expiry, particularly around dividends or when it is deep in the money; a long option that is not exercised by expiry expires worthless. Both are administrative risks that a record should anticipate rather than discover.

Primary sources: <https://www.cboe.com/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the spread in volatility terms and the open interest at each strike used.
- Compute the structure's cost at the executable price, not at mid.
- Record the assignment procedure and the treatment of dividends or events.
- Note the expiry time and the last trading time, which differ.
- For short positions, record the early-exercise risk and the plan.
- Where the book is thin, size the trade to the displayed depth.

## Procedure

1. Pull quotes, spreads, and open interest for each leg.
2. Compute the executable cost of the structure.
3. Check the expiry and settlement mechanics for the venue.
4. Identify assignment and early-exercise exposures.
5. Size to displayed depth and record the sizing rule.
6. Record the execution plan.

## Anti-patterns

- Pricing a structure at mid.
- Ignoring open interest at the strike.
- Assuming expiry and last trading time are the same.
- Forgetting early exercise around events.
- Sizing beyond the displayed depth.

## Done checklist

- [ ] Spreads and open interest recorded per leg.
- [ ] Executable cost computed.
- [ ] Expiry and settlement mechanics checked.
- [ ] Assignment and early-exercise exposures identified.
- [ ] Sizing rule recorded.
- [ ] Execution plan written.

## Sources

- Options market mechanics and data: <https://www.cboe.com/>
- Options disclosure and settlement context: <https://www.sec.gov/investor>
- Investor education on options mechanics: <https://www.investor.gov/introduction-investing>

The cost of execution in options is often larger than the edge being pursued, particularly in smaller books. That is why the executable price, not the mid, belongs in the record at inception: a position that only works at mid has already lost, and the loss is invisible until it is closed.
