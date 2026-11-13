---
name: holder-concentration
domain: crypto-trading/holder-concentration
trigger: "Assessing who holds a token and what their concentration means for exit."
anti_trigger: "Not for tracing a specific wallet's history, and not for price forecasting."
scope: "Top-holder and insider-wallet concentration, treasury and exchange-held balances, and what concentration implies for exit."
status: seedling
---

# Holder concentration

## Standard

Holdings decide who can sell into your exit. A token where ten addresses hold most of the float is not a market; it is a negotiation with ten counterparties who all know their own size. Concentration analysis is therefore an exit-liquidity question first and a governance question second, because concentrated holders can also pass votes.

The data has a known weakness: labels. A wallet marked "team" is a claim by whoever labelled it. Exchange wallets hold customer funds and are not single holders in the economic sense, yet they appear as the largest addresses on most explorers. Good diligence separates what the ledger shows (an address holds X) from what the label asserts (the address belongs to Y).

Primary sources: <https://ethereum.org/en/developers/docs/standards/tokens/> and <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Record the top ten addresses with balances as a percentage of circulating supply, and label each as verified, asserted, or unknown.
- Aggregate by class rather than by address: insiders, treasury, exchanges, funds, unknown.
- Exclude known exchange wallets from "holder" counts and note the exclusion.
- Concentration above one third in insider and treasury classes combined is a recorded finding, not a verdict; state what it enables.
- Where labels are unavailable, state the unknown explicitly; do not infer identity from behaviour alone.
- Re-check concentration after any unlock; the distribution changes when newly unlocked supply moves.

## Procedure

1. Pull the holder table from at least two independent sources; reconcile the top ten.
2. Classify each top address: verified (on-chain identity or issuer disclosure), asserted (third-party label), unknown.
3. Aggregate by class as a percentage of circulating supply.
4. Identify any address that can unilaterally move price at your size; compute the size it would take.
5. Check whether treasury and insider wallets are subject to on-chain vesting or multisig.
6. Record everything with source, date, and confidence.

## Anti-patterns

- Counting exchange hot wallets as whales.
- Treating an explorer's label as verified identity.
- Assuming a token is decentralised because the top holder list has many addresses; one actor can control many.
- Ignoring concentration because the token "has a strong community".
- Reading a single snapshot as the current distribution after an unlock.

## Done checklist

- [ ] Top ten addresses with balances, as percentages, from two sources.
- [ ] Class aggregation (insiders, treasury, exchanges, funds, unknown) with exclusions noted.
- [ ] Addresses able to move price at your size identified, with the size computed.
- [ ] Vesting or multisig status of treasury and insider wallets checked.
- [ ] Unknown labels recorded as unknown.
- [ ] Snapshot date recorded and re-check scheduled after the next unlock.

## Sources

- Ethereum token standards documentation: <https://ethereum.org/en/developers/docs/standards/tokens/>
- Empirical measurement of cascade mechanics on transparent venues: <https://arxiv.org/abs/2608.03616>
- Investor education on ownership and disclosure: <https://www.investor.gov/introduction-investing>
