---
name: fx-trading-record
domain: investing/fx-trading-record
trigger: "Writing the record of an FX trade and the terms it was executed under."
anti_trigger: "Not for recommending a pair, and not for the account statement."
scope: "The written record: pair, size, rate, carry, invalidation, and review."
status: seedling
---

# FX trading record

## Standard

The FX record captures what the statement cannot: why the position existed, what the rate reflected at entry, what the position was paying to be held, and what would prove the view wrong. Statements show fills; they do not show the thesis, the swap expected at entry, or the event the trader decided to hold through.

Because FX positions are financed continuously, the record also has to be a live document during the hold. The expected carry, the cumulative swap, and the distance to the stop are all quantities that change daily, and a review that only looks at the profit and loss misses whether the trade is still the trade that was opened. The record therefore carries a review cadence, not just an entry and an exit.

Primary sources: <https://www.bis.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the pair, direction, notional, entry rate, venue, and timestamp with its time zone.
- The expected swap per night and the cumulative swap to date are recorded.
- The thesis, falsifier, event treatment, and maximum holding period are recorded at entry.
- Review entries are dated and state whether the thesis still holds.
- The exit records the rate, the realized profit or loss net of spread, commission, and swap.
- Amendments are dated; the entry record is never rewritten after the outcome.

## Procedure

1. Record the trade at entry with the venue and timestamp.
2. Record the expected financing and the events to be held through.
3. At each review date, record the thesis status and the cumulative carry.
4. At exit, record the net result including all three cost components.
5. Compare the realized result with the entry assumption.
6. File the record with the other trade records and reference it from the review.

## Anti-patterns

- Recording the fill but not the thesis.
- Reporting profit before swap and commission, which overstates the result.
- Reviewing only the profit and loss and not the thesis.
- Rewriting the entry after the exit.
- Omitting the time zone, which makes FX timestamps ambiguous.

## Done checklist

- [ ] Entry recorded with venue and timestamp.
- [ ] Expected financing recorded.
- [ ] Thesis and falsifier recorded.
- [ ] Review entries dated with thesis status.
- [ ] Net result recorded with all costs.
- [ ] Record filed and referenced.

## Sources

- Foreign exchange market conventions: <https://www.bis.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Rate and policy data: <https://www.federalreserve.gov/>
