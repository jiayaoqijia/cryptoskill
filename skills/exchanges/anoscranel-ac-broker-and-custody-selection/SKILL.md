---
name: ac-broker-and-custody-selection
description: "Choosing where to hold investment assets: custody structure and beneficial ownership, what happens if the broker fails, the full fee stack including FX and inactivity costs, execution quality and routing, conflicts and how the provider earns, access and transfer friction, and the written provider record. It evaluates the plumbing that holds the assets; it never recommends a firm and never predicts returns. Use when asking \"which broker\", \"is my broker safe\", \"custody\", \"segregated assets\", \"transfer my account\", \"why is the FX fee so high\", \"payment for order flow\". Not for evaluating funds themselves (ac-fund-selection), not for crypto venue diligence (ac-perp-venue-diligence), not for equity market mechanics (ac-equity-market-structure)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Broker and custody selection

## Overview

A portfolio is only as reachable as the plumbing that holds it. Two accounts offering the same funds can differ in who legally owns the assets, what happens if the firm fails, how much of the return disappears in conversion and custody fees, and how easily the assets can be moved elsewhere. Those differences are rarely visible in a commission table, and they matter most in the situations where the investor has the least room to manoeuvre.

This skill evaluates the provider rather than the product. It covers the legal structure behind an account, the insolvency path, the cost stack, execution quality, the incentives that shape what a provider recommends, and the friction of leaving. It does not name firms, and it does not judge whether a provider's investment ideas are good.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## When to use

- When opening an account or consolidating several.
- When comparing two providers offering the same investments.
- When a provider changes its fee schedule, custody terms, or ownership.
- When a transfer, withdrawal, or closure proves harder than expected.

## When NOT to use

- For choosing a fund or ETF (use ac-fund-selection).
- For due diligence on a crypto perpetual venue (use ac-perp-venue-diligence).
- For auction, settlement, and market-structure mechanics (use ac-equity-market-structure).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/custody-structure.md` | `investing/custody-structure` | Nominee and omnibus holding, beneficial ownership, and what the account holder actually owns. |
| `subskills/broker-insolvency.md` | `investing/broker-insolvency` | What happens to assets if the firm fails, and how long recovery takes. |
| `subskills/broker-fee-stack.md` | `investing/broker-fee-stack` | Commission, spread, FX conversion, custody and inactivity fees, and the total cost of holding an account. |
| `subskills/execution-quality.md` | `investing/execution-quality` | Routing, best execution, and how to measure the slippage a provider actually delivers. |
| `subskills/conflicts-and-incentives.md` | `investing/conflicts-and-incentives` | How the provider earns, and what its incentives do to the advice and the order flow. |
| `subskills/access-and-transfer.md` | `investing/access-and-transfer` | Withdrawal limits, transfer friction, jurisdiction restrictions, and the cost of leaving. |
| `subskills/broker-record.md` | `investing/broker-record` | The written provider record: structure, cost, controls, and review triggers. |

## Status and honest limits

Provider terms change without notice, and a comparison written last year may describe a firm that no longer exists in that form. The record therefore carries dates and review triggers, and it treats marketing claims about safety as claims rather than facts. Nothing here is a recommendation of any firm, and where an account holds a large share of a household's assets, the structure questions belong with a professional who can read the local insolvency and compensation rules.
