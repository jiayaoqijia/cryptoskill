---
name: ac-trading-operations-runbook
description: "Operational procedures for a live trading book when the infrastructure misbehaves: pre-flight checks, order and position reconciliation, venue outage response, stuck and partial orders, liquidation and ADL verification, incident logging and postmortems, and automation guardrails. It prescribes procedures; it never recommends a trade, a venue, or a strategy. Use when asking \"the API is down\", \"my order is stuck\", \"positions do not match\", \"the exchange halted withdrawals\", \"reconcile my book\", \"trading ops runbook\". Not for the trade decision record (ac-crypto-trading-discipline), not for venue due diligence (ac-perp-venue-diligence), not for exchange account security (ac-exchange-account-security)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Trading operations runbook

## Overview

Markets fail in ordinary ways: an order endpoint times out, a fill arrives twice, a venue stops withdrawals, a position appears that nobody opened. The difference between an incident and a disaster is whether procedures existed before it started. This skill is those procedures, written as runbooks.

Every leaf assumes something is already wrong. None of them discusses strategy, entry, or edge; they discuss restoring an accurate picture of the book and reducing exposure while the picture is wrong.

Primary sources: <https://sre.google/sre-book/table-of-contents/> and <https://www.bybit.com/en/help-center>.

## When to use

- When an order, position, balance, or withdrawal does not match what the desk believes.
- When a venue reports an outage, a halt, or a change in trading conditions.
- Before every trading session, as the pre-flight ritual.
- After any liquidation, ADL event, or unexpected fill.

## When NOT to use

- For deciding whether to enter or exit a position (use ac-crypto-trading-discipline).
- For evaluating whether a venue is safe before opening an account (use ac-perp-venue-diligence).
- For key or account compromise (use ac-exchange-account-security).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/preflight-checks.md` | `crypto-trading/preflight-checks` | The session ritual: keys, balances, margin, connectivity, clock sync, and kill switches armed. |
| `subskills/order-and-position-reconciliation.md` | `crypto-trading/order-and-position-reconciliation` | Matching the desk's records against venue state, and the daily reconciliation that catches drift early. |
| `subskills/venue-outage-response.md` | `crypto-trading/venue-outage-response` | API failures, halts, and withdrawal freezes: the order of decisions, and what not to do into a gapped book. |
| `subskills/stuck-and-partial-orders.md` | `crypto-trading/stuck-and-partial-orders` | Orders that will not fill or cancel, reduce-only traps, cancel-on-disconnect, and the escalation path. |
| `subskills/liquidation-and-adl-verification.md` | `crypto-trading/liquidation-and-adl-verification` | What to verify after a liquidation or ADL event, what the record must show, and the restart rules. |
| `subskills/incident-log-and-postmortem.md` | `crypto-trading/incident-log-and-postmortem` | The incident record: timeline, impact, cause, fix, and the runbook change that follows. |
| `subskills/automation-safety.md` | `crypto-trading/automation-safety` | Guardrails for automated trading: size caps, rate limits, dead-man switches, staged rollout, rollback. |

## Status and honest limits

Procedures reduce the damage of an incident; they do not prevent one. A runbook that has never been rehearsed is a document, not a capability. The pre-flight leaf is the only one that runs every day; the others should be exercised deliberately, with a paper book, before they are needed live. When a venue behaves in a way no leaf anticipated, the correct action is to reduce exposure and write the situation down, not to invent procedure in the moment.
