---
name: ac-perp-venue-diligence
description: "Due diligence on a perpetual-futures venue before capital is committed: is the book real (quoted depth vs traded turnover, flat-slippage red flags), what the fee and clearance structure actually costs (liquidation clearance fees are a cascade amplifier), how deep the backstop is today (insurance fund vs open interest, ADL, exchange continuity), what the venue publishes, whether you can hold an account there, and the custody/counterparty exposure. Ends in a written scorecard. It evaluates venues; it never recommends one and never predicts prices. Use when asking \"is this exchange safe\", \"venue due diligence\", \"is this book real\", \"insurance fund depth\", \"can I trade perps here\", \"exchange risk\", \"compare perp venues\". Not for the liquidation-hunt analysis itself (ac-liquidation-hunt-analysis), not for trade records or risk budget (ac-crypto-trading-discipline), not for codebase security review (ac-security-engineer)."
license: MIT
metadata:
  domain: crypto-trading
---

# ac-perp-venue-diligence

## Overview

`ac-perp-venue-diligence` establishes a systematic, evidence-graded framework for evaluating perpetual swap derivatives exchanges before committing capital or deploying execution strategies. In digital asset derivatives markets, venue failure, illusory liquidity, hidden clearance fees, and opaque backstop mechanisms frequently create catastrophic tail risk. For official exchange guidelines and regulatory standards, consult primary portals such as <https://www.binance.com/en/fee/futuresFee> and <https://www.cftc.gov/PressRoom/PressReleases/9241-26>.

Exchanges present polished interfaces and advertised depth metrics that often diverge sharply from execution reality. By applying microstructure stress tests, fee-stack arithmetic, and regulatory verification, traders and researchers can separate robust venues from fragile platforms. This skill operates strictly as an analytical framework; it never recommends specific venues, never suggests trading directions, and never provides financial advice.

## When to use

- Evaluating whether a newly considered perpetual swap exchange possesses genuine liquidity or illusory order books.
- Auditing the complete cost stack of a derivatives venue, including maker/taker fees, funding rate mechanics, liquidation penalties, and tax wrappers.
- Examining venue backstop resilience, insurance fund capitalization relative to open interest, and historical exchange continuity during market stress.

## When NOT to use

- For analyzing liquidation cascade mechanics, stop hunts, or order-flow imbalances (use `ac-liquidation-hunt-analysis`).
- For maintaining trade journals, defining position sizing rules, or managing risk budgets (use `ac-crypto-trading-discipline`).
- For conducting internal source code security reviews or smart contract audits (use `ac-security-engineer`).

## Structure

The skill is organized into a routing index of seven independent subskills, each addressing a distinct pillar of derivatives venue diligence:

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/liquidity-realism.md` | `crypto-trading/liquidity-realism` | Quoted depth vs traded turnover, flat slippage red flags, and small-order testing protocols. |
| `subskills/fee-and-clearance-structure.md` | `crypto-trading/fee-and-clearance-structure` | Maker/taker fees, funding mechanics, liquidation clearance penalties, and statutory tax cost wrappers. |
| `subskills/backstop-and-continuity.md` | `crypto-trading/backstop-and-continuity` | Insurance fund capitalization, auto-deleveraging, exchange operational disruptions, and reserve proofs. |
| `subskills/data-transparency.md` | `crypto-trading/data-transparency` | Transparency ladder, public API endpoints for liquidations, order books, and historical trade feeds. |
| `subskills/jurisdiction-and-access.md` | `crypto-trading/jurisdiction-and-access` | Product access tests, statutory tax rules, and CFTC regulatory frameworks for derivative products. |
| `subskills/counterparty-and-custody.md` | `crypto-trading/counterparty-and-custody` | Custody models, mid-cascade withdrawal rail resilience, stablecoin counterparty risks, and exit timing. |
| `subskills/venue-scorecard.md` | `crypto-trading/venue-scorecard` | Written diligence record, scored dimensions, weighted risk thresholds, and decision gating. |

## Status and honest limits

- Status: seedling.
- Honest limits: Venue diligence provides structural verification of past and current exchange parameters; it cannot predict sudden insolvency events, rogue insider actions, or unforeseen regulatory black swans. All metrics are bound to specific timestamped observations and public data feeds.
- Public citations: Grounded in official exchange documentation, regulatory filings, academic microstructure literature, and verified incident reports (Kyle, 1985; Binance incident disclosures, 2026; CFTC regulatory releases).
- See official documentation and regulatory disclosures for primary verification before capital commitment: <https://www.cftc.gov/PressRoom/PressReleases/9241-26> and <https://www.binance.com/en/fee/futuresFee>.
