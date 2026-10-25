---
name: cryptyx-holdings
description: The coin study for the coins a user holds or watches - where each coin stands on its shorter and longer horizons, what followed similar readings in the coin's history, setups firing or close to firing, and what changed since last week. Use for "how do my coins look", "is SOL stretched", "what happened last time" questions.
---

# CRYPTYX: THE STUDY on your coins

Follow the [CRYPTYX router](../cryptyx/SKILL.md). If the coins come from an exchange account, read them first with the [exchange bridge](../cryptyx-exchange-bridge/SKILL.md).

## Several coins: scan first

`get_heat_check` with up to 25 symbols gives a quick scan: per coin, three gauges (crowd activity, perpetual funding, coin-specific volatility) against the coin's own history, where it sits against the market, and a `changes` block with what moved since 7 days earlier. Use it to pick which coins to study first. Keep the scan to one short table.

## Each coin: THE STUDY

`get_coin_study` for one coin returns:

- **tactical** (7-14 days) and **structural** (60-180 days) lenses. Each has a `state` (for example stretched, neutral, constructive) and `readings`. Every reading has its z-score, a tag (Very low to Very high), and where today sits in the coin's own history (`pctl_own_history`) and against the market (`pctl_market`). Readings marked `positioning` are funding or open-interest readings.
- **what_followed** on each reading at least ±1σ from normal: the coin's past episodes at least as extreme, with forward returns at 7, 30 and 90 days against the coin's base rate. With fewer than 10 episodes, the past episodes are listed one by one (`recent`) instead of averaged; say how many there were.
- **setups_firing** and **next_to_fire** for each lens, with conditions met and evidence tier.
- **setup_history**: forward returns after past firings of today's setups.
- `fit_line`: one line on how the two lenses fit.

How to present it:

1. Open with the `fit_line` and each lens's state in one or two sentences.
2. Name the two or three readings furthest from normal, in plain words, with their tag and percentiles.
3. If a reading has history, give it as history: "The last 5 times SOL's 90-day return was this stretched, the next 90 days ranged from −44% to +550%." Always include the number of episodes and, when given, the base rate. Never call it a forecast.
4. Mention setups firing or close to firing, with their evidence tier.
5. Offer one next step.

## Recurring checks: lead with what changed

When the user checks the same coins on a schedule, open with the scan's `changes` ("Since last week: …"), then study only the coins that moved. If nothing changed, say so in one line.

## Register

Concise and quantitative. Plain labels in prose; metric codes only if the user wants technical detail. Describe what the engine shows. The user decides what to do.
