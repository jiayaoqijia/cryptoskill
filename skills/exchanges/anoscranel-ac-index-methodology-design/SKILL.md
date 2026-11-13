---
name: ac-index-methodology-design
description: "How an index is built and what that construction decides: eligibility and selection rules, weighting schemes and their consequences, rebalancing frequency and buffers, concentration caps and capping mechanics, the arbitrage created at inclusion and deletion, index integrity and self-serving changes, and the written methodology record. It explains how rules produce an exposure; it never recommends an index product or predicts returns. Use when asking \"index methodology\", \"how should I weight this index\", \"rebalancing buffer\", \"concentration cap\", \"capping mechanics\", \"index inclusion arbitrage\", \"equal weight versus cap weight\", \"design a benchmark\". Not for the return of an index fund (ac-fund-selection), not for factor construction (ac-factor-investing), not for market structure (ac-equity-market-structure)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Index methodology design

## Overview

An index is a rule set that produces a portfolio, and every rule has a consequence. Eligibility criteria decide which securities can be held; the weighting scheme decides how much of each; the rebalancing frequency and the buffers around the selection cut-off decide how much turnover the rules generate; and any concentration cap decides what happens when the largest constituents grow.

Reading an index methodology means tracing those rules to their consequences rather than accepting the index's name as a description. Writing one means choosing the rules with the consequences in view, which is the difference between a benchmark that measures a market and one that measures its own design choices.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## When to use

- When the exposure an index actually provides needs establishing.
- When rebalancing turnover or concentration caps are being assessed.
- When designing a benchmark for a stated purpose.
- When index-driven flows create an apparent opportunity.

## When NOT to use

- For using an index future or option (use ac-equity-index-futures).
- For evaluating a fund that tracks an index (use ac-fund-selection).
- For trading an index change as an event (use ac-special-situations).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/eligibility-and-selection.md` | `investing/eligibility-and-selection` | Gates, screens, and the universe the rules actually admit. |
| `subskills/weighting-schemes.md` | `investing/weighting-schemes` | Cap, equal, fundamental, and what each does to concentration. |
| `subskills/rebalancing-and-buffers.md` | `investing/rebalancing-and-buffers` | Frequency, buffers, and the turnover the rules imply. |
| `subskills/concentration-caps.md` | `investing/concentration-caps` | Caps, capping mechanics, and the drift between reviews. |
| `subskills/inclusion-arbitrage.md` | `investing/inclusion-arbitrage` | The trade created by rules that are known in advance. |
| `subskills/methodology-integrity.md` | `investing/methodology-integrity` | Rule changes, consultation, and self-serving redesign. |
| `subskills/index-design-record.md` | `investing/index-design-record` | The written record: rules, consequences, and review triggers. |

## Status and honest limits

A backtest of an index methodology is a test of a rule set on data where the rule set's consequences were not yet known to the market, so it overstates what a live index would have delivered. Methodologies are also revised, and a revision can change an index's character without changing its name. Nothing here recommends an index or a product built on one, and a methodology that has not been tested for turnover and concentration consequences has not been designed, only described.
