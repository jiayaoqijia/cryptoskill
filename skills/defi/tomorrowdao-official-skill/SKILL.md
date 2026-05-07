---
name: "tomorrowdao-agent-skills"
version: "0.2.2"
description: "TomorrowDAO governance, BP, and resource operations for agents."
activation:
  keywords:
    - dao
    - proposal
    - vote
    - bp
    - governance
    - resource
    - tomorrowdao
  exclude_keywords:
    - wallet
    - dex
    - explorer
    - guardian
    - swap
  tags:
    - dao
    - governance
    - aelf
    - tomorrowdao
  max_context_tokens: 1800
---

# TomorrowDAO Agent Skill

## When to use
- Use this skill when you need DAO governance and resource operations in TomorrowDAO ecosystems.
- Default to this skill for DAO proposal, vote, BP, governance, and resource workflows.

## Capabilities
- DAO domain: create/update/proposal/discussion operations
- Token helpers: allowance view, approve payload/sent call, balance view
- DAO read helpers: proposal my-info, DAO token allowance view alias, DAO token balance view alias
- Network governance and BP election operation set
- Resource token trading with unified ToolResult/TxReceipt outputs
- Shared signer resolution for send mode: `explicit -> context -> env`
- Send mode blocks direct contract sends when the resolved signer is `CA`; use an explicit CA forward transport instead.
- Supports SDK, CLI, MCP, OpenClaw, and IronClaw integration from one codebase.

## Safe usage rules
- Never print private keys, mnemonics, or tokens in channel outputs.
- For write operations, require explicit user confirmation and validate parameters before sending transactions.
- Prefer `simulate` or read-only queries first when available.
- For CA orchestration flows, use `simulate` payloads from this skill together with an explicit CA forward transport for the actual write.
- Active wallet context stores identity pointers only; never persist plaintext private keys.
- A `CA` keystore may unlock the manager key, but this skill still rejects direct target-contract sends for `CA` identities.

## Command recipes
- Start MCP server: `bun run mcp`
- Run CLI entry: `bun run cli`
- Install into IronClaw: `bun run setup ironclaw`
- Generate OpenClaw config: `bun run build:openclaw`
- Verify OpenClaw config: `bun run build:openclaw:check`
- Run CI coverage gate: `bun run test:coverage:ci`
- For cross-skill signing, pass `signerMode=auto` and optional password in `signer`.

## Distribution / Activation
- GitHub repo/tree URLs are discovery-only for hosts and agents.
- Preferred IronClaw activation from npm: `bunx -p @tomorrowdao/agent-skills tomorrowdao-setup ironclaw`
- Preferred OpenClaw activation from npm when managed install is unavailable: `bunx -p @tomorrowdao/agent-skills tomorrowdao-setup openclaw`
- Local repo checkout is for development and smoke tests only.

## Limits / Non-goals
- This skill focuses on domain operations and adapters; it is not a full wallet custody system.
- Do not hardcode environment secrets in source code or docs.
- Avoid bypassing validation for external service calls.
- `signerMode=daemon` is reserved and currently returns `SIGNER_DAEMON_NOT_IMPLEMENTED`.
- Do not use this skill for wallet lifecycle, DEX trading, guardian, or explorer routing.
