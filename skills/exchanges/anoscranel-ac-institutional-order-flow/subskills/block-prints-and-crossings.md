---
name: block-prints-and-crossings
domain: investing/block-prints-and-crossings
trigger: "Reading an off-book block print and what its price says."
anti_trigger: "Not for identifying the parties, and not for inferring intent."
scope: "Off-book trades, dark pool prints, and what the price concession says."
status: seedling
---

# Block prints and crossings

## Standard

A block trade executes away from the continuous book, either negotiated bilaterally or matched in a dark venue, and it prints to the tape afterwards. The print carries size, price, and time. The price relative to the prevailing quote is the informative part: a block that crosses at a discount to the bid indicates a seller who needed to transact, a block at a premium indicates a buyer who did, and a block at the mid indicates a negotiated match with less urgency on either side.

Publication delays matter. Some off-book trades report promptly, others with a delay that varies by size, so a print appearing now may describe a trade from earlier, and the intervening price move can make the concession look larger or smaller than it was. The record should state the time of execution as well as the time of publication, where both are available.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the print's size, price, execution time, and publication time.
- Record the prevailing bid, ask, and mid at execution.
- Compute the concession or premium relative to the mid and the quote.
- Record the venue type if it is disclosed.
- Record the price action after the print, which is the market's response to the news of the trade.
- Where the execution time is unknown, record that the concession cannot be measured precisely.

## Procedure

1. Capture the print and its timestamps.
2. Reconstruct the prevailing quote at execution.
3. Compute the concession in basis points.
4. Note the venue and any publication delay.
5. Record the subsequent price action.
6. Write the summary with the concession and its limit.

## Anti-patterns

- Reading a block print as a directional signal on its own.
- Measuring the concession against the price at publication rather than execution.
- Assuming the seller initiated because the print was at a discount.
- Ignoring the post-print price action.
- Treating one print as the whole position.

## Done checklist

- [ ] Print size, price, timestamps recorded.
- [ ] Prevailing quote recorded.
- [ ] Concession computed.
- [ ] Venue and delay recorded.
- [ ] Subsequent action recorded.
- [ ] Limit on measurement stated.

A useful framing is that the print describes a completed negotiation rather than an intention: the seller found a buyer and the price is the settlement of that conversation. Reading the concession as urgency is reasonable, and reading it as a forecast of the next move is not, because the transaction has already removed the imbalance it represented.


## Sources

- Market structure and trade reporting: <https://www.sec.gov/investor>
- Trading practice guidance: <https://www.finra.org/>
- Investor education on execution: <https://www.investor.gov/introduction-investing>
