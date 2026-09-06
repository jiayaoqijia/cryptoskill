# fomo-research

Smart money research skill for [OpenClaw](https://openclaw.ai). Track top traders, monitor live trades, build watchlists — all powered by [fomo.family](https://fomo.family).

## What it does

Gives your AI agent access to Fomo's smart money social graph through a simple REST API. Leaderboards, live trades, watchlists, and Fomo profile sync.

- Leaderboard of top traders by real PnL (always free)
- Live trade monitoring on Solana + Base
- Watchlists by Fomo handle — we resolve wallet addresses automatically
- Fomo profile sync — pull your follows, start tracking them
- Free polling endpoint for efficient heartbeat patterns
- x402 USDC payments for unlimited access

## Install


### Install

```bash
cd skills
git clone https://github.com/pooowell/fomo-research-skill.git fomo-research
```

## Setup

1. Register for an API key (free, no signup):

```bash
curl -X POST https://api.cope.capital/v1/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-agent"}'
```

2. Save the `cope_` key from the response.

3. Start using endpoints. Everything except `/v1/activity` is free.

## Pricing

- **Free**: 250 activity calls/day, leaderboard/watchlists/polling unlimited
- **x402**: $0.005/call USDC (Base or Solana) after free tier
- Fomo powers the social graph and leaderboard — we only charge for live transaction monitoring

## Links

- **API docs**: https://api.cope.capital/docs
- **Human docs**: https://cope.capital/docs
- **Skill file**: https://cope.capital/skill.md
- **Fomo**: https://fomo.family
- **X**: https://x.com/copedotcapital
