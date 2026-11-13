---
name: crypto-option-venues
domain: crypto-trading/crypto-option-venues
trigger: "Working out where crypto option liquidity exists and at what cost."
anti_trigger: "Not for assessing venue solvency, and not for predicting prices."
scope: "Order books versus request-for-quote, and where the liquidity actually is."
status: seedling
---

# Crypto option venues

## Standard

Crypto option liquidity is concentrated. A few venues carry most of the volume, and within them the liquid instruments are the near-dated at-the-money contracts and a handful of strikes. Larger or longer-dated trades are executed through request-for-quote: a market maker quotes a price for a specified structure, and the quote is firm for seconds rather than displayed continuously.

That structure decides how a trade is executed. There is no consolidated tape to compare against, so the reference price is whatever the venue or an aggregator displays, and the executable price can differ materially. A position sized on the displayed market and executed through a quote can end up with a very different fill, and the record should note which route was used.

Primary sources: <https://www.cftc.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the venue and the execution route: order book or quote.
- Record the displayed market and the executed price, with the times.
- Record the size available at the displayed price.
- Record the quote's validity window and the number of makers approached.
- Record the fee structure, including settlement and exercise fees.
- Record the venue's settlement and margin rules where they affect the position.

## Procedure

1. Identify the venue and route.
2. Record the displayed market and its time.
3. Request a quote for the intended structure and record it.
4. Compare the executed price with the displayed reference.
5. Record fees.
6. Write the execution summary.

## Anti-patterns

- Assuming the displayed price is executable at size.
- Comparing quotes from different times as if simultaneous.
- Ignoring settlement and exercise fees.
- Sizing to a market that does not exist beyond the touch.
- Forgetting that a quote expires in seconds.

## Done checklist

- [ ] Venue and route recorded.
- [ ] Displayed and executed prices recorded.
- [ ] Size at the touch recorded.
- [ ] Quote window recorded.
- [ ] Fees recorded.
- [ ] Execution summary written.

The practical consequence is that execution is part of the strategy rather than an afterthought: a structure that requires four legs in illiquid strikes can lose more in crossing spreads than the thesis expects to earn, and the record should state the number of quotes obtained rather than imply that a single price was the market.


## Sources

- Regulatory information on crypto markets: <https://www.cftc.gov/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on trading costs: <https://www.investor.gov/introduction-investing>
