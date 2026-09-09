---
name: research
description: "Research any token, wallet, or contract with the ChainGPT Web3 toolkit. Composes live market data (DexScreener), security flags (GoPlus + Honeypot.is), on-chain history (Etherscan v2), portfolio holdings (Moralis), AND ChainGPT-native context (crypto news + AI signals + Solidity LLM audits) into a single workflow. Use when a user asks 'what is this token', 'is this rug', 'is this address safe', 'should I buy X', 'is this wallet a whale', or wants to research anything on-chain. Triggers: token research, rug check, honeypot check, wallet research, whale tracking, address risk, contract verification, ChainGPT intel."
---

# ChainGPT Research Skill

When a user wants to research a token, wallet, or contract — your job is to orchestrate the right sequence of MCP tools from this plugin into a coherent answer. Do **not** call the SDKs raw; the MCP tools are pre-tuned for credit efficiency and AI enrichment.

## Core principle: one-shot if you can

If the user asks "research X" without further qualifiers, prefer the single AI-enriched call:

```text
chaingpt_intel_token   query="X"
```

It composes market + risk + ChainGPT news + AI signals in one response and costs ~1 ChainGPT credit (the news fetch). This is what 80% of "research this token" prompts should do.

For a wallet:

```text
chaingpt_intel_wallet  address="0x…"
```

Composes portfolio (Moralis) + per-holding risk-rating (GoPlus). **Requires `MORALIS_API_KEY`** for the portfolio scan — without it, the tool returns a setup hint pointing to https://moralis.io (free 25k req/month tier). The GoPlus risk-rating layer is always free.

## When to fan out to specific tools

Use the granular tools when the user wants depth on one axis the intel call summarized.

| User intent | Tool | Notes |
|---|---|---|
| Live price + volume + liquidity | `chaingpt_research_token` | DexScreener; no key |
| Which pools / pairs exist | `chaingpt_research_pairs` | sort by liquidity |
| Trending right now | `chaingpt_research_trending` | boosted tokens on DexScreener |
| Wallet portfolio (multi-chain) | `chaingpt_wallet_balances` | needs `MORALIS_API_KEY` for ERC-20 scan |
| Wallet DeFi positions | `chaingpt_wallet_positions` | Aave / Uniswap / Lido / etc. |
| Wallet realized P&L | `chaingpt_wallet_pnl` | tax-season report style |
| Token safety flags | `chaingpt_risk_token` | GoPlus — honeypot/mintable/proxy/tax |
| Buy+sell simulation | `chaingpt_risk_honeypot` | Honeypot.is — real simulation |
| Is this address a scammer | `chaingpt_risk_address` | sanctions / phishing / mixer |
| Source code & ABI of a contract | `chaingpt_risk_contract_source` | Etherscan v2 verified source |
| Decode a specific transaction | `chaingpt_onchain_tx` | status / gas / method |
| Address recent activity | `chaingpt_onchain_address` | last 25 txs |
| Current gas prices | `chaingpt_onchain_gas` | safe / standard / fast |
| ChainGPT-curated news | `chaingpt_news_fetch` | filter by token/category |

## Recommended chains and graceful fallback

The plugin supports 11 chains out of the box: `ethereum, base, arbitrum, optimism, polygon, bsc, avalanche, blast, linea, scroll, solana`.

Some tools degrade gracefully when optional API keys are absent:

- **Without `MORALIS_API_KEY`**: `chaingpt_wallet_balances` returns native-coin balances only via public RPC; positions and PnL return a setup hint. **Recommend** the user get a free 25k-req/month key at https://moralis.io.
- **Without `ETHERSCAN_API_KEY`**: on-chain + contract-source tools work but hit a low rate limit. Recommend a free key at https://etherscan.io/myapikey.
- All risk tools work key-free.

## The "research → audit" funnel

When the research surfaces a contract that looks interesting or suspicious, the next step is the existing ChainGPT audit tool:

```text
chaingpt_risk_contract_source  address="…" chain="…"      # get source
chaingpt_audit_contract        sourceCode="…"             # AI audit
```

Always recommend this pair when:
- The user is about to interact with an unknown contract.
- GoPlus flagged a risk that needs a human-readable explanation.
- The contract is a proxy and the user needs to know what the implementation does.

## What this skill does NOT do

- It does **not** execute transactions, sign anything, or move funds. All tools are read-only.
- It does **not** generate strategies or trading signals beyond surfacing ChainGPT's own AI signal output.
- For execution / contract deployment, see the (upcoming) `chaingpt-deploy` and `chaingpt-trade` skills.

## Output style

Always lead with the most important fact: "It's a honeypot," "It's verified and looks safe," "Price is $X with $Y liquidity," etc. Then surface the supporting evidence with tool names so the user can dig deeper. End with one concrete recommended next action.
