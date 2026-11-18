---
name: cryptyx-holdings
description: The asset study for the assets a user holds or watches - where each asset stands on its shorter and longer horizons against its own history, what followed similar readings before, and what changed since last time. Use for "how do my assets look", "is SOL stretched", "what happened last time" questions.
---

# CRYPTYX: the asset study on your holdings

Follow the [CRYPTYX router](../cryptyx/SKILL.md). If the assets come from an exchange account, read them first with the [exchange bridge](../cryptyx-exchange-bridge/SKILL.md).

## Each asset: the study

`get_coin_study` for one asset *(free, daily limit)* returns:

- **tactical** (7-14 days) and **structural** (60-180 days) lenses. Each has a `state` (for example stretched, neutral, washed out) and `readings`. Every reading has its z-score against the asset's own history, a tag that follows from the z-score (Very low to Very high), and where it sits against the market (`pctl_market`). Readings marked `positioning` are funding or open-interest readings.
- **what_followed** on each reading at least ±1σ from normal: the asset's past episodes at least as extreme, with forward returns at 7, 30 and 90 days against the asset's base rate. With few episodes, the past episodes are listed one by one (`recent`) instead of averaged; say how many there were.
- **standing** and **risk**: where today's return sits in the asset's own history, volatility and drawdowns.
- **history.label**: how much history the read covers. Quote it verbatim.
- `fit_line`: one line on how the two lenses fit.

For several assets, call it once per asset and keep the comparison to one short table.

How to present it:

1. Open with the `fit_line` and each lens's state in one or two sentences.
2. Name the two or three readings furthest from normal, in plain words, with their z-score and tag.
3. If a reading has history, give it as history: "The last 5 times SOL's 90-day return was this extreme, the next 90 days ranged from −44% to +550%." Always include the number of episodes, the base rate and the history window. Never call it a forecast.
4. For "what followed moves like this", go on to `get_episode_study` ([investigate](../cryptyx-investigate/SKILL.md)).
5. Offer one next step.

## Recurring checks: lead with what changed

When the user checks the same assets on a schedule run by their own agent, open with what moved since the last check ("Since last week: …"). If nothing changed, say so in one line.

## Register

Concise and quantitative. Plain labels in prose; metric codes only if the user wants technical detail. Describe what the engine shows. The user decides what to do.
