---
name: fx-venues-and-spreads
domain: investing/fx-venues-and-spreads
trigger: "Judging what an FX venue's quote actually costs to trade."
anti_trigger: "Not for recommending a broker, and not for predicting spreads."
scope: "ECN, market maker, prime brokerage, last look, and what a quoted spread really includes."
status: seedling
---

# FX venues and spreads

## Standard

Retail FX reaches the interbank market through an intermediary whose business model determines what the trader pays. A market maker quotes a price and earns the spread; an ECN aggregates liquidity and charges a commission; a broker offering both may route according to its own economics. The quoted spread is therefore one component, and the commission, the markup on the swap, and the fill quality are the others.

Two practices deserve particular attention. Last look allows a liquidity provider to reject or re-price a trade after it has been submitted, which means the price seen is not always the price received, particularly around news. And the swap markup is a small charge per night that compounds into a large one over a position held for months, which is why a carry trade's economics cannot be evaluated from the headline swap rate alone.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the venue type: market maker, ECN, or hybrid.
- Record the spread at the times the strategy trades, not the average of the day.
- Record commission per million traded and convert it into pips for the pair.
- Record the swap markup separately from the interbank differential.
- Record whether the venue uses last look and what that implies for news trading.
- Record the fill statistics if the venue publishes them, and treat them as claims.

## Procedure

1. Identify the venue type and the entity behind the quote.
2. Sample spreads at the hours the strategy actually trades.
3. Convert all charges into pips per round trip.
4. Record the swap markup and its effect over the intended holding period.
5. Check the last-look policy and the complaint route.
6. Write the venue assessment with dated samples.

## Anti-patterns

- Comparing venues on advertised spreads measured at the quietest hour.
- Ignoring commission because the spread looked tight.
- Treating a swap quote as the interbank differential.
- Assuming a fill at the quoted price when last look applies.
- Judging a venue from one week of samples.

## Done checklist

- [ ] Venue type and entity recorded.
- [ ] Spreads sampled at trading hours.
- [ ] All charges converted to pips per round trip.
- [ ] Swap markup recorded.
- [ ] Last-look policy recorded.
- [ ] Assessment dated with its samples.

## Sources

- Foreign exchange market structure and turnover: <https://www.bis.org/>
- Market data and rate references: <https://www.federalreserve.gov/>
- Investor protection guidance for retail products: <https://www.investor.gov/introduction-investing>
