---
name: liquidity-and-market-structure
domain: crypto-trading/liquidity-and-market-structure
trigger: "Testing whether you can exit a token at your own size, on the venues that list it."
anti_trigger: "Not for entry timing, and not for market making."
scope: "Venue depth, market-maker dependence, listings, and the exit-liquidity test at your own size."
status: seedling
---

# Liquidity and market structure

## Standard

Exit liquidity is the question diligence answers last and remembers longest. A token can be economically sound and still be unsellable at size, because the order book is thin, the volume is incentivised, or a single market maker supplies most of the quotes and may withdraw them exactly when you need them.

Volume is not liquidity. Reported volume can be manufactured by wash trading, by incentive programmes that pay for trades, or by a market maker cycling inventory. Depth is closer to the truth: what a book will absorb at a stated price impact. The diligence test is concrete: at your intended size, what is the slippage, and who is on the other side.

Primary sources: <https://ethereum.org/en/developers/docs/standards/tokens/> and <https://doi.org/10.1093/jjfinec/nbt003>.

## Decision rules

- Test at your own size, not at a round number that flatters the book.
- Compare quoted depth to daily turnover; a depth multiple far above turnover is the signature of a book nobody trades against.
- Identify whether volume is incentivised (rebates, points, mining) and record the programme and its expiry.
- Record venue concentration: if most volume sits on one venue, that venue is a single point of failure for exit.
- A token listed on one venue has one exit; treat it as illiquid until proven otherwise.
- If market-maker arrangements are undisclosed, record them as unknown and treat the quoted depth as conditional.

## Procedure

1. Collect venues, daily turnover, and quoted depth at two percent impact.
2. Compute the depth-to-turnover ratio and record it.
3. Check for incentive programmes driving volume, with expiry dates.
4. Place a small test order if permitted, and record observed slippage against quoted.
5. Identify the market-maker footprint if visible; otherwise record unknown.
6. Write the exit test: your size, estimated slippage, and the venues that can absorb it.

## Anti-patterns

- Treating reported volume as exit capacity.
- Testing at a size you would never trade.
- Assuming multi-venue listings mean multi-venue liquidity; the same maker often quotes both.
- Ignoring incentive expiry dates, which can remove volume abruptly.
- Extrapolating calm-market depth to a stressed market.

## Done checklist

- [ ] Venues, turnover, and depth at two percent impact collected with dates.
- [ ] Depth-to-turnover ratio computed and interpreted.
- [ ] Incentive programmes and expiries identified.
- [ ] Observed slippage from a test order recorded, if available.
- [ ] Market-maker dependence assessed or marked unknown.
- [ ] Exit test at your own size written.

## Sources

- Empirical market-microstructure measurement of liquidity: <https://doi.org/10.1093/jjfinec/nbt003>
- Ethereum token standards documentation: <https://ethereum.org/en/developers/docs/standards/tokens/>
- Investor education on trading costs and disclosure: <https://www.investor.gov/introduction-investing>
