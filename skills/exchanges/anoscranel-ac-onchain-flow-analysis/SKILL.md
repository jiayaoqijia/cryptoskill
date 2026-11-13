---
name: ac-onchain-flow-analysis
description: "Reading on-chain flows as evidence: data sources and label quality, exchange inflows and outflows, holder cohorts by age and size, the hard limits of whale watching, stablecoin and liquidity flows, which flow signals have evidence versus folklore, and the written on-chain record. It analyses ledger evidence and states confidence; it never predicts prices or recommends a position. Use when asking \"exchange flows\", \"who is accumulating\", \"whale watching\", \"on-chain analysis\", \"holder cohorts\", \"stablecoin flows\". Not for token supply and governance diligence (ac-token-diligence), not for venue safety (ac-perp-venue-diligence), not for post-event forensics (ac-cascade-forensics)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# On-chain flow analysis

## Overview

A public ledger shows transfers, and transfers are not intentions. The craft of on-chain analysis is the disciplined bridging of the two: what the ledger records, what a label asserts, and what can honestly be inferred when the two are separated. Most published flow commentary collapses that distinction, which is why so much of it sounds confident and predicts so little.

This skill works in one direction only: from the ledger to a stated, confidence-rated inference. It does not tell you what price will do, and it treats any claim about a wallet's identity as a claim, not a fact.

Primary sources: <https://ethereum.org/en/developers/docs/> and <https://arxiv.org/abs/2608.03616>.

## When to use

- When a flow claim (exchange inflow, whale accumulation, stablecoin mint) is part of a decision.
- When assessing whether a move is supported by real ledger activity.
- When building a monitoring set of addresses for a held position.
- Before repeating any on-chain statistic in a memo.

## When NOT to use

- For supply schedules and governance control (use ac-token-diligence).
- For reconstructing a cascade after the fact (use ac-cascade-forensics).
- For venue safety assessment (use ac-perp-venue-diligence).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/data-sources-and-labels.md` | `crypto-trading/data-sources-and-labels` | Explorers, indexers, and label providers, and the difference between a verified and an asserted identity. |
| `subskills/exchange-flows.md` | `crypto-trading/exchange-flows` | Inflows and outflows, what they can and cannot imply, and the custodian-versus-exchange ambiguity. |
| `subskills/holder-cohorts.md` | `crypto-trading/holder-cohorts` | Age and size cohorts, cost-basis proxies, and cohort behaviour over a cycle. |
| `subskills/whale-watching-limits.md` | `crypto-trading/whale-watching-limits` | The hard limits: labels, sybil clusters, omnibus wallets, OTC settlement, and what cannot be known. |
| `subskills/stablecoin-and-liquidity-flows.md` | `crypto-trading/stablecoin-and-liquidity-flows` | Stablecoin mint and burn, venue flows, and what they proxy for liquidity. |
| `subskills/flow-signals-and-failures.md` | `crypto-trading/flow-signals-and-failures` | Which flow signals have evidence versus folklore, and the false positives that retire naive rules. |
| `subskills/onchain-record.md` | `crypto-trading/onchain-record` | The written on-chain record: claim, ledger evidence, label status, confidence, and falsifier. |

## Status and honest limits

The ledger is public; the meaning of a transfer is not. A large transfer to an exchange can be a deposit to sell, a custody reshuffle, or a market maker moving inventory. Label providers disagree, exchange wallets are omnibus, and a single actor can control many addresses. Every finding therefore carries a confidence level and names the label source; where identity is asserted rather than verified, the record says so.
