---
name: ac-institutional-operations
description: "The operations plumbing behind institutional trading: order lifecycle from allocation to affirmation, prime brokerage and give-ups, clearing and central counterparties, settlement cycles and fails, margin and collateral calls, custody and asset segregation, securities lending, and the written operations record. It explains the machinery that moves institutional orders; it never recommends a trade and never gives legal or tax advice. Use when asking \"prime broker\", \"give-up\", \"T+1 settlement\", \"central counterparty\", \"margin call process\", \"custody segregation\", \"stock loan recall\", \"trade fails\", \"allocation and affirmation\". Not for the disclosures institutions file (ac-institutional-positioning), not for reading their execution in the tape (ac-institutional-order-flow), not for retail trading operations (ac-trading-operations-runbook)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Institutional operations

## Overview

An institutional trade is a chain of obligations rather than a single transaction. An order is executed by one entity, allocated to several accounts, affirmed by each, given up to a clearing broker, novated to a central counterparty, settled against a custodian, and financed through margin and collateral — and each link has its own timing, its own failure mode, and its own documentation.

That chain is where the institutional footprint becomes visible to the back office rather than to the screen. A large order that appears as a single print in the tape becomes many allocations, several give-ups, and a set of settlement obligations. Understanding the chain is what makes it possible to interpret settlement data, fails, and lending flows, and it is the difference between reading a market from the front office and reading it from the plumbing.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## When to use

- When an institutional order's path from execution to settlement matters.
- When prime brokerage, give-ups, or allocations are being set up.
- When settlement timing, fails, or margin calls affect a position.
- When custody, segregation, or securities lending terms are being assessed.

## When NOT to use

- For filed position disclosures (use ac-institutional-positioning).
- For detecting institutional execution in the tape (use ac-institutional-order-flow).
- For retail trading incident procedure (use ac-trading-operations-runbook).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/order-lifecycle.md` | `investing/order-lifecycle` | Execution, allocation, confirmation, affirmation, and where the chain breaks. |
| `subskills/prime-brokerage.md` | `investing/prime-brokerage` | Give-ups, custody of positions, financing, and the prime broker's role. |
| `subskills/clearing-and-ccps.md` | `investing/clearing-and-ccps` | Novation, margin at the clearing house, and default funds. |
| `subskills/settlement-and-fails.md` | `investing/settlement-and-fails` | Settlement cycles, buy-ins, and what a fail actually costs. |
| `subskills/margin-and-collateral.md` | `investing/margin-and-collateral` | Initial and variation margin, eligibility, haircuts, and the call process. |
| `subskills/custody-and-segregation.md` | `investing/custody-and-segregation` | Nominee, sub-custody, segregation, and rehypothecation. |
| `subskills/securities-lending.md` | `investing/securities-lending` | Recall, rebate, collateral, and the revenue split. |
| `subskills/operations-record.md` | `investing/operations-record` | The written record: counterparties, timelines, obligations, and escalations. |

## Status and honest limits

Settlement cycles, margin methodologies, and lending terms change, and they differ by jurisdiction and by counterparty. The mechanics here describe the standard structures rather than any one firm's documentation, and the confirmation is the authority in every case. Nothing here recommends a trade, and a position whose operational obligations have not been mapped is a position whose risk includes a chain nobody has read.
