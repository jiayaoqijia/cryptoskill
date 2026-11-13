---
name: trade-size-clustering
domain: investing/trade-size-clustering
trigger: "Looking for algorithmic execution in the distribution of trade sizes."
anti_trigger: "Not for identifying the participant, and not for predicting direction."
scope: "Round lots, repeated sizes, and the signature of algorithmic working."
status: seedling
---

# Trade size clustering

## Standard

An algorithm working a large order slices it into many smaller trades, often at sizes set by a schedule rather than by opportunity. That produces a distribution that differs from the market's natural one: repeated identical sizes, round numbers, and a cadence in time. A single trader buying once would not produce that distribution; a hundred traders trading on their own would not either, because their sizes would be idiosyncratic.

The read is statistical. A cluster of identical sizes around a round number, repeating across minutes, is consistent with a single algorithm. It does not say whether the algorithm is buying or selling — that requires knowing which side the aggressor was on, which the tape can supply through the trade's direction — and it does not say whether the order is a client's or the broker's own.

Primary sources: <https://www.finra.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the distribution of trade sizes over the window examined.
- Identify the modal size and whether it is a round lot.
- Record the cadence: the intervals between trades of that size.
- Record the aggressor side for those trades, using the venue's trade direction where available.
- Compare the distribution with the same name's baseline over previous sessions.
- Record the alternative explanation: a busy market, a retailed flow, or an auction.

## Procedure

1. Pull the trade tape for the window.
2. Build the size distribution and identify the mode.
3. Measure the cadence of the modal size.
4. Classify aggressor side for the clustered trades.
5. Compare with a baseline session.
6. Write the observation with its alternative explanation.

## Anti-patterns

- Treating every large print as institutional.
- Ignoring the aggressor side, which decides accumulation versus distribution.
- Reading clustering in a heavily traded name as unusual.
- Assuming a round size implies one participant.
- Skipping the baseline comparison.

## Done checklist

- [ ] Size distribution recorded.
- [ ] Modal size and round-lot status recorded.
- [ ] Cadence measured.
- [ ] Aggressor side classified.
- [ ] Baseline compared.
- [ ] Alternative explanation recorded.

The cadence is the stronger of the two signals: size alone can be mimicked by a busy market, but a regular interval between similarly sized trades, sustained across a session, is hard to produce without an algorithm. Even so, the algorithm could be a broker working a client order or a market maker replenishing inventory, and the tape cannot distinguish the two.


## Sources

- Trading and reporting guidance: <https://www.finra.org/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on execution quality: <https://www.investor.gov/introduction-investing>
