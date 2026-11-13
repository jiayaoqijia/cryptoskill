---
name: halts-and-news
domain: investing/halts-and-news
trigger: "Trading a stock that is halted or likely to be halted."
anti_trigger: "Not for predicting news, and not for market-structure theory."
scope: "LULD and news-pending halts, resumption, and trading around them."
status: seedling
---

# Halts and news

## Standard

A trading halt suspends price discovery, and the position does not stop existing while it is suspended. The two mechanisms a trader meets are the volatility halt, triggered by a rapid move outside a price band, and the news-pending halt, called by the exchange while material information is disseminated. Both end with a reopening auction, and the reopening price can be far from the last traded price.

The practical consequences are that stops do not execute during a halt and that the reopening is an auction where the clearing price is discovered from the orders submitted. A position sized as if the last price were available is therefore mis-sized, and a position held into a foreseeable event should assume a reopening gap. Where a halt is likely, the record states the exposure at a plausible reopening and the plan for the first minutes after trading resumes.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the halt mechanisms that apply to the name and the exchange's reopening procedure.
- Record the position's exposure at a reopening price materially away from the last trade.
- Record whether stops will execute in the reopening auction or only in continuous trading.
- Record the plan for the first minutes after resumption, rather than improvising.
- Record the halt history of the name, since some names halt repeatedly.
- Where the position cannot tolerate a reopening gap, reduce it before the event.

## Procedure

1. Record the applicable halt rules and reopening process.
2. Compute the exposure at a plausible reopening gap.
3. Check how the venue handles resting orders across a halt.
4. Write the resumption plan: act, wait, or exit.
5. Record the name's halt history.
6. Review the position against the plan after any halt.

## Anti-patterns

- Assuming a stop will execute during a halt.
- Treating the last price before a halt as the price that will reopen.
- Improvising on resumption while the book is unbalanced.
- Holding a name with a history of repeated halts at full size.
- Ignoring how resting orders are treated across the halt.

## Done checklist

- [ ] Halt rules and reopening recorded.
- [ ] Reopening-gap exposure computed.
- [ ] Resting-order treatment checked.
- [ ] Resumption plan written.
- [ ] Halt history recorded.
- [ ] Position reviewed after any halt.

## Sources

- Trading halt and market operations context: <https://www.sec.gov/investor>
- Trading practice guidance: <https://www.finra.org/>
- Investor education on market events: <https://www.investor.gov/introduction-investing>
