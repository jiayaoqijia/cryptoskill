---
name: roll-and-expiry
domain: investing/roll-and-expiry
trigger: "Rolling an index futures position from one quarterly contract to the next."
anti_trigger: "Not for predicting the index, and not for the hedge ratio itself."
scope: "The quarterly roll, roll yield, and the calendar spread between contracts."
status: seedling
---

# Roll and expiry

## Standard

An index future expires quarterly, so a position held beyond the front month must be rolled: closed in the expiring contract and reopened in the next. The cost or benefit of that roll is the difference between the two prices, and over a year it can be a meaningful component of a hedged or leveraged position's return.

The roll is also a liquidity event. As the front contract approaches expiry, its volume and open interest migrate to the next, and the spread between them widens and then narrows as participants move. Rolling early costs a wider spread; rolling late risks thin liquidity on the expiring contract and a settlement on the final price. The record states the roll window chosen and the reason, so that the same decision is not re-litigated every quarter.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## Decision rules

- Record the expiry date and the chosen roll window, with the reason.
- Record the price difference between the front and next contract at the time of the roll.
- Compute the annualised roll cost or benefit and add it to the position's economics.
- Record the liquidity of both legs during the roll window.
- Record the settlement price convention for the expiring contract.
- Where the position is a hedge, record the hedge ratio through the roll, since the next contract may have a different price but the same multiplier.

## Procedure

1. Note the expiry and the typical roll window for the contract.
2. Monitor open interest and volume migration between months.
3. Compare the two prices and compute the roll cost.
4. Execute the roll and record both fills.
5. Verify the position and the hedge ratio after the roll.
6. Record the roll cost in the position's result decomposition.

## Anti-patterns

- Rolling on the last day because the calendar was not checked.
- Ignoring the roll cost in a hedged position's economics.
- Assuming both legs will be equally liquid during the roll.
- Rolling without confirming the new hedge ratio.
- Treating the roll as a separate trade rather than part of the position.

## Done checklist

- [ ] Expiry and roll window recorded.
- [ ] Price difference and roll cost computed.
- [ ] Liquidity of both legs checked.
- [ ] Roll executed and fills recorded.
- [ ] Hedge ratio verified after the roll.
- [ ] Roll cost included in the result.

## Sources

- Exchange expiry calendars and settlement rules: <https://www.cmegroup.com/>
- Market positioning data: <https://www.cftc.gov/>
- Rate and dividend inputs for carry: <https://fred.stlouisfed.org/>
