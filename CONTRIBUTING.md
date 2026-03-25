# Contributing to CryptoSkill

Thank you for your interest in contributing to CryptoSkill! This project is a community-driven effort to build the most comprehensive registry of crypto AI agent skills and MCP servers. We welcome contributions of all kinds: new skills, MCP server submissions, improvements to existing skills, documentation, and bug reports.

All submissions are reviewed for security and quality before merging.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Adding a New Skill](#adding-a-new-skill)
- [Submitting an MCP Server](#submitting-an-mcp-server)
- [Improving an Existing Skill](#improving-an-existing-skill)
- [Skill Format Reference](#skill-format-reference)
- [Quality Guidelines](#quality-guidelines)
- [Security Review Requirements](#security-review-requirements)
- [AI-Assisted Contributions](#ai-assisted-contributions)
- [Pull Request Process](#pull-request-process)
- [Branch Strategy](#branch-strategy)
- [Code Review](#code-review)

---

## Code of Conduct

We are committed to maintaining a welcoming and respectful community. Be kind, constructive, and assume good faith. Harassment or discrimination of any kind will not be tolerated.

---

## How to Submit a Skill

The easiest way to submit a skill or MCP server is to **open a GitHub Issue**:

👉 **[Submit a Skill](https://github.com/jiayaoqijia/cryptoskill/issues/new?template=skill_submission.md&title=%5BSubmit%5D+)**

Just provide the skill name, GitHub URL, and category. We'll review and add it for you.

> **Note:** We no longer accept Pull Requests for skill submissions. PRs are reserved for bug fixes and infrastructure changes only.

## Other Ways to Contribute

- **Skill requests** -- Request a skill for a protocol we don't cover yet: [Open a request](https://github.com/jiayaoqijia/cryptoskill/issues/new?template=skill_request.md)
- **Bug reports** -- Found an issue? [Report it](https://github.com/jiayaoqijia/cryptoskill/issues/new?template=bug_report.md)
- **Feature requests** -- Have an idea? [Tell us](https://github.com/jiayaoqijia/cryptoskill/issues/new?template=feature_request.md)
- **Quick submit** -- Email maintainers@altresear.ch with the skill name, GitHub URL, and category

---

## Adding a New Skill

### 1. Choose a Category

Skills are organized into 13 categories:

| Category | Description |
|---|---|
| `exchanges` | CEX & DEX integrations |
| `chains` | Blockchain-specific skills |
| `analytics` | Data, analytics, and market intelligence |
| `trading` | Trading bots, signals, and strategies |
| `defi` | DeFi protocols and tools |
| `identity` | On-chain identity and reputation |
| `payments` | Crypto payment protocols |
| `prediction-markets` | Prediction market integrations |
| `wallets` | Wallet integrations and management |
| `dev-tools` | Developer tools and SDKs |
| `mcp-servers` | MCP protocol servers (see [Submitting an MCP Server](#submitting-an-mcp-server)) |
| `social` | Decentralized social protocols |
| `ai-crypto` | AI x Crypto integrations |

### 2. Create the Skill Directory

```bash
mkdir -p skills/{category}/{skill-name}
```

Use `kebab-case` for the skill directory name. Choose a descriptive name that includes the protocol or project (e.g., `binance-spot-api`, `uniswap-swap-simulation`).

### 3. Create Required Files

Every skill must include these files:

#### `SKILL.md`

The primary skill file with YAML frontmatter and documentation:

```markdown
---
name: my-skill-name
description: A brief description of what this skill does.
version: 1.0.0
author: your-username
tags:
  - relevant
  - tags
  - here
homepage: https://github.com/your-username/your-skill
triggers:
  - "natural language trigger"
  - "another trigger phrase"
config:
  API_KEY:
---

# My Skill Name

## Overview

Describe what the skill does, what protocol it integrates with, and what use cases it covers.

## Usage

Explain how an agent uses this skill, including example prompts and expected outputs.

## Configuration

Document any required environment variables or API keys.

## API Reference

List the key API endpoints or methods the skill uses.
```

#### `_meta.json`

Version history and ownership metadata:

```json
{
  "owner": "your-username",
  "slug": "my-skill-name",
  "displayName": "My Skill Name",
  "latest": {
    "version": "1.0.0",
    "publishedAt": 1710000000000
  },
  "history": []
}
```

#### `SOURCE.md`

Attribution and provenance:

```markdown
# Source Attribution

- **Original Author**: your-username
- **Original Slug**: my-skill-name
- **Source**: [ClawHub](https://clawhub.ai/skills/your-username/my-skill-name) or direct link
- **License**: MIT-0
- **Classification**: COMMUNITY or OFFICIAL
```

### 4. Optional Files

- `index.js` / `index.py` -- Executable entry point
- `skill.yaml` -- Additional configuration
- `scripts/` -- Executable scripts
- `references/` -- Reference documentation, API specs, or token lists

---

## Submitting an MCP Server

MCP (Model Context Protocol) servers are a special category of skill that provide tool-level integration with AI assistants like Claude, Cursor, and Codex. We maintain the largest curated collection of crypto MCP servers, and we welcome new submissions.

### Steps to Submit an MCP Server

1. **Verify it doesn't already exist.** Check the [MCP Servers table](README.md#mcp-servers) and the `skills/mcp-servers/` directory. If a similar server is already listed, consider improving it instead.

2. **Create the skill directory:**
   ```bash
   mkdir -p skills/mcp-servers/{server-name}-mcp
   ```

3. **Create the required files** (`SKILL.md`, `_meta.json`, `SOURCE.md`) following the same format as other skills. In your `SKILL.md`, be sure to include:
   - What chains or protocols the MCP server supports
   - Installation and configuration instructions (npm package, Docker, etc.)
   - Available tools/functions the server exposes
   - Required API keys or environment variables
   - A working example configuration snippet (e.g., for `claude_desktop_config.json`)

4. **Tag it appropriately.** Use the tag `mcp` along with relevant protocol or chain tags.

5. **Open a pull request** with the title format: `Add {server-name} MCP server`

### MCP Server Requirements

- The MCP server must be **open source** or have a **publicly available npm/Docker package**.
- It must be **crypto-related** (blockchain, DeFi, exchange, wallet, analytics, etc.).
- The `SKILL.md` must include clear setup instructions so a user can get it running.
- If the server requires API keys, document how to obtain them.
- The server should be **actively maintained** -- we may decline servers that have not been updated in over a year with no community activity.

### Official MCP Servers

If you are a project team submitting your own MCP server, note this in the `SOURCE.md` with `Classification: OFFICIAL`. Official servers receive a verification badge on the website.

---

## Improving an Existing Skill

1. Find the skill in `skills/{category}/{skill-name}/`.
2. Make your changes to `SKILL.md`, scripts, or documentation.
3. Update the version in both `SKILL.md` frontmatter and `_meta.json`.
4. Open a pull request describing what you changed and why.

Common improvements:

- Better documentation and usage examples
- Additional trigger phrases
- Bug fixes in scripts
- Updated API references
- New configuration options

---

## Skill Format Reference

### SKILL.md Frontmatter Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Skill slug in kebab-case |
| `description` | Yes | One-line description |
| `version` | Yes | Semantic version (e.g., `1.0.0`) |
| `author` | Yes | Author username |
| `tags` | Yes | Array of relevant tags |
| `homepage` | No | Link to source repository or docs |
| `triggers` | No | Natural language phrases that activate the skill |
| `config` | No | Required environment variables |
| `metadata` | No | Additional metadata (e.g., `clawdbot` requirements) |

### Naming Conventions

- Skill directories: `kebab-case` (e.g., `binance-spot-api`)
- Categories: lowercase (e.g., `exchanges`, `dev-tools`)
- Path structure: `skills/{category}/{skill-name}/`

---

## Quality Guidelines

Not all submissions are equal. Here is what makes a good skill and what will help your PR get merged quickly.

### What Makes a Good Skill

- **Solves a real problem.** The skill addresses an actual use case that crypto AI agents need (e.g., fetching prices, executing trades, monitoring positions).
- **Clear documentation.** The `SKILL.md` is well-written, with a concise overview, usage examples, and configuration instructions. A developer should be able to understand what the skill does in under 30 seconds.
- **Accurate API references.** If the skill references external APIs, the endpoints, parameters, and response formats should be correct and up to date.
- **Meaningful triggers.** The trigger phrases should reflect how a user would naturally ask an agent to perform the skill's function.
- **Proper categorization.** The skill is placed in the most appropriate category directory.

### What Will Slow Down Your PR

- Missing or incomplete required files (`SKILL.md`, `_meta.json`, `SOURCE.md`)
- Vague or copy-pasted documentation
- Incorrect API references or broken links
- Skills that duplicate existing functionality without adding value
- Large PRs that bundle many unrelated skills (split them up)

---

## Security Review Requirements

All submissions undergo a security review before merging. This is non-negotiable.

### What We Check

1. **No hardcoded credentials.** API keys, private keys, mnemonics, and secrets must never appear in skill files. Use the `config` field in `SKILL.md` frontmatter to declare required environment variables.

2. **No malicious code.** Scripts in `scripts/`, `index.js`, or `index.py` must not contain obfuscated code, unauthorized network calls, or attempts to exfiltrate data.

3. **Safe external references.** Any URLs referenced in the skill must point to legitimate, well-known services. We will flag unfamiliar domains.

4. **No unnecessary permissions.** MCP servers and executable scripts should request only the permissions they need. Overly broad access patterns will be questioned.

5. **Dependency review.** If the skill includes a `package.json` or `requirements.txt`, dependencies are checked for known vulnerabilities.

### For MCP Server Submissions Specifically

- The MCP server source code must be inspectable (open source or published package).
- We verify that the server does not transmit user data to unauthorized endpoints.
- Server configuration examples must use placeholder values, never real credentials.

### If Your Submission Fails Security Review

You will receive specific feedback on what needs to change. Fix the issues and update your PR. We are happy to work with you to get your submission to a mergeable state.

---

## AI-Assisted Contributions

CryptoSkill embraces AI-assisted development. Many skills in this repository were created with AI assistance, and we welcome AI-assisted contributions.

### Disclosure Is Required

Every PR must disclose AI involvement using the PR template. There are three levels:

| Level | Description |
|---|---|
| Fully AI-generated | AI wrote the skill; contributor reviewed and validated it |
| Mostly AI-generated | AI produced the draft; contributor made significant modifications |
| Mostly human-written | Contributor led; AI provided suggestions or none at all |

Honest disclosure is expected. There is no stigma attached to any level.

### You Are Responsible for What You Submit

Using AI to generate a skill does not reduce your responsibility as the contributor. Before opening a PR with AI-generated content, you must:

- **Read and understand** the skill documentation and any scripts.
- **Test** the skill with a compatible agent if it includes executable code.
- **Verify correctness** -- AI-generated API references and configuration can be plausible but wrong.
- **Check for security issues** -- ensure no hardcoded credentials, no unsafe external calls.

PRs where it is clear the contributor has not reviewed the AI-generated content will be closed without review.

---

## Pull Request Process

### Before Opening a PR

- [ ] Skill has `SKILL.md` with valid frontmatter
- [ ] Skill has `_meta.json` with correct metadata
- [ ] Skill has `SOURCE.md` with proper attribution
- [ ] Skill is in the correct category directory
- [ ] Directory name uses `kebab-case`
- [ ] No hardcoded credentials or API keys
- [ ] Documentation is clear and accurate
- [ ] Fill in the PR template completely

### PR Size

Prefer focused PRs. A PR adding one skill is much easier to review than one adding ten. If you are contributing multiple skills, consider splitting them into separate PRs unless they are closely related.

---

## Branch Strategy

- **`main`** -- the active development branch. All PRs target `main`.
- Direct pushes to `main` are not permitted.
- At least one maintainer approval is required before merging.

### Workflow

```bash
# Fork and clone
git clone https://github.com/<your-username>/cryptoskill.git
cd cryptoskill

# Create a branch
git checkout -b add/my-new-skill

# Make your changes
# ...

# Commit and push
git add skills/category/my-new-skill/
git commit -m "Add my-new-skill to category"
git push origin add/my-new-skill

# Open a PR on GitHub
```

Use descriptive branch names: `add/binance-lending`, `fix/uniswap-triggers`, `docs/contributing-guide`, `add/mcp-jupiter`.

---

## Code Review

### For Contributors

- Respond to review comments within a reasonable time.
- When you update a PR in response to feedback, briefly note what changed.
- If you disagree with feedback, engage respectfully and explain your reasoning.

### For Reviewers

Review for:

1. **Completeness** -- Does the skill have all required files (`SKILL.md`, `_meta.json`, `SOURCE.md`)?
2. **Accuracy** -- Is the skill documentation correct? Do the API references match reality?
3. **Quality** -- Is the documentation clear and well-organized?
4. **Security** -- Are there any hardcoded credentials, unsafe scripts, or suspicious external calls?
5. **Categorization** -- Is the skill in the right category?
6. **MCP compliance** -- For MCP servers, does the skill include setup instructions and tool documentation?

Be constructive and specific in your feedback.

---

## Communication

- **GitHub Issues** -- Bug reports, feature requests, skill requests.
- **Pull Request comments** -- Skill-specific feedback.

When in doubt, open an issue before writing code. It costs little and prevents wasted effort.

---

Thank you for contributing to CryptoSkill!
