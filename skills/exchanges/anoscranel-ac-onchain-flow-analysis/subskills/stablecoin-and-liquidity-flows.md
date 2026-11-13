---
name: stablecoin-and-liquidity-flows
domain: crypto-trading/stablecoin-and-liquidity-flows
trigger: "Reading stablecoin issuance and venue flows as liquidity proxies."
anti_trigger: "Not for judging a stablecoin's solvency, and not for price prediction."
scope: "Stablecoin mint and burn, venue flows, and what they proxy for liquidity."
status: seedling
---

# Stablecoin and liquidity flows

## Standard

Stablecoins are the working capital of crypto markets, and their issuance and movement are the closest thing to an observable liquidity series. A large mint can precede deployment into venues; a wave of redemptions can precede deleveraging. But the chain of inference is long, and each link can break: a mint may sit idle, a transfer to a venue may be a market maker's inventory move, and a redemption may be one large holder rotating rather than a market-wide withdrawal.

The useful discipline is to treat stablecoin flows as one input among several, measured over windows long enough to separate trend from noise, and always paired with the venue-level evidence that would confirm the story.

Primary sources: <https://ethereum.org/en/developers/docs/> and <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Mint and burn are recorded separately from transfers; issuance is not deployment.
- Venue inflows are netted against intra-venue transfers before being read as buying power.
- A stablecoin flow claim is paired with at least one venue-level confirmatory series.
- Redemption waves are read over days, not hours; single transactions are events to investigate.
- Issuer attestations are read as claims by the issuer, with their date.
- Any inference to liquidity carries a confidence level and a falsifier.

## Procedure

1. Pull issuance and redemption series for the stablecoins in scope, with dates.
2. Pull venue-level stablecoin balances for the venues in scope.
3. Net out intra-venue and inter-custody transfers.
4. Compare issuance with venue balances over the same window.
5. State the liquidity inference and the venue evidence that supports or contradicts it.
6. Record with confidence and falsifier.

## Anti-patterns

- Reading a mint as immediate buying.
- Treating one large transfer as market-wide.
- Ignoring issuer attestation dates.
- Using stablecoin flows without any venue-level check.
- Reporting a percentage change on a tiny base.

## Done checklist

- [ ] Issuance and redemption series pulled with dates.
- [ ] Venue balances pulled for the same window.
- [ ] Transfers netted for internal movement.
- [ ] Issuance and venue balance compared.
- [ ] Inference stated with confirming or contradicting venue evidence.
- [ ] Confidence and falsifier recorded.

## Sources

- Ethereum developer documentation on tokens and transfers: <https://ethereum.org/en/developers/docs/>
- Empirical measurement of venue liquidity under stress: <https://arxiv.org/abs/2608.03616>
- Attestation and disclosure context: <https://www.sec.gov/investor>

The two series to keep are issuance and venue balances, collected on the same schedule, because the interesting events are the divergences between them. A week where issuance rises while venue balances fall is a different market from one where both rise, and only the paired series shows it.
