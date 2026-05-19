---
name: blockscout-official-agent-skills
description: "A collection of AI agent skills for working with the Blockscout ecosystem — blockchain explorers, APIs, and supporting services."
---

# blockscout-official-agent-skills

_Source: [github.com/blockscout/agent-skills](https://github.com/blockscout/agent-skills). The body below is the upstream README.md captured at the time of registration._

---

# Blockscout Agent Skills

A collection of AI agent skills for working with the Blockscout ecosystem — blockchain explorers, APIs, and supporting services.

Each skill is a self-contained directory of structured instructions and helper scripts that give an AI agent domain expertise in a specific area. Skills follow the markdown-based format compatible with Claude Code, Codex, Cursor, OpenClaw, Claude Cowork, and other agents that support skill/instruction loading.

## Skills

| Skill | Description |
|-------|-------------|
| [blockscout-analysis](blockscout-analysis/) | Modular skill for blockchain data analysis and scripting using the Blockscout MCP Server. Guides agents to use native tools, REST API scripts, or hybrid flows for multi-chain EVM data. |
| [web3-dev](web3-dev/) | Build web3 applications, scripts, CLIs, bots, and mobile/desktop clients that read blockchain data via the Blockscout PRO API — a single HTTP API spanning 100+ EVM chains. Sibling to `blockscout-analysis` (which targets the MCP server). |

## Prerequisites

Different skills depend on different Blockscout backends. Pick the row that matches the skill you want to install:

| Skill | Requires |
|-------|----------|
| `blockscout-analysis` | Blockscout MCP server (auto-configured by the Claude Code and Codex plugins; configured manually for other agents — see below) |
| `web3-dev` | Blockscout PRO API key (no MCP server involved) |

## Setup

Each skill is a directory with a `SKILL.md` entry point and supporting docs/scripts. Integration depends on your agent platform — see examples below. In the snippets below, replace `<skill>` with the directory name of the skill you want to install (e.g. `blockscout-analysis`, `web3-dev`).

### Skills CLI (40+ agents)

One command installs a skill to 40+ coding agents (Claude Code, Codex, Cursor, Cline, Copilot, Windsurf, Continue, and more):

```sh
npx skills@latest add https://github.com/blockscout/agent-skills --skill <skill>
```

Use `-g` to install globally, or `-a <agent>` to target a specific agent. See [skills.sh/docs](https://skills.sh/docs) for the full list of supported agents and options.

> **Note:** The Skills CLI installs the skill instructions only. Skill-specific backends (MCP server for `blockscout-analysis`, PRO API key for `web3-dev`) are **not** configured automatically — see [Prerequisites](#prerequisites).

### Claude Code

For `blockscout-analysis`, no separate MCP server configuration is needed — it is set up automatically as part of the plugin installation. For `web3-dev`, you still need to provide a PRO API key (see [Prerequisites](#prerequisites)).

```sh
claude plugin marketplace add blockscout/agent-skills
claude plugin install <plugin>@blockscout-ai
```

Replace `<plugin>` with `blockscout-analysis` or `web3-dev` (or run the install command once per plugin).

### Claude Desktop (Chat / Cowork / Code)

Must be configured separately for Chat/Cowork and for Code by the same procedure.

1. Choose **Customize** in the sidebar:

   ![Customize in sidebar](assets/Claude-Add-Pluging-00-Custmize.png)

2. Choose **Browse plugins** → **Personal** → **Add marketplace from GitHub**:

   ![Add marketplace from GitHub](assets/Claude-Add-Pluging-01-Add-Marketplace.png)

3. Enter the GitHub repo ID `blockscout/agent-skills` and press **Sync**:

   ![Enter repo ID](assets/Claude-Add-Pluging-02-Marketplace-GitHub.png)

4. The marketplace **blockscout-ai** will appear in the list of Personal plugins. Click **Install** on each skill plugin you want (`blockscout-analysis`, `web3-dev`):

   ![Install plugin](assets/Claude-Add-Pluging-03-Install-Plugin.png)

5. Once installed, the plugin details are available in the **Customize** window:

   ![Plugin info](assets/Claude-Add-Pluging-04-Plugin-Info.png)

6. If the plugin has MCP servers associated (e.g. `blockscout-analysis`), their info will be available in the **Connectors** sub-item:

   ![Plugin connector](assets/Claude-Add-Pluging-05-Plugin-Connector.png)

### Codex CLI / Codex App

Add the marketplace first, then enable the skill plugin from inside Codex via the `/plugin` slash command (the command opens an interactive picker). For `blockscout-analysis`, the Blockscout MCP server is auto-configured by the plugin — no manual MCP setup required. For `web3-dev`, provide a PRO API key (see [Prerequisites](#prerequisites)).

```sh
codex plugin marketplace add blockscout/agent-skills
```

Then run `codex` and type:

```plaintext
/plugin
```

Select the marketplace **blockscout-ai** and enable the plugin(s) you want (`blockscout-analysis`, `web3-dev`).`

### Gemini CLI

The first command (registering the Blockscout MCP server) is only needed for `blockscout-analysis`; skip it for `web3-dev`.

```sh
gemini mcp add --transport http blockscout https://mcp.blockscout.com/mcp   # blockscout-analysis only
gemini skills install https://github.com/blockscout/agent-skills --path <skill>
```

## Updating

The skills and the underlying Blockscout infrastructure are under continuous development. Update the marketplace/plugin (Claude) or re-install the skill (Gemini, Codex) periodically to pick up the most recent versions.

## Packaging

To create a distributable zip of a skill:

```sh
bash tools/package.sh <skill-directory>
```

This produces `<skill-directory>-<version>.zip` and `<skill-directory>-<version>.skill` (version read from `SKILL.md` frontmatter) containing all tracked files except `.gitignore` and `README.md`. The `.skill` file is identical to the `.zip` but uses the extension recognised by Claude Desktop and Gemini CLI for one-click import.

## Publishing Codex plugins

The Codex marketplace requires plugins to be self-contained directory trees with no symlinks. To keep each skill as a single source-of-truth directory at the repo root while still serving Codex, the published Codex layout lives on a dedicated `codex-plugins` branch. To regenerate that branch from the current `main` (or a release tag) and push it:

```sh
bash tools/publish-codex-plugins.sh [<source-ref>] [<target-branch>]
```

Defaults are `main` and `codex-plugins`. The script reads only committed content from `<source-ref>`, dereferences the symlinks under `.agents/plugins/*/skills/` into real directories, copies `.agents/plugins/marketplace.json` verbatim, writes a short `README.md`, and pushes the result. See [`.memory_bank/specs/publish-codex-plugins-spec.md`](.memory_bank/specs/publish-codex-plugins-spec.md) for the full specification.

## License

[MIT](LICENSE)
