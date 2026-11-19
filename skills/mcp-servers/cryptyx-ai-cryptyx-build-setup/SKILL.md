---
name: cryptyx-build-setup
description: Go all the way down the CRYPTYX stack - from one reading to a multi-factor, multi-horizon combination of your own, tested on the asset's history with the full analytics (episodes, hit rate, Sharpe, drawdowns, base rate). Use when the user wants to test or build their own idea ("what happened when BTC funding was this negative?", "test trend efficiency above 1.5 sigma with negative funding"), not to read today's state.
---

# CRYPTYX: build and test your own idea

Follow the [CRYPTYX router](../cryptyx/SKILL.md). This is the deepest path: the user brings an idea and tests it on the CRYPTYX engine. Tools marked *Pro* return an upgrade message for free accounts. Relay that message plainly.

## The engine, layer by layer

CRYPTYX is modular. Each layer is built from the one below, and the user can enter at any layer and build upward.

| Layer | What it is | Example |
| --- | --- | --- |
| **Readings** | Hundreds of metrics across eight factor families: trend, trend efficiency, volatility, flows, futures positioning, order book, options and correlation. Each is scored daily as a z-score against the asset's own trailing year and ranked against the market. | 60-day trend efficiency at +1.8σ |
| **Horizons** | The same factor measured over several windows, from days to a year. Tactical readings (7–14 days) and structural readings (60–180 days) answer different questions; keep them separate and never blend them. | Volatility over 7 days vs over 90 days |
| **Conditions** | A threshold on a reading, or the gap between two readings (for example a short window against a long one). | Funding below −1σ |
| **Combinations** | Two to four conditions across different factor families holding at once. Most of the engine's depth is here: one reading alone is often noise. | Trend efficiency high AND funding negative |

Bring this structure out when it helps the user see where their idea sits and what the next layer could add. Do not lecture.

## The journey

| Step | Tool | Use |
| --- | --- | --- |
| Find readings that matter for the asset | `get_featured_metrics` *(Pro)* with `asset` | Ranked by how well each reading has related to later returns (IC). A lead to test, not a result. |
| Or start from today | A reading from the asset study (`get_coin_study`); `scan_metric_universe` *(Pro)* for where a reading is extreme across assets | Use the `metric_id` from the response. Never guess one. |
| Test one reading | `analyze_metric` *(Pro)*: `asset`, `metric_id`, `operator` (`gt`, `lt`, `gte`, `lte`, `abs_gt`), `threshold` in σ | Every horizon from 1 day to 365 days. |
| Combine factors | `analyze_metrics_composite` *(Pro)*: `asset`, `conditions[]` (2–4) | Prefer conditions from different factor families. Compare with each condition alone. |
| Every prior instance of a move | `get_episode_study` *(free, 3 a day)*: a preset, or your own z-score conditions on Pro | What followed each episode at 7, 30 and 90 days, with the t-stat and a random-entry test. |

## Report the full analytics

A result is the whole profile, never one number. For each test, report:

- **Sample:** days observed (`n_observations`), episodes (`n_triggers`, separated by the cooldown), how often the condition holds (`trigger_rate`), and days excluded as data artefacts (`n_pinned_excluded`). Overlapping days mean independent episodes are fewer.
- **Returns, per horizon:** median and mean, best and worst, and spread (`std_return`).
- **Against the base rate, per horizon:** `median_vs_base` and `hit_rate_vs_base`, the asset's every-day result over the same period. A 60% hit rate on an asset that rose on 58% of all days is not an effect.
- **Hit rate:** share of episodes with a positive return.
- **Risk-adjusted:** Sharpe (annualised), withheld under 10 episodes.
- **Path risk:** drawdown along the way: average (`max_dd_mean`), bad case (`max_dd_p95`) and worst (`max_dd_worst`). A setup can end up and still fall 30% first.
- **Every horizon side by side:** short and long horizons often disagree, and that is information. `best_horizon` is picked after the fact and flatters.
- **Warnings:** relay `warnings` verbatim.

Suggested shape: the setup in plain words → sample → a table of horizons (median, mean, hit rate, base rate, Sharpe, drawdowns) → warnings → one possible next step (another factor, another horizon, or a similar asset).

Lead with medians, because a few large moves pull the mean. Under 15 episodes, say the sample is too small to separate an effect from chance.

## Tuning is where false edges come from

Each threshold, reading or horizon tried is another draw. Try enough and one will look strong by chance.

- Say how many variants were tried in the session when reporting the best one.
- Prefer round thresholds (1, 1.5, 2) set before looking.
- A real effect holds across nearby thresholds, on neighbouring horizons and on similar assets. Offer those checks before anything else.
- Up to four conditions. Each extra condition shrinks the sample.

## Register

- Plain labels in prose; metric codes only on request, in `code` after the label.
- Never call a result "proven", "reliable" or an "edge". It is a historical result on one asset.
- The user built the idea: "your condition was followed by…", not "CRYPTYX found…".
- History is history, not a forecast. No advice to buy, sell, add or trim.
- Send asset symbols only, never balances or account identifiers.
