# ownerwatch skill

`SKILL.md` is a portable [Agent Skill](https://modelcontextprotocol.io): drop it
into a coding agent (Claude Code, Cursor, Copilot and others that read the
`SKILL.md` standard) and the agent learns to answer "who controls this EVM
contract?" — owners, proxy admins, Safes, timelocks, AccessControl and
AccessManager roles — and to prove a finding with a simulation.

It pairs with the [ownerwatch-mcp](../README.md) server (read-only MCP tools) but
also works on its own with the `ownerwatch` CLI and a public RPC. Everything is
read-only: no key, no wallet, nothing sent on-chain.

## Install

- **Claude Code:** copy `SKILL.md` into a folder under `~/.claude/skills/evm-contract-control-audit/` (or your project's `.claude/skills/`).
- **Other agents:** place `SKILL.md` wherever that agent loads skills from.

The skill will install and drive `ownerwatch` for you, or call the
ownerwatch-mcp tools if the server is configured.
