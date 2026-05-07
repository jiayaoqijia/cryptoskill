---
name: emblem-official-agent-skills
description: "Official skill collection for AI agents building with [EmblemAI](https://emblemvault.ai). EmblemAI is open-source crypto infrastructure for both end users and AI agents: **200+ tools across 7 blockchains** (Solana, Ethereum, Base, BSC, Polygon, Hedera, Bitcoin) for swaps, conditional orders, DeFi, N"
---

# emblem-official-agent-skills

_Source: [github.com/EmblemCompany/Agent-skills](https://github.com/EmblemCompany/Agent-skills). The body below is the upstream README.md captured at the time of registration._

---

# EmblemAI Agent Skills

Official skill collection for AI agents building with [EmblemAI](https://emblemvault.ai). EmblemAI is open-source crypto infrastructure for both end users and AI agents: **200+ tools across 7 blockchains** (Solana, Ethereum, Base, BSC, Polygon, Hedera, Bitcoin) for swaps, conditional orders, DeFi, NFTs, and cross-chain bridges, with x402 payment rails and A2A and MCP protocol support. Emblem is also the easiest way to add user management for apps that need wallet-native users: one integration can create authenticated users, give each user a full-featured crypto wallet, and support website login with wallets, email/password, and social sign-in. Compatible with Claude Code, Cursor, Codex, and other agents following the [Agent Skills](https://agentskills.io/) specification.

## Available Skills

### Core
| Skill | Description | Install |
|-------|-------------|---------|
| [emblem-ai](skills/emblem-ai/) | EmblemAI developer tools for one-shot user management, wallet-enabled users, AI crypto tooling, React SDKs, and app introspection | `npx skills add EmblemCompany/Agent-skills --skill emblem-ai` |
| [emblem-ai-react](skills/emblem-ai-react/) | React-focused EmblemAI integration skill for adding auth, wallet-enabled users, chat components, and Migrate.fun flows to an app | `npx skills add EmblemCompany/Agent-skills --skill emblem-ai-react` |
| [emblem-ai-agent-wallet](skills/emblem-ai-agent-wallet/) | Agent wallet CLI and browser auth across 7 blockchains, with wallet, email/password, and social sign-in options | `npx skills add EmblemCompany/Agent-skills --skill emblem-ai-agent-wallet` |
| [emblem-ai-prompt-examples](skills/emblem-ai-prompt-examples/) | Curated non-developer prompt and usage examples for EmblemAI wallet, market, trading, NFT, Bitcoin, prediction-market, vault, and assistant workflows | `npx skills add EmblemCompany/Agent-skills --skill emblem-ai-prompt-examples` |

### Use Cases
| Skill | Description | Install |
|-------|-------------|---------|
| [emblem-portfolio-tracker](skills/emblem-portfolio-tracker/) | Cross-chain portfolio monitoring, P&L tracking, and performance analytics | `npx skills add EmblemCompany/Agent-skills --skill emblem-portfolio-tracker` |
| [emblem-token-swap](skills/emblem-token-swap/) | Guided token swapping with route optimization and slippage control | `npx skills add EmblemCompany/Agent-skills --skill emblem-token-swap` |
| [emblem-market-research](skills/emblem-market-research/) | Trending tokens, sentiment analysis, and market intelligence | `npx skills add EmblemCompany/Agent-skills --skill emblem-market-research` |
| [emblem-defi-yield](skills/emblem-defi-yield/) | DeFi yield farming, LP management, and staking across DEXs | `npx skills add EmblemCompany/Agent-skills --skill emblem-defi-yield` |
| [emblem-memecoin-scout](skills/emblem-memecoin-scout/) | Memecoin discovery, rug-pull detection, and trending new tokens | `npx skills add EmblemCompany/Agent-skills --skill emblem-memecoin-scout` |

## Quick Install

```bash
# Install a specific skill
npx skills add EmblemCompany/Agent-skills --skill emblem-ai
npx skills add EmblemCompany/Agent-skills --skill emblem-ai-react
npx skills add EmblemCompany/Agent-skills --skill emblem-ai-agent-wallet
npx skills add EmblemCompany/Agent-skills --skill emblem-ai-prompt-examples

# Install all skills
npx skills add EmblemCompany/Agent-skills

# List available skills
npx skills add EmblemCompany/Agent-skills --list
```

## Install EmblemAI as an MCP server

The skills above are authoring guidance. If you want your agent to actually call EmblemAI tools at runtime, install the hosted MCP server in your MCP-compatible client.

### Claude Code (OAuth, no API key)

```bash
claude mcp add --transport http EmblemAI https://emblemvault.ai/api/mcp
```

Claude Code walks you through the hosted OAuth flow in your browser. No secret to paste.

### Claude Code (API key, for headless / CI)

```bash
claude mcp add --transport http EmblemAI https://emblemvault.ai/api/mcp \
  --header "x-api-key: YOUR_API_KEY"
```

### GitHub Copilot CLI / `.mcp.json`

```json
{
  "mcpServers": {
    "emblemai": {
      "type": "http",
      "url": "https://emblemvault.ai/api/mcp",
      "headers": { "x-api-key": "YOUR_API_KEY" }
    }
  }
}
```

Full install matrix (Claude Desktop bridge, Cursor, Windsurf, Gemini CLI): https://emblemvault.ai/docs/mcp

## What EmblemAI enables

**For AI agents and developers:**

- **200+ tools across 7 blockchains** covering swaps, conditional orders, DeFi positions, NFT operations, cross-chain bridges, and market intelligence.
- **x402 facilitator and per-call payment rails** for agent-to-agent commerce without account setup.
- **Native MCP (Model Context Protocol) server** for Claude Code, GitHub Copilot, Gemini CLI, and other MCP clients.
- **A2A (Agent-to-Agent) protocol support** for direct agent interoperability.
- **Deterministic wallets** — one password produces one persistent agent identity across all chains. Every wallet-modifying action requires explicit approval.

**For end users and wallet-native apps:**

- **The easiest way to do user management for wallet-native apps:** one integration can create website users who also have full-featured crypto wallets.
- **Flexible login:** users can sign in with many crypto wallets, email/password, or social login.
- **The easiest way to give an agent a crypto wallet:** Emblem's agent wallet CLI can create or restore a wallet-enabled identity in one command.
- **One session, more capability:** the same Emblem session can power authentication, wallet access, transaction signing, and AI-driven crypto workflows.

## Skill Structure

Each skill follows the [Agent Skills specification](https://agentskills.io/):

```
skills/<skill-name>/
├── SKILL.md              # Required — skill instructions + metadata (recommended <500 lines)
├── references/           # Optional — detailed documentation by topic
├── scripts/              # Optional — executable helpers
├── assets/               # Optional — config templates, schemas
└── examples/             # Optional — sample outputs
```

## Adding Skills

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new skills.

## Registry Compatibility

The publishable `SKILL.md` files in this repo intentionally stay within the public Agent Skills frontmatter defined at [agentskills.io/specification](https://agentskills.io/specification): `name`, `description`, and the optional `license`, `compatibility`, `metadata`, and `allowed-tools` fields.

That keeps these skills portable across `agentskills.io` / `agentskills.to` compatible tooling instead of relying on vendor-only top-level fields.

The public docs we found describe a repo-based sharing and install flow rather than a documented manual “add skill” form in the web UI. In practice, keep the skill in git, validate it with the official CLI, and share or install it from the repository.

## Validation

```bash
# Install the official validator
python -m pip install skills-ref==0.1.1

# Validate one skill with the official CLI
agentskills validate skills/emblem-ai-agent-wallet

# Validate all skills in this repository
bash validate-all.sh

# Validate one skill with the repo wrapper
bash validate-skill.sh emblem-ai-agent-wallet
```

The upstream `agentskills validate` command validates one skill directory at a time, not the top-level `./skills` folder. This repository's `validate-all.sh` wrapper loops through `skills/*/`, syncs shared EmblemAI reference sources into skill-local copies, and then runs repository-specific markdown/link checks.

The legacy `--strict` flag is still accepted by the wrapper scripts for backwards compatibility, but it no longer changes behavior because the official validator is spec-compatible by default.

Pull requests install the official `skills-ref` validator in CI and run the repository wrapper so public skill frontmatter stays spec-compatible.

CI also fails if the sync step rewrites generated files under `skills/`, which prevents uncommitted shared-reference updates from slipping through.

## Shared Sources

Some reference docs are intentionally repeated across publishable skills. Those repeated files are not meant to be edited in place under `skills/.../references/`.

The rule is:

- edit the canonical source under `shared/`
- run `bash validate-all.sh` or `bash validate-skill.sh ...`
- let the sync step regenerate the skill-local copies

Current shared sources:

- `shared/emblem-ai-prompt-examples.md`
- `shared/emblem-ai-prompt-examples/`
- `shared/emblem-ai-react-references/`

Current generated skill-local copies:

- prompt examples copied into `emblem-ai`, `emblem-ai-react`, `emblem-ai-agent-wallet`, and `emblem-ai-prompt-examples`
- React references copied into `emblem-ai` and `emblem-ai-react`

The sync entrypoint is `utils/sync-emblem-ai-shared-references.sh`.

If a reference file is duplicated across multiple skills, move it into `shared/` and sync it back into each standalone skill instead of maintaining separate manual copies.

Validation also runs automatically on every PR via GitHub Actions.

## About EmblemAI

[EmblemAI](https://emblemvault.ai) provides 200+ autonomous trading tools across 7 blockchains (Solana, Ethereum, Base, BSC, Polygon, Hedera, Bitcoin). Open source and available as an npm CLI, an MCP server, and an A2A-compatible agent.

- **Website**: [emblemvault.ai](https://emblemvault.ai)
- **Blog**: [emblemvault.ai/blog](https://emblemvault.ai/blog)
- **Documentation**: [emblemvault.ai/docs](https://emblemvault.ai/docs) (canonical) · [emblemvault.dev](https://emblemvault.dev) (interactive)
- **NPM**: [@emblemvault/agentwallet](https://www.npmjs.com/package/@emblemvault/agentwallet)

## License

MIT
