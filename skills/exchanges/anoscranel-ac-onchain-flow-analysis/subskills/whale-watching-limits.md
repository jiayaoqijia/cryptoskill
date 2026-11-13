---
name: whale-watching-limits
domain: crypto-trading/whale-watching-limits
trigger: "Stating what on-chain analysis cannot know before making a whale claim."
anti_trigger: "Not for attributing addresses to people, and not for price prediction."
scope: "The hard limits: labels, sybil clusters, omnibus wallets, OTC settlement, and what cannot be known."
status: seedling
---

# Whale-watching limits

## Standard

The limits are the most valuable part of on-chain analysis because they bound every claim that follows. Labels can be wrong; one actor can run thousands of addresses; exchange wallets hide whose coins are inside; over-the-counter settlement never touches a public order book; and the largest holders are often entities whose on-chain footprint is a custody arrangement rather than a position.

A claim that respects these limits is narrow and useful: this address class moved this much, over this window, with this label confidence. A claim that ignores them is a story about a whale that may be three addresses owned by the same fund.

Primary sources: <https://ethereum.org/en/developers/docs/> and <https://www.sec.gov/investor>.

## Decision rules

- Every whale claim states what could make it wrong: a label error, a cluster, an omnibus wallet, an OTC leg.
- Wallet count is never evidence of distinct holders; sybil resistance requires more.
- Exchange-internal movement is excluded before any concentration claim.
- Identity is never inferred from behaviour alone; behaviour is recorded as a hypothesis.
- Where a claim depends on a single label provider, it is marked single-source and its confidence is capped.
- The limit statement is written before the finding, so the finding cannot exceed it.

## Procedure

1. Write the limit list for this question before pulling data.
2. For each planned claim, name the limit it could breach.
3. Pull the data with exclusions applied.
4. Test the claim against each limit; downgrade confidence where a limit binds.
5. Record the surviving claim with its stated bound.
6. Keep the limit statement with the record for review.

## Anti-patterns

- Treating address count as holder count.
- Naming an entity because the timing looked right.
- Ignoring OTC settlement when reading exchange balances.
- Presenting a label-dependent claim as verified.
- Writing the limits after the conclusion.

## Done checklist

- [ ] Limit list written before data pull.
- [ ] Each claim mapped to the limits it could breach.
- [ ] Exclusions applied before analysis.
- [ ] Confidence downgraded where a limit binds.
- [ ] Surviving claim recorded with its bound.
- [ ] Limit statement retained with the record.

## Sources

- Ethereum developer documentation on address and contract data: <https://ethereum.org/en/developers/docs/>
- Disclosure and entity-identity context: <https://www.sec.gov/investor>
- Investor education on concentration and risk: <https://www.investor.gov/introduction-investing>

Write the limits into the record even when the finding survives them, because the next reader will not otherwise know what was ruled out. A claim with its limits attached is reusable; a claim without them has to be re-derived from scratch, and usually is not.
