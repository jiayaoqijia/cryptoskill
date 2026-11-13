# Koinju Agent Skill

A [Claude Code](https://claude.com/claude-code) skill for working with the **Koinju** multi-exchange crypto market-data API ([koinju.io](https://koinju.io)). Helps Claude discover, query, and integrate Koinju data — REST endpoints, ClickHouse SQL, OHLCV / trade / option-chain / funding-rate / market-discovery — into research, backtesting, and production pipelines.

## Install

Via the [skills.sh](https://skills.sh) CLI (recommended):

```bash
npx skills add https://gitlab.com/koinju-public/agent-skill        # into ./.claude/skills/
npx skills add https://gitlab.com/koinju-public/agent-skill -g     # global ~/.claude/skills/
```

Or clone manually:

```bash
git clone https://gitlab.com/koinju-public/agent-skill.git ~/.claude/skills/koinju
```

Update to the latest version:

```bash
npx skills update koinju        # add -g if you installed globally
```

Then in any Claude Code session, the skill triggers automatically on Koinju- and crypto-data-related queries. See `SKILL.md` for the workflow and `references/` for the bundled documentation.

## Command examples this skill helps with 

1. Setup environement to test koinju api
2. What bitcoin pdocuts are available on koinju
2. Retrieve the historical price data for BTC-USDT for the past 7 days using the koinju API
3. Plot the option smile for BTC for okx and bybit using the koinju API data
4. Retrieve the implied volatility for BTC-USDT options from the koinju API
6. What is the current bitcoin volatility ?
7. Optimize the query that computes the average price of LINK-USDT over the past year using koinju
9. Bench mark this strategy (mention script ) against a simple buy and hold strategy using koinju data
10. We have a postgres database with historical price data for a lot of crypto, how can I integrate it with the koinju API to enhance my trading strategy?
11. We already have a clickhouse database with some historical data, how can we integrate it with the koinju API to enhance our trading strategy?
12. Our trading system uses redis for caching, how can we use the koinju API to update our cache with the latest price data for BTC-USDT?


## Credentials

Don't have credentials yet? Sign up at [koinju.io/pricing](https://koinju.io/pricing) — Koinju emails you a link to [dataroom.koinju.io](https://dataroom.koinju.io) where the REST key and ClickHouse host / user / password live. See `references/auth.md` for the env-var layout.
