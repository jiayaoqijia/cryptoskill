---
name: open-interest-reading
domain: crypto-trading/open-interest-reading
trigger: "Analyze open interest quadrants, post-cascade resets, and cross-venue definition discrepancies."
anti_trigger: "Interpret open interest changes without confirming price action context or volume."
scope: "Interprets open interest price quadrants, post-cascade resets, and cross-venue definition differences."
status: seedling
---

## Standard
Open interest (OI) measures the total number of outstanding derivative contracts held by market participants, serving as a primary indicator of capital flow and market engagement. Interpreting OI requires mapping changes alongside price action into four distinct quadrants: rising price with rising OI (strong new long capital entering), rising price with falling OI (short covering rally), falling price with rising OI (aggressive new short positioning), and falling price with falling OI (long liquidation washout). Each quadrant implies different structural motivations among leveraged participants.

Post-cascade OI resets provide critical evidence regarding market health following liquidations. A sharp drop in OI accompanied by massive liquidation volume clears leveraged excess, resetting funding rates toward neutral levels and establishing a durable base for subsequent price movement. However, cross-venue definition discrepancies complicate analysis; exchanges compute and report open interest using different methodologies, such as counting single-leg notional versus dual-leg contract value, or denominating figures in coin units versus USD value. Analysts must verify venue calculation standards before aggregating cross-platform OI data.

Primary sources for the claims in this step: <https://www.intotheblock.com/learning-center/open-interest/> and <https://academy.glassnode.com/derivatives/open-interest>.

## Decision rules
- Classify market structure changes by cross-referencing price direction with open interest expansion or contraction.
- Verify whether reported open interest figures are denominated in coin units or USD notional value.
- Treat sharp drops in open interest combined with high liquidation volume as a structural reset of leveraged positioning.
- Avoid treating rising open interest as inherently bullish or bearish without identifying whether longs or shorts drive the expansion.
- Cross-verify open interest data across multiple independent reporting APIs to detect venue-specific reporting artifacts.

## Procedure
1. Retrieve current price and open interest time series data from primary perpetual futures venues.
2. Calculate percentage changes in price and open interest over standard time windows (one-hour, four-hour, twenty-four-hour).
3. Map the current state into one of the four price-OI quadrants and record the structural interpretation.
4. Monitor post-cascade periods for open interest contraction magnitude and funding rate normalization.
5. Standardize cross-venue open interest units into common USD notional terms for comparative analysis.

## Anti-patterns
- Interpreting high open interest as a sign of impending market collapse without checking funding rate levels.
- Confusing trading volume with open interest; volume measures turnover, while OI measures outstanding contracts.
- Comparing raw contract counts across venues with different contract multipliers and margin structures.
- Ignoring the impact of cash-settled versus coin-margined contracts on open interest valuation during price trends.

## Done checklist
- [ ] Price and open interest changes mapped into structural quadrants.
- [ ] Open interest units standardized into USD notional terms across venues.
- [ ] Post-cascade OI contraction and funding normalization evaluated.
- [ ] Cross-venue reporting discrepancies checked against exchange specifications.
- [ ] Capital flow interpretation logged with supporting price context.

## Sources
- Glassnode Metrics and Documentation on Open Interest and Derivatives: https://academy.glassnode.com/derivatives/open-interest
- IntoTheBlock Research on Crypto Derivatives and Open Interest Quadrants: https://www.intotheblock.com/learning-center/open-interest/
