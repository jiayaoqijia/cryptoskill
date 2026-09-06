# Octav API Skill

Agent skill for integrating with the [Octav API](https://octav.fi) — cryptocurrency portfolio tracking, transaction history, and DeFi analytics across 50+ blockchain networks.

## Install

```bash
npx skills add Octav-Labs/octav-api-skill
```

## What it does

This skill teaches AI agents how to use the Octav API to:

- Track wallet balances and net worth across multiple chains
- Query transaction history with filtering and search
- Monitor DeFi protocol positions (Aave, Uniswap, etc.)
- Access historical portfolio snapshots
- Analyze token distribution and holdings
- Pay per request as an autonomous agent via x402, when appropriate

It covers all 25 REST endpoints and instructs agents to default to the API-key REST API, reaching for the [x402 endpoints](https://docs.octav.fi/api/endpoints/agent-x402) only when the user asks for pay-per-call or the agent holds a wallet and no API key.

## Get an API key

Sign up at [data.octav.fi](https://data.octav.fi) to get your API key.

## Links

- [API Documentation](https://docs.octav.fi)
- [Developer Portal](https://data.octav.fi)
- [Discord](https://discord.com/invite/qvcknAa73A)
- [Supported Protocols](https://protocols.octav.fi)
