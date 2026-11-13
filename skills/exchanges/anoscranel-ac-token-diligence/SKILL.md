---
name: ac-token-diligence
description: "Structured pre-exposure diligence on a crypto token or protocol: supply and unlock schedules, holder concentration, treasury and runway, governance and admin control, liquidity and market structure, a red-flag checklist, and the written diligence record. It analyses evidence and states confidence; it never recommends a token, predicts a price, or gives investment advice. Use when asking \"should I look at this token\", \"token diligence\", \"unlock schedule\", \"who holds this token\", \"is this token safe\", \"tokenomics review\". Not for venue safety (ac-perp-venue-diligence), not for the trade decision record (ac-crypto-trading-discipline), not for post-event forensics (ac-cascade-forensics)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Token diligence

## Overview

A token position is a claim on a protocol's economics and governance, wrapped in a supply schedule. Diligence is the work of establishing what the claim actually is, what dilutes it, who controls it, and whether you can exit it. This skill is that work, in a fixed order, ending in a written record with an explicit confidence level.

It does not tell you whether a token will appreciate. It tells you what is knowable, what is not, and what you must write down before exposure.

Primary sources for the diligence frame: <https://ethereum.org/en/developers/docs/standards/tokens/> and <https://www.investor.gov/introduction-investing>.

## When to use

- Before any first exposure to a token, whatever the size.
- When a held token changes its supply, governance, or treasury materially.
- When evaluating a claim that a token is "undervalued", "safe", or "backed".
- Before writing or reviewing a diligence record for a book.

## When NOT to use

- For evaluating whether an exchange is safe to trade on (use ac-perp-venue-diligence).
- For the trade decision itself, its sizing, or its journal (use ac-crypto-trading-discipline).
- For tracing wallet flows after an incident (use ac-cascade-forensics).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/token-supply-and-unlocks.md` | `crypto-trading/token-supply-and-unlocks` | Circulating versus total versus max supply, emission schedules, and unlock cliffs with their dates and float arithmetic. |
| `subskills/holder-concentration.md` | `crypto-trading/holder-concentration` | Top-holder and insider-wallet concentration, treasury and exchange-held balances, and what concentration implies for exit. |
| `subskills/treasury-and-runway.md` | `crypto-trading/treasury-and-runway` | Protocol treasury, burn rate, fee revenue, and the runway arithmetic that says whether the thing survives without new buyers. |
| `subskills/governance-and-control.md` | `crypto-trading/governance-and-control` | Admin keys, multisigs, upgradeability, and who can change supply or rules unilaterally. |
| `subskills/liquidity-and-market-structure.md` | `crypto-trading/liquidity-and-market-structure` | Venue depth, market-maker dependence, listings, and the exit-liquidity test at your own size. |
| `subskills/red-flags.md` | `crypto-trading/red-flags` | The checklist that ends a diligence early: unauditable reserves, undisclosed unlocks, paid volume, yield promises, anonymous control. |
| `subskills/diligence-record.md` | `crypto-trading/diligence-record` | The written record: criteria, evidence, confidence, decision, and the review date that forces a re-check. |

## Status and honest limits

Diligence reduces surprise; it does not remove it. Supply schedules can change by governance vote, treasury numbers are self-reported unless verifiable on-chain, and holder data is only as good as the labels behind it. Every finding carries a confidence level, and a diligence record that says "unknown" is doing its job. Absence of evidence is recorded as absence, never as safety.
