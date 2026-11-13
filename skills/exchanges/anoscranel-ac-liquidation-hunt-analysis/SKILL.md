---
name: ac-liquidation-hunt-analysis
description: "Reading a set-up that looks like a liquidation hunt: the mechanical chain of forced liquidations, an audit of the folklore claims (heatmaps, cumulative volume delta, top-trader ratios, fake-volume figures), the short list of things that actually have evidence (clustering by UTC hour, order-flow imbalance, funding and open-interest extremes, venue backstop state), after-the-fact cascade forensics, venue and backstop risk, the surviving risk posture, and the honest measurement layer. It analyses, never predicts, never executes, never recommends a direction. Use when asking \"liquidation hunt\", \"stop hunt\", \"liquidation cascade\", \"is this a hunt\", \"where are the liquidation levels\", \"cascade forensics\", \"should I fade this wick\". Not for the trade decision record, risk budget, or journal (use ac-crypto-trading-discipline), not for generic research method (ac-deep-researcher), not for citation conventions (ac-evidence-and-citation)."
license: MIT
metadata:
  domain: crypto-trading
---

# ac-liquidation-hunt-analysis

## Overview

`ac-liquidation-hunt-analysis` provides rigorous analytical framing for market set-ups where leveraged positions experience forced liquidation. In high-leverage digital asset markets, price wicks and rapid reversals are frequently attributed to intentional "liquidation hunts" or coordinated stop runs. This skill establishes what mechanics are real, what indicators belong to folklore, what empirical evidence actually survives verification, and what risk posture traders should maintain. 

This skill analyses historical and live structural mechanics; it never predicts future price direction, never executes orders, and never recommends trading positions. Its purpose is to replace speculative narratives with audited empirical boundaries.

## When to use

- Evaluating whether a rapid price rejection or liquidity sweep exhibits mechanical liquidation characteristics.
- Auditing popular indicators such as liquidation heatmaps, cumulative volume delta (CVD), and top-trader long/short ratios against empirical evidence.
- Examining past cascade events to understand branching ratios, order-flow imbalances, and venue backstop mechanics.
- Designing risk management frameworks that account for volatility clustering, leverage multiplier effects, and maintenance margin ratios.
- Setting up repeatable data collection pipelines for public exchange endpoints and historical liquidation logs.

## When NOT to use

- For managing day-to-day trade journals, position sizing rules, or risk budgets (use `ac-crypto-trading-discipline`).
- For conducting open-ended multi-source academic literature searches or broad qualitative investigations (use `ac-deep-researcher`).
- For formatting reference bibliographies, checking citation styles, or validating quote integrity (use `ac-evidence-and-citation`).

## Subskill index

| Leaf | Domain segment | Scope (one line) |
| :--- | :--- | :--- |
| [`subskills/cascade-anatomy.md`](subskills/cascade-anatomy.md) | `crypto-trading/cascade-anatomy` | Examines the mechanical chain from margin calls to forced market orders and maintenance margin rules. |
| [`subskills/folklore-audit.md`](subskills/folklore-audit.md) | `crypto-trading/folklore-audit` | Audits four widespread claims (heatmaps, CVD, top-trader ratios, fake volume) against empirical standards. |
| [`subskills/what-has-evidence.md`](subskills/what-has-evidence.md) | `crypto-trading/what-has-evidence` | Details empirical findings on UTC time clustering, order-flow imbalance, and funding rate extremes. |
| [`subskills/cascade-forensics.md`](subskills/cascade-forensics.md) | `crypto-trading/cascade-forensics` | Outlines after-the-fact forensic methods for measuring branching ratios and reconstructing cascade events. |
| [`subskills/venue-and-backstop-risk.md`](subskills/venue-and-backstop-risk.md) | `crypto-trading/venue-and-backstop-risk` | Evaluates exchange risk parameters including clearance fees, quoted depth ratios, and insurance funds. |
| [`subskills/risk-posture.md`](subskills/risk-posture.md) | `crypto-trading/risk-posture` | Defines surviving risk practices such as gap-based sizing, margin distance buffers, and strict prohibitions. |
| [`subskills/measurement-layer.md`](subskills/measurement-layer.md) | `crypto-trading/measurement-layer` | Specifies data collection workflows using public API endpoints, custom collectors, and vendor tiers. |

## Status and honest limits

Status: `seedling`. 

The analytical frameworks contained herein are subject to four major structural absences identified in the 2026 research corpus: (1) no validated real-time liquidation hunt detector exists; (2) no empirical decomposition of liquidated trader populations is publicly accessible; (3) granular order-book depth-by-hour collection lacks public infrastructure; and (4) heatmap predictive accuracy remains unvalidated pending structured empirical studies. All analytical conclusions must operate within these verified boundaries.
