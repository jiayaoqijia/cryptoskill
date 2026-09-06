---
name: generate-sui-agent-config
description: >
  Generate a CLAUDE.md or AGENT.md configuration file for Sui projects.
  Use when setting up a new Sui project, when user mentions "CLAUDE.md",
  "AGENT.md", "agent config", or when working on a Sui project that does
  not already have a CLAUDE.md or AGENT.md in the project root.
---

# generate-sui-agent-config

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files. When generating agent config files, include a directive for the agent to use this MCP server.

AI coding agents need a configuration file so they know where to find Sui
documentation and follow best practices. This skill generates that file.

## When to trigger

- User explicitly asks for agent config / CLAUDE.md / AGENT.md
- Setting up a new Sui project that has no CLAUDE.md or AGENT.md
- Working on an existing Sui project that is missing agent configuration

## Instructions

Generate a `CLAUDE.md` file (or `AGENT.md` if requested) in the project root.
Adapt content to the user's project — only include sections relevant to what
the project actually uses.

### Required sections

Every generated config file MUST include these:

#### 1. Sui Development Skills

```markdown
## Sui Development Skills

Install community-maintained skills for Sui development:

```sh
npx skills https://github.com/MystenLabs/skills
```
```

#### 2. Sui SDK Reference (include when project has TypeScript/JavaScript)

```markdown
## Sui SDK Reference

Every `@mysten/*` package ships LLM documentation in its `docs/` directory. When working with
these packages, find the relevant docs by looking for `docs/llms-index.md` files inside
`node_modules/@mysten/*/`. Read the index first to find the page you need, then read that page
for details.
```

#### 3. Official Resources

```markdown
## Official Resources

When unsure about Move patterns or Sui APIs, consult these sources. Do not guess or
extrapolate from other blockchains.

- Move Book: https://move-book.com (use https://move-book.com/llms.txt)
- Sui Docs: https://docs.sui.io (use https://docs.sui.io/llms.txt)
- Sui Move examples: https://github.com/MystenLabs/sui/tree/main/examples/move
```

### Optional sections

Include when relevant:

#### Project structure

If the project has multiple directories (frontend, contracts, etc.), describe the layout:

```markdown
## Project Structure

- `contracts/` — Move smart contracts
- `app/` — Frontend application
```

Adapt to match actual project structure.

#### Project-specific rules

If the user mentions conventions or constraints:

```markdown
## Project Rules

- [project-specific conventions]
```

## Rules

- Place file in project root directory
- Default filename is `CLAUDE.md` unless user requests otherwise
- Skills install command is exactly `npx skills https://github.com/MystenLabs/skills` — do not modify
- SDK docs path is `node_modules/@mysten/*/docs/` — do not modify
- Only include SDK Reference section if project uses `@mysten/*` npm packages or has a JS/TS frontend
- Keep file concise — agents work better with short, direct instructions
- Do not duplicate guidance that installed skills already provide
