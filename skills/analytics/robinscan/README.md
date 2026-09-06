# Robinscan Skill

[![skills.sh](https://skills.sh/b/robinscan/robinscan-skill)](https://skills.sh/robinscan/robinscan-skill)

An AI agent skill for querying [Robinhood Chain](https://robinscan.io) blockchain data.

## Install

```bash
npx skills add robinscan/robinscan-skill
```

## What it does

Teaches any AI agent how to query Robinhood Chain (chain ID 4663) for:

- **Network stats** — gas prices, ROH price, transaction volume
- **Wallet lookups** — transaction history, token holdings
- **Token transfers** — ERC-20/721/1155 movement tracking
- **Transaction logs** — decoded event data and contract interactions
- **Tokenized stocks** — real-time prices for on-chain equities (AAPL, TSLA, NVDA, etc.)
- **Live blocks** — real-time chain activity

## Compatible with

Any agent framework that supports skills or function calling:

Claude Code, Claude Desktop, Cursor, Windsurf, Codex, GitHub Copilot, Gemini, Cline, Zed, OpenCode, and more.

## API

All data comes from `https://robinscan.io` — no API key required.

## License

MIT
