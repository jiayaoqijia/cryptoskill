---
name: liquidity-measurement
domain: investing/liquidity-measurement
trigger: "Measuring liquidity honestly rather than quoting volume."
anti_trigger: "Not for predicting price moves, and not for choosing a venue."
scope: "Quoted versus traded liquidity, spreads, depth, and impact proxies."
status: seedling
---

# Liquidity measurement

## Standard

Liquidity has three observable faces: the spread you pay to trade now, the depth available at and around the quote, and the impact your own order would have. Volume is none of those. High volume with a wide spread is a busy market that is expensive to trade in; low volume with a tight spread may be a market where a market maker is present and patient.

The honest measurement uses all three, at your own size. Quote-based measures describe the moment; trade-based measures describe the past. Neither tells you what happens when everyone wants the same side, which is why the stress test is a separate line in the record.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/rules-guidance>.

## Decision rules

- Record spread, depth, and an impact estimate separately; never substitute volume for all three.
- Measure at your own size, not at a round number that flatters the book.
- Compare quoted depth with traded turnover; a large ratio is a question about who trades there.
- Estimate impact from observed fills or from a stated model, and label which.
- Record the stress behaviour separately: what the same measures showed in the last volatile session.
- State the measurement date and time of day.

## Procedure

1. Record the quoted spread and depth at your size.
2. Record turnover over a stated window.
3. Compute the depth-to-turnover ratio.
4. Estimate impact from fills or a labelled model.
5. Pull the same measures for the last stress session.
6. Record all of it with timestamps.

## Anti-patterns

- Using volume as a proxy for liquidity.
- Measuring at a size you would never trade.
- Quoting a spread without the time of day.
- Ignoring stress behaviour because the calm market looks fine.
- Presenting a model-based impact as an observed fill.

## Done checklist

- [ ] Spread, depth, and impact recorded separately.
- [ ] Measured at own size.
- [ ] Depth-to-turnover computed.
- [ ] Impact source labelled.
- [ ] Stress-session comparison recorded.
- [ ] Timestamps recorded.

## Sources

- Regulatory context for market data and execution: <https://www.sec.gov/investor>
- Rule context for trading and reporting: <https://www.finra.org/rules-guidance>
- Investor education on trading costs: <https://www.investor.gov/introduction-investing>

The stress comparison is what separates a measurement from a reassurance. A tight spread in a calm session describes the market's willingness to quote; the same measure during a volatile session describes its willingness to trade, and only the second is relevant when you actually need to exit.
