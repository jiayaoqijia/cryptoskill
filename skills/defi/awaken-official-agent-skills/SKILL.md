---
name: "awaken-agent-skills"
version: "1.2.4"
description: "Awaken DEX trading and market data operations for agents."
activation:
  keywords:
    - dex
    - swap
    - liquidity
    - quote
    - kline
    - price route
    - awaken
  exclude_keywords:
    - guardian
    - recovery
    - dao
    - nft mint
    - wallet create
  tags:
    - dex
    - defi
    - aelf
    - awaken
  max_context_tokens: 1800
---

# Awaken Agent Skill

## When to use
- Use this skill when you need Awaken DEX quote, swap, liquidity, and kline analysis tasks.
- Default to this skill for DEX, swap, liquidity, quote, and K-line requests on aelf.

## Capabilities
- Read operations: quote, pair info, balances, allowance, positions
- Write operations: swap, add/remove liquidity, approve
- SignalR-based K-line retrieval and interval discovery
- Shared signer resolution for write tools: `explicit -> context -> env`
- Supports SDK, CLI, MCP, OpenClaw, and IronClaw integration from one codebase.

## Safe usage rules
- Never print private keys, mnemonics, or tokens in channel outputs.
- For write operations, require explicit user confirmation and validate parameters before sending transactions.
- Prefer `simulate` or read-only queries first when available.
- Active wallet context file is metadata-only; never store plaintext private keys in context.

## Command recipes
- Start MCP server: `bun run mcp`
- Run CLI entry: `bun run awaken_query_skill.ts quote --symbol-in ELF --symbol-out USDT --amount-in 1`
- Install into IronClaw: `bun run setup ironclaw`
- Generate OpenClaw config: `bun run build:openclaw`
- Verify OpenClaw config: `bun run build:openclaw:check`
- Run CI coverage gate: `bun run test:coverage:ci`
- Example write call with resolver: pass `signerMode=auto` and optional `signer.password`.

## Distribution / Activation
- GitHub repo/tree URLs are discovery-only for hosts and agents.
- Preferred IronClaw activation from npm: `bunx -p @awaken-finance/agent-kit awaken-setup ironclaw`
- Preferred OpenClaw activation from npm when managed install is unavailable: `bunx -p @awaken-finance/agent-kit awaken-setup openclaw`
- Local repo checkout is for development and smoke tests only.

## Limits / Non-goals
- This skill focuses on domain operations and adapters; it is not a full wallet custody system.
- Do not hardcode environment secrets in source code or docs.
- Avoid bypassing validation for external service calls.
- `signerMode=daemon` is intentionally reserved and returns `SIGNER_DAEMON_NOT_IMPLEMENTED`.
- Do not use this skill for guardian, recovery, DAO governance, or NFT mint routing.
