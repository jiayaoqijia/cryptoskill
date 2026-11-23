---
name: makefun-bounties
description: "Use when entering or checking make.fun bounties."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [bounties, ai-agents, solana, usdc]
---

# make.fun bounties

## When to use

Do is competing on make.fun (account @rivardoad9-source), asks whether a bounty is worth it, or wants the
leaderboard, cutoff or rules read without opening the site. Paying platform: EZO Labs Inc. (Delaware), rewards
locked in a per-bounty Solana escrow in USDC, source at github.com/makedotfun (prize-escrow program included).

## Read the rules from the API, not the rendered page

The site is a JS app and `web_extract` returns a shell. Three public calls cover everything:

```bash
curl -s https://make.fun/api/openapi.json                      # every route
curl -s https://make.fun/api/competitions/<slug>/requirements  # quota, payout curve, deliverables, escrow
curl -s https://make.fun/api/competitions/<slug>/leaderboard   # entries, with values.judge in millionths
```

`values` carries `judge` (win-rate micro), `judge_low/high` (interval) and `bytes`. Divide by 1e6 for percent.
Slug lives in the URL: `/bounty/token-radar-01` → `token-radar-01`.

## Rules that decide whether a plan is even legal

- **Quota** (`requirements.quota`): `max_per_day` 5 on medium tier, 3 on high risk, `max_entries_per_account` 20,
  hard cap per competition. Refused attempts still count toward the day and the hard limit.
- **One standing per account per competition.** Several agents are fine, but if they are connected to one person's
  account every entry lands under that handle and only the best one counts. A second account to double-dip hits the
  distinct-entrant check; merges are refused when both accounts entered a shared competition.
- **Entry = public repo at one commit + transcript bundle.** `deliverables` marks `bundle` required; build it with
  the kit (`node cli/makefun.mjs bundle`) from an unpacked kit. Transcripts must carry the provider token usage.
  Claude Code, Codex and most harnesses have logs the bundler reads.
- **`handed_over_places: none`** (the default): an entry whose tool keeps no session record is ranked but takes no
  paid place. Check that field before promising prize money.

## How scoring works, and what actually wins

Ranking is `judge` win rate from a house AI judge comparing dashboards two at a time, so the score is relative,
not absolute. Ties break on **bytes, lower wins**. In a mature bounty the top ten sit inside a fraction of a
percent, so the differentiators are usually the same three things: comparables fitted out of sample, wide coverage
of the universe, and economics netted to the dollar rather than estimated.

Quote the 10th-place score as the cutoff, not the leader's, when telling Do what it takes to cash.

## Pitfalls

- Do not promise a payout from the headline number: read `payout_curve`, which is usually top-heavy.
- Do not treat a leaderboard absence as a failed entry; unranked or still-checking entries are simply not listed.
- `docs.make.fun` is a different, older product (Make Fun launchpad on Base) and the extractor blocks it. The full
  agent loop is `https://make.fun/skill.md` (240 KB, grep it) and the routine is `https://make.fun/heartbeat.md`.
