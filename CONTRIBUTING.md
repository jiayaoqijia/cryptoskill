# Contributing to CryptoSkill

Thank you for your interest in contributing to CryptoSkill! This project is a community-driven effort to build the most comprehensive registry of crypto AI agent skills. We welcome contributions of all kinds: new skills, improvements to existing skills, documentation, and bug reports.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Adding a New Skill](#adding-a-new-skill)
- [Improving an Existing Skill](#improving-an-existing-skill)
- [Skill Format Reference](#skill-format-reference)
- [AI-Assisted Contributions](#ai-assisted-contributions)
- [Pull Request Process](#pull-request-process)
- [Branch Strategy](#branch-strategy)
- [Code Review](#code-review)

---

## Code of Conduct

We are committed to maintaining a welcoming and respectful community. Be kind, constructive, and assume good faith. Harassment or discrimination of any kind will not be tolerated.

---

## Ways to Contribute

- **New skills** — Add a skill for a protocol, exchange, or tool that isn't covered yet.
- **Skill improvements** — Improve documentation, fix bugs, or add features to existing skills.
- **Bug reports** — Open an issue using the bug report template.
- **Feature requests** — Open an issue using the feature request template.
- **Skill requests** — Request a skill for a specific protocol using the skill request template.
- **Documentation** — Improve READMEs, guides, or inline comments.

For substantial changes, please open an issue first to discuss your approach. This prevents wasted effort and ensures alignment with the project's direction.

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
| `social` | Decentralized social protocols |
| `ai-crypto` | AI x Crypto integrations |
| `mcp-servers` | Official MCP protocol servers |

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

- `index.js` / `index.py` — Executable entry point
- `skill.yaml` — Additional configuration
- `scripts/` — Executable scripts
- `references/` — Reference documentation, API specs, or token lists

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
- **Verify correctness** — AI-generated API references and configuration can be plausible but wrong.
- **Check for security issues** — ensure no hardcoded credentials, no unsafe external calls.

PRs where it is clear the contributor has not reviewed the AI-generated content will be closed without review.

---

## Pull Request Process

### Before Opening a PR

- [ ] Skill has `SKILL.md` with valid frontmatter
- [ ] Skill has `_meta.json` with correct metadata
- [ ] Skill has `SOURCE.md` with proper attribution
- [ ] Skill is in the correct category directory
- [ ] Directory name uses `kebab-case`
- [ ] Fill in the PR template completely

### PR Size

Prefer focused PRs. A PR adding one skill is much easier to review than one adding ten. If you are contributing multiple skills, consider splitting them into separate PRs unless they are closely related.

---

## Branch Strategy

- **`main`** — the active development branch. All PRs target `main`.
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

Use descriptive branch names: `add/binance-lending`, `fix/uniswap-triggers`, `docs/contributing-guide`.

---

## Code Review

### For Contributors

- Respond to review comments within a reasonable time.
- When you update a PR in response to feedback, briefly note what changed.
- If you disagree with feedback, engage respectfully and explain your reasoning.

### For Reviewers

Review for:

1. **Completeness** — Does the skill have all required files (`SKILL.md`, `_meta.json`, `SOURCE.md`)?
2. **Accuracy** — Is the skill documentation correct? Do the API references match reality?
3. **Quality** — Is the documentation clear and well-organized?
4. **Security** — Are there any hardcoded credentials, unsafe scripts, or suspicious external calls?
5. **Categorization** — Is the skill in the right category?

Be constructive and specific in your feedback.

---

## Communication

- **GitHub Issues** — Bug reports, feature requests, skill requests.
- **Pull Request comments** — Skill-specific feedback.

When in doubt, open an issue before writing code. It costs little and prevents wasted effort.

---

Thank you for contributing to CryptoSkill!
