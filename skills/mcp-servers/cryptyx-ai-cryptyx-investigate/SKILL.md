---
name: cryptyx-investigate
description: Going deeper after the asset study - every prior instance of a move (breakdown, breakout, flush, capitulation) and what followed, how one reading has behaved over time, and testing an idea with a backtest. Use when the user asks "is this move real", "what happened last time", "why", or wants to test something.
---

# CRYPTYX: going deeper

Follow the [CRYPTYX router](../cryptyx/SKILL.md). Use this skill after the first read in [cryptyx-holdings](../cryptyx-holdings/SKILL.md). Tools marked *Pro* return an upgrade message for free accounts. Relay that message plainly.

## Every prior instance: the episode study

`get_episode_study` *(free, 3 a day)* for one asset and a preset (for example `breakdown`, `capitulation`) finds every past episode that met the same condition and shows what followed each at 7, 30 and 90 days, against the asset's all-days base rate.

- Quote the number of episodes, the median and hit rate next to the base rate, the t-stat and the random-entry test. Under 20 episodes, say "small sample; indicative only" word for word.
- Say how much history the study covers, using `history.label` verbatim.
- Show a compact table of the episodes (date, the defining readings, 7, 30 and 90-day return, max dip). Use each precedent's `text` field for where today ranks.
- History, not a forecast.

## Going further

| The user asks… | Tool | Notes |
| --- | --- | --- |
| How has one reading behaved over time, and what followed its extremes? | `analyze_metric` *(Pro)* | Pass the reading's `metric_id`; speak in its plain label. |
| Did several readings together lead anywhere before? | `analyze_metrics_composite` *(Pro)* | Show sample size and the range of outcomes, not only the average. Flag small samples. |
| Where is this reading extreme across the market today? | `scan_metric_universe` *(Pro)* | One metric across 200+ assets. |

To test or build an idea of their own, go to [cryptyx-build-setup](../cryptyx-build-setup/SKILL.md).

## Register

- Answer the question asked, then offer one further step.
- Plain labels in prose; metric codes only on request, in `code` formatting after the plain label.
- Label interpretation as interpretation. Historical results are history, not forecasts.
