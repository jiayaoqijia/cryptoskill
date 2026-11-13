---
name: ac-special-situations
description: "Trading corporate events as their own category: merger arbitrage spread arithmetic and break risk, spin-off mechanics and when-issued trading, tender offers and odd-lot provisions, rights issues and rump placement, index deletion and forced-seller flows, deal timeline risk and regulatory approvals, and the written event record. It explains the mechanics and the arithmetic of event positions; it never opines on whether a deal will close and never recommends a position. Use when asking \"merger arbitrage\", \"deal spread\", \"break risk\", \"spin-off\", \"when-issued\", \"tender offer\", \"odd lot tender\", \"rights issue\", \"index deletion\", \"forced sellers\". Not for accounting or price adjustment of corporate actions (ac-corporate-actions), not for activist stakes and filings (ac-institutional-positioning), not for the investment case (ac-equity-research)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Special situations

## Overview

A special situation is an event that changes a security's identity or ownership within a defined window: a merger, a spin-off, a tender offer, a rights issue, an index deletion. Each creates a position whose return depends on the event completing rather than on the business performing, and each has its own arithmetic, its own timeline, and its own way of failing.

This skill covers that arithmetic and the mechanics around it. The common structure is a spread: the price difference between the security and the consideration that will replace it, annualised over the expected timeline, with the break scenario defined. The skill does not forecast outcomes; it makes the payoff explicit so that a view about the event can be expressed and reviewed.

Primary sources: <https://www.sec.gov/investor> and <https://www.sec.gov/edgar/search/>.

## When to use

- When a merger, tender, or exchange offer creates a spread.
- When a spin-off or rights issue changes what a share represents.
- When an index event is expected to force selling or buying.
- When a position's return depends on a deal completing.

## When NOT to use

- For the accounting and price adjustment of corporate actions (use ac-corporate-actions).
- For activist filings and ownership thresholds (use ac-institutional-positioning).
- For the fundamental case on a company (use ac-equity-research).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/merger-spread-arithmetic.md` | `investing/merger-spread-arithmetic` | Gross and net spread, annualisation, and the break scenario. |
| `subskills/deal-timeline-and-risk.md` | `investing/deal-timeline-and-risk` | Approvals, financing, and the events that break a deal. |
| `subskills/spin-off-mechanics.md` | `investing/spin-off-mechanics` | Distribution ratios, when-issued trading, and index inclusion. |
| `subskills/tender-and-odd-lot.md` | `investing/tender-and-odd-lot` | Tender mechanics, proration, and odd-lot priority provisions. |
| `subskills/rights-issues.md` | `investing/rights-issues` | Subscription rights, rump placement, and the arbitrage. |
| `subskills/index-deletion-flows.md` | `investing/index-deletion-flows` | Forced selling, deletion candidates, and the flow estimate. |
| `subskills/event-record.md` | `investing/event-record` | The written record: spread, timeline, break case, and review dates. |

## Status and honest limits

Event outcomes are binary and the analysis is probabilistic at best. A spread that looks generous is usually pricing a real risk, and the size of the spread is the market's estimate of the break probability compounded with the time value of the position. Nothing here predicts whether a deal closes, and a position held through an approval decision without the break case written down is a position whose worst outcome has not been considered.
