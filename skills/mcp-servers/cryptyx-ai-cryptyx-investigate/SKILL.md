---
name: cryptyx-investigate
description: Going deeper after the coin study - what else stands out across a few coins, a setup's composition and track record, how one reading has moved over time, and testing an idea with a backtest or custom trigger. Use when the user asks "why", "what else", or wants to test something.
---

# CRYPTYX: going deeper

Follow the [CRYPTYX router](../cryptyx/SKILL.md). Use this skill after the first read in [cryptyx-holdings](../cryptyx-holdings/SKILL.md). Tools marked *Pro* return an upgrade message for free accounts. Relay that message plainly.

## What else stands out

`get_notable_read` with 1-10 symbols *(free, daily limit)* returns, per coin, the three readings furthest from the coin's own norm across all 670+ metrics, each with a one-line summary (own-history and market percentile), plus setups firing or close to firing with their evidence tier, hit rate against the coin's base rate and an `evidence_note`. It also shows what changed since 7 days earlier.

- A **pooled record** combines every past episode across the coins a setup applies to (for example BTC, ETH and SOL), each measured on its own history: more episodes and a steadier read, but not specific to one coin. Say so when quoting it.
- Mention a reading's change only when its tag moved ("very high, normal a week ago").

## Going further

| The user asks… | Tool | Notes |
| --- | --- | --- |
| How has one reading moved over time? | `analyze_metric` *(Pro)* | Pass the reading's `metric_id`; speak in its plain label. |
| What goes into that setup? | `get_setup_details` *(Pro)* | Pass the setup's `setup_id`. Composition and history. |
| Did readings like this lead anywhere before? | `evaluate_custom_trigger` or `backtest_signal` *(Pro)* | Show sample size and the range of outcomes, not only the average. Flag small samples. |
| What's the market backdrop? | `get_regime_analysis` *(Pro)* | Present it as context, not as a call. |

To test or build an idea of their own, go to [cryptyx-build-setup](../cryptyx-build-setup/SKILL.md).

## Register

- Answer the question asked, then offer one further step.
- Plain labels in prose; metric and setup codes only on request, in `code` formatting after the plain label.
- Label interpretation as interpretation. Historical results are history, not forecasts.
